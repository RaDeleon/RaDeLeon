#!/usr/bin/env python3
"""Check local image targets and generated SVGs without fetching third-party sites."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = ['stats.svg', 'languages.svg', 'snake.svg', 'snake-dark.svg']


def check_widgets(folder):
    for name in FILES:
        path = folder / name
        text = path.read_text()
        assert len(text) > 300, f'Empty widget: {name}'
        assert ET.fromstring(text).tag == '{http://www.w3.org/2000/svg}svg', name
        assert not any(x in text.lower() for x in ('something went wrong', 'could not fetch', 'error fetching')), name
    print('Four generated SVG widgets are valid and contain no known error card.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generated', type=Path)
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    if args.generated:
        check_widgets(args.generated)
        return
    readme = (ROOT / 'README.md').read_text()
    paths = re.findall(r'(?:src|srcset)="([^"]+)"', readme)
    for target in paths:
        if target.startswith(('https://', 'http://')):
            continue
        path = unquote(urlsplit(target).path)
        if args.source_only and path.startswith('assets/generated/'):
            continue
        assert (ROOT / path).is_file(), f'Missing local image: {path}'
    assert readme.count('<!-- writing:start -->') == 1
    assert readme.count('<!-- writing:end -->') == 1
    assert not re.search(r'github_pat_|gh[pousr]_[A-Za-z0-9]{30,}', readme)
    print('Profile image targets and writing markers pass.')


if __name__ == '__main__':
    main()
