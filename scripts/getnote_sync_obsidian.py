#!/usr/bin/env python3
"""Sync Obsidian markdown notes to Get笔记.

Intended use from Hermes skills:
  python3 scripts/getnote_sync_obsidian.py --only "00-Inbox/2026-01-01 示例.md" --limit 1 --sleep 2

Design goals:
- lives inside the Obsidian vault so `scripts/getnote_sync_obsidian.py` works from vault cwd;
- reads Get笔记 credentials from /root/.openclaw/openclaw.json by default;
- keeps an idempotency map at /root/.openclaw/workspace/config/getnote_sync_map.json;
- syncs notes into Get笔记 knowledge base MyClaw and tags them with Hermes + folder tag;
- supports parent_id for follow-up child notes.

The Get笔记 OpenAPI `note/save` endpoint is treated as create/upsert-by-request. Because the
public behavior observed here reliably returns a new note_id, this script prevents duplicate
re-creation by skipping files whose content hash is already mapped unless --force is passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

API_BASE = "https://openapi.biji.com/open/api/v1"
DEFAULT_VAULT = Path("/root/obsidian-vault")
DEFAULT_CONFIG = Path("/root/.openclaw/openclaw.json")
DEFAULT_MAP = Path("/root/.openclaw/workspace/config/getnote_sync_map.json")
DEFAULT_KNOWLEDGE = "MyClaw"


@dataclass
class Credentials:
    api_key: str
    client_id: str


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def deep_find(obj: Any, keys: set[str]) -> Any:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and v not in (None, ""):
                return v
        for v in obj.values():
            found = deep_find(v, keys)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = deep_find(item, keys)
            if found not in (None, ""):
                return found
    return None


def deep_collect(obj: Any, key: str) -> list[Any]:
    out: list[Any] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append(v)
            out.extend(deep_collect(v, key))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(deep_collect(item, key))
    return out


def load_credentials(config_path: Path) -> Credentials:
    cfg = load_json(config_path, {})
    entry = (((cfg.get("skills") or {}).get("entries") or {}).get("getnote") or {})
    api_key = os.environ.get("GETNOTE_API_KEY") or entry.get("apiKey")
    client_id = (
        os.environ.get("GETNOTE_CLIENT_ID")
        or (entry.get("env") or {}).get("GETNOTE_CLIENT_ID")
        or (cfg.get("env") or {}).get("GETNOTE_CLIENT_ID")
    )
    if not api_key or not client_id:
        raise SystemExit(
            f"Missing Get笔记 credentials. Expected skills.entries.getnote.apiKey and "
            f"GETNOTE_CLIENT_ID in {config_path}, or env GETNOTE_API_KEY/GETNOTE_CLIENT_ID."
        )
    return Credentials(api_key=api_key, client_id=client_id)


def api_call(creds: Credentials, method: str, path: str, payload: Any | None = None) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        API_BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": creds.api_key,
            "X-Client-ID": creds.client_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Hermes-GetNote-Obsidian-Sync/1.0",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body) if body else {"http_status": resp.status}
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {method} {path}: {body}") from e
    except error.URLError as e:
        raise RuntimeError(f"Network error {method} {path}: {e}") from e


def note_title(path: Path, text: str) -> str:
    for line in text.splitlines()[:40]:
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return path.stem


def folder_tag(rel: Path) -> str:
    parts = rel.parts[:-1]
    if not parts:
        return "Inbox"
    # Special case: 10-Notes/Daily/Hermes -> Daily, otherwise deepest folder sans numeric prefix.
    if "Daily" in parts:
        return "Daily"
    raw = parts[-1]
    raw = re.sub(r"^\d+[-_ ]*", "", raw).strip() or raw
    return raw


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_markdown(vault: Path, only: str | None) -> list[Path]:
    if only:
        p = (vault / only).resolve() if not Path(only).is_absolute() else Path(only).resolve()
        if not p.exists():
            raise SystemExit(f"File not found: {p}")
        if p.suffix.lower() != ".md":
            raise SystemExit(f"Not a markdown file: {p}")
        return [p]
    return sorted(
        p for p in vault.rglob("*.md")
        if "/.git/" not in str(p) and "/scripts/" not in str(p)
    )


def find_topic_id(creds: Credentials, knowledge_name: str) -> str | None:
    resp = api_call(creds, "GET", "/resource/knowledge/list?page=1")
    # Look for a dict whose name matches and has topic_id/id nearby.
    stack = [resp]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if cur.get("name") == knowledge_name:
                return str(cur.get("topic_id") or cur.get("id") or cur.get("knowledge_id") or "") or None
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return None


def batch_add(creds: Credentials, topic_id: str, note_id: str) -> Any:
    return api_call(creds, "POST", "/resource/knowledge/note/batch-add", {
        "topic_id": topic_id,
        "note_ids": [note_id],
    })


def sync_one(creds: Credentials, md_path: Path, vault: Path, sync_map: dict[str, Any], args: argparse.Namespace, topic_id: str | None) -> dict[str, Any]:
    rel = md_path.resolve().relative_to(vault.resolve()).as_posix()
    text = md_path.read_text(encoding="utf-8")
    digest = sha256_text(text)
    prev = sync_map.get(rel)
    if prev and prev.get("sha256") == digest and not args.force:
        return {"file": rel, "status": "skipped", "reason": "unchanged", "note_id": prev.get("note_id"), "topic_id": prev.get("topic_id")}

    tags = ["Hermes", folder_tag(Path(rel))]
    payload: dict[str, Any] = {
        "title": note_title(md_path, text),
        "content": text,
        "note_type": "plain_text",
        "tags": list(dict.fromkeys(tags)),
    }
    parent_id = args.parent_id or (prev or {}).get("parent_id")
    if parent_id:
        payload["parent_id"] = parent_id

    if args.dry_run:
        return {"file": rel, "status": "dry-run", "title": payload["title"], "tags": payload["tags"], "parent_id": parent_id}

    resp = api_call(creds, "POST", "/resource/note/save", payload)
    note_id = deep_find(resp, {"note_id", "id"})
    if not note_id:
        raise RuntimeError(f"note/save succeeded but no note_id found for {rel}: {json.dumps(resp, ensure_ascii=False)[:1000]}")
    note_id = str(note_id)

    batch_resp = None
    success_count = None
    if topic_id:
        batch_resp = batch_add(creds, topic_id, note_id)
        counts = deep_collect(batch_resp, "success_count")
        success_count = counts[0] if counts else None

    sync_map[rel] = {
        "note_id": note_id,
        "sha256": digest,
        "title": payload["title"],
        "tags": payload["tags"],
        "topic_id": topic_id,
        "parent_id": parent_id,
        "synced_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return {"file": rel, "status": "synced", "note_id": note_id, "topic_id": topic_id, "batch_add_success_count": success_count}


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync Obsidian markdown notes to Get笔记 MyClaw")
    ap.add_argument("--vault", default=str(DEFAULT_VAULT), help="Obsidian vault root")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG), help="OpenClaw config containing Get笔记 credentials")
    ap.add_argument("--map", default=str(DEFAULT_MAP), help="idempotency map JSON path")
    ap.add_argument("--only", help="single markdown file path, relative to vault or absolute")
    ap.add_argument("--limit", type=int, default=20, help="max files to sync")
    ap.add_argument("--sleep", type=float, default=0.0, help="seconds between API syncs")
    ap.add_argument("--knowledge", default=DEFAULT_KNOWLEDGE, help="Get笔记 knowledge base name")
    ap.add_argument("--parent-id", help="create synced note as child of an existing Get笔记 note")
    ap.add_argument("--force", action="store_true", help="sync even when file hash is unchanged")
    ap.add_argument("--dry-run", action="store_true", help="do not call OpenAPI or write map")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.exists():
        raise SystemExit(f"Vault not found: {vault}")
    files = iter_markdown(vault, args.only)[: max(args.limit, 0)]
    if not files:
        print("No markdown files to sync.")
        return 0

    creds = load_credentials(Path(args.config))
    sync_map = load_json(Path(args.map), {})
    topic_id = None if args.dry_run else find_topic_id(creds, args.knowledge)
    if not topic_id and not args.dry_run:
        print(f"WARN: knowledge base {args.knowledge!r} not found; notes will be saved but not batch-added.", file=sys.stderr)

    results = []
    for i, md_path in enumerate(files):
        results.append(sync_one(creds, md_path, vault, sync_map, args, topic_id))
        if args.sleep and i < len(files) - 1:
            time.sleep(args.sleep)

    if not args.dry_run:
        save_json(Path(args.map), sync_map)

    for r in results:
        print(json.dumps(r, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
