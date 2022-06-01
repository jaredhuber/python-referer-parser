from dataclasses import dataclass
from referer_parser import Referer
import json
import os
from urllib import parse

landing_url = 'https://opensea.io/assets/solana/CckU35RbCcz5m75if8pXcmeTs7dYR7SJPPBSwQTbYTeE?utm_campaign=paid_search_direct_to_pdp&utm_source=google&utm_medium=search'
referer_url = 'http://www.google.com/search?q=gateway+oracle+cards+denise+linn&hl=en&client=safari'


def load_utms(json_file):
    referers_dict = {}
    with open(json_file) as json_content:
        for medium, conf_list in iteritems(json.load(json_content)):
            for referer_name, config in iteritems(conf_list):
                params = None
                if 'parameters' in config:
                    params = list(map(text_type.lower, config['parameters']))
                for domain in config['domains']:
                    referers_dict[domain] = {
                        'name': referer_name,
                        'medium': medium
                    }
                    if params is not None:
                        referers_dict[domain]['params'] = params
    return referers_dict

#JSON_FILE = os.path.join(os.path.dirname(__file__), 'data', 'utm_params.json')

JSON_FILE = 'referer_parser/data/utm_params.json'

with open(JSON_FILE) as json_content:
    utms = json.load(json_content)

this_url_dict = parse.parse_qs(parse.urlsplit(landing_url).query)

source_data = {i : ""  for i in utms.keys()}
params_whitelist = [v["param"] for k,v in utms.items()]
params_friendly = [k for k,v in utms.items()]
requireds = [k for k,v in utms.items() if v["required"] == "True"]

for i in this_url_dict.keys():
    if i in params_whitelist:
        index = params_whitelist.index(i)
        source_data[params_friendly[index]] = this_url_dict[i][0]
    else:
        pass
    #check requireds
if len([(k,v) for k,v in source_data.items() if (k in requireds and v == '')]) != 0:
    r = Referer(referer_url)
    source_data['channel'] = r.medium
    source_data['source'] = r.referer
    source_data['search_keyword'] = r.search_term
        

print(source_data)