# Complete Setup Guide - Bronze Level

Ye guide tumhe **step-by-step** batayegi ke kaise pure Bronze level ko setup karna hai.

## ⏱️ Estimated Time: 2-3 hours

---

## Part 1: System Prerequisites (30 minutes)

### 1.1 Install Python 3.13+

**Mac:**
```bash
brew install python@3.13
```

**Windows:**
- Download from https://www.python.org/downloads/
- Install karte waqt "Add to PATH" checkbox check karo

**Verify:**
```bash
python --version  # Should show 3.13 or higher
```

### 1.2 Install Node.js v24+

**Mac:**
```bash
brew install node@24
```

**Windows:**
- Download from https://nodejs.org/
- LTS version choose karo

**Verify:**
```bash
node --version  # Should show v24.x.x
npm --version
```

### 1.3 Install UV (Python Package Manager)

```bash
pip install uv
```

**Verify:**
```bash
uv --version
```

### 1.4 Install Git

**Mac:**
```bash
brew install git
```

**Windows:**
- Download from https://git-scm.com/
- Install with default settings

### 1.5 Install Obsidian

- Download from https://obsidian.md/
- Install normally
- Open once to verify it works

### 1.6 Install Claude Code

```bash
# Install globally
npm install -g @anthropic/claude-code

# Verify
claude --version
```

**Important:** Make sure you have a Claude Pro subscription or API key!

---

## Part 2: Project Setup (45 minutes)

### 2.1 Create Project Structure

```bash
# Create main project folder
mkdir AI_Employee_Project
cd AI_Employee_Project

# Create Obsidian vault
mkdir AI_Employee_Vault
cd AI_Employee_Vault

# Create all required folders
mkdir Inbox Needs_Action Done Plans Logs Pending_Approval Approved Rejected

# Go back to project root
cd ..

# Create Python watchers project
mkdir employee-watchers
cd employee-watchers

# Initialize UV project
uv init .

# Install dependencies
uv add watchdog python-dotenv

# Go back to project root
cd ..

# Create skills folder
mkdir -p skills/file-monitor
```

Your structure should now look like:
```
AI_Employee_Project/
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Done/
│   ├── Plans/
│   ├── Logs/
│   ├── Pending_Approval/
│   ├── Approved/
│   └── Rejected/
├── employee-watchers/
│   ├── pyproject.toml
│   └── uv.lock
└── skills/
    └── file-monitor/
```

### 2.2 Create Core Files

Navigate to your `AI_Employee_Vault` folder and create these files:

**Dashboard.md:**
```markdown
# AI Employee Dashboard

---
last_updated: 2026-01-07
status: active
---

## 🎯 Today's Focus
- [ ] Check all pending tasks
- [ ] Review new files
- [ ] Update completed items

## 📊 Quick Stats
- **Pending Tasks:** 0
- **Completed Today:** 0
- **Approval Required:** 0

## 🔔 Recent Activity
<!-- AI will update this section -->

## ⚠️ Alerts
<!-- Important items that need attention -->

---

*Last checked by AI: Never*
```

**Company_Handbook.md:**
```markdown
# Company Handbook - AI Employee Rules

---
version: 1.0
last_updated: 2026-01-07
---

## 🎯 Mission
You are my Personal AI Employee. Help me manage tasks efficiently while keeping me informed and in control.

## ✅ Core Responsibilities

### 1. File Processing
- Monitor files in /Inbox folder
- Create action items in /Needs_Action
- Process files according to type
- Move completed tasks to /Done

### 2. Communication Style
- Always be professional and clear
- Use bullet points for lists
- Keep updates concise
- Update Dashboard after each task

## 🚫 Strict Rules

### Security & Privacy
1. NEVER delete files without confirmation
2. NEVER make changes outside the vault
3. ALWAYS ask before external actions

### Approval Requirements
Ask for approval before:
- Deleting any files
- Making any external calls
- Sharing any information

## 📋 Task Processing Workflow

### When You Find a New Task:
1. Read the task file carefully
2. View the actual file if referenced
3. Determine next steps
4. Create a plan if complex
5. Process or request approval
6. Update Dashboard
7. Move to /Done when complete

## 📊 Reporting

Update Dashboard.md after every task with:
- What you did
- Current status
- Any issues encountered
```

### 2.3 Create File Watcher

In `employee-watchers` folder, create `file_watcher.py`:

