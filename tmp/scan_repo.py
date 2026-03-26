import os, json, ast, re
from pathlib import Path

root = Path('.').resolve()
summary_dir = root / 'Summary'
summary_dir.mkdir(exist_ok=True)

EXCLUDE_DIRS = {
    '.git', '.venv', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'node_modules', 'dist', 'build', '.next', '.cache'
}
BINARY_EXTS = {
    '.pdf','.png','.jpg','.jpeg','.gif','.webp','.joblib','.pyc','.pkl','.exe','.dll',
    '.bin','.zip','.7z','.rar','.ico','.woff','.woff2','.ttf','.otf'
}
MAX_CHARS = 200_000

def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

items = []

for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
    dirnames[:] = sorted([d for d in dirnames if d not in EXCLUDE_DIRS])
    for filename in sorted(filenames):
        path = Path(dirpath) / filename
        if is_excluded(path):
            continue

        rel = '/' + path.relative_to(root).as_posix()
        ext = path.suffix.lower()
        size = path.stat().st_size
        is_binary = ext in BINARY_EXTS

        entry = {
            'path': rel,
            'ext': ext,
            'size_bytes': size,
            'is_binary': is_binary,
        }

        if is_binary:
            items.append(entry)
            continue

        try:
            data = path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            entry['read_error'] = str(e)
            items.append(entry)
            continue

        if len(data) > MAX_CHARS:
            data = data[:MAX_CHARS]
            entry['truncated'] = True

        lines = data.splitlines()
        entry['line_count'] = len(lines)

        if ext in {'.md', '.markdown'}:
            m = re.search(r'^#{1,6}\\s+(.+)$', data, flags=re.M)
            if m:
                entry['title'] = m.group(1).strip()
        elif ext in {'.html', '.htm'}:
            m = re.search(r'<title>(.*?)</title>', data, flags=re.I|re.S)
            if m:
                entry['title'] = re.sub(r'\\s+', ' ', m.group(1)).strip()
        elif ext == '.py':
            try:
                tree = ast.parse(data)
                defs = []
                for node in tree.body:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        defs.append({
                            'name': node.name,
                            'kind': type(node).__name__,
                            'start': getattr(node, 'lineno', None),
                            'end': getattr(node, 'end_lineno', None),
                        })
                if defs:
                    entry['top_level_defs'] = defs
            except Exception as e:
                entry['parse_error'] = str(e)

        items.append(entry)

out = {
    'root': str(root),
    'file_count': len(items),
    'binary_count': sum(1 for i in items if i.get('is_binary')),
    'text_count': sum(1 for i in items if not i.get('is_binary')),
    'items': items,
}

out_path = summary_dir / '_repo_scan.json'
out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')

print('Wrote', out_path)
print('Total files:', out['file_count'])
print('Binary:', out['binary_count'])
print('Text:', out['text_count'])
