# Blog Export System

Clean, efficient blog export and auto-posting for GoHighLevel.

## Quick Start

### Option 1: CSV Export (No Setup)
```bash
python weekly.py
```
Creates `csv_blogs/weekly_blogs.csv` ready for GHL import.

### Option 2: Auto-Post to GHL
```bash
# Setup (one time)
pip install requests
cp ghl_config.json.example ghl_config.json
# Edit ghl_config.json with your credentials

# Run
python ghl_poster.py
```
Blogs automatically post to GHL + CSV backup created.

---

## Files

### Core Scripts (3 files)
- **`core_exporter.py`** - Main export engine
- **`ghl_poster.py`** - Auto-post to GHL
- **`weekly.py`** - Simple weekly runner

### Config
- **`ghl_config.json.example`** - Config template
- **`requirements.txt`** - Dependencies (just requests)

---

## How It Works

```
new_blogs/          →  Script  →  csv_blogs/
  blog1.txt                         weekly_blogs.csv
  blog2.txt                         (all blogs in one CSV)
  blog3.txt
```

---

## Blog File Format

### Simple (Recommended)
**Filename:** `2025-01-15_my-blog.txt`

```html
<h1>My Blog Title</h1>
<p>Content with <a href="...">links</a> and formatting...</p>
```

### With Metadata
**Filename:** `my-blog.txt`

```yaml
---
title: My Blog Title
author: Your Name
category: Marketing
tags: seo,content
meta_description: SEO description
---

<h1>My Blog Title</h1>
<p>Content here...</p>
```

Both work! HTML and markdown both supported.

---

## Folders

- **`new_blogs/`** - Drop blog files here
- **`csv_blogs/`** - CSV exports go here (auto-created)
- **`processed_blogs/`** - Archived files (optional)

---

## GHL Setup

1. Get API key: GHL Settings → API Keys → Create
2. Get location ID: From GHL URL `app.gohighlevel.com/location/[ID]/`
3. Create config:
```bash
cp ghl_config.json.example ghl_config.json
```
4. Edit with your credentials
5. Run: `python ghl_poster.py`

---

## CSV Format

Exports in GHL-compatible format:
- URL Slug (auto-generated)
- Publish Date (from filename or current)
- Title, Content, Author, Category, Tags
- All HTML preserved

---

## Usage Examples

### Weekly Export
```bash
# Drop 5 blog files in new_blogs/
python weekly.py
# Output: csv_blogs/weekly_blogs.csv with all 5 blogs
```

### Auto-Post to GHL
```bash
python ghl_poster.py
# Reads new_blogs/ → Posts to GHL → Creates CSV backup
```

### Core Exporter (Advanced)
```python
from core_exporter import BlogExporter

exporter = BlogExporter()
exporter.load_all_blogs()
exporter.export_csv("custom.csv")
```

---

## Tips

- **Multiple blogs?** Drop all files at once - processes all in one run
- **Archive files?** Uncomment `exporter.archive_processed()` in scripts
- **Automation?** Run `weekly.py` via cron/scheduler

---

## Troubleshooting

**"No blog files found"**
- Check files are in `new_blogs/` folder
- Supported: `.txt`, `.md`, `.markdown`, `.html`

**GHL posting fails**
- Verify credentials in `ghl_config.json`
- Or set env vars: `GHL_API_KEY`, `GHL_LOCATION_ID`

**Install requests**
```bash
pip install requests
```

---

That's it! Drop files, run script, done. 🚀
