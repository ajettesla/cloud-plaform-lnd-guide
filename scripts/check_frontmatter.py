#!/usr/bin/env python3
"""
Validate frontmatter in markdown files.
Required fields: title, description, tags, cloud, level, version, date, authors, references
"""
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any

REQUIRED_FIELDS = ['title', 'description', 'tags', 'cloud', 'level', 'version', 'date', 'authors', 'references']
VALID_CLOUDS = ['aws', 'gcp', 'azure', 'all']
VALID_LEVELS = ['100', '200', '300', '400']
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
VERSION_PATTERN = re.compile(r'^\d+\.\d+(\.\d+)?$')

def check_frontmatter(filepath: Path) -> list:
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for frontmatter
    if not content.startswith('---'):
        return [f"  {filepath}: Missing frontmatter (---)"]
    
    # Extract frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return [f"  {filepath}: Malformed frontmatter"]
    
    try:
        fm = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        return [f"  {filepath}: Invalid YAML in frontmatter: {e}"]
    
    if not fm:
        return [f"  {filepath}: Empty frontmatter"]
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"  {filepath}: Missing required field '{field}'")
    
    # Validate field values
    if 'cloud' in fm:
        clouds = fm['cloud'] if isinstance(fm['cloud'], list) else [fm['cloud']]
        for c in clouds:
            if c not in VALID_CLOUDS:
                errors.append(f"  {filepath}: Invalid cloud '{c}'. Must be one of {VALID_CLOUDS}")
    
    if 'level' in fm:
        level = str(fm['level'])
        if level not in VALID_LEVELS:
            errors.append(f"  {filepath}: Invalid level '{level}'. Must be one of {VALID_LEVELS}")
    
    if 'date' in fm:
        date = str(fm['date'])
        if not DATE_PATTERN.match(date):
            errors.append(f"  {filepath}: Invalid date format '{date}'. Use YYYY-MM-DD")
    
    if 'version' in fm:
        version = str(fm['version'])
        if not VERSION_PATTERN.match(version):
            errors.append(f"  {filepath}: Invalid version format '{version}'. Use semantic version (e.g., 1.0.0)")
    
    if 'tags' in fm:
        tags = fm['tags'] if isinstance(fm['tags'], list) else [fm['tags']]
        for tag in tags:
            if not re.match(r'^[a-z0-9-]+$', tag):
                errors.append(f"  {filepath}: Tag '{tag}' must be lowercase with hyphens only")
    
    if 'authors' in fm:
        authors = fm['authors'] if isinstance(fm['authors'], list) else [fm['authors']]
        if not authors:
            errors.append(f"  {filepath}: Authors list cannot be empty")
    
    if 'references' in fm:
        refs = fm['references'] if isinstance(fm['references'], list) else [fm['references']]
        if not refs:
            errors.append(f"  {filepath}: References list cannot be empty")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: check_frontmatter.py <docs_dir>")
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    print(f"Validating frontmatter in {docs_dir}...")
    all_errors = []
    for md_file in docs_dir.rglob('*.md'):
        errors = check_frontmatter(md_file)
        all_errors.extend(errors)
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} frontmatter errors:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print("✅ All frontmatter valid")
        sys.exit(0)

if __name__ == '__main__':
    main()
