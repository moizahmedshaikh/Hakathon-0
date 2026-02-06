# AI Employee - Bronze Level Submission

**Hackathon:** Personal AI Employee Hackathon 0
**Level:** Bronze (Foundation)
**Date:** January 2026

## 🎯 Project Overview

This is a foundational AI Employee system that monitors files and helps organize tasks using:
- **Obsidian** as the knowledge base and dashboard
- **Claude Code** as the reasoning engine
- **Python Watchers** as the sensory system

## 📁 Project Structure

```
AI_Employee_Project/
├── AI_Employee_Vault/          # Obsidian vault (your AI's office)
│   ├── Inbox/                  # Drop files here
│   ├── Needs_Action/           # Tasks pending AI review
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # AI-generated plans
│   ├── Logs/                   # Activity logs
│   ├── Pending_Approval/       # Items awaiting your approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   ├── Dashboard.md            # Real-time overview
│   └── Company_Handbook.md     # AI employee rules
│
├── employee-watchers/          # Python watcher scripts
│   ├── file_watcher.py         # Monitors Inbox folder
│   ├── pyproject.toml          # UV dependencies
│   └── .env                    # Environment variables (not committed)
│
├── skills/                     # Claude Code skills
│   └── file-monitor/
│       └── SKILL.md            # File monitoring skill guide
│
├── README.md                   # This file
├── SETUP.md                    # Setup instructions
└── CLAUDE_CODE_SETUP.md        # Claude Code configuration
```

## ✅ Bronze Level Requirements (COMPLETED)

### 1. Obsidian Vault ✓
- Created vault with all required folders
- Dashboard.md for real-time status
- Company_Handbook.md with AI behavior rules

### 2. File System Watcher ✓
- Python script monitors /Inbox folder
- Creates action files in /Needs_Action
- Detects file type and size automatically

### 3. Claude Code Integration ✓
- Configured to read/write vault files
- Can process tasks from Needs_Action
- Follows Company_Handbook rules

### 4. Basic Folder Structure ✓
- /Inbox - Drop zone for files
- /Needs_Action - Pending tasks
- /Done - Completed tasks

### 5. Agent Skills ✓
- File Monitor skill created with full documentation
- Skill provides guidance to Claude Code

## 🚀 How to Run

### Prerequisites

```bash
# Install Python dependencies
cd employee-watchers
uv sync

# Install Claude Code (if not already installed)
npm install -g @anthropic/claude-code
```

### Start the System

**Terminal 1 - File Watcher:**
```bash
cd employee-watchers
python file_watcher.py ../AI_Employee_Vault
```

**Terminal 2 - Claude Code:**
```bash
cd AI_Employee_Vault
claude
```

### Test the System

1. **Drop a test file:**
   ```bash
   echo "Test content" > AI_Employee_Vault/Inbox/test.txt
   ```

2. **In Claude, say:**
   ```
   Please check /Needs_Action for new tasks and process them.
   ```

3. **Claude will:**
   - Find the action file created by the watcher
   - Read the test.txt file
   - Process it according to Company_Handbook rules
   - Move it to /Done
   - Update Dashboard.md

## 📊 Features Demonstrated

### 1. Automated File Detection
- Watcher continuously monitors Inbox
- Instant notification when files arrive
- Automatic metadata extraction

### 2. Structured Task Creation
- Every file gets an action file with:
  - File details (name, type, size)
  - Suggested actions checklist
  - Timestamp and status
  - Location reference

### 3. Claude Code Processing
- Reads Company_Handbook for behavior rules
- Processes tasks systematically
- Updates Dashboard with progress
- Follows approval workflow for sensitive actions

### 4. Dashboard Updates
- Real-time task counters
- Recent activity log
- Alert section for urgent items
- Folder status overview

## 🎓 Key Learnings

### What Works Well
1. **File-based communication** between watcher and Claude is simple and reliable
2. **Obsidian vault** provides excellent visibility into AI operations
3. **Skills-based approach** makes Claude's capabilities modular and clear
4. **Markdown format** is both human and AI-readable

### Technical Decisions

**Why Python for Watchers?**
- Excellent file system libraries (watchdog)
- Easy to run as background processes
- Simple to debug and extend

**Why Obsidian for Dashboard?**
- Local-first (privacy!)
- Visual graph view of connections
- Fast search and filtering
- Markdown is version-control friendly

**Why Skills for AI Functionality?**
- Documentation lives with code
- Easy to share and reuse
- Clear separation of concerns
- Claude can reference skills during execution

## 🔐 Security Measures

### Bronze Level Security
1. ✅ All data stored locally (no cloud sync)
2. ✅ No automatic external actions
3. ✅ File operations confined to vault
4. ✅ No credentials stored in code

## 📈 Next Steps (Silver Level)

The Silver tier will add:
- Gmail monitoring skill
- WhatsApp integration
- Plan.md generation workflow
- Email MCP server for sending
- Human-in-the-loop approval for emails
- Scheduled tasks via cron

These will be addressed in Silver and Gold tiers.

## 📝 Documentation

- `SETUP.md` - Full installation guide
- `CLAUDE_CODE_SETUP.md` - Claude configuration
- `skills/file-monitor/SKILL.md` - File monitoring skill
- `Company_Handbook.md` - AI behavior rules



## 📄 License

This is a hackathon project. Feel free to use and modify for learning purposes.

---

**Bronze Tier Status: COMPLETE ✅**

This submission demonstrates:
- ✅ Working Obsidian vault with proper structure
- ✅ Functional Python watcher script
- ✅ Claude Code integration with file system
- ✅ Skill-based architecture
- ✅ Basic automation workflow
- ✅ Clear documentation

Ready to proceed to Silver Level! 🚀
