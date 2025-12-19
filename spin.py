#!/usr/bin/env python3
"""
SpinThatShit - AI Agent Orchestration System
=============================================
Autonomous multi-agent development orchestrator using Claude Code CLI.

Usage: spinthatshit [--config path] [--resume]

Author: Generated for Martin @ Praut s.r.o.
"""

import os
import sys
import json
import subprocess
import datetime
import time
import re
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import signal

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

VERSION = "1.0.0"
CONTEXT_LIMIT_PERCENT = 50  # Start handoff at this percentage
MAX_RETRIES = 3
AGENT_TIMEOUT_MINUTES = 30

class Colors:
    """Terminal colors for pretty output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    DESIGNER = "designer"
    ENGINEER = "engineer"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    TESTER = "tester"
    SUPERVISOR = "supervisor"
    EVOLVER = "evolver"

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class AgentState:
    """State of a single agent execution"""
    role: str
    started_at: str
    ended_at: Optional[str] = None
    status: str = "running"
    tasks_completed: List[str] = field(default_factory=list)
    context_usage_percent: int = 0
    errors: List[str] = field(default_factory=list)
    handoff_reason: Optional[str] = None

@dataclass
class ProjectState:
    """Complete project state for persistence"""
    project_name: str
    docs_path: str
    dev_path: str
    created_at: str
    last_updated: str
    current_phase: str
    current_agent: Optional[str] = None
    completed_phases: List[str] = field(default_factory=list)
    agent_history: List[Dict] = field(default_factory=list)
    evolution_rules: List[str] = field(default_factory=list)
    known_issues: List[str] = field(default_factory=list)
    collision_log: List[Dict] = field(default_factory=list)

# ============================================================================
# UTILITIES
# ============================================================================

def log(message: str, level: str = "INFO", to_file: bool = True):
    """Log message to terminal and optionally to file"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    color_map = {
        "INFO": Colors.CYAN,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "AGENT": Colors.BLUE,
        "PHASE": Colors.HEADER,
    }
    color = color_map.get(level, Colors.END)
    
    # Terminal output (Czech for user)
    terminal_msg = f"{Colors.DIM}[{timestamp}]{Colors.END} {color}[{level}]{Colors.END} {message}"
    print(terminal_msg)
    
    # File output (English for system)
    if to_file and hasattr(log, 'log_file') and log.log_file:
        english_level = level
        with open(log.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{english_level}] {message}\n")

def run_command(cmd: str, cwd: Optional[str] = None, capture: bool = True) -> tuple[int, str, str]:
    """Run shell command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=AGENT_TIMEOUT_MINUTES * 60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def get_timestamp() -> str:
    """Get ISO timestamp"""
    return datetime.datetime.now().isoformat()

def czech(text: str) -> str:
    """Helper for Czech user-facing text"""
    return text

# ============================================================================
# GIT HANDLER
# ============================================================================

class GitHandler:
    """Handles all Git operations with auto-commit and tagging"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self._ensure_git_repo()
    
    def _ensure_git_repo(self):
        """Initialize git repo if not exists"""
        git_dir = Path(self.repo_path) / ".git"
        if not git_dir.exists():
            run_command("git init", cwd=self.repo_path)
            run_command('git config user.email "spinthatshit@local"', cwd=self.repo_path)
            run_command('git config user.name "SpinThatShit Agent"', cwd=self.repo_path)
            log(czech("Git repozitář inicializován"), "SUCCESS")
    
    def commit(self, message: str) -> bool:
        """Commit all changes with message"""
        run_command("git add -A", cwd=self.repo_path)
        code, out, err = run_command(f'git commit -m "{message}"', cwd=self.repo_path)
        if code == 0:
            log(czech(f"Commit: {message[:50]}..."), "SUCCESS")
            return True
        elif "nothing to commit" in err or "nothing to commit" in out:
            return True
        else:
            log(czech(f"Commit selhal: {err}"), "WARNING")
            return False
    
    def tag(self, tag_name: str, message: str = "") -> bool:
        """Create and push tag"""
        cmd = f'git tag -a "{tag_name}" -m "{message or tag_name}"'
        code, _, err = run_command(cmd, cwd=self.repo_path)
        if code == 0:
            # Try to push tag
            push_code, _, _ = run_command(f'git push origin "{tag_name}"', cwd=self.repo_path)
            if push_code == 0:
                log(czech(f"Tag '{tag_name}' vytvořen a pushnut"), "SUCCESS")
            else:
                log(czech(f"Tag '{tag_name}' vytvořen (push selhal - možná není remote)"), "WARNING")
            return True
        return False
    
    def push(self) -> bool:
        """Push to remote"""
        code, _, err = run_command("git push", cwd=self.repo_path)
        if code == 0:
            log(czech("Změny pushnuty na GitHub"), "SUCCESS")
            return True
        else:
            log(czech(f"Push selhal: {err}"), "WARNING")
            return False
    
    def get_recent_commits(self, count: int = 10) -> List[str]:
        """Get recent commit messages"""
        code, out, _ = run_command(f'git log --oneline -n {count}', cwd=self.repo_path)
        if code == 0:
            return out.strip().split('\n')
        return []

