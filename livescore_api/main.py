import json
import logging
from sys import exit
import datetime
import requests
import warnings
from . import __repo__

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

now = datetime.datetime.now()

get_excep = lambda e: e.args[1] if len(e.args) > 1 else e

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    # "Origin" : "https://livescore.com",
}


class utils:
    import sqlite3

    conn = sqlite3.connect(":memory:")
    formats = ["html", "csv", "xlsx", "markdown", "xml", "json"]
    chosen_format = "json"
    chosen_output = "livescore"

    @staticmethod
    def error_handler(resp=None, exit_on_error=False, log=True):
        def decorator(func):
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # import traceback as tb

                    # tb.print_exc()
                    if log:
                        logging.debug(f"Function ({func.__name__}) : {get_excep(e)}")
                        logging.error(get_excep(e))
                    if exit_on_error:
                        exit(1)

                    return resp

            return main

        return decorator

    # @utils.error_handler(exit_on_error=True)
    @staticmethod
    def read_json(fnm):
        with open(fnm) as fh:
            return json.load(fh)

    @staticmethod
    def dump_json(*args, **kwargs):
        return json.dumps(*args, **kwargs)

    @staticmethod
    def write_json(fnm, data, *args, **kwargs):
        with open(fnm, "w") as fh:
            json.dump(data, fh, *args, **kwargs)

    @staticmethod
    def DataFrame(data, format):
        import pandas

        df = pandas.DataFrame(data)
        mapper = {
            "dict": df.to_dict,
            "csv": df.to_csv,
            "json": df.to_json,
            "xlsx": df.to_excel,
            "html": df.to_html,
            "xml": df.to_xml,
            "markdown": df.to_markdown,
        }
        return mapper[format]

    @classmethod
    def filter(
        cls,
        data: dict,
        country: str = None,
        league: str = None,
        name: str = None,
        status: str = None,
    ):
        r"""Filter entries
        :param data: List containing dictionary of matches
        :param country: Filter matches with country-name
        :param league : Filter matches with legeau+name
        :param name: Filter matches with team-name
        :param status: Filter matches with the status
        :type data: dict
        :type others: str
        :rtype: `pd.DataFrame`
        """
        import pandas as pd

        pd.DataFrame(data).to_sql("Livescore", cls.conn)
        name_query = (
            f"AND Home LIKE '%{name}%' OR Away LIKE '%{name}%' " if name else ""
        )
        league_query = f"AND League LIKE '%{league}%' " if league else ""
        country_query = f"AND Country LIKE '%{country}%' " if country else ""
        status = f"AND Status LIKE '%{status}%' " if status else ""
        sql = f"""SELECT * FROM Livescore WHERE Home IS NOT NULL { "".join([name_query,league_query,country_query,status]) };"""
        logging.debug(f"Executing sql : {sql}")
        df = pd.read_sql(sql, cls.conn)
        resp = cls.format(df)
        if cls.chosen_format in ("xlsx", "json"):
            resp = cls.reformat_json(json.loads(resp))
        return resp

    @classmethod
    def format(cls, df):
        r"""Manipulates data to required format
        :param df: `pd.DataFrame` object
        :type df: object `pd.DataFrame`
        :rtype: Instance of `pd.DataFrame`
        """
        if cls.chosen_format == "xlsx":
            df.to_excel(cls.chosen_output + ".xlsx")
            return df.to_json()

        mapper = {
            "csv": df.to_csv,
            "html": df.to_html,
            "markdown": df.to_markdown,
            "xml": df.to_xml,
            "json": df.to_json,
            "dict": df.to_dict,
        }
        return mapper[cls.chosen_format]()

    @classmethod
    def reformat_json(cls, reformatted):
        r"""Reformat json data from `pd.DataFrame` to list of dictionary
        :param reformatted: Jsonified str from `pd.DataFrame`
        :type: str
        :rtype: dict
        """
        resp = []
        if not isinstance(reformatted, dict):
            reformatted = json.loads(reformatted)
        if not "index" in reformatted.keys():
            for x in reformatted["Serial Id"].keys():
                hunted = {}
                for key in reformatted.keys():
                    hunted.update({key: reformatted[key].get(x)})
                resp.append(hunted)
            return resp

        for x in list(reformatted["index"].keys())[1:]:
            hunted = {}
            for val in list(reformatted.keys())[1:]:
                hunted.update({val: reformatted[val].get(x)})
            resp.append(hunted)
        return resp


