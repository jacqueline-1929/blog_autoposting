#!/usr/bin/env python3
"""
GHL Auto-Poster - Clean & Efficient
Posts blogs directly to GoHighLevel
"""

import os
import json
from pathlib import Path
from core_exporter import BlogExporter


class GHLPoster:
    """Simple GHL API integration"""
    
    def __init__(self):
        self.api_key = os.getenv('GHL_API_KEY')
        self.location_id = os.getenv('GHL_LOCATION_ID')
        self.api_base = "https://services.leadconnectorhq.com"
        
        # Try loading from config file
        config_file = Path("ghl_config.json")
        if config_file.exists():
            config = json.loads(config_file.read_text())
            self.api_key = self.api_key or config.get('api_key')
            self.location_id = self.location_id or config.get('location_id')
    
    def post_blog(self, post):
        """Post a single blog to GHL"""
        if not self.api_key or not self.location_id:
            print("❌ GHL credentials not set")
            print("   Set GHL_API_KEY and GHL_LOCATION_ID env vars")
            print("   Or create ghl_config.json")
            return False
        
        try:
            import requests
        except ImportError:
            print("❌ Install requests: pip install requests")
            return False
        
        url = f"{self.api_base}/blogs/"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        }
        
        data = {
            "locationId": self.location_id,
            "title": post["Blog Post Title"],
            "slug": post["URL Slug"],
            "content": post["Blog Post Content"],
            "author": post["Author"],
            "category": post["Category "].strip(),
            "tags": post["Blog Post Tags"].split(",") if post["Blog Post Tags"] else [],
            "metaDescription": post["Meta description"],
            "publishedAt": post["Publish Date"],
            "status": "published"
        }
        
        # Remove empty values
        data = {k: v for k, v in data.items() if v}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                print(f"    ✅ Posted to GHL")
                return True
            else:
                print(f"    ❌ Failed: {response.status_code}")
                print(f"       {response.text[:100]}")
                return False
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return False


def main():
    """Main posting function"""
    print("=" * 60)
    print("🚀 GHL AUTO-POSTER")
    print("=" * 60)
    
    # Load blogs
    exporter = BlogExporter(
        source_folder="new_blogs",
        output_folder="csv_blogs"
    )
    
    count = exporter.load_all_blogs()
    if count == 0:
        print("\nℹ️  Add blog files to 'new_blogs/' folder")
        return
    
    # Post to GHL
    print(f"\n📤 Posting {len(exporter.posts)} blog(s) to GHL...")
    poster = GHLPoster()
    
    success = 0
    for i, post in enumerate(exporter.posts, 1):
        print(f"\n[{i}/{len(exporter.posts)}] {post['Blog Post Title']}")
        if poster.post_blog(post):
            success += 1
    
    # Create CSV backup
    print("\n💾 Creating CSV backup...")
    csv_file = exporter.export_csv(filename="ghl_backup.csv")
    
    # Archive files (optional)
    # exporter.archive_processed()
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Posted: {success}/{len(exporter.posts)} blogs")
    print(f"💾 Backup: {csv_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
