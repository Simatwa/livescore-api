from . import __version__, __repo__, __info__, __program__
from .main import livescore, now, json_formatter, utils
import logging
import argparse

logging.basicConfig(
    format="%(asctime)s : %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


class Enter:

    output_formats = ["html", "csv", "xlsx", "markdown", "xml", "json"]
    filters = ["country", "league", "name", "status"]
    tables = ["html", "pretty", "grid", "fancy_grid", "orgtbl", "secure_html"]

    @classmethod
    def get_args(cls):
        parser = argparse.ArgumentParser(
            description=__info__,
            epilog="This script has no official relation with Livescore.com",
            exit_on_error=True,
            add_help=True,
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"{__program__} v{__version__}"
        )
        parser.add_argument(
            "date",
            nargs="?",
            help="Date of the matches - %(default)s",
            type=int,
            default=now.day,
        )
        parser.add_argument(
            "-m",
            "--month",
            help="Month of the matches - %(default)s",
            type=int,
            default=now.month,
        )
        parser.add_argument(
            "-y",
            "--year",
            help="Year of the matches - %(default)s",
            type=int,
            default=now.year,
        )
        parser.add_argument(
            "-c",
            "--country",
            help="Return matches from the specified countries only - %(default)s",
        )
        parser.add_argument(
            "-l",
            "--league",
            help="Return matches of the specified league(s) only - %(default)s",
        )
        parser.add_argument(
            "-n",
            "--name",
            help="Return matches with the specified team-name only - %(default)s",
        )
        parser.add_argument(
            "-s",
            "--status",
            help="Return matches of the specified status - %(default)s",
        )
        parser.add_argument(
            "-M",
            "--max",
            type=int,
            help="Maximum matches to be returned - %(default)s",
            default=1000,
        )
        parser.add_argument(
            "-H",
            "--headers",
            help="Path to .json file containing http headers - %(default)s",
        )
        parser.add_argument(
            "-o",
            "--output",
            help="Path to save the content - %(default)s",
            metavar="PATH",
        )
        parser.add_argument(
            "-f",
            "--format",
            help="Contents output format - %(default)s",
            choices=cls.output_formats,
            metavar="|".join(cls.output_formats),
            default="json",
        )
        parser.add_argument(
            "-i",
            "--input",
            help="Use .json formatted file in path - %(default)s",
            metavar="PATH",
        )
        parser.add_argument(
            "-t",
            "--tabulate",
            help="Tabulate the contents using style specified - %(default)s",
            choices=cls.tables,
            metavar="|".join(cls.tables),
        )
        parser.add_argument(
            "-D",
            "--code",
            help="Country code for making http request - %(default)s",
            default="KE",
        )
        parser.add_argument(
            "-E",
            "--timeout",
            help="Http request timeout - %(default)ss",
            default=20,
            type=int,
        )
        parser.add_argument(
            "-I",
            "--indent",
            help="Indentation level for formatting .json output - %(default)s",
            type=int,
            default=4,
        )
        parser.add_argument(
            "-C",
            "--config",
            help="Use mapper-keys in path - %(default)s",
            metavar="PATH",
        )
        parser.add_argument(
            "--update",
            help="Update mapper-keys from repo - %(default)s",
            action="store_true",
        )
        parser.add_argument(
            "--raw",
            help="Return contents with zero manipulation - %(default)s",
            action="store_true",
        )
        parser.add_argument(
            "--predict",
            help="Proceed to make predictions - %(default)s",
            action="store_true",
        )
        parser.add_argument(
            "-U",
            "--username",
            help="Username for the REST api - %(default)s",
            default="API",
        )
        parser.add_argument(
            "-P",
            "--password",
            help="Passkey for the REST api - %(default)s",
            default="developer",
        )
        parser.add_argument(
            "-S",
            "--server",
            help="Url pointing to REST api - %(default)s",
            default="http://localhost:8000",
        )
        parser.add_argument(
            "-T",
            "--limit",
            help="Limit number of matches for prediction - %(default)s",
            default=1000,
            type=int,
        )
        parser.add_argument(
            "--offline",
            help="Make predictions based on data available offline - %(default)s",
            action="store_true",
        )
        parser.add_argument(
            "--REST",
            help="Specifies to make predictions using REST api - %(default)s",
            action="store_true",
        )
        parser.add_argument(
            "--include-position",
            help="Include team-league rank in making predictions - %(default)s",
            action="store_true",
        )
        return parser.parse_args()


@utils.error_handler(exit_on_error=True)
def main():
    args = Enter.get_args()

    filters = {
        "country": args.country,
        "league": args.league,
        "name": args.name,
        "status": args.status,
    }

    main_filter = {
        "max": args.max,
        "filters": filters,
        "output": args.output,
        "format": "json" if any([args.predict, args.REST]) else args.format,
    }

    if args.input:
        data = utils.read_json(args.input)
        run = json_formatter(data, args.update, args.config)
        resp = run.main(**main_filter)

    else:
        run = livescore(
            **dict(
                date=args.date,
                month=args.month,
                year=args.year,
                country_code=args.code,
                timeout=args.timeout,
            )
        )

        if args.headers:
            main_filter["headers"] = utils.read_json(args.headers)
        main_filter["raw"] = args.raw
        resp = run.matches(**main_filter)

    if isinstance(resp, list):
        if len(resp) > args.max:
            resp = resp[:max]

        if any([args.predict, args.REST]):

            from .predictor import Make

            run = Make(
                matches=resp,
                username=args.username,
                password=args.password,
                api=args.server,
                net=args.offline == False,
                include_position=args.include_position,
                rest=args.REST,
            )
            resp = run(limit=args.limit)
            df_object = utils.DataFrame(resp, args.format)
            if args.format in ("xlsx"):
                df_object(
                    args.output
                    or f"predictions_{args.date}_{args.month}_{args.year}.xlsx"
                )
                return
            resp = df_object()
            if args.format in ("json"):
                resp = utils.reformat_json(resp)

    if args.tabulate and isinstance(resp, (dict, list)):
        from tabulate import tabulate

        resp = tabulate(resp, headers="keys", tablefmt=args.tabulate)

    elif isinstance(resp, (dict, list)):
        resp = utils.dump_json(
            resp if args.raw else {"matches": resp}, indent=args.indent
        )

    if args.output:

        logging.info(f"Saving contents to '{args.output}'")
        with open(args.output, "w") as fh:
            fh.write(resp)
    else:
        print(resp)
