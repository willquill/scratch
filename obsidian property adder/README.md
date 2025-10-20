# Obsidian Property Adder

A Python script that automatically adds YAML front matter properties to Obsidian markdown files that don't already have them.

## Features

- **Batch Processing**: Process all markdown files in a directory and its subdirectories
- **Smart Detection**: Automatically skips files that already have YAML front matter
- **Flexible Exclusions**: Exclude specific folders and files from processing
- **Dry Run Mode**: Preview changes before applying them
- **Templater Integration**: Uses Templater plugin syntax for automatic date population
- **PARA Method Support**: Automatically detects and categorizes files based on PARA directory structure
- **Automatic File Movement**: Moves files from subdirectories to parent PARA directories after extracting category info
- **Legacy Property Migration**: Removes old `project`, `resource`, `area` properties and migrates `area` to `subcategory`
- **Smart Tag Filtering**: Excludes hashtags from URLs and removes URL-generated tags from existing files
- **Safe Operation**: Only adds properties to files without existing front matter

## Installation

No installation required! Just ensure you have Python 3.6+ installed.

## Usage

### Basic Usage

```bash
python obsidian_properties.py /path/to/your/obsidian/vault
```

### Advanced Usage

```bash
# Exclude specific folders (like templates or archived content)
python obsidian_properties.py /path/to/vault --exclude-folders .trash templates archive

# Exclude specific files
python obsidian_properties.py /path/to/vault --exclude-files README.md index.md

# Combine exclusions
python obsidian_properties.py /path/to/vault --exclude-folders templates --exclude-files README.md

# Dry run to preview changes
python obsidian_properties.py /path/to/vault --dry-run

# Verbose output to see all operations
python obsidian_properties.py /path/to/vault --verbose

# Full example with all options
python obsidian_properties.py /path/to/vault --exclude-folders .trash templates --exclude-files README.md --dry-run --verbose
```

## Properties Template

The script adds the following YAML front matter to each markdown file:

```yaml
---
created: <% tp.file.creation_date() %>
para:
category:
subcategory:
archived: false
priority:
tags:
  - active
  - authentik
---
```

- **created**: Uses Templater plugin syntax to automatically populate the file's creation date
- **para**: Automatically set based on directory structure (project/area/resource)
- **category**: Automatically extracted from subdirectory names or available for manual categorization
- **subcategory**: Automatically extracted from `#cat-` prefixed tags (e.g., `#cat-media` → `subcategory: media`)
- **archived**: Automatically set to `true` for files in `04 - Archive/`, `false` otherwise
- **priority**: Automatically extracted from `#p` prefixed tags (e.g., `#p1` → `priority: 1`)
- **tags**: Automatically populated with all other hashtags found in the content (excluding `#cat-` and `#p` tags). Existing tags in frontmatter are preserved and merged with new tags from content.

### PARA Method Integration

The script automatically detects the PARA method directory structure:

- Files in `01 - Projects/` → `para: project`, `category: ""`, `archived: false`
- Files in `01 - Projects/Category/` → `para: project`, `category: "category"`, `archived: false`
- Files in `02 - Areas/` → `para: area`, `category: ""`, `archived: false`
- Files in `02 - Areas/Category/` → `para: area`, `category: "category"`, `archived: false`
- Files in `03 - Resources/` → `para: resource`, `category: ""`, `archived: false`
- Files in `03 - Resources/Category/` → `para: resource`, `category: "category"`, `archived: false`
- Files in `04 - Archive/` → `para: ""`, `category: ""`, `archived: true`
- Files elsewhere → `para: ""`, `category: ""`, `archived: false`

The script supports both existing subdirectory structures (extracting category names) and new flat structures.

### Automatic File Movement

When the script encounters files in subdirectories under PARA folders, it will:

1. **Extract the category** from the subdirectory name (e.g., `01 - Projects/Advanced Directive/` → `category: advanced directive`)
2. **Add properties** to the file with the extracted category
3. **Move the file** to the parent PARA directory (e.g., `01 - Projects/Advanced Directive/file.md` → `01 - Projects/file.md`)
4. **Handle naming conflicts** by adding numbers if a file with the same name already exists

This eliminates the need for subdirectories since categorization is now handled by the properties.

## Command Line Options

| Option              | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `directory`         | **Required.** Path to the directory containing markdown files |
| `--exclude-folders` | Space-separated list of folder names to exclude               |
| `--exclude-files`   | Space-separated list of specific file names to exclude        |
| `--dry-run`         | Preview changes without making actual modifications           |
| `--verbose`         | Show detailed output for all operations                       |
| `--help`            | Show help message and exit                                    |

## Examples

### Process entire vault

```bash
python obsidian_properties.py ~/Documents/MyVault
```

### Exclude templates and archived folders

```bash
python obsidian_properties.py ~/Documents/MyVault --exclude-folders Clippings Obsidian .trash
```

Real world use case:

```sh
python obsidian_properties.py ~/Obsidian\ Vault --exclude-folders Clippings Obsidian .trash
```

### Safe preview before making changes

```bash
python obsidian_properties.py ~/Documents/MyVault --dry-run --verbose
```

## Safety Features

- **Non-destructive**: Only adds properties to files without existing front matter
- **Backup recommended**: Always backup your vault before running on important data
- **Dry run**: Test the script with `--dry-run` to see what would change
- **Error handling**: Gracefully handles file access errors and encoding issues

## Testing

A test vault is included in the `test_vault` directory with sample files to demonstrate the script's behavior:

- `note1.md`: File without properties (will have properties added)
- `note2.md`: File with existing properties (will be skipped)
- `templates/template.md`: File in excluded folder (when using `--exclude-folders templates`)

Test the script:

```bash
# Test with the included sample files
python obsidian_properties.py test_vault --dry-run --verbose

# Test excluding the templates folder
python obsidian_properties.py test_vault --exclude-folders templates --dry-run --verbose
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!

## Tips for Obsidian Users

1. **Backup First**: Always backup your vault before running the script
2. **Start Small**: Test on a copy or subset of your vault first
3. **Use Dry Run**: Always run with `--dry-run` first to preview changes
4. **Customize Template**: Modify the `create_frontmatter()` function to match your preferred properties
5. **Common Exclusions**: Consider excluding folders like `.trash`, `templates`, `archive`, or `attachments`

## Troubleshooting

**Q: The script says "No markdown files found"**
A: Check that the directory path is correct and contains .md files

**Q: Some files aren't being processed**
A: They likely already have YAML front matter. Use `--verbose` to see which files are skipped

**Q: I want different properties**
A: Edit the `create_frontmatter()` function in the script to customize the template

**Q: How do I undo changes?**
A: Restore from your backup. This is why we recommend always backing up first!
