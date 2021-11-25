import logging

from django_unicorn.components import UnicornView

logger = logging.getLogger(__name__)

STRING_FORMATS = [
    {"format": "{:>10}", "meaning": "Align right"},
    {"format": "{:10}", "meaning": "Align left"},
    {"format": "{:*>10}", "meaning": "Align right padded with a character"},
    {"format": "{:*<10}", "meaning": "Align left padded with a character"},
    {"format": "{:^10}", "meaning": "Center align"},
    {"format": "{:.1}", "meaning": "Truncate string"},
    {"format": "{:10.1}", "meaning": "Truncate and pad string"},
]


INTEGER_FORMATS = [
    {"format": "{:4d}", "meaning": "Pad integer"},
    {"format": "{:04d}", "meaning": "Pad integer with a character"},
    {"format": "{:+d}", "meaning": "Sign number"},
    {"format": "{:=+5d}", "meaning": "Sign number with padding"},
]

FLOAT_FORMATS = [
    {"format": "{:04.2f}", "meaning": "Pad float"},
]


class StringFormatView(UnicornView):
    text = ""
    format = ""
    result = ""
    string_formats = STRING_FORMATS
    integer_formats = INTEGER_FORMATS
    float_formats = FLOAT_FORMATS

    def clear_text(self):
        self.text = ""
        self.format_text()

    def add_format(self, format):
        self.format = format
        self.format_text()

    def clear_format(self):
        self.format = ""
        self.format_text()

    def updated_format(self, _):
        self.format_text()

    def updated_text(self, _):
        self.format_text()

    def format_text(self):
        try:
            number = None
            try:
                number = float(self.text)
            except ValueError:
                pass

            try:
                number = int(self.text)
            except ValueError:
                pass

            if number:
                self.result = self.format.format(number)
            elif self.format:
                self.result = self.format.format(self.text)
            else:
                self.result = self.text

            self.result = self.result.replace(" ", "<span class='space'></span>")
        except Exception as e:
            self.result = ""
            logger.exception(e)

    class Meta:
        safe = ("result",)
