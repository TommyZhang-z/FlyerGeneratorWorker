import datetime
import pytz


def convert_to_syd_time(time_str):
    """
    Convert a time string to a Sydney time string

    >>> convert_to_syd_time("2024-10-23T13:00:00.000Z")
    '23 Oct, 2024'
    """
    try:
        utc_time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        syd_tz = pytz.timezone("Australia/Sydney")
        syd_time = utc_time.astimezone(syd_tz)
        return syd_time.strftime("%d %b, %Y")
    except ValueError:
        return time_str


def convert_to_currency(price: int | float) -> str:
    """
    Convert a price to a currency string

    >>> convert_to_currency(1000000)
    '$1,000,000'
    """
    return f"${price:,}"
