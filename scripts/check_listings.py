#!/usr/bin/env python3
"""
Validate code blocks have language tags.
"""
import re
import sys
from pathlib import Path

CODE_BLOCK_PATTERN = re.compile(r'^```(\w*)\n', re.MULTILINE)

def check_code_blocks(filepath: Path) -> list:
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in CODE_BLOCK_PATTERN.finditer(content):
        lang = match.group(1)
        if not lang:
            # Find line number
            line_no = content[:match.start()].count('\n') + 1
            errors.append(f"  {filepath}:{line_no}: Code block missing language tag")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: check_listings.py <docs_dir>")
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    print(f"Checking code block language tags in {docs_dir}...")
    all_errors = []
    for md_file in docs_dir.rglob('*.md'):
        errors = check_code_blocks(md_file)
        all_errors.extend(errors)
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} code blocks missing language tags:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print("✅ All code blocks have language tags")
        sys.exit(0)

if __name__ == '__main__':
    main()
