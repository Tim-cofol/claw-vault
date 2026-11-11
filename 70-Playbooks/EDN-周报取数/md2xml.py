#!/usr/bin/env python3
"""EDN 2026-11-11 — Markdown -> Feishu Docx XML."""
import re, html

md = open('/root/.hermes/cron/output/edn-insight-data/2026-11-11-report.md').read()


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*([^*\n]+)\*', r'<i>\1</i>', t)
    return t


def strip_num(s):
    return re.sub(r'^\d+\.\s', '', s)


out = ['<title>EDN 市场洞察周报 2026-11-11（周三）</title>']
lines = md.split('\n')
i = 0
while i < len(lines):
    s = lines[i].strip()
    if not s:
        i += 1
        continue
    if s.startswith('|') and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set('|-: '):
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
            i += 1
        hdr = rows[0]
        body = rows[2:] if len(rows) > 2 else []
        out.append('<table><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in hdr) + '</tr>')
        for r in body:
            out.append('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in r) + '</tr>')
        out.append('</table>')
        continue
    if s.startswith('#'):
        lvl = len(s) - len(s.lstrip('#'))
        out.append('<h' + str(lvl) + '>' + inline(s.lstrip('#').strip()) + '</h' + str(lvl) + '>')
    elif s.startswith('---'):
        out.append('<hr/>')
    elif s.startswith('>'):
        out.append('<quote>' + inline(s.lstrip('>').strip()) + '</quote>')
    elif s.startswith('- '):
        out.append('<ul><li>' + inline(s[2:].strip()) + '</li></ul>')
    elif re.match(r'^\d+\.\s', s):
        out.append('<ol><li>' + inline(strip_num(s)) + '</li></ol>')
    else:
        out.append('<p>' + inline(s) + '</p>')
    i += 1

xml = ''.join(out)
open('/tmp/edn-east/full.xml', 'w').write(xml)
print('xml chars:', len(xml))
print('h1:', xml.count('<h1>'), 'h2:', xml.count('<h2>'), 'h3:', xml.count('<h3>'),
      'table:', xml.count('<table>'), 'li:', xml.count('<li>'))
