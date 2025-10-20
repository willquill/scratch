#!/usr/bin/env python3
"""
Obsidian Properties Adder

This script adds YAML front matter properties to Obsidian markdown files
that don't already have them.
"""

import argparse
from pathlib import Path
from typing import List, Tuple


def has_frontmatter(content: str) -> bool:
    """Check if the file already has YAML front matter."""
    return content.strip().startswith('---')


def extract_existing_tags_from_frontmatter(frontmatter: str) -> List[str]:
    """Extract existing tags from YAML frontmatter.
    
    Args:
        frontmatter: The YAML frontmatter content
        
    Returns:
        List of existing tags
    """
    import re
    
    existing_tags = []
    
    # Look for tags section in frontmatter
    tags_match = re.search(r'^tags:\s*\n((?:\s*-\s*.+\n?)*)', frontmatter, re.MULTILINE)
    if tags_match:
        tags_section = tags_match.group(1)
        # Extract individual tags
        tag_matches = re.findall(r'^\s*-\s*(.+)$', tags_section, re.MULTILINE)
        existing_tags = [tag.strip() for tag in tag_matches if tag.strip()]
    
    return existing_tags


def merge_tags(existing_tags: List[str], new_tags: List[str]) -> List[str]:
    """Merge existing and new tags, removing duplicates and sorting.
    
    Args:
        existing_tags: Tags already in frontmatter
        new_tags: Tags extracted from content
        
    Returns:
        Merged and sorted list of unique tags
    """
    all_tags = existing_tags + new_tags
    # Remove duplicates and sort
    return sorted(list(set(tag.lower() for tag in all_tags if tag.strip())))


def clean_old_properties_and_migrate(frontmatter: str) -> Tuple[str, str]:
    """Remove old PARA properties and migrate area to subcategory if needed.
    
    Args:
        frontmatter: The existing frontmatter content
        
    Returns:
        (cleaned_frontmatter, migrated_subcategory): Tuple of cleaned frontmatter and area value to migrate
    """
    import re
    
    # Extract area value before removing it
    area_match = re.search(r'^area:\s*(.*)$', frontmatter, re.MULTILINE)
    migrated_area = ""
    if area_match:
        area_value = area_match.group(1).strip()
        if area_value and area_value.lower() not in ['', 'none', 'null']:
            migrated_area = area_value.lower()
    
    # Remove old properties: project, resource, area
    old_properties = ['project', 'resource', 'area']
    cleaned_frontmatter = frontmatter
    
    for prop in old_properties:
        # Remove the property line
        cleaned_frontmatter = re.sub(rf'^{prop}:.*$\n?', '', cleaned_frontmatter, flags=re.MULTILINE)
    
    return cleaned_frontmatter, migrated_area


def clean_url_generated_tags(tags_list: List[str]) -> List[str]:
    """Remove tags that look like they were generated from URLs.
    
    Args:
        tags_list: List of existing tags
        
    Returns:
        Cleaned list of tags without URL-generated ones
    """
    import re
    
    cleaned_tags = []
    
    # Patterns that indicate a tag was likely generated from a URL
    url_tag_patterns = [
        r'^pdp-.*',  # Product detail page patterns
        r'^post-\d+$',  # Post ID patterns
        r'^[a-f0-9]{8,}$',  # Long hex strings (hashes)
        r'^utm[-_].*',  # UTM parameters
        r'^ref[-_].*',  # Referral parameters
        r'^[0-9]{8,}$',  # Long number sequences
        r'.*-container$',  # Container suffixes common in URLs
        r'.*-wrapper$',   # Wrapper suffixes common in URLs
        r'.*-section$',   # Section suffixes common in URLs
    ]
    
    for tag in tags_list:
        is_url_tag = False
        for pattern in url_tag_patterns:
            if re.match(pattern, tag, re.IGNORECASE):
                is_url_tag = True
                break
        
        if not is_url_tag:
            cleaned_tags.append(tag)
    
    return cleaned_tags


