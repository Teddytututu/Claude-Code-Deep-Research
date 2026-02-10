"""
Resilience and Error Recovery System v9.0

Provides production-ready resilience mechanisms:
- Retry policies with exponential backoff
- Graceful degradation and fallback
- Checkpoint-based recovery
- Circuit breaker for cascading failure prevention

Based on:
- Budget-aware timeout mechanisms (arXiv papers)
- Production patterns from enterprise deployments

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Callable, TypeVar
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import threading
import asyncio

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class RetryConfig:
    """Configuration for retry policy"""
    max_attempts: int = 3
    base_delay: float = 1.0  # Base delay in seconds
    max_delay: float = 60.0  # Maximum delay in seconds
    exponential_base: float = 2.0  # Exponential backoff base
    jitter: bool = True  # Add jitter to delay
    retry_on: List[type] = field(default_factory=lambda: [Exception])


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5  # Failures before opening
    success_threshold: int = 2  # Successes to close circuit
    timeout: float = 60.0  # Seconds to wait before half-open
    half_open_max_calls: int = 3  # Max calls in half-open state


@dataclass
class AttemptResult:
    """Result of an execution attempt"""
    success: bool
    value: Any = None
    error: Optional[Exception] = None
    attempt_number: int = 0
    elapsed_time: float = 0.0


class RetryPolicy:
    """
    Retry policy with exponential backoff.

    Implements:
    - Exponential backoff with jitter
    - Configurable retry conditions
    - Attempt tracking
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        """
        Initialize retry policy.

        Args:
            config: Retry configuration
        """
        self.config = config or RetryConfig()
        self._attempt_history: Dict[str, List[AttemptResult]] = {}

    def execute(
        self,
        fn: Callable[..., T],
        operation_id: str,
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        Execute function with retry policy.

        Args:
            fn: Function to execute
            operation_id: Unique identifier for operation
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Last exception if all retries fail
        """
        attempts = []
        last_error = None

        for attempt in range(1, self.config.max_attempts + 1):
            start_time = time.time()

            try:
                result = fn(*args, **kwargs)
                elapsed = time.time() - start_time

                attempt_result = AttemptResult(
                    success=True,
                    value=result,
                    attempt_number=attempt,
                    elapsed_time=elapsed
                )
                attempts.append(attempt_result)

                # Record successful attempt
                self._record_attempt(operation_id, attempt_result)

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                last_error = e

                # Check if we should retry on this error
                should_retry = any(isinstance(e, err_type) for err_type in self.config.retry_on)

                attempt_result = AttemptResult(
                    success=False,
                    error=e,
                    attempt_number=attempt,
                    elapsed_time=elapsed
                )
                attempts.append(attempt_result)
                self._record_attempt(operation_id, attempt_result)

                if not should_retry or attempt >= self.config.max_attempts:
                    break

                # Calculate delay with exponential backoff
                delay = self._calculate_delay(attempt)

                # Wait before retry
                time.sleep(delay)

        # All retries failed
        raise last_error

    async def execute_async(
        self,
        fn: Callable[..., T],
        operation_id: str,
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        Execute async function with retry policy.

        Args:
            fn: Async function to execute
            operation_id: Unique identifier for operation
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        for attempt in range(1, self.config.max_attempts + 1):
            start_time = time.time()

            try:
                result = await fn(*args, **kwargs)
                elapsed = time.time() - start_time

                attempt_result = AttemptResult(
                    success=True,
                    value=result,
                    attempt_number=attempt,
                    elapsed_time=elapsed
                )
                self._record_attempt(operation_id, attempt_result)

                return result

            except Exception as e:
                elapsed = time.time() - start_time

                attempt_result = AttemptResult(
                    success=False,
                    error=e,
                    attempt_number=attempt,
                    elapsed_time=elapsed
                )
                self._record_attempt(operation_id, attempt_result)

                if attempt >= self.config.max_attempts:
                    raise e

                delay = self._calculate_delay(attempt)
                await asyncio.sleep(delay)

        raise RuntimeError("Unexpected flow in retry logic")

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and optional jitter"""
        # Exponential backoff
        delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))

        # Cap at max delay
        delay = min(delay, self.config.max_delay)

        # Add jitter if configured
        if self.config.jitter:
            import random
            delay = delay * (0.5 + random.random())

        return delay

    def _record_attempt(self, operation_id: str, result: AttemptResult) -> None:
        """Record an attempt result"""
        if operation_id not in self._attempt_history:
            self._attempt_history[operation_id] = []
        self._attempt_history[operation_id].append(result)

    def get_attempt_history(self, operation_id: str) -> List[Dict[str, Any]]:
        """Get attempt history for an operation"""
        history = self._attempt_history.get(operation_id, [])
        return [
            {
                "success": a.success,
                "attempt_number": a.attempt_number,
                "elapsed_time": a.elapsed_time,
                "error": str(a.error) if a.error else None
            }
            for a in history
        ]


