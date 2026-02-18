"""
Rate Limiter Module v10.0
速率限制器模块

Implements async-compatible rate limiting for API calls.
Based on aiolimiter for efficient token bucket algorithm.

Features:
- Async context manager support
- Configurable rate and burst capacity
- Decorator for automatic rate limiting
- Integration with anyio for cross-library compatibility

Author: Deep Research System
Date: 2026-02-18
"""

from typing import Optional, Callable, TypeVar, ParamSpec
from functools import wraps
import asyncio
import time

# Optional imports
try:
    from aiolimiter import AsyncLimiter
    AIOLIMITER_AVAILABLE = True
except ImportError:
    AIOLIMITER_AVAILABLE = False

try:
    import anyio
    ANYIO_AVAILABLE = True
except ImportError:
    ANYIO_AVAILABLE = False


P = ParamSpec('P')
T = TypeVar('T')


class RateLimiter:
    """
    Async rate limiter using token bucket algorithm.

    Supports both aiolimiter (preferred) and a simple fallback implementation.

    Usage:
        # Basic usage
        limiter = RateLimiter(rate=10)  # 10 requests per second

        async with limiter:
            response = await api_call()

        # As decorator
        @rate_limit(rate=5)
        async def my_api_call():
            ...
    """

    def __init__(
        self,
        rate: float = 10.0,
        period: float = 1.0,
        burst: Optional[int] = None
    ):
        """
        Initialize rate limiter.

        Args:
            rate: Number of requests allowed per period
            period: Time period in seconds (default 1.0)
            burst: Maximum burst capacity (defaults to rate)
        """
        self.rate = rate
        self.period = period
        self.burst = burst or int(rate)

        if AIOLIMITER_AVAILABLE:
            self._limiter = AsyncLimiter(rate, period)
        else:
            self._limiter = SimpleRateLimiter(rate, period, self.burst)

    async def __aenter__(self):
        """Acquire rate limit slot."""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release rate limit slot (no-op for token bucket)."""
        return False

    async def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a rate limit slot.

        Args:
            timeout: Maximum time to wait (None = infinite)

        Returns:
            True if acquired, False if timeout
        """
        if timeout is not None:
            try:
                if ANYIO_AVAILABLE:
                    with anyio.fail_after(timeout):
                        await self._limiter.acquire()
                else:
                    await asyncio.wait_for(
                        self._limiter.acquire(),
                        timeout=timeout
                    )
                return True
            except (TimeoutError, asyncio.TimeoutError):
                return False
        else:
            await self._limiter.acquire()
            return True

    def reset(self) -> None:
        """Reset the rate limiter state."""
        if hasattr(self._limiter, 'reset'):
            self._limiter.reset()


class SimpleRateLimiter:
    """
    Simple fallback rate limiter when aiolimiter is not available.

    Uses basic token bucket algorithm with asyncio sleep.
    """

    def __init__(self, rate: float, period: float, burst: int):
        self.rate = rate
        self.period = period
        self.burst = burst
        self._tokens = float(burst)
        self._last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_update

            # Replenish tokens
            self._tokens = min(
                self.burst,
                self._tokens + elapsed * (self.rate / self.period)
            )
            self._last_update = now

            if self._tokens < 1:
                # Wait for token
                wait_time = (1 - self._tokens) * (self.period / self.rate)
                await asyncio.sleep(wait_time)
                self._tokens = 0
            else:
                self._tokens -= 1

    def reset(self) -> None:
        """Reset tokens to burst capacity."""
        self._tokens = float(self.burst)
        self._last_update = time.monotonic()


class MultiRateLimiter:
    """
    Rate limiter supporting multiple API endpoints with different limits.

    Useful for services with different rate limits per endpoint.

    Usage:
        limiter = MultiRateLimiter()
        limiter.add_limit("search", rate=10)
        limiter.add_limit("download", rate=5)

        async with limiter.limit("search"):
            results = await search_api()
    """

    def __init__(self):
        """Initialize multi-rate limiter."""
        self._limiters: dict[str, RateLimiter] = {}

    def add_limit(
        self,
        name: str,
        rate: float = 10.0,
        period: float = 1.0,
        burst: Optional[int] = None
    ) -> None:
        """
        Add a rate limit for a named endpoint.

        Args:
            name: Endpoint name
            rate: Requests per period
            period: Time period in seconds
            burst: Maximum burst capacity
        """
        self._limiters[name] = RateLimiter(rate, period, burst)

    def limit(self, name: str) -> RateLimiter:
        """
        Get rate limiter for a named endpoint.

        Args:
            name: Endpoint name

        Returns:
            RateLimiter instance
        """
        if name not in self._limiters:
            # Create default limiter
            self._limiters[name] = RateLimiter()
        return self._limiters[name]

    async def acquire(self, name: str, timeout: Optional[float] = None) -> bool:
        """
        Acquire rate limit slot for a named endpoint.

        Args:
            name: Endpoint name
            timeout: Maximum wait time

        Returns:
            True if acquired, False if timeout
        """
        return await self.limit(name).acquire(timeout)

    def get_stats(self) -> dict:
        """Get statistics for all rate limiters."""
        return {
            name: {
                "rate": limiter.rate,
                "period": limiter.period,
                "burst": limiter.burst
            }
            for name, limiter in self._limiters.items()
        }