def reorder_frontmatter_properties(frontmatter: str) -> str:
    """Reorder frontmatter properties to the correct order.
    
    Args:
        frontmatter: The existing frontmatter content
        
    Returns:
        Frontmatter with properties in the correct order
    """
    import re
    
    # Define the correct order
    property_order = ['created', 'para', 'category', 'subcategory', 'priority', 'tags', 'archived']
    
    # Extract all properties from the frontmatter
    properties = {}
    
    # Handle tags specially since they can be multi-line
    tags_match = re.search(r'^tags:\s*\n((?:\s*-\s*.+\n?)*)', frontmatter, re.MULTILINE)
    if tags_match:
        full_tags = f"tags:\n{tags_match.group(1).rstrip()}"
        properties['tags'] = full_tags
        # Remove tags from frontmatter for other property processing
        frontmatter_without_tags = re.sub(
            r'^tags:.*?(?=\n\w|\n---|\Z)', '', frontmatter,
            flags=re.MULTILINE | re.DOTALL
        )
    else:
        # Check for empty tags line
        tags_empty_match = re.search(r'^tags:\s*$', frontmatter, re.MULTILINE)
        if tags_empty_match:
            properties['tags'] = 'tags:'
            frontmatter_without_tags = re.sub(r'^tags:\s*$\n?', '', frontmatter, flags=re.MULTILINE)
        else:
            frontmatter_without_tags = frontmatter
    
    # Extract other single-line properties
    for prop in property_order:
        if prop == 'tags':
            continue  # Already handled above
        
        prop_match = re.search(rf'^{prop}:\s*(.*)$', frontmatter_without_tags, re.MULTILINE)
        if prop_match:
            value = prop_match.group(1).strip()
            properties[prop] = f"{prop}: {value}"
    
    # Rebuild frontmatter in correct order
    ordered_lines = []
    for prop in property_order:
        if prop in properties:
            ordered_lines.append(properties[prop])
    
    return '\n'.join(ordered_lines)


