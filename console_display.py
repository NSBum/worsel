from rich import print
from rich.text import Text
from rich.console import Console


def _colour_code_to_colour(c: str):
    c = c.upper()
    if c == 'Y':
        return 'yellow'
    elif c == 'G':
        return 'green3'
    return 'grey'


class Display(object):
    def __init__(self):
        self.console = Console()

    def show_line(self, chars: list, colours: list):
        """
        Using the Rich library, displays a text line
        :param chars: List of characters to display
        :param colours: List of colours y,g,x in which to render characters
        :return: No return value
        """
        out = Text()
        for text in zip(chars, colours):
            colour = _colour_code_to_colour(text[1])
            style = f'bold black on {colour}'
            out.append(text[0], style=style)
        self.console.print(out)

    def show_lines(self, lines: list):
        """
        Displays a series of lines in coloured text
        :param lines: list of tuples (chars, colours)
        :return: No return value
        """
        for line in lines:
            self.show_line(line[0], line[1])

    def print_red(self, msg: str):
        """
        Print text to Rich console in red
        :param msg: text to display
        :return: No return value
        """
        text = Text(msg)
        text.stylize("bold red")
        self.console.print(text)

    def print_blue(self, msg: str):
        """
        Print text to Rich console in blue
        :param msg: text to display
        :return: No return value
        """
        text = Text(msg)
        text.stylize("bold cyan2")
        self.console.print(text)

