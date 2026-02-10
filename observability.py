"""
Observability Stack for Deep Research System v9.0

Provides comprehensive observability for multi-agent research:
- Metrics collection (token usage, latency, costs)
- Distributed tracing for agent execution
- Event logging and streaming
- Real-time monitoring dashboard

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import time
import threading


class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"  # Monotonically increasing
    GAUGE = "gauge"  # Can go up or down
    HISTOGRAM = "histogram"  # Distribution of values


class LogLevel(Enum):
    """Log levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Metric:
    """A metric data point"""
    name: str
    value: float
    type: MetricType
    timestamp: str
    labels: Dict[str, str] = field(default_factory=dict)
    unit: str = ""


@dataclass
class Span:
    """A trace span representing an operation"""
    span_id: str
    parent_id: Optional[str]
    operation: str
    start_time: float
    end_time: Optional[float]
    status: str  # "ok", "error"
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get span duration in seconds"""
        if self.end_time is not None:
            return self.end_time - self.start_time
        return None


@dataclass
class LogEntry:
    """A log entry"""
    timestamp: str
    level: LogLevel
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    agent_id: Optional[str] = None
    session_id: Optional[str] = None


class MetricsCollector:
    """
    Collects and aggregates metrics.

    Metrics tracked:
    - Token usage (input, output, total)
    - Latency (per agent, per operation)
    - Cost (estimated USD)
    - Success/failure rates
    - Task throughput
    """

    def __init__(self):
        self._metrics: Dict[str, List[Metric]] = defaultdict(list)
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, List[float]] = defaultdict(list)

        self._lock = threading.Lock()

    def increment(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a counter metric.

        Args:
            name: Metric name
            value: Value to add (default 1.0)
            labels: Optional labels
        """
        with self._lock:
            self._counters[name] += value
            self._add_metric(name, value, MetricType.COUNTER, labels)

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Set a gauge metric.

        Args:
            name: Metric name
            value: Gauge value
            labels: Optional labels
        """
        with self._lock:
            self._gauges[name] = value
            self._add_metric(name, value, MetricType.GAUGE, labels)

    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record a value in a histogram.

        Args:
            name: Metric name
            value: Value to record
            labels: Optional labels
        """
        with self._lock:
            self._histograms[name].append(value)
            self._add_metric(name, value, MetricType.HISTOGRAM, labels)

    def _add_metric(self, name: str, value: float, metric_type: MetricType, labels: Optional[Dict[str, str]]) -> None:
        """Add a metric point"""
        metric = Metric(
            name=name,
            value=value,
            type=metric_type,
            timestamp=datetime.now().isoformat(),
            labels=labels or {}
        )
        self._metrics[name].append(metric)

    def get_metric(self, name: str) -> Dict[str, Any]:
        """
        Get current value of a metric.

        Args:
            name: Metric name

        Returns:
            Metric value and metadata
        """
        with self._lock:
            if name in self._counters:
                return {"type": "counter", "value": self._counters[name]}
            elif name in self._gauges:
                return {"type": "gauge", "value": self._gauges[name]}
            elif name in self._histograms:
                values = self._histograms[name]
                if values:
                    return {
                        "type": "histogram",
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "mean": sum(values) / len(values),
                        "sum": sum(values)
                    }
        return {"error": f"Metric not found: {name}"}

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metric values"""
        with self._lock:
            result = {}

            for name in self._counters:
                result[name] = self.get_metric(name)

            for name in self._gauges:
                result[name] = self.get_metric(name)

            for name in self._histograms:
                result[name] = self.get_metric(name)

            return result

    def reset(self) -> None:
        """Reset all metrics"""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._metrics.clear()


class Tracer:
    """
    Distributed tracing for agent execution.

    Tracks:
    - Agent execution spans
    - Tool call spans
    - Parent-child relationships
    - Execution timing
    """

    def __init__(self):
        self._spans: Dict[str, Span] = {}
        self._root_spans: List[str] = []
        self._current_span: Optional[str] = None
        self._lock = threading.Lock()

    def start_span(
        self,
        operation: str,
        parent_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start a new trace span.

        Args:
            operation: Operation name
            parent_id: Optional parent span ID
            tags: Optional tags

        Returns:
            Span ID
        """
        import uuid
        span_id = str(uuid.uuid4())
        start_time = time.time()

        span = Span(
            span_id=span_id,
            parent_id=parent_id or self._current_span,
            operation=operation,
            start_time=start_time,
            end_time=None,
            status="ok",
            tags=tags or {}
        )

        with self._lock:
            self._spans[span_id] = span
            if parent_id is None:
                self._root_spans.append(span_id)
            self._current_span = span_id

        return span_id

    def end_span(
        self,
        span_id: str,
        status: str = "ok",
        tags: Optional[Dict[str, Any]] = None
    ) -> Optional[float]:
        """
        End a trace span.

        Args:
            span_id: Span ID
            status: Operation status
            tags: Optional additional tags

        Returns:
            Span duration in seconds
        """
        with self._lock:
            span = self._spans.get(span_id)
            if span is None:
                return None

            span.end_time = time.time()
            span.status = status
            if tags:
                span.tags.update(tags)

            if self._current_span == span_id:
                # Find parent to set as current
                self._current_span = span.parent_id

            return span.duration

    def get_span(self, span_id: str) -> Optional[Dict[str, Any]]:
        """Get span details"""
        with self._lock:
            span = self._spans.get(span_id)
            if span:
                return {
                    "span_id": span.span_id,
                    "parent_id": span.parent_id,
                    "operation": span.operation,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                    "duration": span.duration,
                    "status": span.status,
                    "tags": span.tags,
                    "logs": span.logs
                }
        return None

    def get_trace(self, span_id: str) -> List[Dict[str, Any]]:
        """
        Get full trace for a span.

        Args:
            span_id: Root span ID

        Returns:
            List of all spans in the trace
        """
        trace = []
        self._collect_trace(span_id, trace)
        return trace

    def _collect_trace(self, span_id: str, trace: List[Dict[str, Any]]) -> None:
        """Recursively collect trace spans"""
        span = self.get_span(span_id)
        if span:
            trace.append(span)
            # Find children
            for other_id, other_span in self._spans.items():
                if other_span.parent_id == span_id:
                    self._collect_trace(other_id, trace)

    def add_log(self, span_id: str, level: str, message: str, **kwargs) -> None:
        """Add a log entry to a span"""
        with self._lock:
            span = self._spans.get(span_id)
            if span:
                span.logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": level,
                    "message": message,
                    **kwargs
                })