def update_existing_frontmatter(content: str, file_path: Path) -> Tuple[str, bool]:
    """Update existing frontmatter to add missing properties.
    
    Args:
        content: The file content with existing frontmatter
        file_path: Path to the file for context extraction
        
    Returns:
        (updated_content, was_updated): Tuple of updated content and whether changes were made
    """
    import re
    
    # Extract the existing frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not frontmatter_match:
        return content, False
    
    existing_frontmatter = frontmatter_match.group(1)
    body_content = frontmatter_match.group(2)
    
    # Clean old properties and get migrated area value
    cleaned_frontmatter, migrated_area = clean_old_properties_and_migrate(existing_frontmatter)
    has_old_properties = cleaned_frontmatter != existing_frontmatter
    
    # Check which properties are missing
    required_properties = ['created', 'para', 'category', 'subcategory', 'priority', 'tags', 'archived']
    missing_properties = []
    
    for prop in required_properties:
        if not re.search(rf'^{prop}:', cleaned_frontmatter, re.MULTILINE):
            missing_properties.append(prop)
    
    # Check if properties are in the correct order
    current_order = []
    for prop in required_properties:
        if re.search(rf'^{prop}:', cleaned_frontmatter, re.MULTILINE):
            current_order.append(prop)
    
    needs_reordering = current_order != [prop for prop in required_properties if prop in current_order]
    
    # Clean existing tags from URL-generated ones
    existing_tags = extract_existing_tags_from_frontmatter(cleaned_frontmatter)
    cleaned_existing_tags = clean_url_generated_tags(existing_tags)
    needs_tag_cleanup = len(cleaned_existing_tags) != len(existing_tags)
    
    # Check if we need to update existing tags with new ones from content
    has_existing_tags = bool(re.search(r'^tags:', cleaned_frontmatter, re.MULTILINE))
    new_tags_from_content = extract_remaining_tags(body_content)
    needs_tag_update = has_existing_tags and (new_tags_from_content or needs_tag_cleanup)
    
    if not missing_properties and not needs_tag_update and not has_old_properties and not needs_reordering:
        return content, False
    
    # Extract values for missing properties
    para_type, category = extract_para_and_category_from_path(file_path)
    is_archived = is_in_archive_directory(file_path)
    subcategory = extract_subcategory_from_content(body_content)
    priority = extract_priority_from_content(body_content)
    
    # Use migrated area as subcategory if subcategory is empty and area was migrated
    if migrated_area and not subcategory:
        subcategory = migrated_area
    
    archived_value = "true" if is_archived else "false"
    
    # Handle tags merging and cleaning
    if needs_tag_update:
        merged_tags = merge_tags(cleaned_existing_tags, new_tags_from_content)
        
        # Update the existing tags section
        if merged_tags:
            new_tags_section = "tags:\n" + "\n".join(f"  - {tag}" for tag in merged_tags)
        else:
            new_tags_section = "tags:"
        
        # Replace the existing tags section
        updated_frontmatter = re.sub(
            r'^tags:.*?(?=\n\w|\n---|\Z)',
            new_tags_section,
            cleaned_frontmatter,
            flags=re.MULTILINE | re.DOTALL
        )
    else:
        updated_frontmatter = cleaned_frontmatter
    
    # Ensure all values are lowercase where appropriate
    para_type = para_type.lower() if para_type else ""
    category = category.lower() if category else ""
    subcategory = subcategory.lower() if subcategory else ""
    
    # Add missing properties
    for prop in missing_properties:
        if prop == 'created':
            updated_frontmatter += "\ncreated: <% tp.file.creation_date() %>"
        elif prop == 'para':
            updated_frontmatter += f"\npara: {para_type}"
        elif prop == 'category':
            updated_frontmatter += f"\ncategory: {category}"
        elif prop == 'subcategory':
            updated_frontmatter += f"\nsubcategory: {subcategory}"
        elif prop == 'archived':
            updated_frontmatter += f"\narchived: {archived_value}"
        elif prop == 'priority':
            updated_frontmatter += f"\npriority: {priority}"
        elif prop == 'tags':
            if new_tags_from_content:
                updated_frontmatter += "\ntags:\n" + "\n".join(f"  - {tag}" for tag in new_tags_from_content)
            else:
                updated_frontmatter += "\ntags:"
    
    # Reorder properties to the correct sequence
    updated_frontmatter = reorder_frontmatter_properties(updated_frontmatter)
    
    # Remove tags from body content if we processed any tag-related properties
    cleaned_body_content = body_content
    if any(prop in ['subcategory', 'priority', 'tags'] for prop in missing_properties) or needs_tag_update:
        cleaned_body_content = remove_all_tags(body_content)
    
    # Reconstruct the content
    updated_content = f"---\n{updated_frontmatter}\n---\n{cleaned_body_content}"
    
    return updated_content, True


def extract_subcategory_from_content(content: str) -> str:
    """Extract subcategory from #cat- prefixed tags in markdown content.
    
    Args:
        content: The markdown file content
        
    Returns:
        The subcategory value (e.g., "media" from "#cat-media") or empty string
    """
    import re
    
    # Find all #cat- prefixed tags
    cat_tags = re.findall(r'#cat-(\w+)', content, re.IGNORECASE)
    
    # Return the first found subcategory, or empty string if none found
    return cat_tags[0].lower() if cat_tags else ""


def extract_priority_from_content(content: str) -> str:
    """Extract priority from #p prefixed tags in markdown content.
    
    Args:
        content: The markdown file content
        
    Returns:
        The priority value (e.g., "1" from "#p1") or empty string
    """
    import re
    
    # Find all #p prefixed tags with numbers
    priority_tags = re.findall(r'#p(\d+)', content, re.IGNORECASE)
    
    # Return the first found priority, or empty string if none found
    return priority_tags[0] if priority_tags else ""


