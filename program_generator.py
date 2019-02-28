#!/usr/bin/env python3

import yaml
import glob
import copy
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Create program')
parser.add_argument('date', type=str, help='date of toastmaster program')
parser.add_argument('--last-tme', type=str, help='override last TME')
parser.add_argument('--presenter', '-p', type=str, help='add presenter', action="append", dest="presenters", default=[])
args = parser.parse_args()
date = args.date
last_tme = args.last_tme
presenters = args.presenters

# delete existing
if os.path.isfile("_programs/{}.md".format(date)):
    os.remove("_programs/{}.md".format(date))

# load members and their order
with open("_data/members.yml") as f:
    members = yaml.load(f)

member_list_names = list(members.keys())

# presentaiton count dict
presentation_score_dict = {}
for i in member_list_names:
    presentation_score_dict[i] = 0
program_list = sorted(glob.glob('_programs/*'))

# list down the number of times gust did speeches
for prog_idx, prog in enumerate(program_list):
    with open(prog) as f:
        for doc in yaml.safe_load_all(f):
            for pres in doc['prog']['presentations']:
                if pres['id'] in presentation_score_dict:
                    if prog_idx < len(program_list) - 3:
                        presentation_score_dict[pres['id']] += 1
                    else:
                        presentation_score_dict[pres['id']] += 100
            break

# load last program
program_list = sorted(glob.glob('_programs/*'))
with open(program_list[-1]) as f:
    for doc in yaml.safe_load_all(f):
        last_program = doc
        break
if last_tme is None:
    last_tme = last_program['prog']['tme']

# get next tme
next_tme_index = None
for index, member in enumerate(member_list_names):
    if member == last_tme:
        # select next
        next_tme_index = index+1
        # wrap around
        if len(members) <= next_tme_index:
            next_tme_index = 0

if next_tme_index is None:
    raise "next TME unknown"

roles = ["tme", "declaration", "welcoming_of_guests", "introduction_of_tme", "table_topics", "word_of_the_day", "timer", "ahh_counter","food"]

new_program = copy.deepcopy(last_program)



# who sould present next?
new_program['prog']['presentations'] = []
presentation_score_list = []
for i, p in presentation_score_dict.items():
    presentation_score_list.append({"id": i, "score": p})
presentation_score_list = sorted(presentation_score_list, key=lambda x: x['score'], reverse=False)

# override
if len(presenters) > 0:
    presentation_score_list = [{"id": p} for p in presenters]

presenter_list = []
for i in range(2):
    presenter_list.append(presentation_score_list[i]['id'])
    new_program['prog']['presentations'].append({
        "id": presentation_score_list[i]['id'],
        "project": "--project name--",
        "title": "--title--",
        "evaluator": "--evaluator--",
        "hide": False
    })

# roles
member_for_role_list = copy.copy(member_list_names)
# if presenter, give no role
for p in presenter_list:
    member_for_role_list.remove(p)
for i, r in enumerate(roles):
    next_index = next_tme_index+i
    if next_index >= len(member_list_names):
        next_index = next_index % len(member_list_names)



    new_program['prog'][r] = member_for_role_list[next_index]


new_program['title'] = "---"
new_program['prog']['general_evaluator'] = "--general evaluator--"
new_program['prog']['table_topics_evaluator'] = "--general evaluator--"
new_program['prog']['call_to_order'] = "g.ricalde"
new_program['prog']['closing_remarks'] = "g.ricalde"
new_program['prog']['date'] = "{} 19:00:00 +0800".format(date)



yaml_str = yaml.dump(new_program)

with open("_programs/{}.md".format(date),"w") as f:
    f.write("---\n")
    f.write(yaml_str)
    f.write("\n---")