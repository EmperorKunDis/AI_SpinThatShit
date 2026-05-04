#!/usr/bin/env python3
from __future__ import annotations
"""
SpinThatShit - AI Agent Orchestration System
=============================================
Autonomous multi-agent development orchestrator using Claude Code CLI.

Usage: spinthatshit [--config path] [--resume] [--lang LANG_CODE]

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
import random
import hashlib
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable, TypeVar
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps, lru_cache
import argparse
import signal
import threading

# Add i18n directory to path
sys.path.insert(0, str(Path(__file__).parent))
from i18n import get_i18n, SUPPORTED_LANGUAGES

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

VERSION = "3.0.0"
CONTEXT_LIMIT_PERCENT = 50  # Start handoff at this percentage
CONTEXT_WARNING_PERCENT = 40  # Early warning threshold
MAX_RETRIES = 3
AGENT_TIMEOUT_MINUTES = 30
MAX_CONTEXT_TOKENS = 200000

# Retry configuration
RETRY_INITIAL_DELAY = 1.0
RETRY_MAX_DELAY = 60.0
RETRY_EXPONENTIAL_BASE = 2

# Type variable for retry decorator
T = TypeVar('T')

# Global i18n instance
_i18n = None

def get_config_dir() -> Path:
    """Get or create config directory"""
    config_dir = Path.home() / ".spinthatshit"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def load_language_config() -> str:
    """Load saved language preference or return default"""
    config_file = get_config_dir() / "language.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('language', 'en')
        except:
            pass
    return 'en'

def save_language_config(lang_code: str):
    """Save language preference"""
    config_file = get_config_dir() / "language.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({'language': lang_code}, f)

def select_language() -> str:
    """Interactive language selection"""
    print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}   🌍 Select Your Language / Vyberte Jazyk / 选择语言   {Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")

    # Display languages in columns
    langs = list(SUPPORTED_LANGUAGES.items())
    for i in range(0, len(langs), 3):
        row = langs[i:i+3]
        line = "  ".join([f"{code:8} {info['native']:20}" for code, info in row])
        print(line)

    print(f"\n{Colors.CYAN}Enter language code (default: en): {Colors.END}", end='')
    choice = input().strip().lower() or 'en'

    if choice in SUPPORTED_LANGUAGES:
        save_language_config(choice)
        return choice
    else:
        print(f"{Colors.YELLOW}Invalid code. Using English.{Colors.END}")
        return 'en'

def init_i18n(lang_code: Optional[str] = None) -> None:
    """Initialize i18n system"""
    global _i18n
    if lang_code is None:
        lang_code = load_language_config()
    _i18n = get_i18n(lang_code)

def t(key: str, **kwargs) -> str:
    """Translate key"""
    if _i18n is None:
        init_i18n()
    return _i18n.t(key, **kwargs)

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
# PHASE 1: STRUCTURED LOGGING (AgentLogger)
# ============================================================================

class AgentLogger:
    """
    Structured JSON logging for agent activities.
    Replaces simple print() calls with structured, parseable logs.
    """

    def __init__(self, log_file: str = "spin_session.jsonl", console_output: bool = True):
        self.log_file = Path(log_file)
        self.console_output = console_output
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.entries: List[Dict[str, Any]] = []

        # Create log file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self,
            agent_name: str,
            action: str,
            details: Any,
            context_usage: float = 0.0,
            status: str = "INFO",
            tool_calls: Optional[List[str]] = None,
            duration_ms: Optional[int] = None) -> Dict[str, Any]:
        """
        Log an agent activity with structured data.

        Args:
            agent_name: Name of the agent (PLANNER, DEVELOPER, etc.)
            action: What action was performed
            details: Additional details (dict, string, or any JSON-serializable)
            context_usage: Current context window usage percentage
            status: Log level (INFO, SUCCESS, WARNING, ERROR)
            tool_calls: List of tool calls made
            duration_ms: Duration of the action in milliseconds
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "agent": agent_name,
            "action": action,
            "status": status,
            "context_usage_percent": round(context_usage, 2),
            "details": details if isinstance(details, (dict, list)) else str(details),
            "tool_calls": tool_calls or [],
            "duration_ms": duration_ms
        }

        self.entries.append(entry)

        # Write to JSONL file (append mode)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

        # Console output with colors
        if self.console_output:
            self._print_colored(entry)

        return entry

    def _print_colored(self, entry: Dict[str, Any]):
        """Print colored console output"""
        status = entry["status"]
        color_map = {
            "INFO": Colors.CYAN,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "DEBUG": Colors.DIM
        }
        color = color_map.get(status, Colors.END)
        reset = Colors.END

        # Truncate details for console
        details_str = str(entry["details"])
        if len(details_str) > 100:
            details_str = details_str[:97] + "..."

        agent = entry["agent"]
        action = entry["action"]
        ctx = entry["context_usage_percent"]

        ctx_indicator = ""
        if ctx > 0:
            if ctx >= CONTEXT_LIMIT_PERCENT:
                ctx_indicator = f" {Colors.RED}[CTX:{ctx}%]{Colors.END}"
            elif ctx >= CONTEXT_WARNING_PERCENT:
                ctx_indicator = f" {Colors.YELLOW}[CTX:{ctx}%]{Colors.END}"
            else:
                ctx_indicator = f" {Colors.DIM}[CTX:{ctx}%]{Colors.END}"

        print(f"{color}[{agent}] {action}{reset}{ctx_indicator}: {details_str}")

    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary statistics for the current session"""
        if not self.entries:
            return {"total_entries": 0}

        return {
            "total_entries": len(self.entries),
            "agents_used": list(set(e["agent"] for e in self.entries)),
            "error_count": sum(1 for e in self.entries if e["status"] == "ERROR"),
            "warning_count": sum(1 for e in self.entries if e["status"] == "WARNING"),
            "max_context_usage": max(e["context_usage_percent"] for e in self.entries),
            "session_id": self.session_id
        }

    def export_session(self, output_file: Optional[str] = None) -> str:
        """Export full session log to JSON file"""
        output = output_file or f"session_{self.session_id}.json"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "summary": self.get_session_summary(),
                "entries": self.entries
            }, f, indent=2, ensure_ascii=False)
        return output

# Global logger instance
_agent_logger: Optional[AgentLogger] = None

def get_agent_logger() -> AgentLogger:
    """Get or create global agent logger"""
    global _agent_logger
    if _agent_logger is None:
        _agent_logger = AgentLogger()
    return _agent_logger

# ============================================================================
# PHASE 2: MEMORY MANAGEMENT (ContextManager)
# ============================================================================

@dataclass
class MemoryBlock:
    """Single memory block with metadata"""
    name: str
    content: str
    max_tokens: int
    priority: int  # Higher = more important, kept longer
    last_updated: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def estimate_tokens(self) -> int:
        """Estimate token count (rough: 1 token ≈ 4 chars)"""
        return len(self.content) // 4

class ContextManager:
    """
    Manages context window with memory blocks architecture.
    Instead of one long string, context is divided into discrete blocks
    with different priorities and limits.
    """

    def __init__(self, max_tokens: int = MAX_CONTEXT_TOKENS):
        self.max_tokens = max_tokens
        self.blocks: Dict[str, MemoryBlock] = {
            "system_instructions": MemoryBlock(
                name="system_instructions",
                content="",
                max_tokens=10000,
                priority=100  # Never removed
            ),
            "project_summary": MemoryBlock(
                name="project_summary",
                content="",
                max_tokens=5000,
                priority=90
            ),
            "active_task": MemoryBlock(
                name="active_task",
                content="",
                max_tokens=3000,
                priority=95
            ),
            "recent_history": MemoryBlock(
                name="recent_history",
                content="",
                max_tokens=20000,
                priority=70
            ),
            "tool_outputs": MemoryBlock(
                name="tool_outputs",
                content="",
                max_tokens=15000,
                priority=60
            ),
            "handoff_notes": MemoryBlock(
                name="handoff_notes",
                content="",
                max_tokens=5000,
                priority=85
            )
        }
        self.history: List[Dict[str, str]] = []
        self.max_history_items = 20

    def update_block(self, block_name: str, content: str):
        """Update content of a specific block"""
        if block_name in self.blocks:
            self.blocks[block_name].content = content
            self.blocks[block_name].last_updated = datetime.datetime.now().isoformat()
        else:
            # Create new block with default settings
            self.blocks[block_name] = MemoryBlock(
                name=block_name,
                content=content,
                max_tokens=5000,
                priority=50
            )

    def add_history(self, role: str, content: str):
        """Add message to history with automatic trimming"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        })

        # Trim old history
        while len(self.history) > self.max_history_items:
            self.history.pop(0)

        # Update recent_history block
        history_text = "\n".join(
            f"[{msg['role']}]: {msg['content'][:500]}"
            for msg in self.history[-10:]
        )
        self.update_block("recent_history", history_text)

    def add_tool_output(self, tool_name: str, output: str, max_length: int = 2000):
        """Add tool output with truncation"""
        truncated = output[:max_length] if len(output) > max_length else output
        current = self.blocks["tool_outputs"].content
        new_entry = f"\n[{tool_name}]: {truncated}"

        # Keep only recent tool outputs
        lines = (current + new_entry).split('\n')
        if len(lines) > 50:
            lines = lines[-50:]

        self.update_block("tool_outputs", '\n'.join(lines))

    def get_total_tokens(self) -> int:
        """Get total estimated tokens across all blocks"""
        return sum(block.estimate_tokens() for block in self.blocks.values())

    def get_usage_percent(self) -> float:
        """Get context usage as percentage"""
        return (self.get_total_tokens() / self.max_tokens) * 100

    def needs_compaction(self) -> bool:
        """Check if context needs compaction"""
        return self.get_usage_percent() >= CONTEXT_WARNING_PERCENT

    def compact(self):
        """
        Compact context by summarizing/trimming lower priority blocks.
        Called when approaching context limits.
        """
        usage = self.get_usage_percent()
        if usage < CONTEXT_WARNING_PERCENT:
            return

        # Sort blocks by priority (lowest first for trimming)
        sorted_blocks = sorted(
            self.blocks.values(),
            key=lambda b: b.priority
        )

        for block in sorted_blocks:
            if block.priority >= 90:  # Don't touch high priority
                continue

            current_tokens = block.estimate_tokens()
            if current_tokens > block.max_tokens:
                # Trim to max_tokens
                char_limit = block.max_tokens * 4
                block.content = block.content[-char_limit:]

            # If still over limit, be more aggressive
            if self.get_usage_percent() >= CONTEXT_LIMIT_PERCENT:
                block.content = block.content[-len(block.content)//2:]

    def compile_prompt(self, agent_role: str = "") -> str:
        """Compile all blocks into final prompt string"""
        # Auto-compact if needed
        if self.needs_compaction():
            self.compact()

        sections = []

        # System instructions first
        if self.blocks["system_instructions"].content:
            sections.append(f"=== SYSTEM INSTRUCTIONS ===\n{self.blocks['system_instructions'].content}")

        # Project summary
        if self.blocks["project_summary"].content:
            sections.append(f"=== PROJECT CONTEXT ===\n{self.blocks['project_summary'].content}")

        # Handoff notes (if any)
        if self.blocks["handoff_notes"].content:
            sections.append(f"=== HANDOFF FROM PREVIOUS AGENT ===\n{self.blocks['handoff_notes'].content}")

        # Active task
        if self.blocks["active_task"].content:
            sections.append(f"=== CURRENT TASK ===\n{self.blocks['active_task'].content}")

        # Recent history
        if self.blocks["recent_history"].content:
            sections.append(f"=== RECENT ACTIVITY ===\n{self.blocks['recent_history'].content}")

        # Tool outputs (abbreviated)
        if self.blocks["tool_outputs"].content:
            sections.append(f"=== TOOL OUTPUTS (RECENT) ===\n{self.blocks['tool_outputs'].content[-5000:]}")

        return "\n\n".join(sections)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for checkpointing"""
        return {
            "blocks": {
                name: {
                    "content": block.content,
                    "max_tokens": block.max_tokens,
                    "priority": block.priority,
                    "last_updated": block.last_updated
                }
                for name, block in self.blocks.items()
            },
            "history": self.history,
            "total_tokens": self.get_total_tokens(),
            "usage_percent": self.get_usage_percent()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextManager':
        """Deserialize from checkpoint"""
        manager = cls()
        if "blocks" in data:
            for name, block_data in data["blocks"].items():
                manager.blocks[name] = MemoryBlock(
                    name=name,
                    content=block_data.get("content", ""),
                    max_tokens=block_data.get("max_tokens", 5000),
                    priority=block_data.get("priority", 50),
                    last_updated=block_data.get("last_updated", "")
                )
        if "history" in data:
            manager.history = data["history"]
        return manager

# ============================================================================
# PHASE 4: ERROR HANDLING (Retry with Backoff)
# ============================================================================

class RetryableError(Exception):
    """Error that should trigger a retry"""
    pass

class PermanentError(Exception):
    """Error that should NOT trigger a retry"""
    pass

def retry_with_backoff(
    max_retries: int = MAX_RETRIES,
    initial_delay: float = RETRY_INITIAL_DELAY,
    max_delay: float = RETRY_MAX_DELAY,
    exponential_base: float = RETRY_EXPONENTIAL_BASE,
    retryable_exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    Decorator for retry logic with exponential backoff and jitter.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay cap in seconds
        exponential_base: Base for exponential backoff
        retryable_exceptions: Tuple of exceptions that should trigger retry
        on_retry: Optional callback called on each retry (exception, attempt)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except PermanentError:
                    raise  # Don't retry permanent errors
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        raise  # Final attempt failed

                    # Calculate delay with exponential backoff + jitter
                    delay = min(
                        initial_delay * (exponential_base ** attempt) + random.uniform(0, 1),
                        max_delay
                    )

                    # Call retry callback if provided
                    if on_retry:
                        on_retry(e, attempt + 1)
                    else:
                        print(f"⚠️  Retry {attempt + 1}/{max_retries}: {e}. Waiting {delay:.2f}s...")

                    time.sleep(delay)

            raise last_exception
        return wrapper
    return decorator

def classify_error(error: Exception) -> str:
    """
    Classify error type for appropriate handling.

    Returns:
        - "TRANSIENT": Should retry (network issues, timeouts)
        - "RECOVERABLE": Can fix and retry (missing file, permission)
        - "PERMANENT": Should not retry (syntax error, invalid input)
    """
    error_str = str(error).lower()

    # Transient errors (retry with backoff)
    transient_patterns = [
        'timeout', 'timed out', 'connection refused', 'connection reset',
        'temporary', 'rate limit', 'too many requests', '503', '502', '429'
    ]
    if any(p in error_str for p in transient_patterns):
        return "TRANSIENT"

    # Recoverable errors (fix and retry)
    recoverable_patterns = [
        'permission denied', 'file not found', 'no such file',
        'module not found', 'import error', 'command not found'
    ]
    if any(p in error_str for p in recoverable_patterns):
        return "RECOVERABLE"

    # Permanent errors (don't retry)
    permanent_patterns = [
        'syntax error', 'invalid', 'assertion', 'type error',
        'key error', 'index error', 'value error'
    ]
    if any(p in error_str for p in permanent_patterns):
        return "PERMANENT"

    # Default to transient (give it a retry chance)
    return "TRANSIENT"

# ============================================================================
# PHASE 4: SECURITY (Secret Detection)
# ============================================================================

class SecretDetector:
    """Detects secrets/credentials in code before commits"""

    PATTERNS = {
        "OpenAI API Key": r"sk-[a-zA-Z0-9]{20,}",
        "Anthropic API Key": r"sk-ant-[a-zA-Z0-9\-_]{20,}",
        "GitHub Token": r"ghp_[a-zA-Z0-9]{36,}",
        "GitHub OAuth": r"gho_[a-zA-Z0-9]{36,}",
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "AWS Secret Key": r"[a-zA-Z0-9/+]{40}",
        "Private Key": r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----",
        "Generic API Key": r"(?:api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{16,}['\"]",
        "Generic Secret": r"(?:secret|password|passwd|pwd)['\"]?\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        "Database URL": r"(?:postgres|mysql|mongodb|redis):\/\/[^:]+:[^@]+@",
        "JWT Token": r"eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
        "Slack Token": r"xox[baprs]-[a-zA-Z0-9-]+",
        "Stripe Key": r"sk_(?:live|test)_[a-zA-Z0-9]{24,}",
    }

    # Files to always skip
    SKIP_FILES = {
        '.env.example', '.env.template', 'example.env',
        'secrets.example.json', 'config.example.json'
    }

    # Paths to skip
    SKIP_PATHS = {
        'node_modules', '.git', '__pycache__', '.venv', 'venv',
        '.pytest_cache', '.mypy_cache', 'dist', 'build'
    }

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []

    def scan_content(self, content: str, source: str = "unknown") -> List[Dict[str, Any]]:
        """
        Scan content for secrets.

        Args:
            content: Text content to scan
            source: Source identifier (filename, etc.)

        Returns:
            List of findings with secret type and location
        """
        findings = []

        for secret_type, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Find line number
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_num = content[:match.start()].count('\n') + 1

                # Mask the actual secret for logging
                secret_preview = match.group(0)
                if len(secret_preview) > 10:
                    secret_preview = secret_preview[:5] + "..." + secret_preview[-3:]

                finding = {
                    "type": secret_type,
                    "source": source,
                    "line": line_num,
                    "preview": secret_preview,
                    "severity": "HIGH"
                }
                findings.append(finding)

        self.findings.extend(findings)
        return findings

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan a single file for secrets"""
        # Skip certain files
        if file_path.name in self.SKIP_FILES:
            return []

        # Skip certain paths
        for skip_path in self.SKIP_PATHS:
            if skip_path in str(file_path):
                return []

        # Skip binary files
        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            return []

        return self.scan_content(content, str(file_path))

    def scan_directory(self, directory: Path, extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Scan directory for secrets.

        Args:
            directory: Directory to scan
            extensions: File extensions to check (None = all text files)
        """
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env', '.sh', '.md']

        all_findings = []

        for ext in extensions:
            for file_path in directory.rglob(f'*{ext}'):
                findings = self.scan_file(file_path)
                all_findings.extend(findings)

        return all_findings

def scan_for_secrets(content: str, source: str = "unknown") -> bool:
    """
    Convenience function to scan content and raise if secrets found.
    Use before git commit or file write.

    Returns:
        True if no secrets found

    Raises:
        ValueError if secrets detected
    """
    detector = SecretDetector()
    findings = detector.scan_content(content, source)

    if findings:
        secret_types = list(set(f["type"] for f in findings))
        raise ValueError(
            f"🚨 SECURITY ALERT: Found {len(findings)} potential secrets ({', '.join(secret_types)})! "
            f"Commit blocked. Review and remove secrets before proceeding."
        )

    return True

# ============================================================================
# PHASE 5: TOOL OPTIMIZATION (Caching)
# ============================================================================

class FileCache:
    """
    LRU cache for file reads with invalidation on modification.
    Prevents reading the same file multiple times.
    """

    def __init__(self, max_size: int = 32):
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_order: List[str] = []
        self._lock = threading.Lock()

    def _get_file_hash(self, file_path: Path) -> str:
        """Get file modification time + size as hash"""
        try:
            stat = file_path.stat()
            return f"{stat.st_mtime}_{stat.st_size}"
        except OSError:
            return ""

    def get(self, file_path: str) -> Optional[str]:
        """Get cached file content if still valid"""
        path = Path(file_path)
        key = str(path.resolve())

        with self._lock:
            if key in self._cache:
                cached = self._cache[key]
                current_hash = self._get_file_hash(path)

                if cached["hash"] == current_hash:
                    # Move to end of access order (most recently used)
                    if key in self._access_order:
                        self._access_order.remove(key)
                    self._access_order.append(key)
                    return cached["content"]
                else:
                    # File changed, invalidate
                    del self._cache[key]
                    if key in self._access_order:
                        self._access_order.remove(key)

        return None

    def put(self, file_path: str, content: str):
        """Cache file content"""
        path = Path(file_path)
        key = str(path.resolve())

        with self._lock:
            # Evict oldest if at capacity
            while len(self._cache) >= self.max_size:
                oldest = self._access_order.pop(0)
                if oldest in self._cache:
                    del self._cache[oldest]

            self._cache[key] = {
                "content": content,
                "hash": self._get_file_hash(path),
                "cached_at": datetime.datetime.now().isoformat()
            }
            self._access_order.append(key)

    def invalidate(self, file_path: str):
        """Invalidate cache for specific file (call after edit)"""
        key = str(Path(file_path).resolve())
        with self._lock:
            if key in self._cache:
                del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)

    def clear(self):
        """Clear entire cache"""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "files": list(self._cache.keys())
        }

# Global file cache instance
_file_cache = FileCache()

def read_file_cached(file_path: str) -> str:
    """
    Read file with caching. Returns cached content if file unchanged.
    """
    cached = _file_cache.get(file_path)
    if cached is not None:
        return cached

    # Read and cache
    content = Path(file_path).read_text(encoding='utf-8')
    _file_cache.put(file_path, content)
    return content

def invalidate_file_cache(file_path: str):
    """Invalidate cache after editing a file"""
    _file_cache.invalidate(file_path)

# ============================================================================
# PHASE 5: STATIC ANALYSIS (Code Verification)
# ============================================================================

class CodeAnalyzer:
    """
    Static code analysis for quality verification.
    Supports Python (ruff/pylint) and TypeScript (eslint).
    """

    LINTER_COMMANDS = {
        ".py": ["ruff", "check", "--output-format=concise"],
        ".ts": ["npx", "eslint", "--format=compact"],
        ".tsx": ["npx", "eslint", "--format=compact"],
        ".js": ["npx", "eslint", "--format=compact"],
    }

    FALLBACK_COMMANDS = {
        ".py": ["python", "-m", "py_compile"],  # At least check syntax
    }

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def analyze_file(self, file_path: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Run linter on a single file.

        Returns:
            Dict with 'passed', 'issues', 'output' keys
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        result = {
            "file": str(file_path),
            "passed": True,
            "issues": [],
            "output": "",
            "linter": "none"
        }

        # Get linter command
        linter_cmd = self.LINTER_COMMANDS.get(ext)
        if not linter_cmd:
            result["output"] = f"No linter configured for {ext}"
            return result

        try:
            cmd = linter_cmd + [str(file_path)]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            result["linter"] = linter_cmd[0]
            result["output"] = proc.stdout + proc.stderr
            result["passed"] = proc.returncode == 0

            if not result["passed"]:
                # Parse issues from output
                for line in result["output"].split('\n'):
                    if line.strip() and ':' in line:
                        result["issues"].append(line.strip())

        except FileNotFoundError:
            # Linter not installed, try fallback
            fallback = self.FALLBACK_COMMANDS.get(ext)
            if fallback:
                try:
                    cmd = fallback + [str(file_path)]
                    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                    result["linter"] = "syntax-check"
                    result["passed"] = proc.returncode == 0
                    result["output"] = proc.stderr if proc.returncode != 0 else "Syntax OK"
                except Exception as e:
                    result["output"] = f"Fallback check failed: {e}"
            else:
                result["output"] = f"⚠️ Linter '{linter_cmd[0]}' not installed. Skipping analysis."
        except subprocess.TimeoutExpired:
            result["output"] = "Analysis timed out"
            result["passed"] = False
        except Exception as e:
            result["output"] = f"Analysis error: {e}"

        self.results.append(result)
        return result

    def analyze_directory(self, directory: str, extensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze all files in directory"""
        if extensions is None:
            extensions = [".py", ".ts", ".tsx", ".js"]

        dir_path = Path(directory)
        all_results = []

        for ext in extensions:
            for file_path in dir_path.rglob(f'*{ext}'):
                # Skip common non-source directories
                if any(skip in str(file_path) for skip in ['node_modules', '__pycache__', '.git', 'dist']):
                    continue
                result = self.analyze_file(str(file_path))
                all_results.append(result)

        return {
            "total_files": len(all_results),
            "passed": sum(1 for r in all_results if r["passed"]),
            "failed": sum(1 for r in all_results if not r["passed"]),
            "results": all_results
        }

def run_linter(file_path: str) -> str:
    """
    Convenience function to run linter and return human-readable result.
    """
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(file_path)

    if result["passed"]:
        return f"✅ Code Analysis Passed ({result['linter']})"
    else:
        issues = result["issues"][:5]  # Show first 5 issues
        issue_text = '\n'.join(f"  - {i}" for i in issues)
        more = f"\n  ... and {len(result['issues']) - 5} more" if len(result['issues']) > 5 else ""
        return f"❌ Code Issues Found ({result['linter']}):\n{issue_text}{more}"

# ============================================================================
# PHASE 6: CHECKPOINTING (Save/Load State)
# ============================================================================

@dataclass
class Checkpoint:
    """Complete system state for save/restore"""
    timestamp: str
    stage: str
    agent: str
    context: Dict[str, Any]
    project_state: Dict[str, Any]
    completion_percent: float
    git_commit: str

class CheckpointManager:
    """Manages saving and loading of system checkpoints"""

    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.latest_file = self.checkpoint_dir / "latest_checkpoint.json"
        self.history_dir = self.checkpoint_dir / "history"
        self.history_dir.mkdir(exist_ok=True)

    def save(self,
             stage: str,
             agent: str,
             context_manager: ContextManager,
             project_state: ProjectState,
             completion_percent: float = 0.0) -> str:
        """
        Save current state to checkpoint.

        Returns:
            Checkpoint filename
        """
        # Get current git commit
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=5
            )
            git_commit = result.stdout.strip()[:8] if result.returncode == 0 else "unknown"
        except:
            git_commit = "unknown"

        checkpoint = Checkpoint(
            timestamp=datetime.datetime.now().isoformat(),
            stage=stage,
            agent=agent,
            context=context_manager.to_dict(),
            project_state=asdict(project_state),
            completion_percent=completion_percent,
            git_commit=git_commit
        )

        # Save to latest
        with open(self.latest_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(checkpoint), f, indent=2, ensure_ascii=False)

        # Also save to history
        history_file = self.history_dir / f"checkpoint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(checkpoint), f, indent=2, ensure_ascii=False)

        print(f"💾 Checkpoint saved: Stage {stage}, Agent {agent}, {completion_percent:.1f}% complete")

        return str(history_file)

    def load_latest(self) -> Optional[Dict[str, Any]]:
        """Load most recent checkpoint"""
        if not self.latest_file.exists():
            return None

        try:
            with open(self.latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"📂 Loaded checkpoint from {data['timestamp']} (Stage: {data['stage']}, {data['completion_percent']:.1f}% complete)")
            return data
        except Exception as e:
            print(f"⚠️ Failed to load checkpoint: {e}")
            return None

    def load_by_stage(self, stage: str) -> Optional[Dict[str, Any]]:
        """Load checkpoint for specific stage"""
        # Search history for stage
        for checkpoint_file in sorted(self.history_dir.glob("checkpoint_*.json"), reverse=True):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data.get("stage") == stage:
                    return data
            except:
                continue
        return None

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints"""
        checkpoints = []
        for checkpoint_file in sorted(self.history_dir.glob("checkpoint_*.json"), reverse=True):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                checkpoints.append({
                    "file": str(checkpoint_file),
                    "timestamp": data.get("timestamp"),
                    "stage": data.get("stage"),
                    "agent": data.get("agent"),
                    "completion": data.get("completion_percent", 0)
                })
            except:
                continue
        return checkpoints

# ============================================================================
# PHASE 6: INTERACTIVE MODE
# ============================================================================

class InteractiveController:
    """
    Provides human-in-the-loop control for the orchestration process.
    Allows pausing, reviewing, and modifying agent plans.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.auto_approve_stages: set = set()
        self.feedback_history: List[Dict[str, Any]] = []

    def ask_approval(self, agent_name: str, planned_action: str, details: str = "") -> tuple[bool, Optional[str]]:
        """
        Ask user for approval before agent action.

        Args:
            agent_name: Name of the agent requesting approval
            planned_action: What the agent plans to do
            details: Additional details about the action

        Returns:
            Tuple of (approved: bool, feedback: Optional[str])
        """
        if not self.enabled:
            return True, None

        # Check if this stage is auto-approved
        if agent_name.lower() in self.auto_approve_stages:
            return True, None

        print(f"\n{'='*60}")
        print(f"{Colors.YELLOW}🤖 AGENT APPROVAL REQUEST{Colors.END}")
        print(f"{'='*60}")
        print(f"{Colors.BOLD}Agent:{Colors.END} {agent_name}")
        print(f"{Colors.BOLD}Action:{Colors.END} {planned_action}")
        if details:
            print(f"{Colors.BOLD}Details:{Colors.END}")
            # Truncate long details
            if len(details) > 500:
                print(f"  {details[:500]}...")
                print(f"  [{len(details) - 500} more characters]")
            else:
                print(f"  {details}")
        print(f"{'='*60}")

        while True:
            choice = input(f"\n{Colors.CYAN}Approve? [Y/n/edit/skip/auto]: {Colors.END}").strip().lower()

            if choice in ('', 'y', 'yes'):
                self.feedback_history.append({
                    "agent": agent_name,
                    "action": planned_action,
                    "decision": "approved",
                    "timestamp": datetime.datetime.now().isoformat()
                })
                return True, None

            elif choice in ('n', 'no'):
                print(f"{Colors.RED}Action rejected by user.{Colors.END}")
                self.feedback_history.append({
                    "agent": agent_name,
                    "action": planned_action,
                    "decision": "rejected",
                    "timestamp": datetime.datetime.now().isoformat()
                })
                return False, None

            elif choice == 'edit':
                feedback = input(f"{Colors.CYAN}Enter your instructions/modifications: {Colors.END}").strip()
                self.feedback_history.append({
                    "agent": agent_name,
                    "action": planned_action,
                    "decision": "modified",
                    "feedback": feedback,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                return True, feedback

            elif choice == 'skip':
                print(f"{Colors.YELLOW}Skipping this agent.{Colors.END}")
                return False, "SKIP"

            elif choice == 'auto':
                self.auto_approve_stages.add(agent_name.lower())
                print(f"{Colors.GREEN}Auto-approving all future {agent_name} actions.{Colors.END}")
                return True, None

            else:
                print("Invalid choice. Enter: Y (yes), n (no), edit, skip, or auto")

    def show_progress_update(self, agent: str, progress: str, completion_percent: float):
        """Show progress update with option to intervene"""
        if not self.enabled:
            return

        print(f"\n{Colors.DIM}[{agent}] Progress: {progress} ({completion_percent:.1f}% complete){Colors.END}")

        # Non-blocking check for user input (simplified)
        # In real implementation, could use select() or threading

    def confirm_continue(self, message: str = "Continue to next phase?") -> bool:
        """Ask user to confirm continuation"""
        if not self.enabled:
            return True

        choice = input(f"\n{Colors.CYAN}{message} [Y/n]: {Colors.END}").strip().lower()
        return choice in ('', 'y', 'yes')

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
            log(t("git.repo_initialized"), "SUCCESS")
    
    def commit(self, message: str) -> bool:
        """Commit all changes with message"""
        run_command("git add -A", cwd=self.repo_path)
        code, out, err = run_command(f'git commit -m "{message}"', cwd=self.repo_path)
        if code == 0:
            log(t("git.commit", message=message[:50]+"..."), "SUCCESS")
            return True
        elif "nothing to commit" in err or "nothing to commit" in out:
            return True
        else:
            log(t("git.commit_failed", error=err), "WARNING")
            return False
    
    def tag(self, tag_name: str, message: str = "") -> bool:
        """Create and push tag"""
        cmd = f'git tag -a "{tag_name}" -m "{message or tag_name}"'
        code, _, err = run_command(cmd, cwd=self.repo_path)
        if code == 0:
            # Try to push tag
            push_code, _, _ = run_command(f'git push origin "{tag_name}"', cwd=self.repo_path)
            if push_code == 0:
                log(t("git.tag_created", tag=tag_name), "SUCCESS")
            else:
                log(t("git.tag_created_no_push", tag=tag_name), "WARNING")
            return True
        return False
    
    def push(self) -> bool:
        """Push to remote"""
        code, _, err = run_command("git push", cwd=self.repo_path)
        if code == 0:
            log(t("git.push_success"), "SUCCESS")
            return True
        else:
            log(t("git.push_failed", error=err), "WARNING")
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
# AGENT PROMPTS (PHASE 3: Enhanced Prompt Engineering)
# ============================================================================

class PromptEnhancer:
    """
    Enhances prompts with Chain of Thought, Few-Shot examples,
    and Self-Verification techniques.
    """

    @staticmethod
    def add_chain_of_thought(base_prompt: str) -> str:
        """Add Chain of Thought reasoning instructions"""
        cot_section = """
REASONING PROTOCOL (Chain of Thought):
Before taking any action, follow this thinking pattern:
1. "Let me think step by step..."
2. Analyze what needs to be done
3. Consider potential issues or blockers
4. Plan the sequence of actions
5. Execute with verification after each step

Example reasoning:
"Let me think step by step. I need to implement user authentication.
First, I'll check if there's an existing auth module.
Then I'll review the user model structure.
Finally, I'll implement the login endpoint with proper validation."

"""
        return cot_section + base_prompt

    @staticmethod
    def add_self_verification(base_prompt: str) -> str:
        """Add self-verification instructions"""
        verification = """
SELF-VERIFICATION CHECKLIST:
After completing each task, verify:
□ Does the code compile/parse without errors?
□ Are all imports present and correct?
□ Are there any hardcoded secrets or credentials? (MUST be none)
□ Is error handling present for edge cases?
□ Are variable names descriptive and consistent?
□ Does this follow existing code patterns in the project?

If any check fails, fix it before proceeding.

"""
        return base_prompt + verification

    @staticmethod
    def add_negative_examples(base_prompt: str, role: str) -> str:
        """Add examples of what NOT to do"""
        negatives = {
            "developer": """
WHAT NOT TO DO:
❌ Don't leave TODO comments without implementing
❌ Don't use console.log/print for debugging in production code
❌ Don't hardcode API keys, passwords, or secrets
❌ Don't skip input validation
❌ Don't ignore error handling
❌ Don't create deeply nested code (max 3 levels)
❌ Don't copy-paste code without understanding it

""",
            "reviewer": """
WHAT NOT TO DO:
❌ Don't make code changes (only document issues)
❌ Don't ignore security vulnerabilities
❌ Don't skip checking for hardcoded credentials
❌ Don't approve code with obvious bugs

""",
            "planner": """
WHAT NOT TO DO:
❌ Don't create unrealistic timelines
❌ Don't skip dependency analysis
❌ Don't ignore existing code patterns
❌ Don't plan features not in requirements

"""
        }

        negative_example = negatives.get(role.lower(), "")
        if negative_example:
            return base_prompt + negative_example
        return base_prompt


class AgentPrompts:
    """Prompt templates for each agent role with enhanced engineering"""

    # Few-shot examples for each role
    FEW_SHOT_EXAMPLES = {
        "developer": """
EXAMPLE OF GOOD OUTPUT:

Task: Implement user login endpoint

My thinking process:
1. Check existing user model → Found in apps/users/models.py
2. Review auth patterns → Project uses JWT tokens
3. Plan implementation:
   - Create LoginSerializer with email/password
   - Create LoginViewSet with /api/v1/auth/login/
   - Add password hashing verification
   - Return JWT token on success

Implementation:
```python
# apps/users/serializers.py
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
```

Verification:
✓ Imports are correct
✓ No hardcoded values
✓ Error handling present
✓ Following project patterns

Committed: "feat(auth): Add login endpoint with JWT"

""",
        "planner": """
EXAMPLE OF GOOD OUTPUT:

Task: Create development plan for e-commerce API

My thinking process:
1. Analyzed requirements from docs/requirements.md
2. Identified core entities: User, Product, Order, Cart
3. Reviewed existing codebase → Django 5.0, DRF pattern

Plan structure:
## Phase 1: Data Models (ENGINEER)
- [ ] User model with authentication
- [ ] Product model with categories
- [ ] Order model with status workflow
Complexity: M
Dependencies: None

## Phase 2: Core APIs (DEVELOPER)
- [ ] Product CRUD endpoints
- [ ] Cart management
- [ ] Order placement flow
Complexity: L
Dependencies: Phase 1

""",
        "reviewer": """
EXAMPLE OF GOOD OUTPUT:

## Code Review Report

### File: apps/orders/views.py

#### CRITICAL Issues (Must Fix):
1. Line 45: SQL injection vulnerability
   ```python
   # BAD: User input directly in query
   Order.objects.raw(f"SELECT * WHERE id = {request.GET['id']}")
   # FIX: Use ORM
   Order.objects.filter(id=request.GET.get('id'))
   ```

#### HIGH Issues:
1. Line 78: Missing tenant isolation
   - Orders not filtered by organization
   - Security risk: users can see other org's orders

#### MEDIUM Issues:
1. Line 92: Magic number without explanation
   - Consider using named constant

"""
    }

    @staticmethod
    def get_base_instructions(role: str, project_context: str, docs_path: str, dev_path: str) -> str:
        """Base instructions for all agents with enhanced prompt engineering"""
        base = f"""You are the {role.upper()} agent in the SpinThatShit orchestration system.

PROJECT CONTEXT:
{project_context}

PATHS:
- Documentation: {docs_path}
- Development: {dev_path}

CRITICAL DIRECTIVES:
1. ANALYZE FIRST: Before writing any code, think step by step about what needs to be done.
2. SECURITY: NEVER output API keys, passwords, or secrets. Check all code for credentials.
3. VALIDATE: After each action, verify it was successful before proceeding.
4. ATOMIC COMMITS: After EVERY file edit in {dev_path}, run: git add -A && git commit -m "type(scope): description"
5. CONTEXT AWARENESS: If context usage exceeds 50%, STOP and write handoff notes.
6. CONTINUITY: Read .spinstate/handoff.md and journal.md before starting.

COMMIT MESSAGE FORMAT:
- feat(scope): New feature
- fix(scope): Bug fix
- refactor(scope): Code restructure
- docs(scope): Documentation
- test(scope): Tests

HANDOFF PROTOCOL:
When stopping (context full, task complete, or blocked):
1. Write detailed summary to .spinstate/handoff.md including:
   - What was completed
   - What remains (specific files, line numbers if relevant)
   - Any blockers or issues found
2. Update .spinstate/checklist.md with progress [x] for completed items
3. Commit all changes
4. Exit cleanly

"""
        # Apply enhancements
        base = PromptEnhancer.add_chain_of_thought(base)
        base = PromptEnhancer.add_self_verification(base)
        base = PromptEnhancer.add_negative_examples(base, role)

        # Add few-shot example if available
        if role.lower() in AgentPrompts.FEW_SHOT_EXAMPLES:
            base += AgentPrompts.FEW_SHOT_EXAMPLES[role.lower()]

        return base

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

    def __init__(self, working_dir: str, log_dir: str, git_monitor: Optional['GitMonitor'] = None):
        self.working_dir = working_dir
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.context_monitor = ContextMonitor()
        self.git_monitor = git_monitor
        self.tool_parser = ToolStreamParser()
    
    def run_agent(self, role: str, prompt: str, timeout_minutes: int = AGENT_TIMEOUT_MINUTES) -> tuple[bool, str, int]:
        """
        Run Claude Code with given prompt
        Returns: (success, output, context_percent)
        """
        log(t("agent.starting", role=role), "AGENT")

        # Create log file for this run
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{role}_{timestamp}.log"

        # Save prompt to temp file to avoid shell escaping issues
        prompt_file = self.log_dir / f"{role}_{timestamp}_prompt.txt"
        prompt_file.write_text(prompt, encoding='utf-8')

        # Build claude command using stdin to avoid shell escaping issues
        # Using --print for non-interactive mode with full output
        cmd = ['claude', '--print', '--dangerously-skip-permissions', prompt]

        try:
            # Run with real-time output capture using args list (safer than shell=True)
            process = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            output_lines = []
            start_time = time.time()
            last_git_check = time.time()

            while True:
                # Check timeout
                if time.time() - start_time > timeout_minutes * 60:
                    process.kill()
                    log(t("agent.timeout", role=role, minutes=timeout_minutes), "ERROR")
                    return False, "TIMEOUT", 100

                # Check git status periodically
                if self.git_monitor and (time.time() - last_git_check) >= 30:
                    if self.git_monitor.should_check():
                        git_status = self.git_monitor.get_status()
                        self.git_monitor.record_status(git_status)

                        # Print git status
                        print(self.git_monitor.format_status(git_status))

                        # Check if agent is stuck
                        if self.git_monitor.needs_warning():
                            log(f"⚠️  Agent may be stuck - no changes for {self.git_monitor.unchanged_count} checks", "WARNING")

                        if self.git_monitor.is_stuck():
                            log(f"🔄 Agent appears stuck - no changes for {self.git_monitor.unchanged_count} checks, considering restart", "ERROR")
                            # Don't kill yet, let it finish current operation

                    last_git_check = time.time()

                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break

                if line:
                    output_lines.append(line)
                    # Write to log file
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(line)

                    # Parse for tool calls
                    tool_call = self.tool_parser.parse_line(line)
                    if tool_call:
                        # Display tool call
                        tool_msg = self.tool_parser.format_tool_call(role, tool_call)
                        print(tool_msg)

                    # Also show important non-tool lines
                    stripped = line.strip()
                    if stripped and len(stripped) > 0 and not tool_call:
                        # Only show significant lines
                        if any(keyword in stripped.lower() for keyword in
                               ['error', 'fail', 'success', 'complete', 'warning']):
                            summary = stripped[:100] + "..." if len(stripped) > 100 else stripped
                            log(f"[{role}] {summary}", "AGENT", to_file=False)
            
            output = ''.join(output_lines)
            exit_code = process.returncode

            # Estimate context usage
            context_percent = self.context_monitor.estimate_from_output(output)
            self.context_monitor.record(context_percent, role)

            success = exit_code == 0

            # Show tool summary
            tool_summary = self.tool_parser.get_summary()
            log(f"[{role}] ✅ {tool_summary}", "INFO")

            log(t("agent.completed", role=role, percent=context_percent),
                "SUCCESS" if success else "ERROR")

            return success, output, context_percent
            
        except Exception as e:
            log(t("agent.failed", issue=str(e)), "ERROR")
            return False, str(e), 0
    
    def check_context_limit(self, current_percent: int) -> bool:
        """Check if we should stop due to context limit"""
        return self.context_monitor.should_handoff(current_percent)

# ============================================================================
# TOOL STREAM PARSER
# ============================================================================

class ToolCall:
    """Represents a single tool call from Claude"""
    def __init__(self, tool: str, action: str, detail: str):
        self.tool = tool  # Read, Edit, Write, Bash, etc.
        self.action = action  # File path, command, etc.
        self.detail = detail  # Additional context
        self.timestamp = datetime.datetime.now()

class ToolStreamParser:
    """Parses Claude CLI output to extract tool calls"""

    TOOL_PATTERNS = {
        'read': r'Reading (?:file )?([^\n]+)',
        'edit': r'Editing ([^:]+):(\d+)',
        'write': r'Writing (?:to )?([^\n]+)',
        'bash': r'Running command: (.+)',
        'grep': r'Searching for: (.+)',
        'glob': r'Finding files: (.+)',
    }

    TOOL_COLORS = {
        'read': Colors.BLUE,
        'edit': Colors.YELLOW,
        'write': Colors.GREEN,
        'bash': Colors.RED,
        'grep': Colors.CYAN,
        'glob': Colors.HEADER,
    }

    TOOL_ICONS = {
        'read': '🔵',
        'edit': '🟡',
        'write': '🟢',
        'bash': '🔴',
        'grep': '🔍',
        'glob': '📁',
    }

    def __init__(self):
        self.tool_counts = {'read': 0, 'edit': 0, 'write': 0, 'bash': 0, 'grep': 0, 'glob': 0}
        self.last_tools = []

    def parse_line(self, line: str) -> Optional[ToolCall]:
        """Parse a single line of output for tool calls"""
        line_lower = line.lower()

        for tool, pattern in self.TOOL_PATTERNS.items():
            if tool in line_lower:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if tool == 'edit' and len(match.groups()) >= 2:
                        action = match.group(1)
                        detail = f"line {match.group(2)}"
                    elif match.groups():
                        action = match.group(1)
                        detail = ""
                    else:
                        action = line.strip()
                        detail = ""

                    self.tool_counts[tool] += 1
                    tool_call = ToolCall(tool, action, detail)
                    self.last_tools.append(tool_call)
                    return tool_call

        return None

    def get_summary(self) -> str:
        """Get summary of tool usage"""
        parts = []
        for tool, count in self.tool_counts.items():
            if count > 0:
                parts.append(f"{count} {tool}s")
        return ", ".join(parts) if parts else "no tools used"

    def format_tool_call(self, agent: str, tool_call: ToolCall) -> str:
        """Format tool call for display"""
        icon = self.TOOL_ICONS.get(tool_call.tool, '🔹')
        color = self.TOOL_COLORS.get(tool_call.tool, Colors.END)

        # Shorten file paths
        action = tool_call.action
        if len(action) > 60:
            action = "..." + action[-57:]

        detail_str = f" - {tool_call.detail}" if tool_call.detail else ""

        return f"{color}[{agent}] {icon} {tool_call.tool.upper()}: {action}{detail_str}{Colors.END}"

# ============================================================================
# GIT MONITOR
# ============================================================================

class GitStatus:
    """Git repository status"""
    def __init__(self, files_changed: int, insertions: int, deletions: int, has_changes: bool):
        self.files_changed = files_changed
        self.insertions = insertions
        self.deletions = deletions
        self.has_changes = has_changes
        self.timestamp = datetime.datetime.now()

class GitMonitor:
    """Monitors git repository for changes"""

    def __init__(self, repo_path: str, check_interval: int = 30, max_unchanged: int = 10):
        self.repo_path = repo_path
        self.check_interval = check_interval  # seconds
        self.max_unchanged = max_unchanged
        self.unchanged_count = 0
        self.last_check = None
        self.last_status = None

    def get_status(self) -> GitStatus:
        """Get current git status"""
        # Get diff stats
        code, out, _ = run_command("git diff --stat HEAD", cwd=self.repo_path)

        files_changed = 0
        insertions = 0
        deletions = 0
        has_changes = False

        if code == 0 and out.strip():
            # Parse output like: "3 files changed, 127 insertions(+), 42 deletions(-)"
            match = re.search(r'(\d+) files? changed', out)
            if match:
                files_changed = int(match.group(1))
                has_changes = True

            match = re.search(r'(\d+) insertions?\(\+\)', out)
            if match:
                insertions = int(match.group(1))

            match = re.search(r'(\d+) deletions?\(-\)', out)
            if match:
                deletions = int(match.group(1))

        # Check for unstaged/untracked
        code, out, _ = run_command("git status --porcelain", cwd=self.repo_path)
        if code == 0 and out.strip():
            has_changes = True
            if not files_changed:  # Count untracked/modified files
                files_changed = len([l for l in out.strip().split('\n') if l.strip()])

        status = GitStatus(files_changed, insertions, deletions, has_changes)
        self.last_status = status
        self.last_check = datetime.datetime.now()

        return status

    def should_check(self) -> bool:
        """Check if enough time has passed for status check"""
        if self.last_check is None:
            return True
        elapsed = (datetime.datetime.now() - self.last_check).total_seconds()
        return elapsed >= self.check_interval

    def record_status(self, status: GitStatus):
        """Record status and track unchanged count"""
        if not status.has_changes:
            self.unchanged_count += 1
        else:
            self.unchanged_count = 0

    def is_stuck(self) -> bool:
        """Check if agent appears stuck (no changes for max_unchanged checks)"""
        return self.unchanged_count >= self.max_unchanged

    def needs_warning(self) -> bool:
        """Check if warning should be issued (halfway to stuck)"""
        return self.unchanged_count >= (self.max_unchanged // 2) and self.unchanged_count < self.max_unchanged

    def format_status(self, status: GitStatus) -> str:
        """Format status for display"""
        if not status.has_changes:
            return f"{Colors.DIM}[GIT] 📊 No changes{Colors.END}"

        parts = []
        if status.files_changed:
            parts.append(f"{status.files_changed} files")
        if status.insertions:
            parts.append(f"{Colors.GREEN}+{status.insertions}{Colors.END}")
        if status.deletions:
            parts.append(f"{Colors.RED}-{status.deletions}{Colors.END}")

        return f"[GIT] 📊 {', '.join(parts)}"

# ============================================================================
# COMPLETION CHECKER
# ============================================================================

class CompletionChecker:
    """Checks if project is 100% complete based on plan and checklist"""

    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.plan_file = state_dir / "plan.md"
        self.checklist_file = state_dir / "checklist.md"

    def is_complete(self) -> tuple[bool, str]:
        """
        Check if project is complete
        Returns: (is_complete, reason)
        """
        if not self.checklist_file.exists():
            return False, "Checklist not created yet"

        checklist_content = self.checklist_file.read_text(encoding='utf-8')

        # Count checkboxes
        total_tasks = len(re.findall(r'- \[[x ]\]', checklist_content))
        completed_tasks = len(re.findall(r'- \[x\]', checklist_content))
        pending_tasks = len(re.findall(r'- \[ \]', checklist_content))

        if total_tasks == 0:
            return False, "No tasks in checklist"

        completion_percent = int((completed_tasks / total_tasks) * 100)

        if pending_tasks == 0:
            return True, f"All {total_tasks} tasks completed! 🎉"
        else:
            return False, f"{completed_tasks}/{total_tasks} complete ({completion_percent}%), {pending_tasks} remaining"

    def get_next_pending_tasks(self, limit: int = 5) -> List[str]:
        """Get list of next pending tasks"""
        if not self.checklist_file.exists():
            return []

        checklist_content = self.checklist_file.read_text(encoding='utf-8')

        # Find pending tasks
        pending = []
        lines = checklist_content.split('\n')
        for line in lines:
            if '- [ ]' in line:
                task = line.replace('- [ ]', '').strip()
                if task:
                    pending.append(task)
                if len(pending) >= limit:
                    break

        return pending

# ============================================================================
# BOSS ORCHESTRATOR
# ============================================================================

@dataclass
class AgentDecision:
    """Decision from Boss Orchestrator"""
    next_agent: str
    reason: str
    focus: str
    priority: str  # HIGH, MEDIUM, LOW

class BossOrchestrator:
    """AI-powered decision maker for agent orchestration"""

    def __init__(self, state_dir: Path, docs_path: Path):
        self.state_dir = state_dir
        self.docs_path = docs_path
        self.completion_checker = CompletionChecker(state_dir)

    def _get_decision_context(self) -> str:
        """Gather context for Boss decision"""
        context_parts = []

        # 1. Completion status
        is_complete, completion_msg = self.completion_checker.is_complete()
        context_parts.append(f"COMPLETION STATUS: {completion_msg}")

        # 2. Pending tasks
        pending = self.completion_checker.get_next_pending_tasks(10)
        if pending:
            context_parts.append(f"\nNEXT PENDING TASKS:\n" + "\n".join(f"- {t}" for t in pending))

        # 3. Recent review findings
        review_file = self.state_dir / "review.md"
        if review_file.exists():
            review = review_file.read_text(encoding='utf-8')[:1000]
            context_parts.append(f"\nRECENT REVIEW FINDINGS:\n{review}")

        # 4. Test results
        test_file = self.state_dir / "test_report.md"
        if test_file.exists():
            tests = test_file.read_text(encoding='utf-8')[:1000]
            context_parts.append(f"\nTEST RESULTS:\n{tests}")

        # 5. Last agent activity
        journal_file = self.state_dir / "journal.md"
        if journal_file.exists():
            journal = journal_file.read_text(encoding='utf-8')
            # Get last 500 chars
            context_parts.append(f"\nRECENT ACTIVITY:\n{journal[-500:]}")

        return "\n".join(context_parts)

    def decide_next_agent(self) -> AgentDecision:
        """
        Use Claude to decide which agent should run next

        Returns decision with agent, reason, and focus area
        """
        context = self._get_decision_context()

        prompt = f"""You are the BOSS ORCHESTRATOR for a multi-agent software development system.

AVAILABLE AGENTS:
- planner: Creates project plans and architecture
- designer: Designs UI/UX components
- engineer: Sets up infrastructure and DevOps
- developer: Implements features and APIs
- reviewer: Reviews code quality
- tester: Runs tests and finds bugs
- supervisor: Checks for conflicts and issues

CURRENT PROJECT STATE:
{context}

RULES:
1. Choose the MOST IMPORTANT agent to run next
2. Consider what's incomplete and what's blocking progress
3. Developer can run multiple times in a row if needed
4. Reviewer should run after significant code changes
5. Tester should run after new features
6. Don't run designer if no UI work is needed

OUTPUT FORMAT (JSON):
{{
  "next_agent": "developer",
  "reason": "Phase 2 APIs are 60% complete, need to finish remaining endpoints",
  "focus": "Complete /api/v1/social-posts/ CRUD endpoints",
  "priority": "HIGH"
}}

Respond ONLY with valid JSON, no other text."""

        # Use Claude CLI to make decision
        try:
            cmd = ['claude', '--print', '--dangerously-skip-permissions', prompt]
            result = subprocess.run(
                cmd,
                cwd=str(self.state_dir),
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                # Extract JSON from output
                json_match = re.search(r'\{[^}]+\}', output, re.DOTALL)
                if json_match:
                    decision_data = json.loads(json_match.group(0))
                    return AgentDecision(**decision_data)
        except Exception as e:
            log(f"Boss decision failed: {e}", "WARNING")

        # Fallback: intelligent default based on completion
        is_complete, msg = self.completion_checker.is_complete()
        if is_complete:
            return AgentDecision(
                next_agent="supervisor",
                reason="Project appears complete, final check",
                focus="Verify all requirements met",
                priority="LOW"
            )

        # Default to developer
        return AgentDecision(
            next_agent="developer",
            reason="Continuing development work",
            focus="Complete pending tasks from checklist",
            priority="MEDIUM"
        )

# ============================================================================
# MAIN ORCHESTRATOR (v3.0 - Enhanced with all new components)
# ============================================================================

class Orchestrator:
    """
    Main orchestration logic with integrated v3.0 enhancements:
    - Structured logging (AgentLogger)
    - Memory management (ContextManager)
    - Checkpointing (CheckpointManager)
    - Interactive mode (InteractiveController)
    - Secret detection (SecretDetector)
    - Code analysis (CodeAnalyzer)
    """

    def __init__(self, docs_path: str, dev_path: str, autonomous_mode: bool = False, interactive_mode: bool = False):
        self.docs_path = Path(docs_path).resolve()
        self.dev_path = Path(dev_path).resolve()
        self.state_dir = self.dev_path / ".spinstate"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.autonomous_mode = autonomous_mode
        self.interactive_mode = interactive_mode

        # ===== V3.0 NEW COMPONENTS =====

        # Structured logging
        self.logger = AgentLogger(
            log_file=str(self.state_dir / "spin_session.jsonl"),
            console_output=True
        )

        # Context/Memory management
        self.context_manager = ContextManager(max_tokens=MAX_CONTEXT_TOKENS)

        # Checkpointing
        self.checkpoint_manager = CheckpointManager(self.state_dir / "checkpoints")

        # Interactive controller
        self.interactive = InteractiveController(enabled=interactive_mode)

        # Security - secret detection
        self.secret_detector = SecretDetector()

        # Code quality analysis
        self.code_analyzer = CodeAnalyzer()

        # ===== EXISTING COMPONENTS =====

        # Git handling
        self.git = GitHandler(str(self.dev_path))
        self.journal = Journal(str(self.state_dir / "journal.md"))
        self.git_monitor = GitMonitor(str(self.dev_path), check_interval=30, max_unchanged=10)
        self.runner = ClaudeRunner(str(self.dev_path), str(self.state_dir / "logs"), git_monitor=self.git_monitor)

        # Boss Orchestrator for autonomous mode
        self.boss = BossOrchestrator(self.state_dir, self.docs_path) if autonomous_mode else None
        self.completion_checker = CompletionChecker(self.state_dir)

        # Set up legacy logging (for compatibility)
        log.log_file = str(self.state_dir / "orchestrator.log")

        # Load or create state
        self.state = self._load_state()

        # Try to restore from checkpoint if resuming
        self._try_restore_checkpoint()

        # Agent workflow order (used in non-autonomous mode)
        self.workflow = [
            AgentRole.PLANNER,
            AgentRole.DESIGNER,
            AgentRole.ENGINEER,
            AgentRole.DEVELOPER,
            AgentRole.REVIEWER,
            AgentRole.TESTER,
            AgentRole.SUPERVISOR,
        ]

        # Log initialization with new structured logger
        self.logger.log(
            "ORCHESTRATOR",
            "INITIALIZED",
            {
                "version": VERSION,
                "docs_path": str(self.docs_path),
                "dev_path": str(self.dev_path),
                "autonomous_mode": autonomous_mode,
                "interactive_mode": interactive_mode
            },
            status="SUCCESS"
        )

        log(t("orchestrator.initialized"), "SUCCESS")
        log(f"  Documentation: {self.docs_path}", "INFO")
        log(f"  Development: {self.dev_path}", "INFO")
        if autonomous_mode:
            log(f"  🤖 AUTONOMOUS MODE: Boss Orchestrator active", "INFO")
        if interactive_mode:
            log(f"  👤 INTERACTIVE MODE: Human approval required", "INFO")

    def _try_restore_checkpoint(self):
        """Try to restore from latest checkpoint if available"""
        checkpoint = self.checkpoint_manager.load_latest()
        if checkpoint:
            # Restore context manager
            if "context" in checkpoint:
                self.context_manager = ContextManager.from_dict(checkpoint["context"])
                self.logger.log(
                    "ORCHESTRATOR",
                    "CHECKPOINT_RESTORED",
                    {"stage": checkpoint.get("stage"), "completion": checkpoint.get("completion_percent")},
                    status="INFO"
                )
    
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

    def _get_agent_description(self, role: AgentRole) -> str:
        """Get human-readable description of what an agent does"""
        descriptions = {
            AgentRole.PLANNER: "Analyze documentation and create development plan with phases and checklist",
            AgentRole.DESIGNER: "Design UI/UX components, create design specs and tokens",
            AgentRole.ENGINEER: "Set up infrastructure, database, Docker, and project skeleton",
            AgentRole.DEVELOPER: "Implement features according to the plan and checklist",
            AgentRole.REVIEWER: "Review code quality, identify bugs and security issues",
            AgentRole.TESTER: "Run tests, verify functionality, report failures",
            AgentRole.SUPERVISOR: "Check for conflicts, analyze patterns, detect issues",
            AgentRole.EVOLVER: "Improve the orchestration system based on learnings"
        }
        return descriptions.get(role, "Execute assigned tasks")

    def run_agent(self, role: AgentRole, retry_count: int = 0) -> bool:
        """Run a single agent with retry logic and v3.0 enhancements"""
        start_time = time.time()

        log(f"\n{'='*60}", "PHASE")
        log(f"PHASE: {role.value.upper()}", "PHASE")
        log(f"{'='*60}\n", "PHASE")

        # ===== INTERACTIVE MODE: Ask for approval =====
        if self.interactive_mode:
            approved, feedback = self.interactive.ask_approval(
                role.value,
                f"Run {role.value.upper()} agent",
                f"This agent will: {self._get_agent_description(role)}"
            )
            if not approved:
                if feedback == "SKIP":
                    self.logger.log(role.value, "SKIPPED", "User skipped agent", status="WARNING")
                    return True  # Continue to next
                else:
                    self.logger.log(role.value, "REJECTED", "User rejected agent", status="WARNING")
                    return False

            # If user provided feedback, inject into context
            if feedback:
                self.context_manager.add_history("USER_FEEDBACK", feedback)

        self.state.current_agent = role.value
        self._save_state()

        # Log start with structured logger
        self.logger.log(
            role.value,
            "STARTED",
            {"retry_count": retry_count, "phase": self.state.current_phase},
            context_usage=self.context_manager.get_usage_percent(),
            status="INFO"
        )

        # Update journal
        self.journal.update_status(role.value, role.value)
        self.journal.add_entry(role.value, "STARTED", f"Agent {role.value} zahájen")

        # Create git tag for phase start
        tag_name = f"phase-{role.value}-start-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.git.tag(tag_name, f"Starting {role.value} phase")

        # ===== CONTEXT MANAGEMENT: Update context with current state =====
        self.context_manager.update_block("active_task", f"Current agent: {role.value}")

        # Load handoff notes if they exist
        handoff_file = self.state_dir / "handoff.md"
        if handoff_file.exists():
            handoff_content = handoff_file.read_text(encoding='utf-8')
            self.context_manager.update_block("handoff_notes", handoff_content)

        # Get prompt and run
        prompt = self._get_prompt_for_agent(role)
        success, output, context_percent = self.runner.run_agent(role.value, prompt)

        # Record context usage
        self.context_manager.add_history(role.value, f"Completed with {context_percent}% context")

        duration_ms = int((time.time() - start_time) * 1000)

        # Check completion status
        status = self._check_agent_status()

        # ===== V3.0: POST-AGENT SECURITY SCAN =====
        if role == AgentRole.DEVELOPER:
            try:
                # Scan for secrets in modified files
                secrets_found = self.secret_detector.scan_directory(self.dev_path, extensions=['.py', '.ts', '.js', '.env'])
                if secrets_found:
                    self.logger.log(
                        role.value,
                        "SECURITY_ALERT",
                        {"secrets_found": len(secrets_found), "types": [s["type"] for s in secrets_found]},
                        status="ERROR"
                    )
                    log(f"🚨 SECURITY: Found {len(secrets_found)} potential secrets! Review before commit.", "ERROR")
            except Exception as e:
                self.logger.log(role.value, "SECURITY_SCAN_FAILED", str(e), status="WARNING")

            # ===== V3.0: CODE QUALITY CHECK =====
            try:
                analysis = self.code_analyzer.analyze_directory(str(self.dev_path), extensions=[".py"])
                if analysis["failed"] > 0:
                    self.logger.log(
                        role.value,
                        "CODE_QUALITY",
                        {"passed": analysis["passed"], "failed": analysis["failed"]},
                        status="WARNING"
                    )
                    log(f"⚠️  Code quality: {analysis['failed']}/{analysis['total_files']} files have issues", "WARNING")
            except Exception as e:
                self.logger.log(role.value, "CODE_ANALYSIS_FAILED", str(e), status="WARNING")

        # ===== V3.0: CHECKPOINTING =====
        is_complete, completion_msg = self.completion_checker.is_complete()
        completion_percent = 0.0
        if "%" in completion_msg:
            try:
                completion_percent = float(re.search(r'(\d+)%', completion_msg).group(1))
            except:
                pass

        self.checkpoint_manager.save(
            stage=role.value,
            agent=role.value,
            context_manager=self.context_manager,
            project_state=self.state,
            completion_percent=completion_percent
        )

        if success and status and "COMPLETE" in status:
            # Agent completed successfully
            self.logger.log(
                role.value,
                "COMPLETED",
                {"duration_ms": duration_ms, "context_percent": context_percent},
                context_usage=context_percent,
                duration_ms=duration_ms,
                status="SUCCESS"
            )
            self.journal.add_entry(role.value, "COMPLETED", f"Agent dokončen úspěšně")
            self.state.completed_phases.append(role.value)
            self.git.commit(f"[{role.value}] Phase completed")
            self.git.push()
            self._save_state()
            return True

        elif context_percent >= CONTEXT_LIMIT_PERCENT:
            # Context limit reached - handoff
            self.logger.log(
                role.value,
                "CONTEXT_LIMIT",
                {"percent": context_percent, "limit": CONTEXT_LIMIT_PERCENT},
                context_usage=context_percent,
                status="WARNING"
            )
            log(t("agent.context_limit", percent=context_percent), "WARNING")
            self.journal.add_handoff(
                role.value,
                role.value,
                f"Context limit reached ({context_percent}%)",
                "Continuing from handoff.md"
            )
            self.git.commit(f"[{role.value}] Context limit handoff")

            # Clear context for fresh start
            self.context_manager.compact()

            # Run same agent again with fresh context
            if retry_count < MAX_RETRIES:
                log(t("agent.restart", role=role.value, current=retry_count+1, max=MAX_RETRIES), "INFO")
                return self.run_agent(role, retry_count + 1)
            else:
                log(t("agent.max_retries", role=role.value), "ERROR")
                return False

        elif not success:
            # Agent failed - use error classification
            issue, fix = self._analyze_failure(role.value, output)
            error_type = classify_error(Exception(issue))

            self.logger.log(
                role.value,
                "FAILED",
                {"issue": issue, "fix": fix, "error_type": error_type, "duration_ms": duration_ms},
                status="ERROR"
            )
            log(t("agent.failed", issue=issue), "ERROR")
            log(t("agent.recommendation", fix=fix), "INFO")

            self.journal.add_entry(role.value, "FAILED", f"Selhání: {issue}", f"Fix: {fix}")

            # Add to collision log if it's a recurring issue
            self.state.known_issues.append(f"{role.value}: {issue}")

            # Only retry transient/recoverable errors
            if error_type != "PERMANENT" and retry_count < MAX_RETRIES:
                log(t("agent.retry"), "INFO")
                # Use exponential backoff for retries
                delay = RETRY_INITIAL_DELAY * (RETRY_EXPONENTIAL_BASE ** retry_count) + random.uniform(0, 1)
                time.sleep(delay)
                return self.run_agent(role, retry_count + 1)
            else:
                return False

        else:
            # Unclear state - treat as needing continuation
            self.logger.log(
                role.value,
                "UNCLEAR_STATE",
                {"duration_ms": duration_ms},
                status="WARNING"
            )
            log(t("agent.unclear_state", role=role.value), "WARNING")
            self.git.commit(f"[{role.value}] Partial progress")
            return True  # Continue to next phase
    
    def run_full_workflow(self):
        """Run complete development workflow"""
        log(f"\n{t('orchestrator.workflow_start')}\n", "PHASE")
        
        # Determine starting point
        start_index = 0
        if self.state.completed_phases:
            last_completed = self.state.completed_phases[-1]
            for i, role in enumerate(self.workflow):
                if role.value == last_completed:
                    start_index = i + 1
                    break
        
        if start_index > 0:
            log(t("orchestrator.resume_from", phase=self.workflow[start_index].value), "INFO")

        # Run workflow
        for role in self.workflow[start_index:]:
            if not self.run_agent(role):
                log(t("orchestrator.workflow_stopped", phase=role.value), "ERROR")
                return False

        # Final supervision
        log(f"\n{t('orchestrator.final_supervision')}\n", "PHASE")
        self.run_agent(AgentRole.SUPERVISOR)
        
        # Evolution phase
        log(f"\n{t('orchestrator.evolution')}\n", "PHASE")
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

        log(f"\n{t('orchestrator.workflow_complete')}\n", "SUCCESS")
        return True

    def run_autonomous_loop(self, max_iterations: int = 100):
        """
        Run autonomous loop with Boss Orchestrator making decisions
        Continues until 100% complete or max iterations reached
        """
        if not self.autonomous_mode:
            log("Autonomous mode not enabled! Use --autonomous flag", "ERROR")
            return False

        log(f"\n{'='*60}", "PHASE")
        log("🤖 AUTONOMOUS ORCHESTRATION MODE ACTIVE", "PHASE")
        log(f"{'='*60}\n", "PHASE")

        iteration = 0
        consecutive_failures = 0
        max_failures = 3

        while iteration < max_iterations:
            iteration += 1

            # Check completion
            is_complete, completion_msg = self.completion_checker.is_complete()
            log(f"📊 Status: {completion_msg}", "INFO")

            if is_complete:
                log(f"\n{'='*60}", "SUCCESS")
                log("✅ PROJECT 100% COMPLETE!", "SUCCESS")
                log(f"{'='*60}\n", "SUCCESS")

                # Final supervision
                log("\n🔍 Running final supervision...\n", "PHASE")
                self.run_agent(AgentRole.SUPERVISOR)

                # Final tag
                self.git.tag(f"complete-{datetime.datetime.now().strftime('%Y%m%d%H%M')}", "Autonomous completion")
                self.git.push()

                return True

            # Get Boss decision
            log(f"\n[Iteration {iteration}/{max_iterations}]", "PHASE")
            log("🧠 Boss Orchestrator deciding next move...", "PHASE")

            decision = self.boss.decide_next_agent()

            # Display decision
            priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(decision.priority, "🔵")
            log(f"{priority_icon} DECISION: {decision.next_agent.upper()}", "PHASE")
            log(f"   Reason: {decision.reason}", "INFO")
            log(f"   Focus: {decision.focus}", "INFO")

            # Map decision to AgentRole
            agent_map = {
                "planner": AgentRole.PLANNER,
                "designer": AgentRole.DESIGNER,
                "engineer": AgentRole.ENGINEER,
                "developer": AgentRole.DEVELOPER,
                "reviewer": AgentRole.REVIEWER,
                "tester": AgentRole.TESTER,
                "supervisor": AgentRole.SUPERVISOR,
            }

            agent_role = agent_map.get(decision.next_agent.lower())
            if not agent_role:
                log(f"Unknown agent: {decision.next_agent}", "WARNING")
                agent_role = AgentRole.DEVELOPER  # Fallback

            # Run the selected agent
            success = self.run_agent(agent_role)

            if not success:
                consecutive_failures += 1
                log(f"⚠️  Agent failed ({consecutive_failures}/{max_failures} consecutive failures)", "WARNING")

                if consecutive_failures >= max_failures:
                    log(f"❌ Too many consecutive failures, stopping autonomous loop", "ERROR")
                    return False
            else:
                consecutive_failures = 0  # Reset on success

            # Brief pause between iterations
            time.sleep(2)

        log(f"\n⚠️  Reached maximum iterations ({max_iterations}) without full completion", "WARNING")
        is_complete, completion_msg = self.completion_checker.is_complete()
        log(f"Final status: {completion_msg}", "INFO")

        return False

# ============================================================================
# INTERACTIVE SETUP
# ============================================================================

def interactive_setup() -> tuple[str, str]:
    """Interactive setup to get paths from user"""
    print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}   🔄 SpinThatShit - AI Agent Orchestrator v{VERSION} 🔄{Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")

    print(t("welcome.message") + "\n")
    
    # Documentation path
    while True:
        docs_input = input(f"📁 {t('setup.docs_prompt')}: ").strip()

        if docs_input.lower() == 'new':
            docs_path = input(f"   {t('setup.docs_new_path')}: ").strip()
            docs_path = Path(docs_path).expanduser().resolve()
            create = input(f"   {t('setup.docs_confirm_create', path=docs_path)} ").strip().lower()
            if create != 'n':
                docs_path.mkdir(parents=True, exist_ok=True)
                # Create sample README
                readme = docs_path / "README.md"
                readme.write_text("# Project Documentation\n\nAdd your project documentation here.\n")
                print(f"   ✅ {t('setup.docs_created', path=docs_path)}")
                break
        else:
            docs_path = Path(docs_input).expanduser().resolve()
            if docs_path.exists():
                if docs_path.is_dir():
                    print(f"   ✅ {t('setup.docs_found', path=docs_path)}")
                    break
                else:
                    print(f"   ❌ {t('setup.docs_not_folder')}")
            else:
                create = input(f"   {t('setup.folder_not_exist')} ").strip().lower()
                if create != 'n':
                    docs_path.mkdir(parents=True, exist_ok=True)
                    print(f"   ✅ {t('setup.docs_created', path=docs_path)}")
                    break
    
    print()
    
    # Development path
    while True:
        dev_input = input(f"💻 {t('setup.dev_prompt')}: ").strip()

        if dev_input.lower() == 'new':
            dev_path = input(f"   {t('setup.dev_new_path')}: ").strip()
            dev_path = Path(dev_path).expanduser().resolve()
            create = input(f"   {t('setup.dev_confirm_create', path=dev_path)} ").strip().lower()
            if create != 'n':
                dev_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ {t('setup.dev_created', path=dev_path)}")
                break
        else:
            dev_path = Path(dev_input).expanduser().resolve()
            if dev_path.exists():
                if dev_path.is_dir():
                    print(f"   ✅ {t('setup.dev_found', path=dev_path)}")
                    break
                else:
                    print(f"   ❌ {t('setup.dev_not_folder')}")
            else:
                create = input(f"   {t('setup.folder_not_exist')} ").strip().lower()
                if create != 'n':
                    dev_path.mkdir(parents=True, exist_ok=True)
                    print(f"   ✅ {t('setup.dev_created', path=dev_path)}")
                    break
    
    print()
    
    # Validation summary
    print(f"\n{Colors.CYAN}📋 {t('setup.summary_title')}:{Colors.END}")
    print(f"   {t('setup.summary_docs')}: {docs_path}")
    print(f"   {t('setup.summary_dev')}: {dev_path}")

    # Count files
    doc_files = list(docs_path.glob('**/*'))
    dev_files = list(dev_path.glob('**/*'))
    print(f"   {t('setup.summary_doc_files')}: {len([f for f in doc_files if f.is_file()])}")
    print(f"   {t('setup.summary_dev_files')}: {len([f for f in dev_files if f.is_file()])}")

    confirm = input(f"\n🚀 {t('setup.confirm_start')} ").strip().lower()
    if confirm == 'n':
        print(t("setup.cancelled"))
        sys.exit(0)
    
    return str(docs_path), str(dev_path)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point with v3.0 enhancements"""
    parser = argparse.ArgumentParser(
        description="SpinThatShit v3.0 - AI Agent Orchestration System with Enhanced Features"
    )
    parser.add_argument('--docs', help='Path to documentation folder')
    parser.add_argument('--dev', help='Path to development folder')
    parser.add_argument('--resume', action='store_true', help='Resume from last checkpoint')
    parser.add_argument('--autonomous', action='store_true', help='Enable autonomous mode with Boss Orchestrator')
    parser.add_argument('--interactive', '-i', action='store_true', help='Enable interactive mode (human approval for each agent)')
    parser.add_argument('--lang', help='Language code (e.g., en, cs, es)')
    parser.add_argument('--list-checkpoints', action='store_true', help='List available checkpoints and exit')
    parser.add_argument('--restore-checkpoint', help='Restore from specific checkpoint file')
    parser.add_argument('--version', action='version', version=f'SpinThatShit v{VERSION}')

    args = parser.parse_args()

    # Initialize language
    if args.lang:
        # Use language from command line
        init_i18n(args.lang)
        save_language_config(args.lang)
    else:
        # Check if language is already configured
        saved_lang = load_language_config()
        if saved_lang == 'en' and not (get_config_dir() / "language.json").exists():
            # First run - ask user to select language
            selected_lang = select_language()
            init_i18n(selected_lang)
        else:
            # Use saved language
            init_i18n(saved_lang)

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print(f"\n\n⚠️  {t('orchestrator.stopped_by_user')}")
        print(f"   {t('orchestrator.state_saved')}\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # ===== V3.0: Handle checkpoint commands =====
    if args.list_checkpoints:
        if not args.dev:
            print("❌ --dev path required to list checkpoints")
            sys.exit(1)
        checkpoint_dir = Path(args.dev) / ".spinstate" / "checkpoints"
        manager = CheckpointManager(checkpoint_dir)
        checkpoints = manager.list_checkpoints()
        if not checkpoints:
            print("📭 No checkpoints found")
        else:
            print(f"\n📋 Available checkpoints ({len(checkpoints)}):\n")
            for cp in checkpoints[:10]:
                print(f"  [{cp['timestamp']}] Stage: {cp['stage']}, Agent: {cp['agent']}, {cp['completion']:.1f}% complete")
                print(f"    File: {cp['file']}")
        sys.exit(0)

    if args.restore_checkpoint:
        if not args.dev:
            print("❌ --dev path required to restore checkpoint")
            sys.exit(1)
        checkpoint_file = Path(args.restore_checkpoint)
        if not checkpoint_file.exists():
            print(f"❌ Checkpoint file not found: {checkpoint_file}")
            sys.exit(1)
        print(f"📂 Restoring from checkpoint: {checkpoint_file}")
        # Will be loaded by Orchestrator automatically

    # Get paths
    if args.docs and args.dev:
        docs_path = args.docs
        dev_path = args.dev
    else:
        docs_path, dev_path = interactive_setup()

    # ===== V3.0: Create orchestrator with new parameters =====
    try:
        orchestrator = Orchestrator(
            docs_path,
            dev_path,
            autonomous_mode=args.autonomous,
            interactive_mode=args.interactive
        )

        # Log session start
        print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}  SpinThatShit v{VERSION} - Session Started{Colors.END}")
        print(f"{Colors.HEADER}{'='*60}{Colors.END}")
        print(f"  Mode: {'🤖 Autonomous' if args.autonomous else '👤 Interactive' if args.interactive else '📋 Sequential'}")
        print(f"  Docs: {docs_path}")
        print(f"  Dev:  {dev_path}")
        print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")

        if args.autonomous:
            # Run autonomous loop
            orchestrator.run_autonomous_loop(max_iterations=100)
        else:
            # Run traditional workflow
            orchestrator.run_full_workflow()

        # ===== V3.0: Export session log on completion =====
        session_file = orchestrator.logger.export_session()
        summary = orchestrator.logger.get_session_summary()
        print(f"\n{Colors.GREEN}✅ Session completed successfully!{Colors.END}")
        print(f"   Session log: {session_file}")
        print(f"   Total actions: {summary.get('total_entries', 0)}")
        print(f"   Errors: {summary.get('error_count', 0)}")
        print(f"   Warnings: {summary.get('warning_count', 0)}")
        print(f"   Max context usage: {summary.get('max_context_usage', 0):.1f}%")

    except KeyboardInterrupt:
        print(f"\n\n⚠️  {t('orchestrator.stopped_by_user')}")
        if 'orchestrator' in locals():
            orchestrator.checkpoint_manager.save(
                stage="INTERRUPTED",
                agent="user",
                context_manager=orchestrator.context_manager,
                project_state=orchestrator.state
            )
            print(f"   💾 Checkpoint saved. Use --resume to continue.")
        sys.exit(0)
    except Exception as e:
        log(t("orchestrator.critical_error", error=str(e)), "ERROR")
        if 'orchestrator' in locals():
            orchestrator.logger.log(
                "ORCHESTRATOR",
                "CRITICAL_ERROR",
                {"error": str(e), "type": type(e).__name__},
                status="ERROR"
            )
        raise

if __name__ == "__main__":
    main()
