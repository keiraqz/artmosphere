'''
Created on Sep 19, 2015
@author: Keira Zhou
'''

import os
import csv
import json
import subprocess
from sys import argv
from pprint import pprint


file_id = 0
source_file = '/home/ubuntu/Insight/dataset/Artsy/artworks/artwork_%d.txt' % file_id
target = open(source_file, 'w')

first_page = "'https://api.artsy.net/api/artworks'"
call_path = "curl -v %s -H 'X-Xapp-Token:JvTPWe4WsQO-xqX6Bts49tlrQV0OaoXmXFl8-RBueb0ZMGgKLlvXvxU3xw9a_qDnuGe2_DGF9-lPh9ToJ3s8_7CidpplHcmtsVHknm5uCmgRSKB9gvz3rHO2Riy-CbXv0LJ-FTjgk65xvR7dBsRCs62246kEN1UizlPCHiFCXtimXdjcNoj4oZMw7qUCwhk4UpzCqZQZcaZzbqx6Rd7CYSuqtQ0-9QP_SSFUZFyQ9D4='" % first_page
result = subprocess.check_output(call_path, shell=True)
json_output = json.loads(result)
artworks = json_output['_embedded']['artworks']
target.write(json.dumps(artworks))
file_id = file_id + 1
next_page = json_output['_links']['next']['href']
target.close()

while (next_page != "") :
    source_file = '/home/ubuntu/Insight/dataset/Artsy/artworks/artwork_%d.txt' % file_id
    target = open(source_file, 'w')
    call_path = "curl -v %s -H 'X-Xapp-Token:JvTPWe4WsQO-xqX6Bts49tlrQV0OaoXmXFl8-RBueb0ZMGgKLlvXvxU3xw9a_qDnuGe2_DGF9-lPh9ToJ3s8_7CidpplHcmtsVHknm5uCmgRSKB9gvz3rHO2Riy-CbXv0LJ-FTjgk65xvR7dBsRCs62246kEN1UizlPCHiFCXtimXdjcNoj4oZMw7qUCwhk4UpzCqZQZcaZzbqx6Rd7CYSuqtQ0-9QP_SSFUZFyQ9D4='" % next_page
    result = subprocess.check_output(call_path, shell=True)
    json_output = json.loads(result)
    artworks = json_output['_embedded']['artworks']
    target.write(json.dumps(artworks))
    
    file_id = file_id + 1
    next_page = json_output['_links']['next']['href']
    target.close()
