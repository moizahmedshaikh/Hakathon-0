#!/usr/bin/env python3
"""
File Watcher - Monitors Inbox folder for new files
Part of Bronze Tier AI Employee Project
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
import time
import sys

class InboxHandler(FileSystemEventHandler):
    """Handles new file events in the Inbox folder"""
    
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        
        # Create folders if they don't exist
        self.inbox.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)
        
    def on_created(self, event):
        """Called when a new file is created in Inbox"""
        if event.is_directory:
            return
            
        source = Path(event.src_path)
        
        # Skip hidden files, temp files, and system files
        if source.name.startswith('.') or source.name.startswith('~') or source.name == '.DS_Store':
            return
        
        print(f"\n🔔 New file detected: {source.name}")
        
        # Small delay to ensure file is fully written
        time.sleep(0.5)
        
        # Create action file
        self.create_action_file(source)
        
    def create_action_file(self, file_path):
        """Create a markdown action file in Needs_Action folder"""
        
        # Get file info
        try:
            size = file_path.stat().st_size
            size_str = f"{size / 1024:.1f} KB" if size < 1_000_000 else f"{size / 1_048_576:.1f} MB"
        except Exception as e:
            print(f"⚠️  Error getting file size: {e}")
            size_str = "Unknown"
        
        # Determine file type
        ext = file_path.suffix.lower()
        file_types = {
            '.pdf': 'document',
            '.docx': 'document',
            '.doc': 'document',
            '.txt': 'document',
            '.md': 'document',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.xlsx': 'spreadsheet',
            '.xls': 'spreadsheet',
            '.csv': 'spreadsheet'
        }
        file_type = file_types.get(ext, 'other')
        
        # Create markdown file
        timestamp = datetime.now().isoformat()
        safe_filename = "".join(c for c in file_path.stem if c.isalnum() or c in (' ', '-', '_'))
        action_file = self.needs_action / f"FILE_{safe_filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        content = f"""---
type: file_drop
original_name: {file_path.name}
file_type: {file_type}
size: {size_str}
detected: {timestamp}
status: pending
---

# New File: {file_path.name}

## File Details
- **Original Name:** {file_path.name}
- **Type:** {file_type}
- **Size:** {size_str}
- **Location:** /Inbox/{file_path.name}

## Suggested Actions
- [ ] Review content
- [ ] Categorize
- [ ] Create follow-up task if needed
- [ ] Archive or delete after processing

## Notes
*Awaiting AI review*

---
*Detected by File Monitor Skill at {timestamp}*
"""
        
        try:
            action_file.write_text(content)
            print(f"✅ Created action file: {action_file.name}")
        except Exception as e:
            print(f"❌ Error creating action file: {e}")

def main():
    """Main function to start the file watcher"""
    
    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default path - change this to your vault location
        vault_path = Path.home() / 'AI_Employee_Vault'
    
    vault_path = Path(vault_path)
    
    if not vault_path.exists():
        print(f"❌ Error: Vault path does not exist: {vault_path}")
        print(f"Usage: python {sys.argv[0]} /path/to/vault")
        sys.exit(1)
    
    print("=" * 60)
    print("📁 FILE WATCHER - AI Employee")
    print("=" * 60)
    print(f"Vault: {vault_path}")
    print(f"Monitoring: {vault_path / 'Inbox'}")
    print(f"Output: {vault_path / 'Needs_Action'}")
    print("=" * 60)
    print("\n🟢 Watcher is running... (Press Ctrl+C to stop)\n")
    
    # Create and start observer
    event_handler = InboxHandler(vault_path)
    observer = Observer()
    inbox_path = vault_path / 'Inbox'
    
    observer.schedule(event_handler, str(inbox_path), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping watcher...")
        observer.stop()
        print("✅ Watcher stopped successfully")
    
    observer.join()

if __name__ == '__main__':
    main()