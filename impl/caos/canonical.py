"""The one canonical JSON form used by every digest in the system.

A digest is only comparable with another digest if both were computed over
the same bytes. Two canonical forms in one implementation would make a digest
computed in the Ledger and a digest computed in the model incomparable, and
the comparison would fail silently rather than loudly.

The rules are the ones the platform architecture specification fixes:

- keys are ordered by Unicode code point, ascending, applied recursively;
- no whitespace between tokens;
- JSON minimal escaping, with all other characters emitted literally as UTF-8;
- no trailing newline;
- non-finite numbers are refused, because ``NaN`` and ``Infinity`` are not
  valid JSON and a digest over them would not be reproducible.
"""

from __future__ import annotations

import json
from typing import Any

__all__ = ["canonical_json", "canonical_bytes"]


def _reject_non_serialisable(value: Any) -> Any:
    raise TypeError(
        f"value of type {type(value).__name__!r} is not serialisable; "
        "the canonical form must be exact"
    )


def canonical_json(payload: Any) -> str:
    """Return the canonical JSON string for ``payload``."""
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=_reject_non_serialisable,
    )


def canonical_bytes(payload: Any) -> bytes:
    """Return the canonical UTF-8 bytes for ``payload``."""
    return canonical_json(payload).encode("utf-8")