```python
#!/usr/bin/env python3
"""File Watcher - Monitors Inbox for new files"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
import time
import sys

class InboxHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        
        self.inbox.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        source = Path(event.src_path)
        
        # Skip system files
        if source.name.startswith('.') or source.name.startswith('~'):
            return
        
        print(f"\n🔔 New file: {source.name}")
        time.sleep(0.5)
        self.create_action_file(source)
        
    def create_action_file(self, file_path):
        try:
            size = file_path.stat().st_size
            size_str = f"{size / 1024:.1f} KB" if size < 1_000_000 else f"{size / 1_048_576:.1f} MB"
        except:
            size_str = "Unknown"
        
        ext = file_path.suffix.lower()
        file_types = {
            '.pdf': 'document', '.docx': 'document', '.txt': 'document',
            '.jpg': 'image', '.png': 'image',
            '.xlsx': 'spreadsheet', '.csv': 'spreadsheet'
        }
        file_type = file_types.get(ext, 'other')
        
        timestamp = datetime.now().isoformat()
        safe_name = "".join(c for c in file_path.stem if c.isalnum() or c in (' ', '-', '_'))
        action_file = self.needs_action / f"FILE_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
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
- **Name:** {file_path.name}
- **Type:** {file_type}
- **Size:** {size_str}
- **Location:** /Inbox/{file_path.name}

## Suggested Actions
- [ ] Review content
- [ ] Process according to type
- [ ] Archive when done

---
*Detected at {timestamp}*
"""
        
        action_file.write_text(content)
        print(f"✅ Created: {action_file.name}")

def main():
    vault_path = sys.argv[1] if len(sys.argv) > 1 else Path.home() / 'AI_Employee_Vault'
    vault_path = Path(vault_path)
    
    if not vault_path.exists():
        print(f"❌ Vault not found: {vault_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("📁 FILE WATCHER")
    print("=" * 60)
    print(f"Vault: {vault_path}")
    print(f"Monitoring: {vault_path / 'Inbox'}")
    print("🟢 Running... (Ctrl+C to stop)\n")
    
    handler = InboxHandler(vault_path)
    observer = Observer()
    observer.schedule(handler, str(vault_path / 'Inbox'), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    main()
```

Make it executable:
```bash
chmod +x file_watcher.py
```

### 2.4 Create Skill Documentation

In `skills/file-monitor/` create `SKILL.md`:

```markdown
# File Monitor Skill

## Purpose
Monitor the /Inbox folder and create action items for new files.

## How It Works

1. Python watcher detects new files
2. Creates markdown file in /Needs_Action
3. Claude processes the action file
4. Claude views the actual file
5. Claude completes the task
6. Moves to /Done

## Claude Workflow

When you see a new file in /Needs_Action:

1. Read the action file
2. Use `view` tool on the actual file in /Inbox
3. Analyze the content
4. Take appropriate action
5. Update Dashboard.md
6. Move action file to /Done

## Example

```
I see FILE_report_20260107.md in Needs_Action.

Let me check what this is...
[reads action file]

This is a PDF report. Let me view it:
[view /Inbox/report.pdf]

This appears to be a Q4 financial report. I'll:
1. Note this in Dashboard
2. Mark as reviewed
3. Move to Done

[Updates Dashboard.md]
[Moves FILE_report_20260107.md to /Done]

Task complete!
```
```

---

## Part 3: Configuration (20 minutes)

### 3.1 Setup Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select `AI_Employee_Vault`
4. Your vault should open with all files visible

### 3.2 Test File Watcher

**Terminal 1:**
```bash
cd AI_Employee_Project/employee-watchers
python file_watcher.py ../AI_Employee_Vault
```

You should see:
```
📁 FILE WATCHER
====================================
Vault: /path/to/AI_Employee_Vault
Monitoring: /path/to/AI_Employee_Vault/Inbox
🟢 Running...
```

**Terminal 2:**
```bash
cd AI_Employee_Project/AI_Employee_Vault
echo "Test file content" > Inbox/test.txt
```

Terminal 1 should show:
```
🔔 New file: test.txt
✅ Created: FILE_test_20260107_143022.md
```

Check `Needs_Action` folder - you should see the action file!

### 3.3 Setup Claude Code

```bash
cd AI_Employee_Project/AI_Employee_Vault
claude
```

When Claude starts, give this prompt:

