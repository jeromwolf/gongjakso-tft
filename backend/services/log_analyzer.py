"""
Log Analyzer Service

Analyzes application logs and provides insights
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from collections import defaultdict, Counter
from loguru import logger as loguru_logger


class LogEntry:
    """Parsed log entry"""
    def __init__(
        self,
        timestamp: datetime,
        level: str,
        module: str,
        function: str,
        line: int,
        message: str,
    ):
        self.timestamp = timestamp
        self.level = level
        self.module = module
        self.function = function
        self.line = line
        self.message = message

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "module": self.module,
            "function": self.function,
            "line": self.line,
            "message": self.message,
        }


class LogAnalyzer:
    """Log analyzer for AI ON application"""

    # Loguru log pattern
    LOG_PATTERN = re.compile(
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| '
        r'(\w+)\s+\| '
        r'([^:]+):([^:]+):(\d+) - '
        r'(.+)'
    )

    def __init__(self, log_dir: Path = None):
        """
        Initialize log analyzer

        Args:
            log_dir: Directory containing log files (default: backend/logs/)
        """
        if log_dir is None:
            log_dir = Path(__file__).parent.parent / "logs"
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def parse_log_line(self, line: str) -> Optional[LogEntry]:
        """Parse a single log line"""
        match = self.LOG_PATTERN.match(line)
        if not match:
            return None

        timestamp_str, level, module, function, line_no, message = match.groups()

        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            timestamp = timestamp.replace(tzinfo=timezone.utc)

            return LogEntry(
                timestamp=timestamp,
                level=level,
                module=module,
                function=function,
                line=int(line_no),
                message=message.strip(),
            )
        except Exception as e:
            loguru_logger.warning(f"Failed to parse log line: {e}")
            return None

    def read_logs(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None,
        limit: int = 1000
    ) -> List[LogEntry]:
        """
        Read and parse log files

        Args:
            start_time: Filter logs after this time
            end_time: Filter logs before this time
            level: Filter by log level (INFO, WARNING, ERROR, etc.)
            limit: Maximum number of entries to return

        Returns:
            List of parsed log entries
        """
        entries = []

        # Find log files (sorted by modification time, newest first)
        log_files = sorted(
            self.log_dir.glob("*.log"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        entry = self.parse_log_line(line)
                        if not entry:
                            continue

                        # Apply filters
                        if start_time and entry.timestamp < start_time:
                            continue
                        if end_time and entry.timestamp > end_time:
                            continue
                        if level and entry.level != level:
                            continue

                        entries.append(entry)

                        if len(entries) >= limit:
                            break

                if len(entries) >= limit:
                    break

            except Exception as e:
                loguru_logger.warning(f"Failed to read log file {log_file}: {e}")

        # Sort by timestamp (newest first)
        entries.sort(key=lambda e: e.timestamp, reverse=True)

        return entries[:limit]

    def get_error_summary(
        self,
        hours: int = 24
    ) -> Dict:
        """
        Get error summary for the last N hours

        Args:
            hours: Number of hours to analyze

        Returns:
            Dict with error statistics
        """
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        error_entries = self.read_logs(
            start_time=start_time,
            level="ERROR",
            limit=10000
        )

        # Count errors by module
        errors_by_module = Counter()
        # Count errors by message pattern
        error_patterns = Counter()
        # Recent errors
        recent_errors = []

        for entry in error_entries:
            errors_by_module[entry.module] += 1

            # Extract error pattern (first 100 chars)
            pattern = entry.message[:100]
            error_patterns[pattern] += 1

            if len(recent_errors) < 10:
                recent_errors.append(entry.to_dict())

        return {
            "period": f"Last {hours} hours",
            "total_errors": len(error_entries),
            "errors_by_module": dict(errors_by_module.most_common(10)),
            "common_patterns": [
                {"pattern": pattern, "count": count}
                for pattern, count in error_patterns.most_common(5)
            ],
            "recent_errors": recent_errors,
        }

    def get_activity_summary(
        self,
        hours: int = 24
    ) -> Dict:
        """
        Get activity summary for the last N hours

        Args:
            hours: Number of hours to analyze

        Returns:
            Dict with activity statistics
        """
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        entries = self.read_logs(
            start_time=start_time,
            limit=10000
        )

        # Count by level
        levels = Counter()
        # Count by module
        modules = Counter()
        # Activity timeline (hourly)
        timeline = defaultdict(lambda: {"INFO": 0, "WARNING": 0, "ERROR": 0, "SUCCESS": 0})

        for entry in entries:
            levels[entry.level] += 1
            modules[entry.module] += 1

            # Group by hour
            hour_key = entry.timestamp.strftime("%Y-%m-%d %H:00")
            timeline[hour_key][entry.level] += 1

        # Convert timeline to list
        timeline_list = [
            {"hour": hour, **counts}
            for hour, counts in sorted(timeline.items(), reverse=True)
        ]

        return {
            "period": f"Last {hours} hours",
            "total_logs": len(entries),
            "by_level": dict(levels),
            "top_modules": dict(modules.most_common(10)),
            "timeline": timeline_list[:24],  # Last 24 hours
        }

    def get_api_stats(
        self,
        hours: int = 24
    ) -> Dict:
        """
        Get API request statistics

        Args:
            hours: Number of hours to analyze

        Returns:
            Dict with API statistics
        """
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        entries = self.read_logs(
            start_time=start_time,
            limit=10000
        )

        # Look for API-related logs
        api_requests = []
        api_errors = []
        endpoints = Counter()

        for entry in entries:
            # Match API request patterns
            if "GET" in entry.message or "POST" in entry.message or "PUT" in entry.message or "DELETE" in entry.message:
                # Extract endpoint
                match = re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+(/api/[^\s]+)', entry.message)
                if match:
                    method, endpoint = match.groups()
                    endpoints[f"{method} {endpoint}"] += 1
                    api_requests.append({
                        "timestamp": entry.timestamp.isoformat(),
                        "method": method,
                        "endpoint": endpoint,
                        "level": entry.level,
                    })

            # Track API errors
            if entry.level == "ERROR" and "api" in entry.module.lower():
                api_errors.append(entry.to_dict())

        return {
            "period": f"Last {hours} hours",
            "total_requests": len(api_requests),
            "total_errors": len(api_errors),
            "top_endpoints": [
                {"endpoint": endpoint, "count": count}
                for endpoint, count in endpoints.most_common(10)
            ],
            "recent_errors": api_errors[:10],
        }

    def get_automation_stats(
        self,
        days: int = 7
    ) -> Dict:
        """
        Get automation (blog/newsletter) statistics

        Args:
            days: Number of days to analyze

        Returns:
            Dict with automation statistics
        """
        start_time = datetime.now(timezone.utc) - timedelta(days=days)

        entries = self.read_logs(
            start_time=start_time,
            limit=10000
        )

        blog_generated = 0
        blog_published = 0
        newsletter_generated = 0
        newsletter_sent = 0
        automation_errors = []

        for entry in entries:
            msg = entry.message.lower()

            # Blog stats
            if "blog generated" in msg or "draft blog created" in msg:
                blog_generated += 1
            if "blog" in msg and "published" in msg:
                blog_published += 1

            # Newsletter stats
            if "newsletter generated" in msg or "draft newsletter created" in msg:
                newsletter_generated += 1
            if "newsletter" in msg and ("sent" in msg or "발송" in msg):
                newsletter_sent += 1

            # Automation errors
            if entry.level == "ERROR" and ("blog" in msg or "newsletter" in msg):
                automation_errors.append(entry.to_dict())

        return {
            "period": f"Last {days} days",
            "blog": {
                "generated": blog_generated,
                "published": blog_published,
                "draft_rate": f"{((blog_generated - blog_published) / max(blog_generated, 1) * 100):.1f}%"
            },
            "newsletter": {
                "generated": newsletter_generated,
                "sent": newsletter_sent,
                "draft_rate": f"{((newsletter_generated - newsletter_sent) / max(newsletter_generated, 1) * 100):.1f}%"
            },
            "errors": automation_errors[:10],
        }


def get_log_analyzer() -> LogAnalyzer:
    """Get log analyzer instance"""
    return LogAnalyzer()
