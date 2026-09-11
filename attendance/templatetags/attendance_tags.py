from django import template
from datetime import datetime

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by a separator."""
    return value.split(arg)

@register.filter
def calculate_duration(check_in_time, check_out_time):
    """Calculate the duration between check-in and check-out times."""
    if not check_in_time or not check_out_time:
        return "-"
    try:
        duration = check_out_time - check_in_time
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    except (TypeError, AttributeError):
        return "-"