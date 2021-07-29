#!.venv/bin/python
"""
Check guides for required directives / sections.

See `STYLE.md` for guidance.
"""
import argparse
import json
import re
import sys
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Callable
from typing import Iterable
from typing import List
from typing import Match
from typing import Optional
from typing import Union

__version__ = "0.1.0"

DESCRIPTION, EPILOG = __doc__.strip().split("\n\n")
ERROR_CODE = 5
STATIC_PATH = Path(__file__).parent / "source/_static/images"

CheckArgument = Union[str, Match, Callable]


@dataclass(order=True)
class CheckResult:
    """Collect the results of a check along with meta info."""

    filename: str
    key: str
    passed: bool
    warning: bool
    help: str = field(compare=False)

    @property
    def result(self):
        if self.passed:
            return "okay"
        elif self.warning:
            return "warning"
        else:
            return "error"


class ChecklistResults:

    """
    Collect :cls:`CheckResult` instances.

    The :cls:`ChecklistResults` instance is considered *failed*, if at least one
    of the collected :cls:`CheckResult` instances failed, it is considered
    *passed* only if every check succeded.
    """

    results: List[CheckResult]

    def __init__(self, results):
        self.results = results

    def __iter__(self) -> Iterable[CheckResult]:
        return iter(self.results)

    def __bool__(self) -> bool:
        return self.is_passed

    @property
    def passed_checks(self) -> Iterable[CheckResult]:
        return (c for c in self if c.passed)

    @property
    def missed_checks(self) -> Iterable[CheckResult]:
        return (c for c in self if not c.passed)

    @property
    def failed_checks(self) -> Iterable[CheckResult]:
        return (c for c in self.missed_checks if not c.warning)

    @property
    def warnings(self) -> Iterable[CheckResult]:
        return (c for c in self.missed_checks if c.warning)

    @property
    def is_failed(self) -> bool:
        return bool(any(self.failed_checks))

    @property
    def is_passed(self) -> bool:
        return not bool(any(self.missed_checks))

    @property
    def result(self):
        if self.is_passed:
            return "okay"
        elif self.is_failed:
            return "error"
        else:
            return "warning"


@dataclass(order=True)
class Check:
    """
    A check definded by metadata (:attr:`key`, :attr:`category` and
    :attr:`help`) and one of the possible :attr:`action` (together with an
    :attr:`argument` for it).

    A check is considered *failed*, if it did not pass and also did not fall
    into one of the :attr:`Check.WARN_ONLY_CATEGORIES`.
    """

    AVAILABLE_ACTIONS = ("search", "regex", "function")
    AVAILABLE_CATEGORIES = ("error", "warning")
    WARN_ONLY_CATEGORIES = ("warning",)

    key: str
    help: str = field(compare=False)
    action: str = field(compare=False)
    argument: CheckArgument = field(compare=False)

    def __post_init__(self):
        if self.category not in self.AVAILABLE_CATEGORIES:
            raise ValueError(f"unknown category: '{self.category}'")
        if self.action not in self.AVAILABLE_ACTIONS:
            raise ValueError(f"unknown action: '{self.action}'")
        _ = self.action_function  # just checking

    @property
    def category(self) -> str:
        return self.key.split("-")[0]

    @property
    def is_warning(self) -> bool:
        return self.category in self.WARN_ONLY_CATEGORIES

    @property
    def action_function(self) -> Callable:
        func_name = f"check_action_{self.action}"
        try:
            return getattr(self, func_name)
        except AttributeError:
            msg = f"missing function '{func_name}' for action: '{self.action}'"
            raise ValueError(msg)

    def __call__(self, filename: Path, content: str) -> CheckResult:
        passed = self.action_function(filename, content)
        return CheckResult(
            filename=str(filename),
            key=self.key,
            passed=passed,
            warning=self.is_warning,
            help=self.help,
        )

    def check_action_search(self, filename: Path, content: str) -> bool:
        """Check if string is found in content."""
        return bool(self.argument in content)

    def check_action_regex(self, filename: Path, content: str) -> bool:
        """Check if *argument* regex is found in content."""
        if not isinstance(self.argument, re.Pattern):
            self.argument = re.compile(self.argument)
        return bool(self.argument.search(content))

    def check_action_function(self, filename: Path, content: str) -> bool:
        """Call *argument* with filename and content, return the results."""
        return bool(self.argument(filename, content))

    @classmethod
    def get_unsupported_categories(cls, categories: List[str]) -> List[str]:
        return [c for c in categories if c not in cls.AVAILABLE_CATEGORIES]


class Checklist:
    """
    Contains :cls:`Check`, can run them over a guide and collects the
    :cls:`CheckResults` in a cls`ChecklistResults` instance.
    """

    checks: List[Check]

    def __init__(self, *checks):
        self.checks = checks

    def __call__(
        self, filename: Path, categories=("error"), report_all=False
    ) -> ChecklistResults:
        if unsuported := Check.get_unsupported_categories(categories):
            raise ValueError(f"unknown categories: {', '.join(unsuported)}")

        with open(filename, "r") as fh:
            content = fh.read()

        results = []

        for check in (c for c in self.checks if c.category in categories):
            result = check(filename, content)
            if report_all or not result.passed:
                results.append(result)

        return ChecklistResults(results)