```
Hello! You are my AI Employee. 

First, please:
1. List the files in the current directory
2. Read Company_Handbook.md to understand your role
3. Check the /Needs_Action folder for any pending tasks

After reading the handbook, tell me:
- What are your main responsibilities?
- What requires my approval?
- What folders should you monitor?
```

---

## Part 4: Testing the Complete System (30 minutes)

### Test 1: Basic File Processing

1. **Drop a file:**
   ```bash
   echo "Meeting notes from client call" > Inbox/meeting_notes.txt
   ```

2. **In Claude, say:**
   ```
   Please check for new tasks and process them.
   ```

3. **Claude should:**
   - Find the action file in /Needs_Action
   - Read meeting_notes.txt
   - Update Dashboard
   - Move to /Done

### Test 2: Dashboard Updates

**Ask Claude:**
```
Please update the Dashboard with current status:
- How many tasks are pending?
- How many were completed?
- What's in the Recent Activity?
```

### Test 3: Multiple Files

```bash
cd Inbox
echo "Report 1" > report1.txt
echo "Report 2" > report2.txt
echo "Report 3" > report3.txt
```

**Ask Claude:**
```
I just added 3 reports. Please:
1. Process all of them
2. Update Dashboard with a summary
3. Move them all to Done
```

---

## Part 5: Verification Checklist

Before submitting Bronze level, verify:

### ✅ Structure
- [ ] All folders created correctly
- [ ] Dashboard.md exists and is readable
- [ ] Company_Handbook.md exists with rules
- [ ] Watcher script is in employee-watchers folder
- [ ] Skill documentation exists

### ✅ Functionality  
- [ ] Watcher detects new files
- [ ] Action files are created in Needs_Action
- [ ] Claude can read all vault files
- [ ] Claude can update Dashboard
- [ ] Claude follows Company_Handbook rules
- [ ] Files move to Done after processing

### ✅ Documentation
- [ ] README.md explains the project
- [ ] SETUP.md has installation steps
- [ ] Skills have clear documentation
- [ ] Comments in code explain key parts

---

## Part 6: Common Issues & Solutions

### Issue: "claude: command not found"
```bash
# Reinstall Claude Code
npm install -g @anthropic/claude-code

# Check PATH
echo $PATH

# Try with full path
/usr/local/bin/claude
```

### Issue: Watcher doesn't detect files
```bash
# Check if watcher is running
ps aux | grep file_watcher

# Check permissions
ls -la AI_Employee_Vault/Inbox

# Try with full path
python file_watcher.py /full/path/to/AI_Employee_Vault
```

### Issue: Claude can't see files
```bash
# Make sure you're IN the vault when starting Claude
cd AI_Employee_Vault
claude

# Or use --cwd flag
claude --cwd /path/to/AI_Employee_Vault
```

### Issue: Permission denied errors
```bash
# Fix folder permissions
chmod -R 755 AI_Employee_Vault
```

---

## Part 7: Next Steps

Congratulations! 🎉 You've completed Bronze Level!

### What You've Built:
✅ Local-first AI workspace (Obsidian)
✅ Automated file detection (Python watcher)
✅ AI reasoning engine (Claude Code)  
✅ Skill-based architecture
✅ Basic task workflow

### Ready for Silver Level?

Silver will add:
- Gmail integration
- Email sending via MCP
- More complex reasoning
- Approval workflows
- Scheduled tasks

---

## 📋 Bronze Submission Checklist

Before submitting:

1. **Code Quality**
   - [ ] All scripts have comments
   - [ ] No hardcoded paths (use sys.argv or config)
   - [ ] Error handling in place

2. **Documentation**
   - [ ] README explains project clearly
   - [ ] Setup guide is step-by-step
   - [ ] Skills are documented
   - [ ] Known limitations listed

3. **Demo**
   - [ ] Record a 5-minute video showing:
     - Starting the watcher
     - Dropping a file
     - Claude processing it
     - Dashboard update
     - Task completion

4. **GitHub**
   - [ ] Create repository
   - [ ] Commit all files (except .env)
   - [ ] Add .gitignore for sensitive files
   - [ ] Push to GitHub

5. **Submit**
   - [ ] Fill submission form
   - [ ] Include GitHub link
   - [ ] Attach demo video
   - [ ] Declare Bronze tier

---

**Setup Complete! Aap ab Bronze Level submit kar sakte ho! 🚀**