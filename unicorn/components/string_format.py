from django_unicorn.components import UnicornView

ALL_FORMATS = [
    {"format": "{:>10}", "meaning": "Align right"},
    {"format": "{:10}", "meaning": "Align left"},
    {"format": "{:*>10}", "meaning": "Align right padded with a character"},
    {"format": "{:*<10}", "meaning": "Align left padded with a character"},
    {"format": "{:^10}", "meaning": "Center align"},
    {"format": "{:.1}", "meaning": "Truncate string"},
    {"format": "{:10.1}", "meaning": "Truncate and pad string"},
]


class StringFormatView(UnicornView):
    text = ""
    format = ""
    result = ""
    formats = ALL_FORMATS

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
        if self.format:
            self.result = self.format.format(self.text)
        else:
            self.result = self.text

        # self.result = "{:10}".format("test")

        # print("self.result", len(self.result))

        self.result = self.result.replace(" ", "<span class='space'></span>")

