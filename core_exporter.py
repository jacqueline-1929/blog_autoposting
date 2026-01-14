#!/usr/bin/env python3
"""
Core Blog Exporter - Clean & Efficient
Reads blog files from folder, exports to CSV
"""

import csv
import re
from datetime import datetime
from pathlib import Path


class BlogExporter:
    """Simple, efficient blog exporter"""
    
    def __init__(self, source_folder="new_blogs", output_folder="csv_blogs"):
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)
        self.posts = []
        
        # Create folders if they don't exist
        self.source_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
    
    def _extract_frontmatter(self, content):
        """Extract YAML frontmatter if present"""
        if not content.strip().startswith('---'):
            return {}, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        metadata = {}
        for line in parts[1].strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
        
        return metadata, parts[2].strip()
    
    def _extract_title(self, content):
        """Extract title from first heading"""
        # Try HTML heading
        match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try markdown heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _make_slug(self, text):
        """Generate clean URL slug"""
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')
    
    def _parse_filename(self, filepath):
        """Extract metadata from filename"""
        name = filepath.stem
        
        # Check for date prefix: 2025-01-15_title
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)', name)
        if date_match:
            return {
                'date': date_match.group(1),
                'slug': date_match.group(2)
            }
        
        return {'slug': name}
    
    def read_blog(self, filepath):
        """Read and parse a single blog file"""
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Extract frontmatter
            frontmatter, body = self._extract_frontmatter(content)
            
            # Extract filename metadata
            file_meta = self._parse_filename(filepath)
            
            # Combine metadata
            meta = {**file_meta, **frontmatter}
            
            # Get title
            title = meta.get('title') or self._extract_title(body)
            if not title:
                title = filepath.stem.replace('-', ' ').replace('_', ' ').title()
            
            # Get slug
            slug = meta.get('slug') or self._make_slug(title)
            
            # Get date
            if 'date' in meta:
                publish_date = f"{meta['date']}T09:00:00+00:00"
            else:
                publish_date = datetime.now().isoformat() + "+00:00"
            
            # Build post
            post = {
                "URL Slug": slug,
                "Publish Date": publish_date,
                "Scheduled Date": meta.get('scheduled_date', ''),
                "Blog Post Title": title,
                "Meta description": meta.get('meta_description', title),
                "Meta Image": meta.get('meta_image', ''),
                "Meta Image Alt text": meta.get('meta_image_alt', ''),
                "Author": meta.get('author', 'Far Beyond Marketing'),
                "Category ": meta.get('category', 'Marketing'),
                "Blog Post Tags": meta.get('tags', ''),
                "Blog Post Content": body
            }
            
            return post
            
        except Exception as e:
            print(f"❌ Error reading {filepath.name}: {e}")
            return None
    
    def load_all_blogs(self):
        """Load all blog files from source folder"""
        extensions = ['*.txt', '*.md', '*.markdown', '*.html']
        files = []
        
        for ext in extensions:
            files.extend(self.source_folder.glob(ext))
        
        if not files:
            print(f"⚠️  No blog files found in {self.source_folder}")
            return 0
        
        print(f"📚 Found {len(files)} blog file(s)")
        
        for filepath in sorted(files):
            print(f"  → {filepath.name}")
            post = self.read_blog(filepath)
            if post:
                self.posts.append(post)
                print(f"    ✅ {post['Blog Post Title']}")
        
        return len(self.posts)
    
    def export_csv(self, filename=None):
        """Export all posts to CSV in output folder"""
        if not self.posts:
            print("❌ No posts to export!")
            return None
        
        if not filename:
            filename = "blog_export.csv"
        
        output_path = self.output_folder / filename
        
        fieldnames = [
            "URL Slug", "Publish Date", "Scheduled Date", "Blog Post Title",
            "Meta description", "Meta Image", "Meta Image Alt text", "Author",
            "Category ", "Blog Post Tags", "Blog Post Content"
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.posts)
        
        print(f"\n✅ Exported {len(self.posts)} blog(s) to: {output_path}")
        return str(output_path)
    
    def archive_processed(self, archive_folder="processed_blogs"):
        """Move processed files to archive"""
        archive = Path(archive_folder)
        archive.mkdir(exist_ok=True)
        
        for filepath in self.source_folder.glob('*'):
            if filepath.suffix in ['.txt', '.md', '.markdown', '.html']:
                new_path = archive / filepath.name
                filepath.rename(new_path)
                print(f"📦 Archived: {filepath.name}")


def main():
    """Main export function"""
    print("=" * 60)
    print("🚀 BLOG EXPORTER")
    print("=" * 60)
    
    exporter = BlogExporter(
        source_folder="new_blogs",
        output_folder="csv_blogs"
    )
    
    # Load all blogs
    count = exporter.load_all_blogs()
    
    if count == 0:
        print("\nℹ️  Add blog files to 'new_blogs/' folder")
        return
    
    # Export to CSV
    csv_file = exporter.export_csv(filename="blog_export.csv")
    
    # Archive files (optional - uncomment to enable)
    # exporter.archive_processed()
    
    print("=" * 60)
    print(f"✅ DONE! CSV ready: {csv_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