class json_formatter:
    def __init__(self, data: dict, update: bool = False, config_file: str = None):
        r"""Intantiator
        :param data: Dict or Json response from Livescorem-API
        :type data: Dict
        :param update: Update data keys from online
        :type update: bool
        :param config_file: Path to .json file containing mappers
        :type config_file: str
        :rtype : None
        """
        if not isinstance(data, dict):
            data = json.loads(data)
        self.data = data
        self.mappers = {
            "Stages": "Stages",
            "Events": "Events",
            "T1": "T1",  # Home team dict
            "T2": "T2",  # Away team dict
        }
        self.targets = {
            # Intro
            "Serial Id": "Sid",
            "League": "Snm",
            "Country": "Cnm",
            # Events
            "Match Id": "Eid",
            "H Scores": "Tr1",
            "A Scores": "Tr2",
            "Kickoff": "Esd",
            "Status": "Eps",
            "Home": "Nm",
            "Away": "Nm",
            "H id": "ID",
            "A id": "ID",
        }
        if update:
            logging.info("Updating mappers from script official repo")
            self.update_keys()

        if config_file:
            logging.info(f"Updating mappers in path '{config_file}'")
            new_config = utils.read_json(config_file)
            self.mappers.update(new_config.get("mappers", self.mappers))
            self.targets.update(new_config.get("targets", self.targets))

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    @utils.error_handler()
    def update_keys(self) -> None:
        link = f"{__repo__}/raw/main/assets/config.json"
        resp = requests.get(link, timeout=30)
        if resp.ok:
            data = resp.json()
            self.mappers.update(data.get("mappers", self.mappers))
            self.targets.update(data.get("targets", self.targets))
        else:
            logging.warning(
                f"Failed to update keys : ({resp.status_code} - {resp.reason})"
            )
            logging.debug("Content :" + resp.text)

    def __get_intro(self, data: dict) -> dict:
        targets = list(self.targets.keys())[:3]
        resp = {}
        for key in targets:
            resp[key] = data.get(self.targets[key])
        return resp

    def __get_events(self, data: dict) -> dict:
        resp = {}
        targets = list(self.targets.keys())[3:8]
        for key in targets:
            resp[key] = data.get(self.targets[key])
        return resp

    def __get_team_info(self, data: dict) -> dict:
        resp = {}
        for x in range(2):
            if x == 0:
                T1 = data.get(self.mappers["T1"])[0]
                resp["Home"] = T1.get(self.targets["Home"])
                resp["H id"] = T1.get(self.targets["H id"])
            else:
                T2 = data.get(self.mappers["T2"])[0]
                resp["Away"] = T2.get(self.targets["Away"])
                resp["A id"] = T2.get(self.targets["A id"])
        return resp

    @utils.error_handler({})
    def main(
        self,
        max: int = 1000,
        filters: dict = {},
        output: str = None,
        format: str = "json",
    ):
        r"""Formats livescore data into readable dict
        :param max: Total number of matches to be returned
        :param filters: Key, value of entries to be filtered
        :type max: int
        :type filters: dict
        :param output: Path to save contents in case of `xlsx`
        :type output: str
        :param format: Output format `["html","csv","xlsx","markdown","xml"]`
        :type format: str
        :rtype: list of dict or `pd.DataFrame` if filters
        """
        response = []
        for x, entry in enumerate(self.data.get(self.mappers["Stages"]), start=1):
            Entry, resp = entry, {}
            resp.update(self.__get_intro(Entry))  # First 3 values of self.targets
            resp.update(
                self.__get_events(Entry.get(self.mappers["Events"])[0])
            )  ## handle events
            resp.update(self.__get_team_info(Entry.get(self.mappers["Events"])[0]))
            response.append(resp)
            if x == max:
                break
        if filters or not format == "json":
            logging.info(f"Using filters - {filters}")
            utils.chosen_output = output or utils.chosen_output
            utils.chosen_format = format
            return utils.filter(response, **filters)
        return response


class livescore:
    def __init__(
        self,
        date=now.day,
        month=now.month,
        year=now.year,
        country_code="KE",
        timeout=20,
    ):
        r"""Livescore instantiator
        :param date: Date of the matches
        :param month: Month of the matches
        :param year: Year of the matches
        :param country_code: Country code while making Http request
        :param timeout: Request timeout in seconds
        :type date: int|str
        :type month: int|str
        :type year: int|str
        :type country_code: str
        :type timeout: int
        """
        self.timeout = timeout
        self.url = f"https://prod-public-api.livescore.com/v1/api/app/date/soccer/{year}{str(month).zfill(2)}{str(date).zfill(2)}/3?MD=1&countryCode={country_code}"

    def __str__(self):
        return self.url

    def __call__(self, *args, **kwargs):
        return self.matches(*args, **kwargs)

    @utils.error_handler({})
    def matches(
        self,
        max: int = 1000,
        filters: dict = {},
        output: str = None,
        format: str = "json",
        raw: bool = False,
        headers: dict = headers,
    ):
        r"""Fetches data from Livescore and formats the
        :param max: Total number of matches to be returned
        :type max: int
        :param headers: Http Request headers to be used
        :type headers: dict
        :param filter: Keys, value of entries to be filtered
        :type filter: dict
        :param output: Path to save contents in case of `xlsx`
        :type output: str
        :param raw: Return unmanipulated content
        :type raw: dict
        :param format: Output format `["html","csv","xlsx","markdown","xml"]`
        :type format: str
        :rtype: list of dict
        """
        logging.info(f"Fetching matches from livescore with url - {self.url}")
        reqs = requests.get(self.url, timeout=self.timeout, headers=headers)
        if reqs.ok and reqs.headers.get("Content-Type") == "application/json":
            raw_content = reqs.json()
            if raw:
                return raw_content
            return json_formatter(data=raw_content).main(max, filters, output, format)
        else:
            logging.debug(
                f"Content-Type : {reqs.headers.get('content-type')} Content : {reqs.text}"
            )
            raise Exception(
                f"Failed to fetch required contents  : URL - {self.url}, STATUS_CODE - {reqs.status_code} , REASON - {reqs.reason}"
            )


if __name__ == "__main__":
    fnm = "livescore_matches_june_10_KE.json"
    with open(fnm) as fh:
        data = json.load(fh)
    run = json_formatter(data)
    resp = run.main(filters={"status": "FT", "country": "australia"}, format="json")
    index = 0
    # print(resp)
    print(json.dumps(resp, indent=5))
    # print(resp[index])
