#! /usr/bin/env python3

import re, sys
import urllib.request as url


issue_head = "http://www.eemaata.com/em/category/issues/"
issue_ids = ("201301","201211","201209","201207","201205","201203","201201","201111",
             "201109","201107","201105","201103","201101","201011","201009","201007",
             "201005","201003","201001","200911","200909","200907","200905","200903",
             "200901","200811","200809","200807","200806","200805","200803","200801",
             "200711","200709","200707","200705","200703","200701","200611","200609",
             "200607","200605","200603","200601","200511","200509","200507","200505",
             "200503","200501","200411","200409","200407","200403","200401","200311",
             "200309","200307","200305","200303","200301","200211","200209","200207",
             "200205","200203","200201","200111","200107","200105","200103","200101",
             "200011","200009","200007","200005","200003","200001","199911","199909",
             "199907","199903","199901","199810")

store = {}
for issue_id in issue_ids:
    #Fetch the issue
    print("Fetching : ", issue_id)
    issue = url.urlopen(issue_head+issue_id+"/")
    content = issue.read().decode('utf-8')
    pattern = re.compile(issue_id + r"\/(\d+)", re.S)

    for m in pattern.finditer(content):
        id = m.group(1)
        store[id] = issue_id

print(store)

if False:
    import pickle
    pickle.dump(store, open("artid_issueid_dict.pickle"))


