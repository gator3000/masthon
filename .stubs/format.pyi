from typing import IO, Callable, Any

_escape: Callable[[Any, Any], str]
_escape_graph: Callable[[Any], str]

class ANSI:
    SAVE: str
    RESTORE: str
    class FORMAT:
        RESET: str
        BOLD: str
        FAINT: str
        ITALIC: str
        UNDERLINE: str
        BLINK: str
        _RAPID_BLINK: str
        REVERSE_BGFG: str
        CONCEAL: str
        STRIKE: str
        OVERLINE: str
        DOUBLE_UNDERLINE: str
        NO_BOLD_FAINT: str
        NO_BOLD = NO_BOLD_FAINT
        NO_FAINT = NO_BOLD_FAINT
        NO_ITALIC: str
        NO_UNDERLINE: str
        NO_BLINK: str
        RESET_REVERSE_BGFG: str
        NO_CONCEAL: str
        NO_STRIKE: str
        NO_OVERLINE: str
        class FG:
            RESET: str
            BLACK_D: str
            BLACK = BLACK_D
            RED_D: str
            RED = RED_D
            GREEN_D: str
            YELLOW_D: str
            BLUE_D: str
            MAGENTA_D: str
            CYAN_D: str
            WHITE_D: str
            BLACK_B: str
            RED_B: str
            GREEN_B: str
            GREEN = GREEN_B
            YELLOW_B: str
            YELLOW = YELLOW_B
            BLUE_B: str
            BLUE = BLUE_B
            MAGENTA_B: str
            MAGENTA = MAGENTA_B
            CYAN_B: str
            CYAN = CYAN_B
            WHITE_B: str
            WHITE = WHITE_B
            GRAY_D = BLACK_B
            GRAY_B = WHITE_D
            GRAY = GRAY_D
            @staticmethod
            def RGB(r: int, g: int, b: int) -> str: ...
        RESET_FG: str
        class BG:
            RESET: str
            BLACK_D: str
            BLACK = BLACK_D
            RED_D: str
            RED = RED_D
            GREEN_D: str
            YELLOW_D: str
            BLUE_D: str
            MAGENTA_D: str
            CYAN_D: str
            WHITE_D: str
            BLACK_B: str
            RED_B: str
            GREEN_B: str
            GREEN = GREEN_B
            YELLOW_B: str
            YELLOW = YELLOW_B
            BLUE_B: str
            BLUE = BLUE_B
            MAGENTA_B: str
            MAGENTA = MAGENTA_B
            CYAN_B: str
            CYAN = CYAN_B
            WHITE_B: str
            WHITE = WHITE_B
            GRAY_D = BLACK_B
            GRAY_B = WHITE_D
            GRAY = GRAY_D
            @staticmethod
            def RGB(r: int, g: int, b: int) -> str: ...
        RESET_BG: str
FORMAT = ANSI.FORMAT

def ansi(*args: str, sep: str = ' ', fend: str = ..., end: str = '\n', flush: bool = False, file: IO[str] | str | None = ..., **kwargs: str) -> str: ...
