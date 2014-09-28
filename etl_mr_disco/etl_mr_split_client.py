#!/usr/bin/env python
"""
LiveMR returns a JSON like dict of the imput 30 minute stream:

 {client: {
   cid: "row['clientKey']",
   videos: {
     video: {
      url: row['query']['u']}
      length: ""
      users: {
       user: {
        uname:  "row['query']['uid']",
        events: "row['query']['a'],row['query']['a'],..."
        times:  "row['timestamp'] ,row['timestamp'] ,..."},
        {uname: "", events: "", times: ""},
        {...}},
      {user: {}},
      {user: {}}},
     {video: {users: {user: {...}}}},
     {video: {users: {user: {...}}}}}
    {cid: {videos: {video: {users: {user: {...}}}}},
    {cid: {videos: {video: {users: {user: {...}}}}}
 }

base chunks:
base_user[uname] = [events: "", times: ""]
base_videos[url] = [base_user,base_user]

clients[client] = {videos= {users={[name:"",events:"",times:""]}}}
"""

from disco.core import Job, result_iterator

def map(line, params):
    for word in line.split():
        yield word, 1

def reduce(iter, params):
    from disco.util import kvgroup
    for word, counts in kvgroup(sorted(iter)):
        yield word, sum(counts)

if __name__ == '__main__':
    job = Job()
    run_with = disco.ddfs.DDFS().list(prefix="events:time")[-4:]
    print run_with
