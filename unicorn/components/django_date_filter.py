import logging

from django.template.defaultfilters import date
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django_unicorn.components import UnicornView

logger = logging.getLogger(__name__)

DAY_FORMATS = (
    {"format": "d", "meaning": "Day of the month, 2 digits with leading zeros."},
    {"format": "j", "meaning": "Day of the month without leading zeros."},
    {"format": "D", "meaning": "Day of the week, textual, 3 letters."},
    {"format": "l", "meaning": "Day of the week, textual, long."},
    {
        "format": "S",
        "meaning": "English ordinal suffix for day of the month, 2 characters.",
    },
    {"format": "w", "meaning": "Day of the week, digits without leading zeros."},
    {"format": "z", "meaning": "Day of the year."},
)

WEEK_FORMATS = (
    {
        "format": "W",
        "meaning": "ISO-8601 week number of year, with weeks starting on Monday.",
    },
)

MONTH_FORMATS = (
    {"format": "m", "meaning": "Month, 2 digits with leading zeros."},
    {"format": "n", "meaning": "Month without leading zeros."},
    {"format": "M", "meaning": "Month, textual, 3 letters."},
    {"format": "b", "meaning": "Month, textual, 3 letters, lowercase."},
    {
        "format": "E",
        "meaning": "Month, locale specific alternative representation usually used for long date representation.",
    },
    {"format": "F", "meaning": "Month, textual, long."},
    {
        "format": "N",
        "meaning": "Month abbreviation in Associated Press style. Proprietary extension.",
    },
    {"format": "t", "meaning": "Number of days in the given month."},
)

YEAR_FORMATS = (
    {"format": "y", "meaning": "Year, 2 digits."},
    {"format": "Y", "meaning": "Year, 4 digits."},
    {"format": "L", "meaning": "Boolean for whether it’s a leap year."},
    {
        "format": "o",
        "meaning": "ISO-8601 week-numbering year, corresponding to the ISO-8601 week number (W) which uses leap weeks. See Y for the more common year format.",
    },
)

TIME_FORMATS = (
    {"format": "g", "meaning": "Hour, 12-hour format without leading zeros."},
    {"format": "G", "meaning": "Hour, 24-hour format without leading zeros."},
    {"format": "h", "meaning": "Hour, 12-hour format."},
    {"format": "H", "meaning": "Hour, 24-hour format."},
    {"format": "i", "meaning": "Minutes."},
    {"format": "s", "meaning": "Seconds, 2 digits with leading zeros."},
    {"format": "u", "meaning": "Microseconds."},
    {
        "format": "a",
        "meaning": "'a.m.' or 'p.m.' (Note that this is slightly different than PHP’s output, because this includes periods to match Associated Press style.)",
    },
    {"format": "A", "meaning": "'AM' or 'PM'."},
    {
        "format": "f",
        "meaning": "Time, in 12-hour hours and minutes, with minutes left off if they’re zero. Proprietary extension.",
    },
    {
        "format": "P",
        "meaning": "Time, in 12-hour hours, minutes and ‘a.m.’/’p.m.’, with minutes left off if they’re zero and the special-case strings ‘midnight’ and ‘noon’ if appropriate. Proprietary extension.",
    },
)

TIMEZONE_FORMATS = (
    {
        "format": "e",
        "meaning": "Timezone name. Could be in any format, or might return an empty string, depending on the datetime.",
    },
    {
        "format": "I",
        "meaning": "Daylight Savings Time, whether it’s in effect or not.",
    },
    {"format": "O", "meaning": "Difference to Greenwich time in hours."},
    {"format": "T", "meaning": "Time zone of this machine."},
    {
        "format": "Z",
        "meaning": "Time zone offset in seconds. The offset for timezones west of UTC is always negative, and for those east of UTC is always positive.",
    },
)

DATETIME_FORMATS = (
    {
        "format": "c",
        "meaning": "ISO 8601 format. (Note: unlike other formatters, such as “Z”, “O” or “r”, the “c” formatter will not add timezone offset if value is a naive datetime (see datetime.tzinfo).",
    },
    {"format": "r", "meaning": "RFC 5322 formatted date.",},
    {
        "format": "U",
        "meaning": "Seconds since the Unix Epoch (January 1 1970 00:00:00 UTC).",
    },
)

ALL_FORMATS = (
    DAY_FORMATS
    + WEEK_FORMATS
    + MONTH_FORMATS
    + YEAR_FORMATS
    + TIME_FORMATS
    + TIMEZONE_FORMATS
    + DATETIME_FORMATS
)

SET_OF_FORMATS = set([f.get("format") for f in ALL_FORMATS])


class DjangoDateFilterView(UnicornView):
    datetime = now()
    format = ""
    result = ""
    day_formats = DAY_FORMATS
    week_formats = WEEK_FORMATS
    month_formats = MONTH_FORMATS
    year_formats = YEAR_FORMATS
    time_formats = TIME_FORMATS
    timezone_formats = TIMEZONE_FORMATS
    datetime_formats = DATETIME_FORMATS

    def mount(self):
        self.format_datetime()

    def set_now(self):
        self.datetime = now()
        self.format_datetime()

    def add_format(self, code):
        self.format = f"{self.format}{code}"
        self.format_datetime()

    def clear_format(self):
        self.format = ""
        self.format_datetime()

    def updated_format(self, val):
        self.format_datetime()

    def format_datetime(self):
        self.call("updateDateFormat", self.format)

        try:
            if self.datetime and isinstance(self.datetime, str):
                self.datetime = parse_datetime(self.datetime)

            self.result = ""
            # potential_format = ""

            for s in self.format:
                if s in SET_OF_FORMATS:
                    format = s
                    meaning = next(
                        filter(lambda f: f.get("format") == format, ALL_FORMATS)
                    ).get("meaning")

                    format_result = date(self.datetime, format)
                    htmlized_format_result = f"<span class='has-tooltip-arrow has-tooltip-multiline result' data-tooltip='{format}: {meaning}'><span class='code'></span>{format_result}</span>"
                    self.result += htmlized_format_result
                else:
                    if s == " ":
                        self.result += "<span class='space'>&nbsp;</span>"
                    else:
                        self.result += s

            if not self.format:
                self.result = date(self.datetime)
        except Exception as e:
            logger.exception(e)

    class Meta:
        safe = ("result",)
