import logging
from dataclasses import dataclass

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django_unicorn.components import UnicornView

logger = logging.getLogger(__name__)


@dataclass
class Directive:
    code: str
    meaning: str
    requires_36: bool = False


SET_OF_DIRECTIVES = {
    "%a",
    "%A",
    "%w",
    "%d",
    "%-d",
    "%b",
    "%B",
    "%m",
    "%-m",
    "%y",
    "%Y",
    "%H",
    "%-H",
    "%I",
    "%-I",
    "%p",
    "%M",
    "%-M",
    "%S",
    "%-S",
    "%f",
    "%z",
    "%Z",
    "%j",
    "%-j",
    "%U",
    "%W",
    "%c",
    "%x",
    "%X",
    "%%",
    "%G",
    "%u",
    "%V",
}

ALL_DIRECTIVES = [
    Directive("%a", "Weekday as locale’s abbreviated name.",),
    Directive("%A", "Weekday as locale’s full name.",),
    Directive(
        "%w", "Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.",
    ),
    Directive("%d", "Day of the month as a zero-padded decimal number.",),
    Directive("%-d", "Day of the month as a decimal number. (Platform specific)",),
    Directive("%b", "Month as locale’s abbreviated name.",),
    Directive("%B", "Month as locale’s full name.",),
    Directive("%m", "Month as a zero-padded decimal number.",),
    Directive("%-m", "Month as a decimal number. (Platform specific)",),
    Directive("%y", "Year without century as a zero-padded decimal number.",),
    Directive("%Y", "Year with century as a decimal number.",),
    Directive("%H", "Hour (24-hour clock) as a zero-padded decimal number.",),
    Directive("%-H", "Hour (24-hour clock) as a decimal number. (Platform specific)",),
    Directive("%I", "Hour (12-hour clock) as a zero-padded decimal number.",),
    Directive("%-I", "Hour (12-hour clock) as a decimal number. (Platform specific)",),
    Directive("%p", "Locale’s equivalent of either AM or PM.",),
    Directive("%M", "Minute as a zero-padded decimal number.",),
    Directive("%-M", "Minute as a decimal number. (Platform specific)",),
    Directive("%S", "Second as a zero-padded decimal number.",),
    Directive("%-S", "Second as a decimal number. (Platform specific)",),
    Directive("%f", "Microsecond as a decimal number, zero-padded on the left.",),
    Directive(
        "%z",
        "UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive).",
    ),
    Directive("%Z", "Time zone name (empty string if the object is naive).",),
    Directive("%j", "Day of the year as a zero-padded decimal number.",),
    Directive("%-j", "Day of the year as a decimal number. (Platform specific)",),
    Directive(
        "%U",
        "Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.",
    ),
    Directive(
        "%W",
        "Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.",
    ),
    Directive("%c", "Locale’s appropriate date and time representation.",),
    Directive("%x", "Locale’s appropriate date representation.",),
    Directive("%X", "Locale’s appropriate time representation.",),
    Directive("%%", "A literal % character.",),
    Directive(
        "%G",
        "ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V).",
        True,
    ),
    Directive("%u", "ISO 8601 weekday as a decimal number where 1 is Monday.", True,),
    Directive(
        "%V",
        "ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.",
        True,
    ),
]


class StrftimeView(UnicornView):
    datetime = now()
    format = ""
    result = ""
    directives = []
    directive_search = ""
    exclude_36 = False

    def mount(self):
        self.directives = ALL_DIRECTIVES

    def updated_directive_search(self, _):
        filtered_directives = []

        # Handle either the dataclass or dictionary because `dataclass` isn't re-hydrated automatically, yet
        for directive in ALL_DIRECTIVES:
            if isinstance(directive, Directive):
                if self.directive_search.lower() in directive.meaning.lower():
                    filtered_directives.append(directive)
            else:
                if (
                    self.directive_search.lower()
                    in directive.get("meaning", "").lower()
                ):
                    filtered_directives.append(directive)

        self.directives = filtered_directives

    def set_now(self):
        self.datetime = now()
        self.format_datetime()

    def add_directive(self, code):
        self.format = f"{self.format} {code}"
        self.format_datetime()

    def clear_format(self):
        self.format = ""
        self.format_datetime()

    def updated_format(self, val):
        self.format_datetime()

    def format_datetime(self):
        try:
            if self.datetime and isinstance(self.datetime, str):
                self.datetime = parse_datetime(self.datetime)

            self.result = ""
            potential_directive = ""

            for s in self.format:
                if potential_directive + s in SET_OF_DIRECTIVES:
                    code = potential_directive + s
                    meaning = next(
                        filter(lambda d: d.code == code, ALL_DIRECTIVES)
                    ).meaning

                    code_result = self.datetime.strftime(code)
                    htmlized_code_result = f"<span class='has-tooltip-arrow has-tooltip-multiline' style='background-color: #FFDF00' data-tooltip='{code}: {meaning}'>{code_result}</span>"
                    self.result += htmlized_code_result

                    potential_directive = ""
                elif s == "%":
                    potential_directive = s
                elif potential_directive and s == "-":
                    potential_directive += s
                else:
                    if s == " ":
                        self.result += "&nbsp;"
                    else:
                        self.result += s
        except Exception as e:
            logger.exception(e)
