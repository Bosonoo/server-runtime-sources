"""Verify published third-party source bytes without extracting or executing them."""
import hashlib
import json
from pathlib import Path
import sys
import tarfile


def verify(path):
    root = Path(__file__).resolve().parent
    receipt = json.loads((root / 'bundle.json').read_text(encoding='utf-8'))
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if path.stat().st_size != receipt['bytes'] or actual != receipt['sha256']:
        raise ValueError('bundle size or SHA-256 differs from published receipt')
    expected = {'sources/' + row['filename']: row for row in receipt['sourceArchives']}
    if len(expected) != len(receipt['sourceArchives']):
        raise ValueError('duplicate source in published inventory')
    for name in ('source-index.json', 'SOURCE_SHA256SUMS'):
        payload = (root / name).read_bytes()
        expected[name] = {'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
    seen = set()
    with tarfile.open(path, 'r:') as archive:
        for member in archive:
            if not member.isfile() or member.name in seen or member.name not in expected:
                raise ValueError('unexpected, nonregular or duplicate archive member')
            row = expected[member.name]
            if member.size != row['bytes']:
                raise ValueError('source byte count differs')
            with archive.extractfile(member) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            if digest != row['sha256']:
                raise ValueError('source SHA-256 differs')
            seen.add(member.name)
    if seen != set(expected):
        raise ValueError('missing archive members')
    return len(receipt['sourceArchives'])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 verify_bundle.py SOURCE_BUNDLE.tar')
    print(f'Verified {verify(Path(sys.argv[1]))} source RPMs; no sources executed or extracted.')
