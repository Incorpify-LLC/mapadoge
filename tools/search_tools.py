import time
import random
from crewai.tools import tool
from ddgs import DDGS

_MAX_RETRIES = 3
_BASE_DELAY = 2.0

def _ddgs_search_with_retry(search_fn, query, max_results):
    """Execute a DDGS search with exponential backoff and jitter to handle 403 rate limits."""
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            # Small random delay to avoid burst patterns
            if attempt > 1:
                delay = _BASE_DELAY * (2 ** (attempt - 1)) + random.uniform(0, 1)
                time.sleep(delay)
            with DDGS() as ddgs:
                results = list(search_fn(ddgs, query, max_results))
                if results:
                    return results
                return []
        except Exception as e:
            err_str = str(e).lower()
            if "403" in err_str or "ratelimit" in err_str or "rate limit" in err_str:
                if attempt == _MAX_RETRIES:
                    return None  # Signal rate-limit exhaustion
                continue
            # Non-retryable error
            return None
    return None

@tool("internet_search")
def internet_search(query: str):
    """Searches the internet for technical documentation and whitepapers.
    If results are found, returns a synthesis of sources.
    If no results are found or rate limited, explicitly states the issue
    to trigger internal knowledge fallback."""
    results = _ddgs_search_with_retry(lambda d, q, mr: d.text(q, max_results=mr), query, 10)
    if results is None:
        return ("Search Error: Rate limited by search provider. "
                "Please rely on your internal expert knowledge for this technical topic.")
    if results:
        return "\n\n".join([f"Source: {r[href]}\nContent: {r[body]}" for r in results])
    return ("No results found. Please use your internal expert training data "
            "to provide detailed technical content on this standard protocol.")
