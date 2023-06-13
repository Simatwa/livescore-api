from smartbets_API import rest_api, predictor
import logging


class Make:
    def __init__(
        self,
        matches: list,
        api: str = None,
        username: str = None,
        password: str = None,
        net: bool = True,
        include_position: bool = False,
        rest: bool = False,
    ):
        r"""Instantiates class
        :param matches: List of dictionary containing matches-info
        :param api: url pointing to prediction server
        :param include_position: Include teams's league position while making predictions
        :param rest: Use REST api in making predictions
        :type matches: list
        :type api:str
        :type include_position:bool
        :type rest: bool
        """
        if isinstance(matches, str):
            from .main import utils

            matches = utils.read_json(matches)
        self.matches = matches
        self.api = api
        self.username = username
        self.password = password
        self.net = net
        self.include_position = include_position
        self.rest = rest

    def __str__(self):
        return self.matches

    def __call__(self, progress_bar=True, *args, **kwargs):
        if progress_bar:
            return self.main_(*args, **kwargs)
        return self.main(*args, **kwargs)

    def __get_matches(self, match_info: dict):
        return dict(home=match_info["Home"], away=match_info["Away"], net=self.net)

    def main(self, limit: int = 1000, *args, **kwargs):
        r"""Predict maker
        :param limit: Maximum number of predictions to be made
        :param args: Positional arguments to be parsed to `predict` class
        :param kwargs: Keyworded arguments ti be parsed to `predict` class
        :type limit: int
        :type args: list|tuple
        :type kwargs: dict
        """

        resp = []
        if self.rest:

            logging.info(f"Making predictions using REST-API - '{self.api}'")
            engine = rest_api(self.api, self.password, self.username)

            for x, match in enumerate(self.matches):
                predictions = engine(**self.__get_matches(match))
                if predictions[0]:
                    match.update(predictions[1])
                    resp.append(match)
                else:
                    logging.error(
                        f"Failed to place predictions on - [{match['Home']} : {match['Away']}]"
                    )
                if x + 1 >= limit:
                    break

        else:
            logging.info("Making predictions using smartbetsAPI lib")
            kwargs["include_position"] = self.include_position
            engine = predictor(*args, **kwargs)
            for x, match in enumerate(self.matches):
                predictions = engine.predictorL(
                    **dict(teams=[match["Home"], match["Away"]], net=self.net)
                )
                match.update(predictions)
                resp.append(match)

                if x + 1 >= limit:
                    break

        return resp

    def main_(self, limit: int = 1000, *args, **kwargs):
        r"""Predict maker
        :param limit: Maximum number of predictions to be made
        :param args: Positional arguments to be parsed to `predict` class
        :param kwargs: Keyworded arguments ti be parsed to `predict` class
        :type limit: int
        :type args: list|tuple
        :type kwargs: dict
        """

        resp = []

        from tqdm import tqdm
        from colorama import Fore

        tqdm_kwargs = dict(
            total=len(self.matches) if limit == 1000 else limit,
            bar_format="%s{bar}%s {l_bar}%s" % (Fore.CYAN, Fore.YELLOW, Fore.RESET),
        )

        if self.rest:

            logging.info(f"Making predictions using REST-API - '{self.api}'")
            engine = rest_api(self.api, self.password, self.username)
            with tqdm(**tqdm_kwargs) as progress_bar:
                for x, match in enumerate(self.matches):
                    predictions = engine(**self.__get_matches(match))
                    if predictions[0]:
                        match.update(predictions[1])
                        resp.append(match)
                    else:
                        logging.error(
                            f"Failed to place predictions on - [{match['Home']} : {match['Away']}]"
                        )
                    progress_bar.update(1)
                    if x + 1 >= limit:
                        break

        else:
            logging.info("Making predictions using smartbetsAPI lib")
            kwargs["include_position"] = self.include_position
            engine = predictor(*args, **kwargs)
            with tqdm(**tqdm_kwargs) as progress_bar:
                for x, match in enumerate(self.matches):
                    predictions = engine.predictorL(
                        **dict(teams=[match["Home"], match["Away"]], net=self.net)
                    )
                    match.update(predictions)
                    resp.append(match)
                    progress_bar.update(1)
                    if x + 1 >= limit:
                        break

        return resp
