from __future__ import unicode_literals
from datetime import datetime


# Accepted input formats
_PARSE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d",
]


def _parse_dt(value):
    """
    Try to parse various DB date/datetime strings into a datetime.
    Returns a datetime on success, or None on failure.
    - Accepts None/"" and datetime inputs.
    - Uses dateutil.parser.parse if available; otherwise tries known formats.
    """
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value

    # Try python-dateutil if present (handles lots of cases)
    try:
        from dateutil import parser as _du_parser  # optional dependency
        try:
            return _du_parser.parse(value)
        except Exception:
            pass
    except Exception:
        pass

    # Fallback: try known formats
    for fmt in _PARSE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def format_date(date_from_db):
    dt = _parse_dt(date_from_db)
    return dt.strftime("%d/%m/%Y") if dt else ""


def format_datetime(date_from_db):
    dt = _parse_dt(date_from_db)
    return dt.strftime("%d/%m/%Y %H:%M:%S") if dt else ""


def format_datetime_short(date_from_db):
    dt = _parse_dt(date_from_db)
    return dt.strftime("%d/%m/%Y %H:%M") if dt else ""


def format_datetime_for_gantt(date_from_db):
	return system.date.parse(date_from_db.replace("T", " "), "yyyy-MM-dd HH:mm:ss")


def format_datetime_for_db(ignition_datetime):
	if ignition_datetime not in ["", None]:
		return datetime.fromtimestamp(ignition_datetime.getTime()/1000.0).isoformat()
	else:
		return None


def format_datetime_header(ignition_datetime):
	return system.date.format(ignition_datetime, "dd/MM/yy - HH:mm:ss")


def get_date_week_from_db(date_from_db):
    """
    ISO-8601 week number (Monday=week start), which is standard in EU.
    Replaces %U + 1 (Sunday-based weeks) for correctness.
    """
    dt = _parse_dt(date_from_db)
    return dt.isocalendar()[1] if dt else ""


def get_date_year_from_db(date_from_db):
    dt = _parse_dt(date_from_db)
    return dt.year if dt else ""


def duration_to_datetime(base_duration):
	try:
		hours_float = float(base_duration)
	except:
		hours_float = base_duration

	# Calculate total minutes
	total_minutes = hours_float * 60

	# Calculate days, hours, and minutes
	days = int(total_minutes // (24 * 60))
	total_minutes %= (24 * 60)
	hours = int(total_minutes // 60)
	minutes = int(total_minutes % 60)

	# Return formatted string
	return "{days:02d}j{hours:02d}h{minutes:02d}min".format(days=days, hours=hours, minutes=minutes) if days > 0 else "{hours:02d}h{minutes:02d}min".format(hours=hours, minutes=minutes)


def duration_to_datetime_short(base_duration):
	try:
		hours_float = float(base_duration)
	except:
		hours_float = base_duration

	# Calculate total minutes
	total_minutes = hours_float * 60

	# Calculate days, hours, and minutes
	days = int(total_minutes // (24 * 60))
	total_minutes %= (24 * 60)
	hours = int(total_minutes // 60)
	minutes = int(total_minutes % 60)

	# Return formatted string
	return "{days:02d}j{hours:02d}h".format(days=days, hours=hours + 1 if minutes > 0 else hours) if days > 0 else "{hours:02d}h{minutes:02d}min".format(hours=hours, minutes=minutes)


def string_duration_to_float_hours(datetime_str):
	days = 0
	hours = 0
	minutes = 0

	# Check if the string contains days
	if 'j' in datetime_str:
		parts = datetime_str.split('j')
		days = int(parts[0])
		time_str = parts[1]
	else:
		time_str = datetime_str

	# Split the remaining time string into hours and minutes
	if 'h' in time_str and 'min' in time_str:
		time_parts = time_str.split('h')
		hours = int(time_parts[0])
		minutes = int(time_parts[1].replace('min', ''))

	# Calculate the total hours
	total_hours = days * 24 + hours + minutes / 60.0

	return total_hours


def convert_seconds_to_hours_minutes(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return "{}h{}".format(hours, str(minutes).zfill(2))


def convert_to_24_hours_format(timestamp_str):
	# Parse the timestamp string to a datetime object (depending milliseconds or not)
	try:
		timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
	except:
		timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")

	# Format the datetime object to a 24-hours time string (HH:MM:SS)
	time_24_hours_format = timestamp.strftime("%H:%M")

	return time_24_hours_format