def check_image_file(filename: Path, content: str) -> bool:
    image_regex = r"\.\. image::\s+_static/images/(?P<image>\w+\.(png|svg))"
    if match := re.search(image_regex, content):
        image_path = STATIC_PATH / match.group("image")
        if not image_path.exists():
            return False
    return True


CHECKLIST = Checklist(
    Check(
        "error-meta-author",
        action="regex",
        argument=r"\.\. author:: +[^<]+(<[^>]+>)?",
        help="needs at least one `.. author:: {name}` directive",
    ),
    Check(
        "error-meta-authorlist",
        action="search",
        argument=".. author_list::",
        help="missing `.. author_list::` directive",
    ),
    Check(
        "error-meta-tag",
        action="regex",
        argument=r"\.\. tag:: \w+",
        help="needs at least one `.. tag` directive",
    ),
    Check(
        "error-meta-taglist",
        action="search",
        argument=".. tag_list::",
        help="missing `.. tag_list::` directive",
    ),
    Check(
        "error-files-image",
        action="function",
        argument=check_image_file,
        help="used image file not provided in `_source/static/images/`",
    ),
    Check(
        "warning-content-username",
        action="search",
        argument="isabell",
        help="username `isabell` not used",
    ),
    Check(
        "warning-content-hostanme",
        action="search",
        argument="stardust",
        help="hostname `stardust` not used",
    ),
    Check(
        "warning-meta-sidebar",
        action="regex",
        argument=r"\.\. sidebar::\s+\w+\n\s+.. image",
        help="missing `.. sidebar::` directive for logo",
    ),
    Check(
        "warning-meta-image",
        action="regex",
        argument=r"\.\. image::\s+_static/images/\w+\.(png|svg)",
        help="no articel image declared `image:: _static/images/article.(png|svg)",
    ),
    Check(
        "warning-structure-intro",
        action="regex",
        argument=r"###+\n\w+\n###+\n\n([^=].+\n+)+\n---+\n\n",
        help="no introductory section",
    ),
    Check(
        "warning-structure-installation",
        action="regex",
        argument=r"Installation\n===+",
        help="no `Installation` section",
    ),
    Check(
        "warning-structure-configuration",
        action="regex",
        argument="Configuration\n===+",
        help="no `Configuration` section",
    ),
    Check(
        "warning-structure-updates",
        action="regex",
        argument="Updates\n===+",
        help="no `Updates` section",
    ),
    Check(
        "warning-structure-tested",
        action="search",
        argument="Tested on Uberspace v",
        help="no `Tested on Uberspace` part",
    ),
    Check(
        "warning-structure-pre",
        action="search",
        argument="a",
        help="no `Prerequisites` section",
    ),
    Check(
        "warning-structure-finishing",
        action="search",
        argument="a",
        help="no `Finishing` section",
    ),
    Check(
        "warning-structure-practices",
        action="search",
        argument="a",
        help="no `Best Practices` section",
    ),
)


def get_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    ap.add_argument("guides", nargs="+", metavar="PATH", help="RST file to check")
    ap.add_argument(
        "--check",
        action="store_true",
        dest="check_mode",
        help=f"exit with `{ERROR_CODE}` on results",
    )
    ap.add_argument(
        "--warn", action="store_true", dest="check_warnings", help="check warnings too"
    )
    ap.add_argument(
        "--report-all", action="store_true", help="report passed checks too"
    )
    ap.add_argument(
        "--verbose", action="store_true", help="list checked files (on STDERR)"
    )
    ap.add_argument(
        "--absolute-paths",
        action="store_true",
        help="use absolute paths in the results",
    )
    ap.add_argument(
        "--json", action="store_true", dest="output_json", help="results as JSON"
    )
    ap.add_argument("--version", action="version", version=__version__)
    args = ap.parse_args(argv)
    return args


def main(
    guides: List[str],
    check_mode=False,
    check_warnings=False,
    report_all=False,
    verbose=False,
    absolute_paths=False,
    output_json=False,
    checklist=CHECKLIST,
) -> int:
    # collect errors and warnings (only with `--check_warnings`) and
    # also passed checks (with `--report_all`).
    results_by_guide = {}
    # will be `True` if any errors are found
    errors_found = False
    # only used to build relative paths in the output
    base_path = Path.cwd()
    # check these categories
    categories = ("error", "warning") if check_warnings else ("error",)

    for guide in guides:
        guide = Path(guide).resolve()
        key = str(guide) if absolute_paths else str(guide.relative_to(base_path))

        if not guide.exists():
            print(f"# skippping '{guide}': file not found", file=sys.stderr)
            continue

        if verbose:
            print(f"# checking '{guide}'", end="... ", file=sys.stderr)

        result = checklist(guide, categories=categories, report_all=report_all)

        if report_all or not result.is_passed:
            results_by_guide[key] = result
            if result.is_failed:
                errors_found = True

        if verbose:
            print(f"{result.result.upper()}.", file=sys.stderr)

    if output_json:
        checks = [
            asdict(check) for results in results_by_guide.values() for check in results
        ]
        print(json.dumps(checks, indent=2))
    else:
        for guide in sorted(results_by_guide):
            for check in sorted(results_by_guide[guide]):
                print(f"{guide} : {check.result.upper()} : {check.key} : {check.help}")

    if check_mode and errors_found:
        return ERROR_CODE
    else:
        return 0


if __name__ == "__main__":
    args = get_args()
    sys.exit(main(**vars(args)))