def extract_remaining_tags(content: str) -> List[str]:
    """Extract all hashtags from content except #cat- and #p tags, and exclude URL fragments.
    
    Args:
        content: The markdown file content
        
    Returns:
        List of tag names (without the # prefix)
    """
    import re
    
    # Remove URLs from content temporarily to avoid extracting URL fragments as tags
    # Match various URL patterns including http(s), www, and markdown links
    url_patterns = [
        r'https?://[^\s\]]+',  # http/https URLs
        r'www\.[^\s\]]+',      # www URLs
        r'\[.*?\]\([^\)]*\)',  # Markdown links [text](url)
        r'<[^>]*>',            # Angle bracket URLs <url>
    ]
    
    content_without_urls = content
    for pattern in url_patterns:
        content_without_urls = re.sub(pattern, '', content_without_urls, flags=re.IGNORECASE)
    
    # Find all hashtags in content without URLs
    all_tags = re.findall(r'#(\w+(?:-\w+)*)', content_without_urls)
    
    # Filter out cat- and p tags
    remaining_tags = []
    for tag in all_tags:
        tag_lower = tag.lower()
        # Skip cat- prefixed tags and p followed by numbers
        if not (tag_lower.startswith('cat-') or re.match(r'^p\d+$', tag_lower)):
            remaining_tags.append(tag.lower())
    
    # Remove duplicates and sort
    return sorted(list(set(remaining_tags)))


def remove_all_tags(content: str) -> str:
    """Remove all hashtags from content after extraction, but preserve URL fragments.
    
    Args:
        content: The markdown file content
        
    Returns:
        Content with all hashtags removed except those in URLs
    """
    import re
    
    # First, protect URLs by temporarily replacing them with placeholders
    urls = []
    url_patterns = [
        r'https?://[^\s\]]+',  # http/https URLs
        r'www\.[^\s\]]+',      # www URLs
        r'\[.*?\]\([^\)]*\)',  # Markdown links [text](url)
        r'<[^>]*>',            # Angle bracket URLs <url>
    ]
    
    protected_content = content
    url_counter = 0
    for pattern in url_patterns:
        def replace_url(match):
            nonlocal url_counter
            urls.append(match.group(0))
            placeholder = f"__URL_PLACEHOLDER_{url_counter}__"
            url_counter += 1
            return placeholder
        protected_content = re.sub(pattern, replace_url, protected_content, flags=re.IGNORECASE)
    
    # Remove hashtags from protected content
    protected_content = re.sub(r'#\w+(?:-\w+)*\s*', '', protected_content)
    
    # Restore URLs
    for i, url in enumerate(urls):
        protected_content = protected_content.replace(f"__URL_PLACEHOLDER_{i}__", url)
    
    # Clean up any multiple spaces or trailing spaces on lines
    protected_content = re.sub(r' +', ' ', protected_content)  # Multiple spaces to single space
    protected_content = re.sub(r' +\n', '\n', protected_content)  # Trailing spaces before newlines
    
    return protected_content


def create_journal_frontmatter(content: str = "") -> str:
    """Create simplified YAML frontmatter for journal files."""
    # Extract remaining tags from content (excluding cat- and p tags)
    remaining_tags = extract_remaining_tags(content)
    
    # Format tags as YAML list
    tags_section = "tags:"
    if remaining_tags:
        tags_section += "\n" + "\n".join(f"  - {tag}" for tag in remaining_tags)
    
    frontmatter = f"""---
created: <% tp.file.creation_date() %>
para: journal
{tags_section}
---

"""
    return frontmatter


def create_archive_frontmatter() -> str:
    """Create simplified YAML frontmatter for archive files."""
    frontmatter = """---
created: <% tp.file.creation_date() %>
para: project
category:
subcategory:
priority:
tags:
archived: true
---

"""
    return frontmatter


def create_inbox_frontmatter() -> str:
    """Create empty YAML frontmatter for inbox files to be populated manually."""
    frontmatter = """---
created: <% tp.file.creation_date() %>
para:
category:
subcategory:
priority:
tags:
archived: false
---

"""
    return frontmatter


