import livescore_api as api
import logging

run = api.json_formatter(open("matches.json").read())
# resp = run.main()
print(run())
