#!/usr/bin/env python3
"""
Validate Mermaid diagrams in markdown files.
Checks that all mermaid code blocks have captions.
"""
import re
import sys
from pathlib import Path

MERMAID_PATTERN = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
CAPTION_PATTERN = re.compile(r'\*\*Figure \d+:\*\*')

def check_mermaid_in_file(filepath: Path) -> list:
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    mermaid_blocks = list(MERMAID_PATTERN.finditer(content))
    
    for i, match in enumerate(mermaid_blocks):
        # Check if there's a caption after the code block
        after_block = content[match.end():match.end()+200]
        if not CAPTION_PATTERN.search(after_block):
            # Try to find figure number from context
            errors.append(f"  {filepath}: Mermaid block #{i+1} missing caption (**Figure N:** Description)")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: check_figures.py <docs_dir>")
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    print(f"Checking Mermaid diagrams in {docs_dir}...")
    all_errors = []
    for md_file in docs_dir.rglob('*.md'):
        errors = check_mermaid_in_file(md_file)
        all_errors.extend(errors)
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} diagrams missing captions:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print("✅ All Mermaid diagrams have captions")
        sys.exit(0)

if __name__ == '__main__':
    main()
