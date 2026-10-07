from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .settings import get_settings


class ValidationError(RuntimeError):
    pass


@dataclass
class ValidationReport:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


REQUIRED_PATHS = ("data", ".streamlit")

REQUIRED_SECRETS: list[tuple[str, tuple[str, ...]]] = [
    ("github", ("token",)),
]

SOFT_SECRETS: list[tuple[str, tuple[str, ...]]] = [
    ("paypal", ("client_id", "client_secret")),
    ("ayrshare", ("api_key",)),
]


def _check_paths() -> Iterable[str]:
    for path in REQUIRED_PATHS:
        if not Path(path).exists():
            yield f"required path missing: {path}"


def _check_hard_secrets() -> Iterable[str]:
    s = get_settings()
    for group, keys in REQUIRED_SECRETS:
        section = getattr(s, group, None)
        if section is None:
            continue
        for key in keys:
            if not getattr(section, key, None):
                yield f"missing required secret: {group}.{key}"


def _check_soft_secrets() -> Iterable[str]:
    s = get_settings()
    for group, keys in SOFT_SECRETS:
        section = getattr(s, group, None)
        if section is None:
            continue
        missing = [k for k in keys if not getattr(section, k, None)]
        if missing:
            yield f"integration not configured: {group} ({', '.join(missing)})"


def _check_webhook_secret() -> Iterable[str]:
    s = get_settings()
    if s.github.token and not s.github.webhook_secret:
        yield "github.webhook_secret not set — webhooks will reject all deliveries"


def validate_startup(*, strict: bool = False) -> ValidationReport:
    errors: list[str] = []
    errors.extend(_check_paths())
    errors.extend(_check_hard_secrets())
    errors.extend(_check_webhook_secret())

    warnings: list[str] = list(_check_soft_secrets())

    report = ValidationReport(errors=errors, warnings=warnings)
    if strict and not report.ok:
        raise ValidationError(
            "startup validation failed:\n  - " + "\n  - ".join(errors)
        )
    return report
