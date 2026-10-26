"""Reproduce the cron delivery failure at the API level.

Mirrors FeishuAdapter._send_raw_message() exactly:
  - metadata has thread_id -> _build_create_message_request("thread_id", body)
  - no thread_id          -> _build_create_message_request("chat_id", body)

If the thread_id variant returns [99992402] while the chat_id variant
succeeds, the stale origin.thread_id is proven to be the root cause.
"""
import json
import os

import lark_oapi as lark
from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
    ReplyMessageRequest,
    ReplyMessageRequestBody,
)

from dotenv import load_dotenv

load_dotenv("/root/.hermes/.env")

APP_ID = os.environ["FEISHU_APP_ID"]
APP_SECRET = os.environ["FEISHU_APP_SECRET"]
CHAT_ID = "oc_d5de551525d3a4ae9e1a52815bb9a92b"
THREAD_ID = "omt_195b15107a561c82"

client = (
    lark.Client.builder()
    .app_id(APP_ID)
    .app_secret(APP_SECRET)
    .log_level(lark.LogLevel.WARNING)
    .build()
)


def attempt(label, *, receive_id, receive_id_type, text):
    body = (
        CreateMessageRequestBody.builder()
        .receive_id(receive_id)
        .msg_type("text")
        .content(json.dumps({"text": text}, ensure_ascii=False))
        .uuid(f"probe-{label}")
        .build()
    )
    request = (
        CreateMessageRequest.builder()
        .receive_id_type(receive_id_type)
        .request_body(body)
        .build()
    )
    resp = client.im.v1.message.create(request)
    code = getattr(resp, "code", None)
    msg = getattr(resp, "msg", None)
    ok = getattr(resp, "success", lambda: False)()
    message_id = None
    if ok:
        data = getattr(resp, "data", None)
        message_id = getattr(data, "message_id", None) if data else None
    print(f"[{label}] receive_id_type={receive_id_type!r} success={ok} code={code} msg={msg!r} message_id={message_id}")
    return message_id


print("=== A) cron path today: metadata.thread_id set -> receive_id_type='thread_id' ===")
mid_a = attempt("thread", receive_id=THREAD_ID, receive_id_type="thread_id", text="[probe] idea-recall delivery probe")

print()
print("=== B) proposed path: no thread_id -> receive_id_type='chat_id' ===")
mid_b = attempt("chat", receive_id=CHAT_ID, receive_id_type="chat_id", text="[probe] idea-recall delivery probe (no thread)")

print()
print(f"PROBE_MESSAGE_IDS={mid_a},{mid_b}")