# ============================================================================
# CONTEXT MONITOR
# ============================================================================

class ContextMonitor:
    """Monitors Claude Code context usage"""
    
    # Approximate token limits for Claude
    MAX_CONTEXT_TOKENS = 200000
    
    def __init__(self):
        self.current_estimate = 0
        self.history = []
    
    def estimate_from_output(self, output: str) -> int:
        """Estimate context usage from Claude's output patterns"""
        # Look for context indicators in output
        # Claude Code sometimes shows context usage
        patterns = [
            r'context[:\s]+(\d+)%',
            r'(\d+)%\s*(?:of\s*)?context',
            r'tokens?[:\s]+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output.lower())
            if match:
                value = int(match.group(1))
                if value <= 100:
                    return value
        
        # Fallback: estimate based on output length
        # Rough heuristic: 1 token ≈ 4 characters
        estimated_tokens = len(output) / 4
        estimated_percent = int((estimated_tokens / self.MAX_CONTEXT_TOKENS) * 100)
        
        return min(estimated_percent, 100)
    
    def should_handoff(self, current_percent: int) -> bool:
        """Check if context is approaching limit"""
        return current_percent >= CONTEXT_LIMIT_PERCENT
    
    def record(self, percent: int, agent: str):
        """Record context usage"""
        self.current_estimate = percent
        self.history.append({
            "timestamp": get_timestamp(),
            "agent": agent,
            "percent": percent
        })

# ============================================================================
# JOURNAL SYSTEM
# ============================================================================

class Journal:
    """Persistent journal for agent continuity"""
    
    def __init__(self, journal_path: str):
        self.path = Path(journal_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.path.exists():
            self._create_initial()
    
    def _create_initial(self):
        """Create initial journal structure"""
        content = f"""# Agent Journal / Deník Agentů
Created: {get_timestamp()}

---

## Quick Status / Rychlý Stav
- Current Phase: INITIALIZING
- Last Agent: None
- Last Update: {get_timestamp()}

---

## Agent Handoffs / Předávky Agentů

(Entries will be added here)

---

## Collision Log / Log Kolizí

(Any conflicts or issues will be logged here)

---

## Evolution Notes / Poznámky k Evoluci

(Self-improvement notes will be added here)

---

## Detailed Log / Podrobný Log

"""
        self.path.write_text(content, encoding='utf-8')
    
    def add_entry(self, agent: str, action: str, details: str = "", english_details: str = ""):
        """Add journal entry"""
        timestamp = get_timestamp()
        entry = f"""
### [{timestamp}] {agent}
**Action:** {action}
{f'**Details:** {details}' if details else ''}
{f'**Technical:** {english_details}' if english_details else ''}
---
"""
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def add_handoff(self, from_agent: str, to_agent: str, reason: str, state_summary: str):
        """Record agent handoff"""
        self.add_entry(
            f"{from_agent} → {to_agent}",
            "HANDOFF",
            f"Důvod: {reason}",
            f"State: {state_summary}"
        )
    
    def add_collision(self, description: str, resolution: str):
        """Record a collision/conflict"""
        timestamp = get_timestamp()
        entry = f"\n- [{timestamp}] {description}\n  - Resolution: {resolution}\n"
        
        content = self.path.read_text(encoding='utf-8')
        collision_marker = "## Collision Log"
        if collision_marker in content:
            parts = content.split(collision_marker)
            # Find the next section
            after_collision = parts[1]
            next_section = after_collision.find("\n## ")
            if next_section > 0:
                updated = parts[0] + collision_marker + after_collision[:next_section] + entry + after_collision[next_section:]
            else:
                updated = content + entry
            self.path.write_text(updated, encoding='utf-8')
    
    def get_last_state(self) -> Dict[str, Any]:
        """Parse journal to get last known state"""
        content = self.path.read_text(encoding='utf-8')
        
        state = {
            "last_agent": None,
            "last_action": None,
            "phase": "UNKNOWN"
        }
        
        # Find quick status section
        if "Current Phase:" in content:
            match = re.search(r'Current Phase:\s*(\w+)', content)
            if match:
                state["phase"] = match.group(1)
        
        if "Last Agent:" in content:
            match = re.search(r'Last Agent:\s*(\w+)', content)
            if match:
                state["last_agent"] = match.group(1)
        
        return state
    
    def update_status(self, phase: str, last_agent: str):
        """Update quick status section"""
        content = self.path.read_text(encoding='utf-8')
        
        # Update Current Phase
        content = re.sub(
            r'Current Phase:\s*\w+',
            f'Current Phase: {phase}',
            content
        )
        
        # Update Last Agent
        content = re.sub(
            r'Last Agent:\s*\w+',
            f'Last Agent: {last_agent}',
            content
        )
        
        # Update Last Update
        content = re.sub(
            r'Last Update:\s*[\d\-T:\.]+',
            f'Last Update: {get_timestamp()}',
            content
        )
        
        self.path.write_text(content, encoding='utf-8')

# ============================================================================
# AGENT PROMPTS
# ============================================================================

class AgentPrompts:
    """Prompt templates for each agent role"""
    
    @staticmethod
    def get_base_instructions(role: str, project_context: str, docs_path: str, dev_path: str) -> str:
        """Base instructions for all agents"""
        return f"""You are the {role.upper()} agent in the SpinThatShit orchestration system.

PROJECT CONTEXT:
{project_context}

PATHS:
- Documentation: {docs_path}
- Development: {dev_path}

CRITICAL RULES:
1. After EVERY file edit in {dev_path}, run: git add -A && git commit -m "SHORT_DESCRIPTION"
2. Keep commits atomic and descriptive
3. If context usage exceeds 50%, STOP and write handoff notes to .spinstate/handoff.md
4. Log all significant actions to .spinstate/agent_log.md
5. Read .spinstate/journal.md before starting for previous agent's notes

HANDOFF PROTOCOL:
When you need to stop (context full, task complete, or blocked):
1. Write summary to .spinstate/handoff.md
2. Update .spinstate/checklist.md with progress
3. Commit all changes
4. Exit cleanly

"""

    @staticmethod
    def planner(project_context: str, docs_path: str, dev_path: str) -> str:
        """Planner agent prompt"""
        return AgentPrompts.get_base_instructions("PLANNER", project_context, docs_path, dev_path) + """
YOUR ROLE: Analyze documentation and create comprehensive development plan.

TASKS:
1. Read ALL documentation in the docs folder
2. Analyze current state of the dev folder (if any code exists)
3. Create .spinstate/plan.md with:
   - Project overview
   - Architecture decisions
   - Phase breakdown (each phase should be completable in one agent session)
   - Dependencies between phases
   - Risk assessment

4. Create .spinstate/checklist.md with:
   - [ ] Each task as checkbox
   - Grouped by phase
   - Include which agent type should handle each task
   - Estimated complexity (S/M/L/XL)

5. Create .spinstate/architecture.md with:
   - Tech stack decisions
   - Folder structure
   - Key interfaces/contracts
   - Database schema (if applicable)

OUTPUT FORMAT for plan.md:
```markdown
# Project Plan: {PROJECT_NAME}
Generated: {TIMESTAMP}

## Phase 1: {PHASE_NAME}
Agent: {AGENT_TYPE}
Tasks:
- Task 1 description
- Task 2 description
Deliverables:
- What should exist when done
Dependencies: None / Phase X

## Phase 2: ...
```

When done, write "PLANNER_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def designer(project_context: str, docs_path: str, dev_path: str) -> str:
        """Designer agent prompt"""
        return AgentPrompts.get_base_instructions("DESIGNER", project_context, docs_path, dev_path) + """
YOUR ROLE: Design UI/UX components and visual structure.

TASKS:
1. Read plan.md and architecture.md
2. Create component specifications
3. Design Tailwind CSS patterns
4. Create mockup descriptions or ASCII layouts
5. Define design tokens (colors, spacing, typography)

OUTPUT:
- .spinstate/design/components.md - Component specifications
- .spinstate/design/tokens.md - Design tokens
- .spinstate/design/layouts.md - Layout patterns

Focus on Angular 19 with Tailwind CSS patterns.
When done, write "DESIGNER_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def engineer(project_context: str, docs_path: str, dev_path: str) -> str:
        """Engineer agent prompt"""
        return AgentPrompts.get_base_instructions("ENGINEER", project_context, docs_path, dev_path) + """
YOUR ROLE: Set up infrastructure, DevOps, and foundational architecture.

TASKS:
1. Read plan.md and architecture.md
2. Set up project structure if not exists
3. Configure build tools, Docker, CI/CD basics
4. Set up database schemas and migrations
5. Create base configuration files
6. Set up API structure and routing

TECH STACK FOCUS:
- Django 5.0+ backend
- PostgreSQL 16 with pgvector
- Angular 19.2.16 frontend
- Tailwind CSS 3.4

OUTPUT:
- Working project skeleton
- Database migrations
- Docker configuration
- Environment templates

When done, write "ENGINEER_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def developer(project_context: str, docs_path: str, dev_path: str, current_phase: str = "") -> str:
        """Developer agent prompt"""
        phase_context = f"\nCURRENT PHASE: {current_phase}" if current_phase else ""
        
        return AgentPrompts.get_base_instructions("DEVELOPER", project_context, docs_path, dev_path) + f"""
YOUR ROLE: Implement features according to the plan.
{phase_context}

TASKS:
1. Read checklist.md - find unchecked items for DEVELOPER
2. Read handoff.md if exists - continue from last agent
3. Implement features one by one
4. After each feature:
   - Git commit with descriptive message
   - Mark checkbox in checklist.md as [x]
   - Brief note in agent_log.md
5. Run tests if available
6. If blocked or context full, write detailed handoff

CODING STANDARDS:
- Clean, readable code
- Meaningful variable names
- Comments for complex logic
- Follow existing patterns in codebase

When phase complete or context full, write status to .spinstate/status.txt
"""

    @staticmethod
    def reviewer(project_context: str, docs_path: str, dev_path: str) -> str:
        """Reviewer agent prompt"""
        return AgentPrompts.get_base_instructions("REVIEWER", project_context, docs_path, dev_path) + """
YOUR ROLE: Review code quality and identify issues.

TASKS:
1. Read all code in dev folder
2. Check against plan.md and architecture.md
3. Create .spinstate/review.md with:
   - Code quality assessment
   - Potential bugs found
   - Security concerns
   - Performance issues
   - Suggestions for improvement
   - Duplicate code identification
   - Hardcoded values that should be configurable

4. Update checklist.md with new tasks for fixes if needed
5. Prioritize issues: CRITICAL / HIGH / MEDIUM / LOW

DO NOT make direct code changes. Only document issues.
When done, write "REVIEWER_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def tester(project_context: str, docs_path: str, dev_path: str) -> str:
        """Tester agent prompt"""
        return AgentPrompts.get_base_instructions("TESTER", project_context, docs_path, dev_path) + """
YOUR ROLE: Test the application and verify functionality.

TASKS:
1. Read plan.md for expected functionality
2. Run existing tests
3. Create new tests for untested code
4. Manual testing (if applicable - check URLs, endpoints)
5. Create .spinstate/test_report.md with:
   - Test results summary
   - Failing tests and reasons
   - Coverage gaps
   - Edge cases not handled

6. If tests fail, document clearly what's broken
7. Update checklist.md with fix tasks if needed

When done, write "TESTER_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def supervisor(project_context: str, docs_path: str, dev_path: str) -> str:
        """Supervisor agent prompt - checks for collisions and issues"""
        return AgentPrompts.get_base_instructions("SUPERVISOR", project_context, docs_path, dev_path) + """
YOUR ROLE: Check for conflicts, collisions, and integration issues.

TASKS:
1. Read journal.md - look for patterns of repeated failures
2. Read all agent logs and handoffs
3. Check git history for reverted changes or conflicts
4. Analyze test results and review findings
5. Create .spinstate/supervision_report.md with:
   - Collision detection (same code changed multiple times without resolution)
   - Pattern analysis (recurring issues)
   - Integration problems between components
   - Recommendations for orchestrator rules changes

6. If collisions found, add to journal.md Collision Log section
7. If process improvements identified, add to Evolution Notes

COLLISION TYPES TO WATCH:
- Same file edited by multiple agents without clear progression
- Tests passing then failing on same functionality
- Circular dependencies
- Conflicting implementations of same feature

When done, write "SUPERVISOR_COMPLETE" to .spinstate/status.txt
"""

    @staticmethod
    def evolver(project_context: str, docs_path: str, dev_path: str, spin_path: str) -> str:
        """Evolver agent prompt - improves the orchestration system itself"""
        return AgentPrompts.get_base_instructions("EVOLVER", project_context, docs_path, dev_path) + f"""
YOUR ROLE: Improve the SpinThatShit orchestration system based on project learnings.

ORCHESTRATOR PATH: {spin_path}

TASKS:
1. Read supervision_report.md
2. Analyze what worked and what didn't
3. Read current agent prompts in the orchestrator
4. Create .spinstate/evolution_proposal.md with:
   - What problems occurred
   - Root cause analysis
   - Proposed changes to agent prompts
   - Proposed changes to workflow order
   - New rules or checks to add

5. If approved changes (no human override):
   - Update agent prompts in {spin_path}/prompts/
   - Add new validation rules
   - Improve handoff protocols
   - Update checklist templates

EVOLUTION PRINCIPLES:
- Small, incremental changes
- Don't break working functionality
- Add checks, don't remove them
- Document all changes

When done, write "EVOLVER_COMPLETE" to .spinstate/status.txt
"""

# ============================================================================
# CLAUDE CODE RUNNER
# ============================================================================

class ClaudeRunner:
    """Runs Claude Code CLI with specific prompts"""
    
    def __init__(self, working_dir: str, log_dir: str):
        self.working_dir = working_dir
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.context_monitor = ContextMonitor()
    
    def run_agent(self, role: str, prompt: str, timeout_minutes: int = AGENT_TIMEOUT_MINUTES) -> tuple[bool, str, int]:
        """
        Run Claude Code with given prompt
        Returns: (success, output, context_percent)
        """
        log(czech(f"Spouštím agenta: {role}"), "AGENT")
        
        # Create log file for this run
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{role}_{timestamp}.log"
        
        # Build claude command
        # Using --print for non-interactive mode with full output
        cmd = f'claude --print --dangerously-skip-permissions "{prompt}"'
        
        try:
            # Run with real-time output capture
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            output_lines = []
            start_time = time.time()
            
            while True:
                # Check timeout
                if time.time() - start_time > timeout_minutes * 60:
                    process.kill()
                    log(czech(f"Agent {role} timeout po {timeout_minutes} minutách"), "ERROR")
                    return False, "TIMEOUT", 100
                
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                
                if line:
                    output_lines.append(line)
                    # Write to log file
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(line)
                    
                    # Print summary to terminal (shortened)
                    stripped = line.strip()
                    if stripped and len(stripped) > 0:
                        # Only show significant lines
                        if any(keyword in stripped.lower() for keyword in 
                               ['error', 'success', 'complete', 'created', 'updated', 
                                'commit', 'failed', 'warning', 'task', 'phase']):
                            summary = stripped[:100] + "..." if len(stripped) > 100 else stripped
                            log(f"[{role}] {summary}", "AGENT", to_file=False)
            
            output = ''.join(output_lines)
            exit_code = process.returncode
            
            # Estimate context usage
            context_percent = self.context_monitor.estimate_from_output(output)
            self.context_monitor.record(context_percent, role)
            
            success = exit_code == 0
            
            log(czech(f"Agent {role} dokončen (kontext: ~{context_percent}%)"), 
                "SUCCESS" if success else "ERROR")
            
            return success, output, context_percent
            
        except Exception as e:
            log(czech(f"Chyba při spouštění agenta {role}: {str(e)}"), "ERROR")
            return False, str(e), 0
    
    def check_context_limit(self, current_percent: int) -> bool:
        """Check if we should stop due to context limit"""
        return self.context_monitor.should_handoff(current_percent)

# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class Orchestrator:
    """Main orchestration logic"""
    
    def __init__(self, docs_path: str, dev_path: str):
        self.docs_path = Path(docs_path).resolve()
        self.dev_path = Path(dev_path).resolve()
        self.state_dir = self.dev_path / ".spinstate"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.git = GitHandler(str(self.dev_path))
        self.journal = Journal(str(self.state_dir / "journal.md"))
        self.runner = ClaudeRunner(str(self.dev_path), str(self.state_dir / "logs"))
        
        # Set up logging
        log.log_file = str(self.state_dir / "orchestrator.log")
        
        # Load or create state
        self.state = self._load_state()
        
        # Agent workflow order
        self.workflow = [
            AgentRole.PLANNER,
            AgentRole.DESIGNER,
            AgentRole.ENGINEER,
            AgentRole.DEVELOPER,
            AgentRole.REVIEWER,
            AgentRole.TESTER,
            AgentRole.SUPERVISOR,
        ]
        
        log(czech(f"Orchestrátor inicializován"), "SUCCESS")
        log(czech(f"  Dokumentace: {self.docs_path}"), "INFO")
        log(czech(f"  Vývoj: {self.dev_path}"), "INFO")
    
    def _load_state(self) -> ProjectState:
        """Load or create project state"""
        state_file = self.state_dir / "state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return ProjectState(**data)
            except:
                pass
        
        # Create new state
        return ProjectState(
            project_name=self.dev_path.name,
            docs_path=str(self.docs_path),
            dev_path=str(self.dev_path),
            created_at=get_timestamp(),
            last_updated=get_timestamp(),
            current_phase="INIT"
        )
    
    def _save_state(self):
        """Save project state"""
        self.state.last_updated = get_timestamp()
        state_file = self.state_dir / "state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.state), f, indent=2, ensure_ascii=False)
    
    def _get_project_context(self) -> str:
        """Read documentation to get project context"""
        context_parts = []
        
        # Read README if exists
        for readme_name in ['README.md', 'readme.md', 'README.txt']:
            readme_path = self.docs_path / readme_name
            if readme_path.exists():
                context_parts.append(f"README:\n{readme_path.read_text(encoding='utf-8')[:2000]}")
                break
        
        # List doc files
        doc_files = list(self.docs_path.glob('**/*.md')) + list(self.docs_path.glob('**/*.txt'))
        if doc_files:
            context_parts.append(f"Documentation files: {', '.join(f.name for f in doc_files[:20])}")
        
        # Check existing code
        dev_files = list(self.dev_path.glob('**/*.py')) + list(self.dev_path.glob('**/*.ts'))
        if dev_files:
            context_parts.append(f"Existing code files: {len(dev_files)} files")
        
        return '\n\n'.join(context_parts) if context_parts else "New project - no existing documentation"
    
    def _get_prompt_for_agent(self, role: AgentRole) -> str:
        """Get appropriate prompt for agent role"""
        context = self._get_project_context()
        
        prompt_map = {
            AgentRole.PLANNER: AgentPrompts.planner,
            AgentRole.DESIGNER: AgentPrompts.designer,
            AgentRole.ENGINEER: AgentPrompts.engineer,
            AgentRole.DEVELOPER: AgentPrompts.developer,
            AgentRole.REVIEWER: AgentPrompts.reviewer,
            AgentRole.TESTER: AgentPrompts.tester,
            AgentRole.SUPERVISOR: AgentPrompts.supervisor,
        }
        
        if role in prompt_map:
            return prompt_map[role](context, str(self.docs_path), str(self.dev_path))
        
        return AgentPrompts.get_base_instructions(role.value, context, str(self.docs_path), str(self.dev_path))
    
    def _check_agent_status(self) -> Optional[str]:
        """Check status file for agent completion"""
        status_file = self.state_dir / "status.txt"
        if status_file.exists():
            status = status_file.read_text(encoding='utf-8').strip()
            # Clear status file
            status_file.unlink()
            return status
        return None
    
    def _analyze_failure(self, role: str, output: str) -> tuple[str, str]:
        """Analyze why agent failed and suggest fix"""
        # Common failure patterns
        patterns = {
            r'permission denied': ("Permission issue", "Check file permissions and ownership"),
            r'command not found': ("Missing dependency", "Install required tools"),
            r'syntax error': ("Code syntax error", "Review recent changes for typos"),
            r'import error|module not found': ("Missing module", "Install required packages"),
            r'connection refused': ("Service not running", "Check if required services are up"),
            r'out of memory': ("Memory exhausted", "Reduce batch size or clear caches"),
            r'timeout': ("Operation timeout", "Increase timeout or optimize operation"),
        }
        
        output_lower = output.lower()
        for pattern, (issue, fix) in patterns.items():
            if re.search(pattern, output_lower):
                return issue, fix
        
        return "Unknown error", "Review agent logs for details"
    
    def run_agent(self, role: AgentRole, retry_count: int = 0) -> bool:
        """Run a single agent with retry logic"""
        log(czech(f"\n{'='*60}"), "PHASE")
        log(czech(f"FÁZE: {role.value.upper()}"), "PHASE")
        log(czech(f"{'='*60}\n"), "PHASE")
        
        self.state.current_agent = role.value
        self._save_state()
        
        # Update journal
        self.journal.update_status(role.value, role.value)
        self.journal.add_entry(role.value, "STARTED", f"Agent {role.value} zahájen")
        
        # Create git tag for phase start
        tag_name = f"phase-{role.value}-start-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.git.tag(tag_name, f"Starting {role.value} phase")
        
        # Get prompt and run
        prompt = self._get_prompt_for_agent(role)
        success, output, context_percent = self.runner.run_agent(role.value, prompt)
        
        # Check completion status
        status = self._check_agent_status()
        
        if success and status and "COMPLETE" in status:
            # Agent completed successfully
            self.journal.add_entry(role.value, "COMPLETED", f"Agent dokončen úspěšně")
            self.state.completed_phases.append(role.value)
            self.git.commit(f"[{role.value}] Phase completed")
            self.git.push()
            self._save_state()
            return True
        
        elif context_percent >= CONTEXT_LIMIT_PERCENT:
            # Context limit reached - handoff
            log(czech(f"Kontext na {context_percent}% - předávám dalšímu agentovi"), "WARNING")
            self.journal.add_handoff(
                role.value, 
                role.value,
                f"Context limit reached ({context_percent}%)",
                "Continuing from handoff.md"
            )
            self.git.commit(f"[{role.value}] Context limit handoff")
            
            # Run same agent again with fresh context
            if retry_count < MAX_RETRIES:
                log(czech(f"Restart agenta {role.value} (pokus {retry_count + 1}/{MAX_RETRIES})"), "INFO")
                return self.run_agent(role, retry_count + 1)
            else:
                log(czech(f"Maximální počet pokusů dosažen pro {role.value}"), "ERROR")
                return False
        
        elif not success:
            # Agent failed
            issue, fix = self._analyze_failure(role.value, output)
            log(czech(f"Agent selhal: {issue}"), "ERROR")
            log(czech(f"Doporučení: {fix}"), "INFO")
            
            self.journal.add_entry(role.value, "FAILED", f"Selhání: {issue}", f"Fix: {fix}")
            
            # Add to collision log if it's a recurring issue
            self.state.known_issues.append(f"{role.value}: {issue}")
            
            if retry_count < MAX_RETRIES:
                log(czech(f"Pokus o opravu a restart..."), "INFO")
                time.sleep(5)  # Brief pause before retry
                return self.run_agent(role, retry_count + 1)
            else:
                return False
        
        else:
            # Unclear state - treat as needing continuation
            log(czech(f"Agent {role.value} skončil bez jasného stavu"), "WARNING")
            self.git.commit(f"[{role.value}] Partial progress")
            return True  # Continue to next phase
    
    def run_full_workflow(self):
        """Run complete development workflow"""
        log(czech("\n🚀 SPOUŠTÍM KOMPLETNÍ VÝVOJOVÝ WORKFLOW 🚀\n"), "PHASE")
        
        # Determine starting point
        start_index = 0
        if self.state.completed_phases:
            last_completed = self.state.completed_phases[-1]
            for i, role in enumerate(self.workflow):
                if role.value == last_completed:
                    start_index = i + 1
                    break
        
        if start_index > 0:
            log(czech(f"Pokračuji od fáze: {self.workflow[start_index].value}"), "INFO")
        
        # Run workflow
        for role in self.workflow[start_index:]:
            if not self.run_agent(role):
                log(czech(f"Workflow zastaven na fázi: {role.value}"), "ERROR")
                return False
        
        # Final supervision
        log(czech("\n🔍 FINÁLNÍ SUPERVIZE 🔍\n"), "PHASE")
        self.run_agent(AgentRole.SUPERVISOR)
        
        # Evolution phase
        log(czech("\n🧬 EVOLUCE SYSTÉMU 🧬\n"), "PHASE")
        evolver_prompt = AgentPrompts.evolver(
            self._get_project_context(),
            str(self.docs_path),
            str(self.dev_path),
            str(Path(__file__).parent)
        )
        self.runner.run_agent("evolver", evolver_prompt)
        
        # Final tag
        self.git.tag(f"release-{datetime.datetime.now().strftime('%Y%m%d')}", "Workflow completed")
        self.git.push()
        
        log(czech("\n✅ WORKFLOW DOKONČEN ✅\n"), "SUCCESS")
        return True

# ============================================================================
# INTERACTIVE SETUP
# ============================================================================

def interactive_setup() -> tuple[str, str]:
    """Interactive setup to get paths from user"""
    print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}   🔄 SpinThatShit - AI Agent Orchestrator v{VERSION} 🔄{Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")
    
    print(czech("Vítejte! Pojďme nastavit váš projekt.\n"))
    
    # Documentation path
    while True:
        docs_input = input(czech("📁 Cesta k dokumentaci (nebo 'new' pro vytvoření): ")).strip()
        
        if docs_input.lower() == 'new':
            docs_path = input(czech("   Zadejte cestu pro novou složku dokumentace: ")).strip()
            docs_path = Path(docs_path).expanduser().resolve()
            create = input(czech(f"   Vytvořit složku '{docs_path}'? [Y/n]: ")).strip().lower()
            if create != 'n':
                docs_path.mkdir(parents=True, exist_ok=True)
                # Create sample README
                readme = docs_path / "README.md"
                readme.write_text("# Project Documentation\n\nAdd your project documentation here.\n")
                print(czech(f"   ✅ Složka vytvořena: {docs_path}"))
                break
        else:
            docs_path = Path(docs_input).expanduser().resolve()
            if docs_path.exists():
                if docs_path.is_dir():
                    print(czech(f"   ✅ Dokumentace nalezena: {docs_path}"))
                    break
                else:
                    print(czech("   ❌ Zadaná cesta není složka"))
            else:
                create = input(czech(f"   Složka neexistuje. Vytvořit? [Y/n]: ")).strip().lower()
                if create != 'n':
                    docs_path.mkdir(parents=True, exist_ok=True)
                    print(czech(f"   ✅ Složka vytvořena: {docs_path}"))
                    break
    
    print()
    
    # Development path
    while True:
        dev_input = input(czech("💻 Cesta k vývojové složce (nebo 'new' pro vytvoření): ")).strip()
        
        if dev_input.lower() == 'new':
            dev_path = input(czech("   Zadejte cestu pro novou vývojovou složku: ")).strip()
            dev_path = Path(dev_path).expanduser().resolve()
            create = input(czech(f"   Vytvořit složku '{dev_path}'? [Y/n]: ")).strip().lower()
            if create != 'n':
                dev_path.mkdir(parents=True, exist_ok=True)
                print(czech(f"   ✅ Složka vytvořena: {dev_path}"))
                break
        else:
            dev_path = Path(dev_input).expanduser().resolve()
            if dev_path.exists():
                if dev_path.is_dir():
                    print(czech(f"   ✅ Vývojová složka nalezena: {dev_path}"))
                    break
                else:
                    print(czech("   ❌ Zadaná cesta není složka"))
            else:
                create = input(czech(f"   Složka neexistuje. Vytvořit? [Y/n]: ")).strip().lower()
                if create != 'n':
                    dev_path.mkdir(parents=True, exist_ok=True)
                    print(czech(f"   ✅ Složka vytvořena: {dev_path}"))
                    break
    
    print()
    
    # Validation summary
    print(f"\n{Colors.CYAN}📋 Shrnutí konfigurace:{Colors.END}")
    print(f"   Dokumentace: {docs_path}")
    print(f"   Vývoj: {dev_path}")
    
    # Count files
    doc_files = list(docs_path.glob('**/*'))
    dev_files = list(dev_path.glob('**/*'))
    print(f"   Soubory v dokumentaci: {len([f for f in doc_files if f.is_file()])}")
    print(f"   Soubory ve vývoji: {len([f for f in dev_files if f.is_file()])}")
    
    confirm = input(czech(f"\n🚀 Spustit orchestraci? [Y/n]: ")).strip().lower()
    if confirm == 'n':
        print(czech("Zrušeno uživatelem."))
        sys.exit(0)
    
    return str(docs_path), str(dev_path)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SpinThatShit - AI Agent Orchestration System"
    )
    parser.add_argument('--docs', help='Path to documentation folder')
    parser.add_argument('--dev', help='Path to development folder')
    parser.add_argument('--resume', action='store_true', help='Resume from last state')
    parser.add_argument('--version', action='version', version=f'SpinThatShit v{VERSION}')
    
    args = parser.parse_args()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print(czech("\n\n⚠️  Zastaveno uživatelem (Ctrl+C)"))
        print(czech("   Stav byl uložen. Použijte --resume pro pokračování.\n"))
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get paths
    if args.docs and args.dev:
        docs_path = args.docs
        dev_path = args.dev
    else:
        docs_path, dev_path = interactive_setup()
    
    # Create and run orchestrator
    try:
        orchestrator = Orchestrator(docs_path, dev_path)
        orchestrator.run_full_workflow()
    except Exception as e:
        log(czech(f"Kritická chyba: {str(e)}"), "ERROR")
        raise

if __name__ == "__main__":
    main()
