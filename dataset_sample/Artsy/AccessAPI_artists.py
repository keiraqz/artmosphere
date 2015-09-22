'''
Created on Sep 19, 2015

@author: Shanghai
'''

import os
import csv
import json
import subprocess
from sys import argv
from pprint import pprint

# source_file = '/Users/Shanghai/Developer/Java/workspace/GetArtsy/gene_id_list.txt'
file_id = 0
source_file = '/home/ubuntu/Insight/dataset/Artsy/artists/artists_%d.txt' % file_id
target = open(source_file, 'w')

first_page = "'https://api.artsy.net/api/artists'"
call_path = "curl -v %s -H 'X-Xapp-Token:JvTPWe4WsQO-xqX6Bts49tlrQV0OaoXmXFl8-RBueb0ZMGgKLlvXvxU3xw9a_qDnuGe2_DGF9-lPh9ToJ3s8_7CidpplHcmtsVHknm5uCmgRSKB9gvz3rHO2Riy-CbXv0LJ-FTjgk65xvR7dBsRCs62246kEN1UizlPCHiFCXtimXdjcNoj4oZMw7qUCwhk4UpzCqZQZcaZzbqx6Rd7CYSuqtQ0-9QP_SSFUZFyQ9D4='" % first_page
result = subprocess.check_output(call_path, shell=True)
json_output = json.loads(result)
artworks = json_output['_embedded']['artists']
target.write(json.dumps(artworks))

file_id = file_id + 1
next_page = json_output['_links']['next']['href']

target.close()

while (next_page != "") :
    source_file = '/home/ubuntu/Insight/dataset/Artsy/artists/artists_%d.txt' % file_id
    target = open(source_file, 'w')
    call_path = "curl -v %s -H 'X-Xapp-Token:JvTPWe4WsQO-xqX6Bts49tlrQV0OaoXmXFl8-RBueb0ZMGgKLlvXvxU3xw9a_qDnuGe2_DGF9-lPh9ToJ3s8_7CidpplHcmtsVHknm5uCmgRSKB9gvz3rHO2Riy-CbXv0LJ-FTjgk65xvR7dBsRCs62246kEN1UizlPCHiFCXtimXdjcNoj4oZMw7qUCwhk4UpzCqZQZcaZzbqx6Rd7CYSuqtQ0-9QP_SSFUZFyQ9D4='" % next_page
    result = subprocess.check_output(call_path, shell=True)
    json_output = json.loads(result)
    artworks = json_output['_embedded']['artists']
    target.write(json.dumps(artworks))
    
    file_id = file_id + 1
    next_page = json_output['_links']['next']['href']
    target.close()




# def genData():
#     while True:
#         with open(source_file) as f:
#             for line in f:
#                 # print line
#                 # producer.send(topic, key, line.rstrip())
#                 call_path = "curl -v 'https://api.artsy.net/api/genes/%s' -H 'X-Xapp-Token:JvTPWe4WsQO-xqX6Bts49tlrQV0OaoXmXFl8-RBueb0ZMGgKLlvXvxU3xw9a_qDnuGe2_DGF9-lPh9ToJ3s8_7CidpplHcmtsVHknm5uCmgRSKB9gvz3rHO2Riy-CbXv0LJ-FTjgk65xvR7dBsRCs62246kEN1UizlPCHiFCXtimXdjcNoj4oZMw7qUCwhk4UpzCqZQZcaZzbqx6Rd7CYSuqtQ0-9QP_SSFUZFyQ9D4='" % line
#                 os.system(call_path) 
#         f.close()
# 
# genData()