def rate_limit(
    rate: float = 10.0,
    period: float = 1.0,
    burst: Optional[int] = None,
    limiter: Optional[RateLimiter] = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator for rate limiting async functions.

    Args:
        rate: Requests per period
        period: Time period in seconds
        burst: Maximum burst capacity
        limiter: Existing RateLimiter instance (optional)

    Returns:
        Decorated function

    Usage:
        @rate_limit(rate=5)
        async def my_api_call():
            return await fetch_data()

        # Or with shared limiter
        shared_limiter = RateLimiter(rate=10)

        @rate_limit(limiter=shared_limiter)
        async def another_call():
            return await fetch_more()
    """
    _limiter = limiter or RateLimiter(rate, period, burst)

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            async with _limiter:
                return await func(*args, **kwargs)
        return wrapper

    return decorator


class AdaptiveRateLimiter(RateLimiter):
    """
    Rate limiter that adapts based on API response times and errors.

    Automatically reduces rate on errors and increases on success.
    """

    def __init__(
        self,
        initial_rate: float = 10.0,
        min_rate: float = 1.0,
        max_rate: float = 50.0,
        period: float = 1.0
    ):
        """
        Initialize adaptive rate limiter.

        Args:
            initial_rate: Starting rate
            min_rate: Minimum rate (floor)
            max_rate: Maximum rate (ceiling)
            period: Time period in seconds
        """
        super().__init__(initial_rate, period)
        self.min_rate = min_rate
        self.max_rate = max_rate
        self._consecutive_successes = 0
        self._consecutive_errors = 0

    def on_success(self) -> None:
        """
        Call on successful API response.

        Gradually increases rate after consecutive successes.
        """
        self._consecutive_successes += 1
        self._consecutive_errors = 0

        # Increase rate after 5 consecutive successes
        if self._consecutive_successes >= 5:
            self.rate = min(self.max_rate, self.rate * 1.1)
            self._consecutive_successes = 0

            # Update underlying limiter
            if AIOLIMITER_AVAILABLE:
                self._limiter = AsyncLimiter(self.rate, self.period)

    def on_error(self, is_rate_limit_error: bool = True) -> None:
        """
        Call on API error.

        Args:
            is_rate_limit_error: Whether this was a rate limit error (429)
        """
        self._consecutive_errors += 1
        self._consecutive_successes = 0

        # Reduce rate on errors
        reduction_factor = 0.5 if is_rate_limit_error else 0.8
        self.rate = max(self.min_rate, self.rate * reduction_factor)

        # Update underlying limiter
        if AIOLIMITER_AVAILABLE:
            self._limiter = AsyncLimiter(self.rate, self.period)

    async def safe_execute(
        self,
        func: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:
        """
        Execute function with automatic rate adaptation.

        Args:
            func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If function fails (after rate adaptation)
        """
        async with self:
            try:
                result = await func(*args, **kwargs)
                self.on_success()
                return result
            except Exception as e:
                # Check if it's a rate limit error
                error_str = str(e).lower()
                is_rate_limit = '429' in error_str or 'rate limit' in error_str
                self.on_error(is_rate_limit)
                raise


# Global default rate limiter
_default_limiter: Optional[RateLimiter] = None


def get_default_limiter() -> RateLimiter:
    """Get or create the global default rate limiter."""
    global _default_limiter
    if _default_limiter is None:
        _default_limiter = RateLimiter()
    return _default_limiter


def set_default_limiter(limiter: RateLimiter) -> None:
    """Set the global default rate limiter."""
    global _default_limiter
    _default_limiter = limiter


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rate Limiter Module")
    parser.add_argument("--test", action="store_true", help="Run rate limiter test")
    parser.add_argument("--rate", type=float, default=5.0, help="Requests per second")
    parser.add_argument("--count", type=int, default=20, help="Number of test requests")

    args = parser.parse_args()

    if args.test:
        print(f"Testing Rate Limiter ({args.rate} req/s, {args.count} requests)")

        limiter = RateLimiter(rate=args.rate)
        start_time = time.time()

        async def test_request(n: int) -> float:
            async with limiter:
                elapsed = time.time() - start_time
                print(f"  Request {n:2d}: {elapsed:.3f}s")
                return elapsed

        async def run_test():
            tasks = [test_request(i) for i in range(args.count)]
            await asyncio.gather(*tasks)

            total_time = time.time() - start_time
            actual_rate = args.count / total_time
            print(f"\nResults:")
            print(f"  Total time: {total_time:.2f}s")
            print(f"  Actual rate: {actual_rate:.2f} req/s")
            print(f"  Expected time: {args.count / args.rate:.2f}s")

        asyncio.run(run_test())

    else:
        parser.print_help()
