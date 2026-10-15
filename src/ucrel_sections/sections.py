from time import time
from traceback import print_exception

class Color:
    # Reset / styles
    RESET = '\033[0m'
    END = RESET
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    # Standard foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Dark / dim foreground colors
    DARK_BLACK = '\033[2;30m'
    DARK_RED = '\033[2;31m'
    DARK_GREEN = '\033[2;32m'
    DARK_YELLOW = '\033[2;33m'
    DARK_BLUE = '\033[2;34m'
    DARK_MAGENTA = '\033[2;35m'
    DARK_CYAN = '\033[2;36m'
    DARK_WHITE = '\033[2;37m'

    # Backward-compatible aliases
    PURPLE = BRIGHT_MAGENTA
    DARKCYAN = DARK_CYAN

    STYLE_SECTION = DIM + CYAN + BOLD
    STYLE_TIMING = DIM + CYAN + BOLD
    STYLE_UNITTEST_PASS = BRIGHT_GREEN + BOLD
    STYLE_UNITTEST_FAIL = BRIGHT_RED + BOLD
    STYLE_UNITTEST_INFO = DIM + CYAN

    STYLE_ERROR = BRIGHT_RED + BOLD

def fmt( text: str, style: str | None = None, width: int = 120 ) -> str:
        text_block = f" {text} "
        available = max(width - len(text_block), 0)
        left_bars = available // 2
        right_bars = available - left_bars
        if style:
            return f"{style}{'=' * left_bars}{text_block}{'=' * right_bars}{Color.RESET}"
        return f"{'=' * left_bars}{text_block}{'=' * right_bars}"

class Section:
    def __init__(self, title: str | None = None, width: int = 120):
        self.title = title or ""
        self.width = width
        self.tests = []

    def test(self, name: str, canFail: bool = False) -> "UnitTest":
        unit = UnitTest((name and f"<Test> {name}") or "<Test>", canFail = canFail)
        self.tests.append(unit)
        return unit

    def timer(self, name: str) -> "Timer":
        unit = Timer((name and f"<Timer> {name}") or "<Timer>")
        self.tests.append(unit)
        return unit

    def report(self, name: str, message: str):
        self.tests.append(TestResult(
            (name and f"<Report> {name}") or "<Report>",
            failed=False,
            detail=message
        ))

    def tryAssert(self, condition, detail: str | None = None, name: str | None = None):
        if not condition:
            self.tests.append(TestResult(
                (name and f"<Assertion> {name}") or "<Assertion>",
                failed=True,
                detail=detail or "Assertion failed"
            ))
        else:
            self.tests.append(TestResult(
                (name and f"<Assertion> {name}") or "<Assertion>",
                failed=False,
                detail=None
            ))

    def __enter__(self):
        print(f"\n{fmt(self.title, Color.STYLE_SECTION, self.width)}", flush=True)
        self.t0 = time()
        return self
    
    def divider(self, showTime: bool = False):
        t1 = time()
        if showTime:
            print(f"{fmt(f'[Time: {round(t1 - self.t0, 2)} seconds]', Color.STYLE_SECTION, self.width)}\n", flush=True)
        else:
            print(f"{Color.STYLE_SECTION}{'=' * self.width}{Color.RESET}\n", flush=True)
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        t1 = time()
        if exc_type is None:
            print(f"{fmt(f'END: {self.title}, Time: {round(t1 - self.t0, 2)} seconds', Color.STYLE_SECTION, self.width)}\n", flush=True)
        else:
            print(f"{fmt('HALT // ERROR', Color.STYLE_ERROR, self.width)}", flush=True)

        if len(self.tests) > 0:
            print(f"{Color.STYLE_SECTION}Test Results:{Color.RESET}", flush=True)
            for test in self.tests:
                if hasattr(test, 'failed') and test.failed:
                    if hasattr(test, 'detail') and test.detail:
                        print(f"  - {Color.STYLE_UNITTEST_FAIL}{test.name}: [✘] Failed - {test.detail}{Color.RESET}", flush=True)
                    else:
                        print(f"  - {Color.STYLE_UNITTEST_FAIL}{test.name}: [✘] Failed {Color.RESET}", flush=True)
                else:
                    if hasattr(test, 'detail') and test.detail:
                        print(f"  - {Color.STYLE_UNITTEST_PASS}{test.name}: [✔] Passed - {test.detail}{Color.RESET}", flush=True)
                    else:
                        print(f"  - {Color.STYLE_UNITTEST_PASS}{test.name}: [✔] Passed{Color.RESET}", flush=True)
                if hasattr(test, 'reports') and len(test.reports) > 0:
                    for message in test.reports:
                        print(f"      - {Color.STYLE_UNITTEST_INFO}{message}{Color.RESET}", flush=True)

            print("", flush=True)

class TestResult:
    def __init__(self, name: str, failed: bool = False, detail: str | None = None):
        self.name = name
        self.failed = failed
        self.detail = detail
        self.reports = []

    def report(self, message):
        self.reports.append(message)

class Timer(TestResult):
    def __init__(self, title: str | None = None):
        super().__init__(title or "<Timer>", False, None)

    def __enter__(self):
        print(f'{Color.STYLE_TIMING}[{self.name} - Started Timer]{Color.RESET}', flush=True)
        self.failed = True
        self.detail = "Timer did not complete successfully"
        self.t0 = time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        t1 = time()
        self.detail = None
        self.failed = False
        self.detail = f"Complete in {round(t1 - self.t0, 2)} seconds"
        print(f'{Color.STYLE_TIMING}[Time {round(t1 - self.t0, 2)} seconds]{Color.RESET}', flush=True)

class UnitTest(TestResult):
    def __init__(self, name: str | None = None, showPassed: bool = False, canFail: bool = False):
        super().__init__(name or "<UnitTest>", False, None)
        self.showPassed = showPassed
        self.canFail = canFail 

    def __enter__(self) -> "UnitTest":
        return self

    def reject(self, condition: bool, detail: str | None = None):
        if not condition:
            return
        
        self.failed = True
        self.detail = detail
        if detail:
            raise AssertionError(f"Unit test '{self.name}' failed: {detail}")
        raise AssertionError(f"Unit test '{self.name}' failed.")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            if self.showPassed:
                print(f"{Color.STYLE_UNITTEST_PASS}{self.name}: ✔ Passed{Color.RESET}", flush=True)
        else:
            if self.canFail:
                self.failed = True
                self.detail = str(exc_value)
                print(f"{Color.STYLE_UNITTEST_FAIL}{self.name}: ✘ Failed{Color.RESET}", flush=True)
                print(f"{Color.STYLE_UNITTEST_FAIL}{self.name}:     - Error: {exc_value}{Color.RESET}", flush=True)
                return True
            else:
                raise exc_value