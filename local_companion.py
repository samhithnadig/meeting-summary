import os
import re
from datetime import datetime

# Configuration - All files stay strictly in your local directory
WORKSPACE_FILE = "workspace.md"
TODO_FILE = "todo_list.md"
HISTORY_FILE = "history_log.md"

def initialize_workspace():
    """Creates a sample workspace file if it doesn't exist yet."""
    if not os.path.exists(WORKSPACE_FILE):
        template = (
            "# Local Workspace Scratchpad\n\n"
            "## Meeting Notes & Brainstorming\n"
            "- Discussed architecture changes. Need to keep latency low.\n\n"
            "## Action Items\n"
            "- [ ] Fix local file-parsing edge cases\n"
            "- [x] Design minimal CLI layout\n"
            "- [ ] Review privacy boundary configurations\n"
        )
        with open(WORKSPACE_FILE, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"[Core] Initialized fresh local workspace: {WORKSPACE_FILE}")

def parse_workspace():
    if not os.path.exists(WORKSPACE_FILE):
        print("[Core] No workspace file found to parse.")
        return

    print("[Core] Scanning local workspace...")
    
    with open(WORKSPACE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex patterns for markdown task lists
    todo_pattern = re.compile(r'^\s*-\s*\[\s*\]\s+(.+)$', re.MULTILINE)
    done_pattern = re.compile(r'^\s*-\s*\[[xX]\]\s+(.+)$', re.MULTILINE)

    todos = todo_pattern.findall(content)
    dones = done_pattern.findall(content)

    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Handle Active Todo List
    if todos:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# Active Action Items\n*Updated: {today_str}*\n\n")
            for item in todos:
                f.write(f"- [ ] {item}\n")
        print(f"[Core] Synced {len(todos)} active tasks to {TODO_FILE}")
    else:
        if os.path.exists(TODO_FILE):
            os.remove(TODO_FILE)
        print("[Core] No active tasks found. Todo list cleared.")

    # 2. Archive Completed Tasks to History Log
    if dones:
        log_exists = os.path.exists(HISTORY_FILE)
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            if not log_exists:
                f.write("# Archive & Accomplishments Log\n\n")
            f.write(f"### Logged on {today_str}\n")
            for item in dones:
                f.write(f"- [x] {item}\n")
            f.write("\n")
        print(f"[Core] Archived {len(dones)} completed tasks to {HISTORY_FILE}")

        # 3. Clean up the Workspace
        # Remove the completed tasks from workspace.md so they don't get double-logged next run
        cleaned_content = content
        for item in dones:
            escaped_item = re.escape(item)
            cleaned_content = re.sub(r'^\s*-\s*\[[xX]\]\s+' + escaped_item + r'$\n?', '', cleaned_content, flags=re.MULTILINE)
        
        with open(WORKSPACE_FILE, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print("[Core] Workspace cleaned of completed tasks.")
    else:
        print("[Core] No new completed tasks to archive.")

if __name__ == "__main__":
    initialize_workspace()
    parse_workspace()
    print("[Core] Local automation execution finished successfully.")