def create_frontmatter(file_path: Path, content: str = "") -> str:
    """Create the YAML front matter template."""
    # Extract para type and category from path
    para_type, category = extract_para_and_category_from_path(file_path)
    
    # Handle journal files differently
    if para_type == "journal":
        return create_journal_frontmatter(content)
    
    # Handle inbox files differently
    if para_type == "inbox":
        return create_inbox_frontmatter()
    
    # Check if file is in archive directory
    is_archived = is_in_archive_directory(file_path)
    
    # Handle archive files differently
    if is_archived:
        return create_archive_frontmatter()
    # Extract subcategory, priority, and remaining tags from content
    subcategory = extract_subcategory_from_content(content)
    priority = extract_priority_from_content(content)
    remaining_tags = extract_remaining_tags(content)
    
    archived_value = "true" if is_archived else "false"
    
    # Ensure all values are lowercase where appropriate
    para_type = para_type.lower() if para_type else ""
    category = category.lower() if category else ""
    subcategory = subcategory.lower() if subcategory else ""
    
    # Format tags as YAML list
    tags_section = "tags:"
    if remaining_tags:
        tags_section += "\n" + "\n".join(f"  - {tag}" for tag in remaining_tags)
    
    frontmatter = f"""---
created: <% tp.file.creation_date() %>
para: {para_type}
category: {category}
subcategory: {subcategory}
priority: {priority}
{tags_section}
archived: {archived_value}
---

"""
    return frontmatter


def is_in_archive_directory(file_path: Path) -> bool:
    """Check if the file is in the archive directory."""
    parts = file_path.parts
    
    for part in parts:
        part_lower = part.lower()
        if "04" in part and "archive" in part_lower:
            return True
    
    return False


def extract_para_and_category_from_path(file_path: Path) -> Tuple[str, str]:
    """Extract para type and category from file path based on directory structure.
    
    Supports both old subdirectory structure and new flat structure:
    - 01 - Projects/Advanced Directive/note.md → para: project, category: "advanced directive"
    - 01 - Projects/note.md → para: project, category: ""
    - 02 - Areas/Family/note.md → para: area, category: "family"
    - 02 - Areas/note.md → para: area, category: ""
    """
    parts = file_path.parts
    
    # Look for PARA directory patterns
    for i, part in enumerate(parts):
        part_lower = part.lower()
        
        # Check for "01 - Projects"
        if "01" in part and "project" in part_lower:
            # Check if there's a subdirectory after the Projects folder
            if i + 1 < len(parts) and not parts[i + 1].endswith('.md'):
                category = parts[i + 1].lower()
                return "project", category
            return "project", ""
        
        # Check for "02 - Areas"
        elif "02" in part and "area" in part_lower:
            # Check if there's a subdirectory after the Areas folder
            if i + 1 < len(parts) and not parts[i + 1].endswith('.md'):
                category = parts[i + 1].lower()
                return "area", category
            return "area", ""
        
        # Check for "03 - Resources"
        elif "03" in part and "resource" in part_lower:
            # Check if there's a subdirectory after the Resources folder
            if i + 1 < len(parts) and not parts[i + 1].endswith('.md'):
                category = parts[i + 1].lower()
                return "resource", category
            return "resource", ""
        
        # Check for "04 - Archive"
        elif "04" in part and "archive" in part_lower:
            # Archive files should have para: project and archived: true
            return "project", ""
        
        # Check for "05 - Journal"
        elif "05" in part and "journal" in part_lower:
            return "journal", ""
        
        # Check for "00 - INBOX"
        elif "00" in part and "inbox" in part_lower:
            return "inbox", ""
    
    # Default values if no PARA directory found
    return "", ""


