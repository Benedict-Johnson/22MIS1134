from .constants import ALLOWED_STACKS, ALLOWED_LEVELS, ALLOWED_PACKAGES


def validate_log_params(stack: str, level: str, package_name: str, message: str) -> tuple[bool, str | None]:
    if not stack or not isinstance(stack, str):
        return False, "Stack is required and must be a string"
    if not level or not isinstance(level, str):
        return False, "Level is required and must be a string"
    if not package_name or not isinstance(package_name, str):
        return False, "PackageName is required and must be a string"
    if not message or not isinstance(message, str):
        return False, "Message is required and must be a string"

    if stack not in ALLOWED_STACKS:
        return False, f"Invalid stack. Allowed: {', '.join(ALLOWED_STACKS)}"
    if level not in ALLOWED_LEVELS:
        return False, f"Invalid level. Allowed: {', '.join(ALLOWED_LEVELS)}"
    if package_name not in ALLOWED_PACKAGES:
        return False, f"Invalid package. Allowed: {', '.join(ALLOWED_PACKAGES)}"

    return True, None