class EventLogger:
    """
    Event logging system.

    Logs:
    - Agent lifecycle events
    - Task assignments
    - Errors and warnings
    - System state changes
    """

    def __init__(self, log_dir: str = "research_data/logs"):
        """
        Initialize event logger.

        Args:
            log_dir: Directory for log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._logs: List[LogEntry] = []
        self._session_logs: Dict[str, List[LogEntry]] = defaultdict(list)
        self._lock = threading.Lock()

    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> None:
        """
        Log an event.

        Args:
            level: Log level
            message: Log message
            context: Optional context data
            agent_id: Optional agent ID
            session_id: Optional session ID
        """
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            message=message,
            context=context or {},
            agent_id=agent_id,
            session_id=session_id
        )

        with self._lock:
            self._logs.append(entry)
            if session_id:
                self._session_logs[session_id].append(entry)

        # Also write to file if error or critical
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            self._write_to_file(entry)

    def _write_to_file(self, entry: LogEntry) -> None:
        """Write log entry to file"""
        log_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "timestamp": entry.timestamp,
                "level": entry.level.value,
                "message": entry.message,
                "context": entry.context,
                "agent_id": entry.agent_id,
                "session_id": entry.session_id
            }) + "\n")

    def get_logs(
        self,
        session_id: Optional[str] = None,
        level: Optional[LogLevel] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get log entries.

        Args:
            session_id: Filter by session ID
            level: Filter by log level
            limit: Maximum number of entries

        Returns:
            List of log entries
        """
        with self._lock:
            logs = self._session_logs.get(session_id, self._logs) if session_id else self._logs

            filtered = logs
            if level:
                filtered = [l for l in filtered if l.level == level]

            # Return most recent first
            result = [
                {
                    "timestamp": l.timestamp,
                    "level": l.level.value,
                    "message": l.message,
                    "context": l.context,
                    "agent_id": l.agent_id,
                    "session_id": l.session_id
                }
                for l in reversed(filtered[-limit:])
            ]

        return result

    def get_session_logs(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all logs for a session"""
        return self.get_logs(session_id=session_id, limit=10000)


class ObservabilityStack:
    """
    Complete observability stack.

    Integrates metrics, tracing, and logging.
    """

    def __init__(self, log_dir: str = "research_data/logs"):
        """
        Initialize observability stack.

        Args:
            log_dir: Directory for log files
        """
        self.metrics = MetricsCollector()
        self.tracer = Tracer()
        self.logger = EventLogger(log_dir)

    def record_agent_execution(
        self,
        agent_id: str,
        operation: str,
        execute_fn: Callable,
        **kwargs
    ) -> Any:
        """
        Record and execute an agent operation with full tracing.

        Args:
            agent_id: Agent ID
            operation: Operation name
            execute_fn: Function to execute
            **kwargs: Arguments to pass to execute_fn

        Returns:
            Result from execute_fn
        """
        # Start span
        span_id = self.tracer.start_span(
            operation,
            tags={"agent_id": agent_id}
        )

        self.logger.log(
            LogLevel.INFO,
            f"Starting: {operation}",
            context={"agent_id": agent_id},
            session_id=kwargs.get("session_id")
        )

        try:
            # Execute
            start_time = time.time()
            result = execute_fn(**kwargs)
            duration = time.time() - start_time

            # Record metrics
            self.metrics.record_histogram(
                f"agent.{agent_id}.duration",
                duration,
                labels={"operation": operation}
            )
            self.metrics.increment(
                f"agent.{agent_id}.calls",
                labels={"operation": operation, "status": "success"}
            )

            # End span
            self.tracer.end_span(span_id, status="ok", tags={
                "duration": duration,
                "tokens_used": getattr(result, "tokens_used", 0)
            })

            self.logger.log(
                LogLevel.INFO,
                f"Completed: {operation} in {duration:.2f}s",
                context={"agent_id": agent_id, "duration": duration},
                session_id=kwargs.get("session_id")
            )

            return result

        except Exception as e:
            duration = time.time() - start_time

            # Record error metrics
            self.metrics.increment(
                f"agent.{agent_id}.errors",
                labels={"operation": operation, "error_type": type(e).__name__}
            )

            # End span with error
            self.tracer.end_span(span_id, status="error", tags={
                "error": str(e),
                "error_type": type(e).__name__
            })

            self.logger.log(
                LogLevel.ERROR,
                f"Error in {operation}: {str(e)}",
                context={"agent_id": agent_id, "error": str(e)},
                session_id=kwargs.get("session_id")
            )

            raise

    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get data for monitoring dashboard.

        Returns:
            Dashboard data with metrics, traces, and logs
        """
        return {
            "metrics": self.metrics.get_all_metrics(),
            "recent_traces": [
                self.tracer.get_trace(span_id)
                for span_id in self.tracer._root_spans[-10:]
            ],
            "recent_errors": self.logger.get_logs(
                level=LogLevel.ERROR,
                limit=20
            ),
            "timestamp": datetime.now().isoformat()
        }

    def export_metrics(self, filepath: str) -> None:
        """Export metrics to JSON file"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics.get_all_metrics(),
            "traces": [
                self.tracer.get_trace(span_id)
                for span_id in self.tracer._root_spans
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)


# Singleton instance
_observability: Optional[ObservabilityStack] = None


def get_observability() -> ObservabilityStack:
    """Get the global observability stack instance"""
    global _observability
    if _observability is None:
        _observability = ObservabilityStack()
    return _observability


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Observability Stack v9.0")
    parser.add_argument("--metrics", action="store_true", help="Show current metrics")
    parser.add_argument("--export", type=str, help="Export metrics to file")
    parser.add_argument("--dashboard", action="store_true", help="Show dashboard data")
    parser.add_argument("--logs", type=str, help="Get logs for session ID")
    parser.add_argument("--reset", action="store_true", help="Reset all metrics")

    args = parser.parse_args()

    obs = get_observability()

    if args.metrics:
        print(json.dumps(obs.metrics.get_all_metrics(), indent=2))

    if args.export:
        obs.export_metrics(args.export)
        print(f"Metrics exported to {args.export}")

    if args.dashboard:
        print(json.dumps(obs.get_dashboard_data(), indent=2))

    if args.logs:
        logs = obs.logger.get_session_logs(args.logs)
        print(json.dumps(logs, indent=2))

    if args.reset:
        obs.metrics.reset()
        print("Metrics reset")

    if not any([args.metrics, args.export, args.dashboard, args.logs, args.reset]):
        print("Observability Stack v9.0")
        print("Use --metrics, --export, --dashboard, or --logs")