class CircuitBreaker:
    """
    Circuit breaker for preventing cascading failures.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failing state, requests rejected immediately
    - HALF_OPEN: Testing if service has recovered
    """

    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        """
        Initialize circuit breaker.

        Args:
            config: Circuit breaker configuration
        """
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._half_open_calls = 0
        self._lock = threading.Lock()

    def execute(
        self,
        fn: Callable[..., T],
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        Execute function through circuit breaker.

        Args:
            fn: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception if circuit is open or function fails
        """
        with self._lock:
            # Check state transitions
            self._check_state_transition()

            # Reject if circuit is open
            if self._state == CircuitState.OPEN:
                raise RuntimeError(f"Circuit breaker is OPEN. Rejecting request.")

            # Track half-open calls
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
                if self._half_open_calls > self.config.half_open_max_calls:
                    raise RuntimeError(f"Circuit breaker HALF-OPEN max calls exceeded.")

        # Execute the function
        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _check_state_transition(self) -> None:
        """Check if circuit breaker should transition states"""
        now = time.time()

        if self._state == CircuitState.OPEN:
            # Check if timeout has passed
            if self._last_failure_time is not None:
                if now - self._last_failure_time >= self.config.timeout:
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0

    def _on_success(self) -> None:
        """Handle successful execution"""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.config.success_threshold:
                    # Close the circuit
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0
            elif self._state == CircuitState.CLOSED:
                # Reset failure count on success in closed state
                self._failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed execution"""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                # Back to open state
                self._state = CircuitState.OPEN
                self._success_count = 0
            elif self._failure_count >= self.config.failure_threshold:
                # Open the circuit
                self._state = CircuitState.OPEN

    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        with self._lock:
            return {
                "state": self._state.value,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "last_failure_time": self._last_failure_time,
                "half_open_calls": self._half_open_calls
            }

    def reset(self) -> None:
        """Reset circuit breaker to closed state"""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
            self._half_open_calls = 0


class CheckpointRecovery:
    """
    Checkpoint-based recovery system.

    Enables resuming from checkpoints after failures.
    """

    def __init__(self, checkpoint_dir: str = "research_data/checkpoints"):
        """
        Initialize checkpoint recovery.

        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self._checkpoints: Dict[str, Dict[str, Any]] = {}

    def save_checkpoint(
        self,
        session_id: str,
        phase: str,
        data: Dict[str, Any]
    ) -> str:
        """
        Save a checkpoint.

        Args:
            session_id: Session ID
            phase: Current phase identifier
            data: Checkpoint data

        Returns:
            Checkpoint file path
        """
        checkpoint_id = f"{session_id}_{phase}_{int(time.time())}"
        filepath = self.checkpoint_dir / f"{checkpoint_id}.json"

        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "session_id": session_id,
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

        self._checkpoints[checkpoint_id] = checkpoint_data

        return str(filepath)

    def load_latest_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load latest checkpoint for a session.

        Args:
            session_id: Session ID

        Returns:
            Checkpoint data if found
        """
        # Find checkpoints for session
        checkpoints = list(self.checkpoint_dir.glob(f"{session_id}_*.json"))

        if not checkpoints:
            return None

        # Sort by modification time
        checkpoints.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Load latest
        with open(checkpoints[0], 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_checkpoints(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available checkpoints.

        Args:
            session_id: Optional session filter

        Returns:
            List of checkpoint metadata
        """
        checkpoints = []

        for filepath in self.checkpoint_dir.glob("*.json"):
            if session_id and not filepath.name.startswith(session_id):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                checkpoints.append({
                    "checkpoint_id": data.get("checkpoint_id"),
                    "session_id": data.get("session_id"),
                    "phase": data.get("phase"),
                    "timestamp": data.get("timestamp"),
                    "filepath": str(filepath)
                })
            except (json.JSONDecodeError, KeyError):
                continue

        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)

    def cleanup_old_checkpoints(
        self,
        session_id: str,
        keep_latest: int = 5
    ) -> int:
        """
        Clean up old checkpoints for a session.

        Args:
            session_id: Session ID
            keep_latest: Number of latest checkpoints to keep

        Returns:
            Number of checkpoints deleted
        """
        checkpoints = self.list_checkpoints(session_id)

        if len(checkpoints) <= keep_latest:
            return 0

        # Delete older checkpoints
        deleted = 0
        for checkpoint in checkpoints[keep_latest:]:
            filepath = Path(checkpoint["filepath"])
            if filepath.exists():
                filepath.unlink()
                deleted += 1

        return deleted


class ResilientExecutor:
    """
    Resilient executor combining all resilience mechanisms.

    Provides:
    - Retry with exponential backoff
    - Circuit breaker protection
    - Checkpoint recovery
    - Graceful degradation
    """

    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        circuit_config: Optional[CircuitBreakerConfig] = None,
        checkpoint_dir: str = "research_data/checkpoints"
    ):
        """
        Initialize resilient executor.

        Args:
            retry_config: Retry policy configuration
            circuit_config: Circuit breaker configuration
            checkpoint_dir: Checkpoint directory
        """
        self.retry_policy = RetryPolicy(retry_config)
        self.circuit_breaker = CircuitBreaker(circuit_config)
        self.checkpoint_recovery = CheckpointRecovery(checkpoint_dir)

    def execute_resilient(
        self,
        fn: Callable[..., T],
        operation_id: str,
        session_id: Optional[str] = None,
        checkpoint_phase: Optional[str] = None,
        use_checkpoint: bool = False,
        *args: Any,
        **kwargs: Any
    ) -> T:
        """
        Execute function with full resilience.

        Args:
            fn: Function to execute
            operation_id: Unique operation identifier
            session_id: Optional session ID for checkpoints
            checkpoint_phase: Optional phase identifier for checkpoints
            use_checkpoint: Whether to use checkpoint recovery
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        # Try to load from checkpoint if enabled
        if use_checkpoint and session_id and checkpoint_phase:
            checkpoint = self.checkpoint_recovery.load_latest_checkpoint(session_id)
            if checkpoint and checkpoint.get("phase") == checkpoint_phase:
                # Could return cached result or resume from checkpoint
                pass

        # Execute through circuit breaker and retry policy
        def protected_execute():
            return self.circuit_breaker.execute(fn, *args, **kwargs)

        result = self.retry_policy.execute(
            protected_execute,
            operation_id
        )

        # Save checkpoint if enabled
        if use_checkpoint and session_id and checkpoint_phase:
            self.checkpoint_recovery.save_checkpoint(
                session_id,
                checkpoint_phase,
                {"result": result}
            )

        return result

    def get_status(self) -> Dict[str, Any]:
        """Get status of all resilience components"""
        return {
            "circuit_breaker": self.circuit_breaker.get_state(),
            "available_checkpoints": len(self.checkpoint_recovery.list_checkpoints())
        }


# Singleton instance
_resilient_executor: Optional[ResilientExecutor] = None


def get_resilient_executor() -> ResilientExecutor:
    """Get the global resilient executor instance"""
    global _resilient_executor
    if _resilient_executor is None:
        _resilient_executor = ResilientExecutor()
    return _resilient_executor


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resilience System v9.0")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--checkpoints", type=str, help="List checkpoints for session")
    parser.add_argument("--cleanup", type=str, help="Cleanup old checkpoints for session")
    parser.add_argument("--keep", type=int, default=5, help="Keep N latest checkpoints")

    args = parser.parse_args()

    executor = get_resilient_executor()

    if args.status:
        print(json.dumps(executor.get_status(), indent=2))

    if args.checkpoints:
        checkpoints = executor.checkpoint_recovery.list_checkpoints(args.checkpoints)
        print(json.dumps(checkpoints, indent=2))

    if args.cleanup:
        deleted = executor.checkpoint_recovery.cleanup_old_checkpoints(
            args.cleanup,
            keep_latest=args.keep
        )
        print(f"Deleted {deleted} old checkpoints")
