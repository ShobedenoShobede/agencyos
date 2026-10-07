from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any


def _secret(group: str, key: str, default: Any = None) -> Any:
    env_key = f"{group.upper()}_{key.upper()}"
    try:
        import streamlit as st
        val = st.secrets.get(group, {}).get(key)
        if val is not None:
            return val
    except Exception:
        pass
    if os.environ.get(env_key) is not None:
        return os.environ[env_key]
    return default


@dataclass(frozen=True)
class GitHubSettings:
    token: str = ""
    webhook_secret: str = ""


@dataclass(frozen=True)
class PayPalSettings:
    client_id: str = ""
    client_secret: str = ""
    mode: str = "sandbox"

    @property
    def base_url(self) -> str:
        return (
            "https://api-m.paypal.com"
            if self.mode == "live"
            else "https://api-m.sandbox.paypal.com"
        )


@dataclass(frozen=True)
class AyrshareSettings:
    api_key: str = ""


@dataclass(frozen=True)
class NotificationSettings:
    slack_webhook: str = ""
    discord_webhook: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    from_addr: str = "agencyos@localhost"
    admin_email: str = ""


@dataclass(frozen=True)
class RuntimeSettings:
    rate_limit_per_hour: int = 2500
    audit_log_path: str = "data/audit.log"
    job_workers: int = 4
    job_max_retries: int = 3
    job_retry_base_seconds: float = 5.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_cooldown: int = 60
    health_check_timeout: float = 3.0


@dataclass(frozen=True)
class Settings:
    github: GitHubSettings = field(default_factory=GitHubSettings)
    paypal: PayPalSettings = field(default_factory=PayPalSettings)
    ayrshare: AyrshareSettings = field(default_factory=AyrshareSettings)
    notifications: NotificationSettings = field(default_factory=NotificationSettings)
    runtime: RuntimeSettings = field(default_factory=RuntimeSettings)
    environment: str = "development"
    version: str = "1.0.0"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        github=GitHubSettings(
            token=_secret("github", "token", ""),
            webhook_secret=_secret("github", "webhook_secret", ""),
        ),
        paypal=PayPalSettings(
            client_id=_secret("paypal", "client_id", ""),
            client_secret=_secret("paypal", "client_secret", ""),
            mode=_secret("paypal", "mode", "sandbox"),
        ),
        ayrshare=AyrshareSettings(
            api_key=_secret("ayrshare", "api_key", ""),
        ),
        notifications=NotificationSettings(
            slack_webhook=_secret("notifications", "slack_webhook", ""),
            discord_webhook=_secret("notifications", "discord_webhook", ""),
            smtp_host=_secret("notifications", "smtp_host", ""),
            smtp_port=int(_secret("notifications", "smtp_port", 587)),
            smtp_user=_secret("notifications", "smtp_user", ""),
            smtp_pass=_secret("notifications", "smtp_pass", ""),
            from_addr=_secret("notifications", "from_addr", "agencyos@localhost"),
            admin_email=_secret("notifications", "admin_email", ""),
        ),
        runtime=RuntimeSettings(
            rate_limit_per_hour=int(_secret("agencyos", "rate_limit_per_hour", 2500)),
            audit_log_path=_secret("agencyos", "audit_log_path", "data/audit.log"),
            job_workers=int(_secret("agencyos", "job_workers", 4)),
            job_max_retries=int(_secret("agencyos", "job_max_retries", 3)),
            job_retry_base_seconds=float(_secret("agencyos", "job_retry_base_seconds", 5.0)),
            circuit_breaker_threshold=int(_secret("agencyos", "circuit_breaker_threshold", 5)),
            circuit_breaker_cooldown=int(_secret("agencyos", "circuit_breaker_cooldown", 60)),
            health_check_timeout=float(_secret("agencyos", "health_check_timeout", 3.0)),
        ),
        environment=_secret("agencyos", "environment", os.environ.get("ENV", "development")),
        version=_secret("agencyos", "version", "1.0.0"),
    )
