# File Monitor Skill

## Purpose
Monitor the `/Inbox` folder for new files and automatically process them.

## When to Use This Skill
- When files are dropped in the Inbox folder
- When you need to categorize and organize incoming files
- When you want to create action items from uploaded documents

## How It Works

### 1. Detection
The skill watches the `/Inbox` folder continuously for new files.

### 2. Processing Steps
When a new file is detected:

1. **Identify the file type**
   - Document (.pdf, .docx, .txt)
   - Image (.jpg, .png)
   - Spreadsheet (.xlsx, .csv)
   - Other

2. **Create an action file**
   - Move to `/Needs_Action` folder
   - Create a markdown summary file

3. **Update Dashboard**
   - Add entry to Recent Activity
   - Increment pending tasks counter

### 3. Action File Template

For each new file, create a markdown file in `/Needs_Action`:

```markdown
---
type: file_drop
original_name: [filename]
file_type: [document/image/spreadsheet]
size: [file size]
detected: [timestamp]
status: pending
---

# New File: [Filename]

## File Details
- **Original Name:** [filename]
- **Type:** [file type]
- **Size:** [size in KB/MB]
- **Location:** /Inbox/[filename]

## Suggested Actions
- [ ] Review content
- [ ] Categorize  
- [ ] Create follow-up task if needed
- [ ] Archive or delete after processing

## Notes
[AI can add observations here after viewing the file]

---
*Detected by File Monitor Skill*
```

## Implementation Guide

### Python Watcher Script

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
import shutil

class InboxHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        source = Path(event.src_path)
        
        # Skip hidden files and temp files
        if source.name.startswith('.') or source.name.startswith('~'):
            return
        
        # Create action file
        self.create_action_file(source)
        
    def create_action_file(self, file_path):
        # Get file info
        size = file_path.stat().st_size
        size_str = f"{size / 1024:.1f} KB" if size < 1_000_000 else f"{size / 1_048_576:.1f} MB"
        
        # Determine file type
        ext = file_path.suffix.lower()
        file_types = {
            '.pdf': 'document',
            '.docx': 'document', 
            '.txt': 'document',
            '.jpg': 'image',
            '.png': 'image',
            '.xlsx': 'spreadsheet',
            '.csv': 'spreadsheet'
        }
        file_type = file_types.get(ext, 'other')
        
        # Create markdown file
        timestamp = datetime.now().isoformat()
        action_file = self.needs_action / f"FILE_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
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
        
        action_file.write_text(content)
        print(f"✓ Created action file for: {file_path.name}")

def start_monitoring(vault_path):
    event_handler = InboxHandler(vault_path)
    observer = Observer()
    inbox_path = Path(vault_path) / 'Inbox'
    observer.schedule(event_handler, str(inbox_path), recursive=False)
    observer.start()
    print(f"📁 Monitoring {inbox_path}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### How to Run

1. **Install dependencies:**
   ```bash
   uv add watchdog
   ```

2. **Create the watcher script** in your project folder

3. **Run the watcher:**
   ```bash
   python file_watcher.py
   ```

## Claude Code Integration

When Claude Code processes files from `/Needs_Action`:

1. **Read the action file** to understand what was detected
2. **View the actual file** using the `view` tool
3. **Analyze content** and determine next steps
4. **Update the action file** with findings
5. **Move to /Done** when complete

### Example Claude Workflow

```markdown
I see a new file in Needs_Action: "FILE_contract_draft.md"

Let me check what this is about...

[reads action file]

This is a PDF contract. Let me view it:

[uses view tool on /Inbox/contract_draft.pdf]

Analysis:
- This appears to be a service agreement
- Needs legal review
- Has payment terms

I'll update the action file with these notes and flag it for your review.
```

## Success Criteria

✓ Files dropped in /Inbox are detected within 5 seconds
✓ Action files are created in /Needs_Action
✓ Dashboard.md is updated with new pending count
✓ No files are lost or missed

## Troubleshooting

**Problem:** Watcher not detecting files
**Solution:** Check that the watcher script is running and Inbox path is correct

**Problem:** Permission errors
**Solution:** Ensure the script has read/write access to vault folders

## Notes
- This skill runs continuously in the background
- It does NOT make decisions - only creates action items
- Actual file processing is done by Claude Code
- Keep the watcher simple and focused on detection only