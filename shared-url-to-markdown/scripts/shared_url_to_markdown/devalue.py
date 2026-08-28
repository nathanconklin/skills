from __future__ import annotations

import math
from typing import Any


class DevalueError(ValueError):
    pass


def unflatten(values: list[Any], root_reference: int = 0) -> Any:
    """Hydrate the reference-array format emitted by Remix/devalue."""

    if not isinstance(values, list) or not values:
        raise DevalueError("Expected a non-empty devalue reference array")

    memo: dict[int, Any] = {}

    def hydrate(reference: Any) -> Any:
        if not isinstance(reference, int) or isinstance(reference, bool):
            return reference
        if reference < 0:
            return _special(reference)
        if reference >= len(values):
            raise DevalueError(f"Reference {reference} is outside the value table")
        if reference in memo:
            return memo[reference]

        value = values[reference]
        if isinstance(value, dict):
            result: dict[str, Any] = {}
            memo[reference] = result
            for encoded_key, item_reference in value.items():
                if not isinstance(encoded_key, str) or not encoded_key.startswith("_"):
                    key = encoded_key
                else:
                    try:
                        key = hydrate(int(encoded_key[1:]))
                    except (ValueError, TypeError) as exc:
                        raise DevalueError(f"Invalid encoded key: {encoded_key}") from exc
                result[str(key)] = hydrate(item_reference)
            return result

        if isinstance(value, list):
            if value and isinstance(value[0], str):
                # Tagged values can participate in cycles (notably Remix promise
                # placeholders). Reserve the reference before hydrating children.
                memo[reference] = None
                result = _hydrate_tagged(value, hydrate)
                memo[reference] = result
                return result
            result_list: list[Any] = []
            memo[reference] = result_list
            result_list.extend(hydrate(item) for item in value)
            return result_list

        memo[reference] = value
        return value

    return hydrate(root_reference)


def _special(reference: int) -> Any:
    if reference in {-1, -2}:
        return None
    if reference == -3:
        return math.nan
    if reference == -4:
        return math.inf
    if reference == -5:
        return -math.inf
    if reference == -6:
        return -0.0
    return None


def _hydrate_tagged(value: list[Any], hydrate) -> Any:
    tag = value[0]
    if tag in {"Date", "BigInt", "URL", "P"}:
        return hydrate(value[1]) if len(value) > 1 else None
    if tag == "Set":
        return [hydrate(item) for item in value[1:]]
    if tag == "Map":
        return {
            str(hydrate(value[index])): hydrate(value[index + 1])
            for index in range(1, len(value) - 1, 2)
        }
    if tag == "RegExp":
        return hydrate(value[1]) if len(value) > 1 else ""
    if tag in {"null", "Object"}:
        result: dict[str, Any] = {}
        for index in range(1, len(value) - 1, 2):
            result[str(hydrate(value[index]))] = hydrate(value[index + 1])
        return result
    return [tag, *(hydrate(item) for item in value[1:])]