def should_move_file(file_path: Path) -> Tuple[bool, Path]:
    """Check if file should be moved from subdirectory to parent PARA directory.
    
    Returns:
        (should_move, new_path): Tuple indicating if file should move and the target path
    """
    parts = file_path.parts
    
    # Look for PARA directory patterns with subdirectories
    for i, part in enumerate(parts):
        part_lower = part.lower()
        
        # Check if this is a PARA directory with a subdirectory (excluding journal)
        is_para_dir = (
            ("01" in part and "project" in part_lower) or
            ("02" in part and "area" in part_lower) or
            ("03" in part and "resource" in part_lower) or
            ("04" in part and "archive" in part_lower)
        )
        
        # Skip journal directories - they should keep their subdirectories
        is_journal_dir = "05" in part and "journal" in part_lower
        if is_journal_dir:
            continue
        
        if is_para_dir:
            # Check if there's a subdirectory after the PARA folder
            if i + 1 < len(parts) and not parts[i + 1].endswith('.md'):
                # File is in a subdirectory, should be moved to parent PARA directory
                new_parts = parts[:i+1] + parts[i+2:]  # Remove the subdirectory part
                new_path = Path(*new_parts)
                return True, new_path
            break
    
    return False, file_path


def should_exclude_path(file_path: Path, exclude_folders: List[str], exclude_files: List[str]) -> bool:
    """Check if the file path should be excluded."""
    # Check if file is in excluded files list
    if file_path.name in exclude_files:
        return True
    
    # Check if any parent folder is in the exclude list
    for folder in exclude_folders:
        if folder in file_path.parts:
            return True
    
    return False


def process_markdown_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, bool]:
    """Process a single markdown file to add properties and move if needed.
    
    Returns:
        (properties_added, file_moved): Tuple indicating what actions were taken
    """
    import shutil
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        properties_added = False
        file_moved = False
        updated_content = content
        
        # Handle frontmatter - add if missing or update if incomplete
        if not has_frontmatter(content):
            # Add front matter to the beginning of the file
            updated_content = create_frontmatter(file_path, content) + remove_all_tags(content)
            properties_added = True
        else:
            # Update existing frontmatter if missing properties
            updated_content, was_updated = update_existing_frontmatter(content, file_path)
            if was_updated:
                properties_added = True
            
            # Remove all tags from the body content if there are any tags
            remaining_tags = extract_remaining_tags(content)
            has_cat_tags = bool(extract_subcategory_from_content(content))
            has_priority_tags = bool(extract_priority_from_content(content))
            
            if remaining_tags or has_cat_tags or has_priority_tags:
                # Extract body content and remove all tags
                import re
                frontmatter_match = re.match(r'^(---\n.*?\n---\n)(.*)', updated_content, re.DOTALL)
                if frontmatter_match:
                    frontmatter_part = frontmatter_match.group(1)
                    body_part = frontmatter_match.group(2)
                    cleaned_body = remove_all_tags(body_part)
                    updated_content = frontmatter_part + cleaned_body
                    properties_added = True  # Mark as updated since we removed tags
        
        # Write the updated content if changes were made
        if properties_added and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        # Check if file should be moved from subdirectory to parent PARA directory
        should_move, new_path = should_move_file(file_path)
        
        if should_move:
            if not dry_run:
                # Ensure the target directory exists
                new_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Handle filename conflicts
                counter = 1
                original_new_path = new_path
                while new_path.exists():
                    stem = original_new_path.stem
                    suffix = original_new_path.suffix
                    new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                # Move the file
                shutil.move(str(file_path), str(new_path))
            
            file_moved = True
        
        return properties_added, file_moved
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, False


def remove_empty_directories(directory: Path, dry_run: bool = False) -> int:
    """Remove empty directories recursively, starting from the deepest level.
    
    Returns:
        Number of directories that were (or would be) removed
    """
    import os
    
    removed_count = 0
    
    # Walk the directory tree bottom-up (deepest first)
    for root, dirs, files in os.walk(directory, topdown=False):
        current_dir = Path(root)
        
        # Skip the root directory itself
        if current_dir == directory:
            continue
            
        try:
            # Check if directory is empty (no files and no subdirectories)
            if not files and not dirs:
                if not dry_run:
                    current_dir.rmdir()
                removed_count += 1
                if dry_run:
                    print(f"WOULD REMOVE empty directory: {current_dir}")
                else:
                    print(f"REMOVED empty directory: {current_dir}")
        except OSError:
            # Directory might not be empty or might have permission issues
            pass
    
    return removed_count


