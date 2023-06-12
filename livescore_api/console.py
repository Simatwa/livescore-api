from . import __version__, __repo__,__info__,__program__
from .main import livescore,now,json_formatter,utils
import logging
import argparse

logging.basicConfig(format="%(asctime)s : %(levelname)s - %(message)s",datefmt="%H:%M:%S", level=logging.INFO)

class Enter:
	
	output_formats = ["html","csv","xlsx","markdown","xml","json"]
	filters = ["country","league","name","status"]
	tables = ["html","pretty","grid","fancy_grid","orgtbl","secure_html"]
	@classmethod
	def get_args(cls):
		parser = argparse.ArgumentParser(description=__info__,epilog="This script has no official relation with Livescore.com",exit_on_error=True,add_help=True)
		parser.add_argument("-v","--version",action="version",version=f"{__program__} v{__version__}")
		parser.add_argument("date",nargs="?",help="Date of the matches - %(default)s",type=int,default=now.day)
		parser.add_argument("-m","--month",help="Month of the matches - %(default)s",type=int,default=now.month)
		parser.add_argument("-y","--year",help="Year of the matches - %(default)s",type=int,default=now.year,)
		parser.add_argument("-c","--country",help="Return matches from the specified countries only - %(default)s")
		parser.add_argument("-l","--league",help="Return matches of the specified league(s) only - %(default)s")
		parser.add_argument("-n","--name",help="Return matches with the specified team-name only - %(default)s")
		parser.add_argument("-s","--status",help="Return matches of the specified status - %(default)s",)
		parser.add_argument("-M","--max",type=int,help="Maximum matches to be returned - %(default)s",default=1000)
		parser.add_argument("-H","--headers",help="Path to .json file containing http headers - %(default)s",)
		parser.add_argument("-o","--output",help="Path to save the content - %(default)s",metavar="PATH")
		parser.add_argument("-f","--format",help="Contents output format - %(default)s",choices=cls.output_formats,metavar="|".join(cls.output_formats),default="json")
		parser.add_argument("-i","--input",help="Use .json formatted file in path - %(default)s",metavar="PATH")
		parser.add_argument("-t","--tabulate",help="Tabulate the contents using style specified",choices=cls.tables,metavar="|".join(cls.tables))
		parser.add_argument("--code",help="Country code for making http request - %(default)s",default="KE")
		parser.add_argument("--timeout",help="Http request timeout - %(default)ss",default=20,type=int)
		parser.add_argument("--indent",help="Indentation level for formatting .json output - %(default)s",type=int,default=4)
		parser.add_argument("--config",help="Use mapper-keys in path",metavar="PATH")
		parser.add_argument("--update",help="Update mapper-keys from repo",action="store_true")
		parser.add_argument("--raw",help="Return contents with zero manipulation",action="store_true")
		return parser.parse_args()
	
@utils.error_handler()
def main():
	args = Enter.get_args()
	
	filters = {"country":args.country,"league":args.league,"name":args.name,"status":args.status}
	
	main_filter = {"max":args.max,"filters": filters,"output":args.output,"format":args.format}
	
	if args.input:
		data= utils.read_json(args.input)
		run = json_formatter(data,args.update,args.config)
		resp = run.main(**main_filter)
		
	else:
		run=livescore(**dict(date=args.date,month=args.month,year=args.year,country_code=args.code,timeout=args.timeout))
		
		if args.headers:
			main_filter["headers"] = utils.read_json(args.headers)
		main_filter["raw"] = args.raw
		resp = run.matches(**main_filter)
		
	if isinstance(resp,list):
		if args.tabulate:
			from tabulate import tabulate
			resp = tabulate(resp,headers="keys",tablefmt=args.tabulate)
		else:
			resp = {"matches":resp}
			resp = utils.dump_json(resp,indent=args.indent)
	
	if isinstance(resp,dict) and args.raw:
		resp = utils.dump_json(resp,indent=args.indent)
	if args.output:
		with open(args.output,"w") as fh:
			fh.write(resp)
	else:
		print(resp)
			