#!/usr/bin/env python3
"""Apply or remove the avatar sway CSS in a compatible local BotHarness bundle."""
import argparse
import hashlib
import os
from pathlib import Path
import tempfile

DEFAULT = Path.home() / '.dsh/profiles/desktop/node_modules/@botharness/ui/lib/client.js'
ANCHOR = '.bh-avatar-media {\n  display: inline-flex;'
CSS = '''/* Local presentation change: sway active portrait avatars. */
@keyframes bh-task-avatar-sway {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-18deg); }
  75% { transform: rotate(18deg); }
}
.bh-persona-avatar[data-surface='portrait'][data-active='true'],
.bh-row-avatar > .bh-persona-avatar[data-state='thinking'],
.bh-row-avatar > .bh-persona-avatar[data-state='working'] {
  animation: bh-task-avatar-sway 1.2s ease-in-out infinite;
  transform-origin: 50% 70%;
}
html[data-botharness-activity='stale'] .bh-persona-avatar[data-active='true'],
html[data-botharness-activity='stale'] .bh-row-avatar > .bh-persona-avatar { animation-play-state: paused; }
@media (prefers-reduced-motion: reduce) {
  .bh-persona-avatar[data-surface='portrait'][data-active='true'],
  .bh-row-avatar > .bh-persona-avatar[data-state='thinking'],
  .bh-row-avatar > .bh-persona-avatar[data-state='working'] { animation: none; }
}
'''
ORIGINAL_SHA256 = 'dd23da70804714a86ec1a1a2a45b0f2310082df49824d8eda56892ae77761305'
PATCHED_SHA256 = '1428297bfd1aa0ea8bbaf7e7e14c8b6141057f70a7968b8f7b566cdfbe48c793'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'remove', 'status'))
    parser.add_argument('--file', type=Path, default=DEFAULT, help='BotHarness client.js path')
    args = parser.parse_args()
    target = args.file.expanduser().resolve(strict=True)
    raw = target.read_bytes()
    current = digest(raw)
    state = 'installed' if current == PATCHED_SHA256 else 'original' if current == ORIGINAL_SHA256 else 'unsupported'
    print(f'{target}: {state} ({current})')
    if args.action == 'status':
        return
    if state == 'unsupported':
        raise SystemExit('Unsupported or modified bundle; no changes made.')
    if (args.action, state) in [('install', 'installed'), ('remove', 'original')]:
        print('Nothing to change.')
        return
    text = raw.decode('utf-8')
    if args.action == 'install':
        if text.count(ANCHOR) != 1 or 'bh-task-avatar-sway' in text:
            raise SystemExit('Anchor mismatch; no changes made.')
        result = text.replace(ANCHOR, CSS + ANCHOR, 1).encode()
        expected = PATCHED_SHA256
    else:
        if text.count(CSS) != 1:
            raise SystemExit('Patch mismatch; no changes made.')
        result = text.replace(CSS, '', 1).encode()
        expected = ORIGINAL_SHA256
    if digest(result) != expected:
        raise SystemExit('Output verification failed; no changes made.')
    backup = target.with_name(target.name + '.sway-backup-' + current[:12])
    try:
        with backup.open('xb') as f:
            f.write(raw)
    except FileExistsError:
        if backup.read_bytes() != raw:
            raise SystemExit('Backup conflict; no changes made.')
    fd, name = tempfile.mkstemp(prefix='.sway-', dir=target.parent)
    try:
        os.fchmod(fd, target.stat().st_mode & 0o777)
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
            f.flush()
            os.fsync(f.fileno())
        if target.read_bytes() != raw:
            raise RuntimeError('Bundle changed during preparation; no replacement made.')
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    print(f'Updated. Backup: {backup}. Restart DSH to load changes.')

if __name__ == '__main__':
    main()
