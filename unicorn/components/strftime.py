from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django_unicorn.components import UnicornView


class StrftimeView(UnicornView):
    datetime = now()
    format = "%c"
    result = ""
    formatters = [
        ("%a", "Weekday as locale’s abbreviated name.",),
        ("%A", "Weekday as locale’s full name.",),
        ("%w", "Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.",),
        ("%d", "Day of the month as a zero-padded decimal number.",),
        ("%-d", "Day of the month as a decimal number. (Platform specific)",),
        ("%b", "Month as locale’s abbreviated name.",),
        ("%B", "Month as locale’s full name.",),
        ("%m", "Month as a zero-padded decimal number.",),
        ("%-m", "Month as a decimal number. (Platform specific)",),
        ("%y", "Year without century as a zero-padded decimal number.",),
        ("%Y", "Year with century as a decimal number.",),
        ("%H", "Hour (24-hour clock) as a zero-padded decimal number.",),
        ("%-H", "Hour (24-hour clock) as a decimal number. (Platform specific)",),
        ("%I", "Hour (12-hour clock) as a zero-padded decimal number.",),
        ("%-I", "Hour (12-hour clock) as a decimal number. (Platform specific)",),
        ("%p", "Locale’s equivalent of either AM or PM.",),
        ("%M", "Minute as a zero-padded decimal number.",),
        ("%-M", "Minute as a decimal number. (Platform specific)",),
        ("%S", "Second as a zero-padded decimal number.",),
        ("%-S", "Second as a decimal number. (Platform specific)",),
        ("%f", "Microsecond as a decimal number, zero-padded on the left.",),
        (
            "%z",
            "UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive).",
        ),
        ("%Z", "Time zone name (empty string if the object is naive).",),
        ("%j", "Day of the year as a zero-padded decimal number.",),
        ("%-j", "Day of the year as a decimal number. (Platform specific)",),
        (
            "%U",
            "Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.",
        ),
        (
            "%W",
            "Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.",
        ),
        ("%c", "Locale’s appropriate date and time representation.",),
        ("%x", "Locale’s appropriate date representation.",),
        ("%X", "Locale’s appropriate time representation.",),
        ("%%", "A literal % character.",),
    ]

    def hydrate(self):
        self.format_datetime()

    def set_now(self):
        self.datetime = now()
        self.format_datetime()

    def add_format(self, formatter):
        self.format += " " + formatter
        self.format = self.format.strip()
        self.format_datetime()

    def clear_format(self):
        self.format = ""
        self.format_datetime()

    def format_datetime(self):
        try:
            if self.datetime and isinstance(self.datetime, str):
                self.datetime = parse_datetime(self.datetime)

            self.result = self.datetime.strftime(self.format)
        except Exception as e:
            pass
