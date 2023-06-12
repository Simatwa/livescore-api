# Livescore-api
**Access and manipulate football data from [Livescore](https://livescore.com).**

## Installation

1. From pip (soon)

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
* For more info run `$ livescore-api -h`
</summary>

```
usage: livescore-api [-h] [-v]
                     [-m MONTH]
                     [-y YEAR]
                     [-c COUNTRY]
                     [-l LEAGUE]
                     [-n NAME]
                     [-s STATUS]
                     [-M MAX]
                     [-H HEADERS]
                     [-o PATH]
                     [-f html|csv|xlsx|markdown|xml|json]
                     [-i PATH]
                     [-t html|pretty|grid|fancy_grid|orgtbl|secure_html]
                     [--code CODE]
                     [--timeout TIMEOUT]
                     [--indent INDENT]
                     [--config PATH]
                     [--update]
                     [--raw]
                     [date]

Access and manipulate matches from
Livescore.com

positional arguments:
  date         Date of the matches
               - 12

optional arguments:
  -h, --help   show this help
               message and exit
  -v, --version
               show program's
               version number and
               exit
  -m MONTH, --month MONTH
               Month of the matches
               - 6
  -y YEAR, --year YEAR
               Year of the matches
               - 2023
  -c COUNTRY, --country COUNTRY
               Return matches from
               the specified
               countries only -
               None
  -l LEAGUE, --league LEAGUE
               Return matches of
               the specified
               league(s) only -
               None
  -n NAME, --name NAME
               Return matches with
               the specified team-
               name only - None
  -s STATUS, --status STATUS
               Return matches of
               the specified status
               - None
  -M MAX, --max MAX
               Maximum matches to
               be returned - 1000
  -H HEADERS, --headers HEADERS
               Path to .json file
               containing http
               headers - None
  -o PATH, --output PATH
               Path to save the
               content - None
  -f html|csv|xlsx|markdown|xml|json, --format html|csv|xlsx|markdown|xml|json
               Contents output
               format - json
  -i PATH, --input PATH
               Use .json formatted
               file in path - None
  -t html|pretty|grid|fancy_grid|orgtbl|secure_html, --tabulate html|pretty|grid|fancy_grid|orgtbl|secure_html
               Tabulate the
               contents using style
               specified
  --code CODE  Country code for
               making http request
               - KE
  --timeout TIMEOUT
               Http request timeout
               - 20s
  --indent INDENT
               Indentation level
               for formatting .json
               output - 4
  --config PATH
               Use mapper-keys in
               path
  --update     Update mapper-keys
               from repo
  --raw        Return contents with
               zero manipulation

This script has no official
relation with Livescore.com
```
</details>

