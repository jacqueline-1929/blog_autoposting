#!/usr/bin/env python3
"""
Weekly Blog Export - Simple Runner
Run this every week to export blogs
"""

from core_exporter import BlogExporter


def main():
    """Weekly export runner"""
    print("📅 WEEKLY BLOG EXPORT\n")
    
    exporter = BlogExporter(
        source_folder="new_blogs",
        output_folder="csv_blogs"
    )
    
    # Load and export
    count = exporter.load_all_blogs()
    
    if count > 0:
        exporter.export_csv(filename="weekly_blogs.csv")
        # Uncomment to archive processed files:
        # exporter.archive_processed()
    else:
        print("No blogs to export. Add files to 'new_blogs/' folder.")


if __name__ == "__main__":
    main()
