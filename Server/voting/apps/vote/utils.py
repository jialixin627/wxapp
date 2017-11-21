from django.utils import timezone


def format_datetime(value, default=''):
    if value:
        return timezone.localtime(value).strftime('%y-%m-%d %H:%M')
    return default
