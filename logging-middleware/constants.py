ALLOWED_STACKS = ["backend", "frontend"]
ALLOWED_LEVELS = ["debug", "info", "warn", "error", "fatal"]
ALLOWED_BACKEND_PACKAGES = [
    "cache", "controller", "cron_job", "db",
    "domain", "handler", "repository", "route", "service"
]
ALLOWED_SHARED_PACKAGES = ["auth", "config", "middleware", "utils"]
ALLOWED_PACKAGES = ALLOWED_BACKEND_PACKAGES + ALLOWED_SHARED_PACKAGES
