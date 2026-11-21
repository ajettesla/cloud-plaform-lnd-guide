#!/usr/bin/env python3
"""
Validate cross-references in markdown files.
Checks that all [§XX.Y], [Figure N], [Table N], [Eq. N], [Listing N], [Algorithm N], [Appendix X] references resolve.
"""
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REF_PATTERN = re.compile(r'\[(§\d{2}\.\d+|Figure \d+|Table \d+|Eq\. \d+|Listing \d+|Algorithm \d+|Appendix [A-Z])\]')
ANCHOR_PATTERN = re.compile(r'^(#{1,4})\s+(.+)$')

def extract_anchors(filepath: Path) -> Dict[str, str]:
    anchors = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in ANCHOR_PATTERN.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        anchor = title.lower().replace(' ', '-')
        anchor = re.sub(r'[^\w\-]', '', anchor)
        anchors[anchor] = title
    
    return anchors

def find_all_anchors(docs_dir: Path) -> Dict[str, Tuple[Path, str]]:
    all_anchors = {}
    for md_file in docs_dir.rglob('*.md'):
        anchors = extract_anchors(md_file)
        for anchor, title in anchors.items():
            if anchor in all_anchors:
                print(f"WARNING: Duplicate anchor '{anchor}' in {md_file} and {all_anchors[anchor][0]}")
            all_anchors[anchor] = (md_file, title)
    return all_anchors

def check_refs_in_file(filepath: Path, all_anchors: Dict) -> List[str]:
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in REF_PATTERN.finditer(content):
        ref = match.group(1)
        if ref.startswith('§'):
            anchor = ref.replace('§', '').replace('.', '-')
        elif ref.startswith('Figure'):
            anchor = ref.lower().replace(' ', '-')
        elif ref.startswith('Table'):
            anchor = ref.lower().replace(' ', '-')
        elif ref.startswith('Eq.'):
            anchor = ref.lower().replace('. ', '-').replace(' ', '-')
        elif ref.startswith('Listing'):
            anchor = ref.lower().replace(' ', '-')
        elif ref.startswith('Algorithm'):
            anchor = ref.lower().replace(' ', '-')
        elif ref.startswith('Appendix'):
            anchor = ref.lower().replace(' ', '-')
        else:
            continue
        
        found = False
        for anchor_key in all_anchors:
            if anchor in anchor_key or anchor_key in anchor:
                found = True
                break
        
        if not found:
            errors.append(f"  {filepath}: Unresolved reference [{ref}]")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: check_refs.py <docs_dir>")
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    print(f"Scanning {docs_dir} for anchors...")
    all_anchors = find_all_anchors(docs_dir)
    print(f"Found {len(all_anchors)} anchors")
    
    print("Checking cross-references...")
    all_errors = []
    for md_file in docs_dir.rglob('*.md'):
        errors = check_refs_in_file(md_file, all_anchors)
        all_errors.extend(errors)
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} unresolved references:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print("✅ All cross-references resolved")
        sys.exit(0)

if __name__ == '__main__':
    main()
