import json, ast, re
from pathlib import Path

root = Path('.').resolve()
scan = json.loads((root/'Summary'/'_repo_scan.json').read_text(encoding='utf-8'))

# Map path -> scan entry
items = scan['items']

# Utility: read first N lines

def head_text(rel_path: str, max_lines: int = 40) -> str:
    p = root / rel_path.lstrip('/')
    try:
        txt = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return ''
    return '\n'.join(txt.splitlines()[:max_lines])


def infer_purpose(entry) -> str:
    path = entry['path']
    ext = entry['ext']
    if entry.get('is_binary'):
        return 'Binary asset'

    h = head_text(path, 60)

    if ext == '.py':
        try:
            mod = ast.parse(h)
            ds = ast.get_docstring(mod)
            if ds:
                return re.sub(r'\s+', ' ', ds).strip()
        except Exception:
            pass
        return 'Python module'

    if ext in {'.md', '.markdown'}:
        m = re.search(r'^#{1,6}\s+(.+)$', h, flags=re.M)
        if m:
            return m.group(1).strip()
        return 'Markdown document'

    if ext in {'.html', '.htm'}:
        m = re.search(r'<title>(.*?)</title>', h, flags=re.I|re.S)
        if m:
            return re.sub(r'\s+', ' ', m.group(1)).strip()
        return 'HTML template'

    if ext == '.json':
        return 'JSON data/config'
    if ext == '.csv':
        return 'CSV dataset'
    if ext == '.resolved':
        return 'Resolved spec/notes'

    return 'Text file'


def key_defs(entry) -> str:
    defs = entry.get('top_level_defs') or []
    if not defs:
        return ''
    parts = []
    for d in defs:
        rng = ''
        if d.get('start') and d.get('end'):
            rng = f" (lines {d['start']}-{d['end']})"
        elif d.get('start'):
            rng = f" (line {d['start']})"
        parts.append(f"- {d['kind']}: {d['name']}{rng}")
    return '\n'.join(parts)

# Group by top-level folder

def top_folder(p: str) -> str:
    parts = p.strip('/').split('/')
    return parts[0] if parts else ''

items_sorted = sorted(items, key=lambda e: (top_folder(e['path']), e['path']))

out = []
out.append('# File Details')
out.append('')
out.append('Auto-generated per-file notes (purpose + key symbols where available).')
out.append('Source: `Summary/_repo_scan.json`.')
out.append('')

current = None
for entry in items_sorted:
    folder = top_folder(entry['path'])
    if folder != current:
        out.append(f"## /{folder}/" if folder else '## /')
        out.append('')
        current = folder

    purpose = infer_purpose(entry)
    out.append(f"### {entry['path']}")
    out.append('')
    out.append(f"- Purpose: {purpose}")
    out.append(f"- Type: {'binary' if entry.get('is_binary') else 'text'}{entry.get('ext','')}")
    if not entry.get('is_binary'):
        if 'line_count' in entry:
            out.append(f"- Lines: {entry['line_count']}")
        if entry.get('truncated'):
            out.append('- Note: content truncated in scan (large file).')
        kd = key_defs(entry)
        if kd:
            out.append('- Top-level symbols:')
            out.append(kd)
    out.append('')

(target := root/'Summary'/'file_details.md').write_text('\n'.join(out), encoding='utf-8')
print('Wrote', target)
