from datetime import datetime, timedelta
from typing import List

# Make up a bunch of server options
OS_OPTIONS: List[str] = [
    "Ubuntu", "Ubuntu Server", "Unix", "Debian", "Red Hat", "Fedora", "Alpine"
]

APACHE_VERSIONS: List[str] = [
    "1.2.0", "1.2.1", "1.2.2", "1.3.0", "1.3.1", "1.3.10", "1.3.11", "1.3.12", "1.3.13", "1.3.14", "1.3.2", "1.3.3",
    "1.3.4", "1.3.5", "1.3.6", "1.3.7", "1.3.8", "1.3.9", "2.0.1", "2.0.10", "2.0.11", "2.0.12", "2.0.13", "2.0.14",
    "2.0.15", "2.0.16", "2.0.17", "2.0.18", "2.0.19", "2.0.2", "2.0.20", "2.0.21", "2.0.22", "2.0.23", "2.0.24",
    "2.0.25", "2.0.26", "2.0.27", "2.0.28", "2.0.29", "2.0.3", "2.0.30", "2.0.31", "2.0.32", "2.0.33", "2.0.34",
    "2.0.35", "2.0.36", "2.0.37", "2.0.38", "2.0.39", "2.0.4", "2.0.40", "2.0.41", "2.0.42", "2.0.43", "2.0.44",
    "2.0.45", "2.0.46", "2.0.47", "2.0.48", "2.0.49", "2.0.5", "2.0.50", "2.0.51", "2.0.52", "2.0.53", "2.0.54",
    "2.0.55", "2.0.56", "2.0.57", "2.0.58", "2.0.59", "2.0.6", "2.0.60", "2.0.61", "2.0.62", "2.0.63", "2.0.64",
    "2.0.65", "2.0.7", "2.0.8", "2.0.9", "2.1.1", "2.1.10", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7",
    "2.1.8", "2.1.9", "2.2.0", "2.2.1", "2.2.10", "2.2.11", "2.2.12", "2.2.13", "2.2.14", "2.2.15", "2.2.16", "2.2.17",
    "2.2.18", "2.2.19", "2.2.2", "2.2.20", "2.2.21", "2.2.22", "2.2.23", "2.2.24", "2.2.25", "2.2.26", "2.2.27",
    "2.2.28", "2.2.29", "2.2.3", "2.2.30", "2.2.31", "2.2.32", "2.2.33", "2.2.34", "2.2.4", "2.2.5", "2.2.6", "2.2.7",
    "2.2.8", "2.2.9", "2.3.0", "2.3.1", "2.3.10", "2.3.11", "2.3.12", "2.3.13", "2.3.14", "2.3.15", "2.3.16", "2.3.2",
    "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.3.8", "2.3.9", "2.4.0", "2.4.1", "2.4.10", "2.4.11", "2.4.12",
    "2.4.13", "2.4.14", "2.4.15", "2.4.16", "2.4.17", "2.4.18", "2.4.19", "2.4.2", "2.4.20", "2.4.21", "2.4.22",
    "2.4.23", "2.4.24", "2.4.25", "2.4.26", "2.4.27", "2.4.28", "2.4.29", "2.4.3", "2.4.30", "2.4.31", "2.4.32",
    "2.4.33", "2.4.34", "2.4.35", "2.4.36", "2.4.37", "2.4.38", "2.4.39", "2.4.4", "2.4.40", "2.4.41", "2.4.42",
    "2.4.43", "2.4.44", "2.4.45", "2.4.46", "2.4.47", "2.4.48", "2.4.49", "2.4.5", "2.4.50", "2.4.51", "2.4.52",
    "2.4.53", "2.4.54", "2.4.55", "2.4.56", "2.4.57", "2.4.58", "2.4.59", "2.4.6", "2.4.60", "2.4.61", "2.4.62",
    "2.4.7", "2.4.8", "2.4.9", "2.5.0"
]

IIS_VERSIONS = [
    "10.0", "8.5", "7.5", "6.0"
]

LIGHTTPD_VERSIONS = [
    "1.4.59", "1.4.58", "1.4.56"
]

NGINX_VERSIONS = [
    "1.18.0", "1.21.3", "1.22.0", "1.20.1 (Ubuntu)"
]

OTHER_SERVERS = [
    "Caddy/2.4.3", "Cherokee/1.2.104", "Hiawatha/10.11.0"
]

SERVER_OPTIONS = []

# Combine everything into a list to save CPU time during bot interation
for os_option in OS_OPTIONS:
    SERVER_OPTIONS.extend(f"Apache/{version} ({os_option})" for version in APACHE_VERSIONS)

SERVER_OPTIONS.extend(f"nginx/{version}" for version in NGINX_VERSIONS)
SERVER_OPTIONS.extend(f"Microsoft-IIS/{version}" for version in IIS_VERSIONS)
SERVER_OPTIONS.extend(f"lighttpd/{version}" for version in LIGHTTPD_VERSIONS)
SERVER_OPTIONS.extend(OTHER_SERVERS)


def now() -> str:
    """
    Get the current time as a string for logging.
    :return: Current time string.
    """
    return datetime.now().__str__()


def log(message: str) -> None:
    print(f"[{now()[:-7]}] {message}")


def time_format(start: float, end: float) -> str:
    time_diff = timedelta(seconds=(end - start))
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    seconds = (end - start) % 60

    result = ""
    if days == 1:
        result += "1 day, "
    elif days > 1:
        result += f"{days} days, "

    if hours == 1:
        result += "1 hour, "
    elif hours > 1:
        result += f"{hours} hours, "

    if minutes == 1:
        result += "1 minute, "
    elif minutes > 1:
        result += f"{minutes} minutes, "

    result += f"{seconds:.4f} seconds"
    return result