def find_markdown_files(directory: Path, exclude_folders: List[str], exclude_files: List[str]) -> List[Path]:
    """Find all markdown files in the directory and subdirectories."""
    markdown_files = []
    
    for file_path in directory.rglob("*.md"):
        if not should_exclude_path(file_path, exclude_folders, exclude_files):
            markdown_files.append(file_path)
    
    return markdown_files


def main():
    parser = argparse.ArgumentParser(
        description="Add Obsidian properties to markdown files that don't have them",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all markdown files in a directory
  python obsidian_properties.py /path/to/obsidian/vault
  
  # Exclude specific folders
  python obsidian_properties.py /path/to/vault --exclude-folders .trash templates
  
  # Exclude specific files
  python obsidian_properties.py /path/to/vault --exclude-files README.md index.md
  
  # Dry run to see what would be changed
  python obsidian_properties.py /path/to/vault --dry-run
        """
    )
    
    parser.add_argument(
        "directory",
        type=str,
        help="Directory containing markdown files to process"
    )
    
    parser.add_argument(
        "--exclude-folders",
        nargs="*",
        default=[],
        help="Folder names to exclude from processing"
    )
    
    parser.add_argument(
        "--exclude-files",
        nargs="*",
        default=[],
        help="Specific file names to exclude from processing"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making actual changes"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    # Validate directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return 1
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory")
        return 1
    
    # Find all markdown files
    print(f"Scanning for markdown files in: {directory}")
    if args.exclude_folders:
        print(f"Excluding folders: {', '.join(args.exclude_folders)}")
    if args.exclude_files:
        print(f"Excluding files: {', '.join(args.exclude_files)}")
    
    markdown_files = find_markdown_files(directory, args.exclude_folders, args.exclude_files)
    
    if not markdown_files:
        print("No markdown files found to process")
        return 0
    
    print(f"Found {len(markdown_files)} markdown files")
    
    if args.dry_run:
        print("\n--- DRY RUN MODE ---")
    
    # Process files
    processed_count = 0
    moved_count = 0
    skipped_count = 0
    
    for file_path in markdown_files:
        properties_added, file_moved = process_markdown_file(file_path, dry_run=args.dry_run)
        
        if properties_added:
            processed_count += 1
            status = "WOULD ADD" if args.dry_run else "ADDED"
            if args.verbose or args.dry_run:
                print(f"{status} properties to: {file_path}")
        
        if file_moved:
            moved_count += 1
            move_status = "WOULD MOVE" if args.dry_run else "MOVED"
            if args.verbose or args.dry_run:
                should_move, new_path = should_move_file(file_path)
                print(f"{move_status}: {file_path} → {new_path}")
        
        if not properties_added and not file_moved:
            skipped_count += 1
            if args.verbose:
                print(f"SKIPPED (already has properties): {file_path}")
    
    # Clean up empty directories if any files were moved
    removed_dirs_count = 0
    if moved_count > 0:
        if args.verbose or args.dry_run:
            print("\nCleaning up empty directories...")
        removed_dirs_count = remove_empty_directories(directory, dry_run=args.dry_run)
    
    # Summary
    print("\nSummary:")
    if args.dry_run:
        print(f"  Would add properties to: {processed_count} files")
        print(f"  Would move files: {moved_count} files")
        if removed_dirs_count > 0:
            print(f"  Would remove empty directories: {removed_dirs_count}")
    else:
        print(f"  Added properties to: {processed_count} files")
        print(f"  Moved files: {moved_count} files")
        if removed_dirs_count > 0:
            print(f"  Removed empty directories: {removed_dirs_count}")
    print(f"  Skipped (no changes needed): {skipped_count} files")
    print(f"  Total files processed: {len(markdown_files)}")
    
    return 0


if __name__ == "__main__":
    exit(main())