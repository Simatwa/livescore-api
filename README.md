# Livescore-api
<p align="center">
<a href="https://github.com/Simatwa/livescore-api/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/livescore-api/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/livescore-api"><img alt="PyPi" src="https://img.shields.io/static/v1?logo=pypi&label=Pypi&message=v0.0.4&color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/static/v1?logo=Black&label=Code-style&message=Black"/></a>
<a href="#"><img alt="Passing" src="https://img.shields.io/static/v1?logo=Docs&label=Docs&message=Passing&color=green"/></a>
<a href="#"><img alt="coverage" src="https://img.shields.io/static/v1?logo=Coverage&label=Coverage&message=60%&color=yellowgreen"/></a>
<a href="#" alt="progress"><img alt="Progress" src="https://img.shields.io/static/v1?logo=Progress&label=Progress&message=95%&color=green"/></a>
<a href="https://pepy.tech/project/livescore-api"><img src="https://static.pepy.tech/personalized-badge/livescore-api?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads" alt="Downloads"></a>
</p>

**Access and manipulate football data from [Livescore](https://livescore.com).**

## Installation

1. From pip

```sh
pip install livescore-api
```

2. From source

- Clone repo and install

```sh
git clone https://github.com/Simatwa/livescore-api.git
cd livescore-api
pip install .
```

## Usage

- `$ livescore-api`

<details>
<summary>

### Developer docs

</summary>

1. Retrieving data offline

```py
from livescore_api import json_formatter
raw_matches = open("matches.json").read()
sorted_matches = json_formatter(raw_matches)
print(sorted_matches(max=1))

"""
Output
[
{
    "Serial Id": "12413",
    "League": "Primera Division",
    "Country": "Argentina",
    "Match Id": "866073",
    "H Scores": "1",
    "A Scores": "4",
    "Kickoff": 20230613011500,
    "Status": "FT",
    "Home": "Banfield",
    "H id": "5252",
    "Away": "River Plate",
    "A id": "4802"
}
]
"""
```

2. Retrieving data online

```py
from livescore_api import livescore

matches = livescore()
print(matches(max=1))

"""
Output

[
{
    "Serial Id": "12413",
    "League": "Primera Division",
    "Country": "Argentina",
    "Match Id": "866073",
    "H Scores": "1",
    "A Scores": "4",
    "Kickoff": 20230613011500,
    "Status": "FT",
    "Home": "Banfield",
    "H id": "5252",
    "Away": "River Plate",
    "A id": "4802"
}
]
"""
```

3. Making predictions

```py
from livescore_api import Make
matches = [{"Home":"Arsenal", "Away":"Liverpool"}]
bet = Make(matches)
print(bet())

"""
Output

[{'Home': 'Arsenal', 'Away': 'Liverpool', 'g': 10.0, 'gg': 55.0, 'ov15': 60.0, 'ov25': 45.0, 'ov35': 25.0, 'choice': 62.5, 'result': '2', 'pick': '2'}]
"""

```
</details>

</summary>

<details>

<summary>

For more info run `$ livescore-api -h`

</summary>

```
usage: livescore-api [-h] [-v] [-m MONTH] [-y YEAR] [-c COUNTRY]
                     [-l LEAGUE] [-n NAME] [-s STATUS] [-M MAX]
                     [-H HEADERS] [-o PATH]
                     [-f html|csv|xlsx|markdown|xml|json] [-i PATH]
                     [-t html|pretty|grid|fancy_grid|orgtbl|secure_html]
                     [-D CODE] [-E TIMEOUT] [-I INDENT] [-C PATH]
                     [--update] [--raw] [--predict] [-U USERNAME]
                     [-P PASSWORD] [-S SERVER] [-T LIMIT] [--offline]
                     [--REST] [--include-position]
                     [date]

Access and manipulate matches from Livescore.com

positional arguments:
  date                  Date of the matches - 13

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -m MONTH, --month MONTH
                        Month of the matches - 6
  -y YEAR, --year YEAR  Year of the matches - 2023
  -c COUNTRY, --country COUNTRY
                        Return matches from the specified countries only
                        - None
  -l LEAGUE, --league LEAGUE
                        Return matches of the specified league(s) only -
                        None
  -n NAME, --name NAME  Return matches with the specified team-name only
                        - None
  -s STATUS, --status STATUS
                        Return matches of the specified status - None
  -M MAX, --max MAX     Maximum matches to be returned - 1000
  -H HEADERS, --headers HEADERS
                        Path to .json file containing http headers - None
  -o PATH, --output PATH
                        Path to save the content - None
  -f html|csv|xlsx|markdown|xml|json, --format html|csv|xlsx|markdown|xml|json
                        Contents output format - json
  -i PATH, --input PATH
                        Use .json formatted file in path - None
  -t html|pretty|grid|fancy_grid|orgtbl|secure_html, --tabulate html|pretty|grid|fancy_grid|orgtbl|secure_html
                        Tabulate the contents using style specified -
                        None
  -D CODE, --code CODE  Country code for making http request - KE
  -E TIMEOUT, --timeout TIMEOUT
                        Http request timeout - 20s
  -I INDENT, --indent INDENT
                        Indentation level for formatting .json output - 4
  -C PATH, --config PATH
                        Use mapper-keys in path - None
  --update              Update mapper-keys from repo - False
  --raw                 Return contents with zero manipulation - False
  --predict             Proceed to make predictions - False
  -U USERNAME, --username USERNAME
                        Username for the REST api - API
  -P PASSWORD, --password PASSWORD
                        Passkey for the REST api - developer
  -S SERVER, --server SERVER
                        Url pointing to REST api - http://localhost:8000
  -T LIMIT, --limit LIMIT
                        Limit number of matches for prediction - 1000
  --offline             Make predictions based on data available offline
                        - False
  --REST                Specifies to make predictions using REST api -
                        False
  --include-position    Include team-league rank in making predictions -
                        False

This script has no official relation with Livescore.com
```
</details>

## Disclaimer

This script utilizes the Livescore API to provide live scores and other information about sporting events. The Livescore-API is a third-party service and is not affiliated with any specific sporting event or organization. The accuracy of the information provided by the Livescore API is not guaranteed and may vary depending on a number of factors, including the availability of data and the quality of the data. The user of this script assumes all responsibility for any  legal action, errors or omissions in the information provided by the Livescore API.

<details>

<summary>

Author

</summary>

The author of this script makes no representations or warranties, express or implied, about the accuracy, completeness, or suitability of the information provided by the Livescore API. The author of this script accepts no liability for any legal action,  errors or omissions in the information provided by the Livescore API.

**Note** : This is just for information purposes do not sue me.
</details>
