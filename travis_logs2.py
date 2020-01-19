import http.client
import wrapt


def wrapper(wrapped, instance, args, kwargs):
    s=  wrapped(*args, **kwargs)
    print("HACK",s)
    print("HACK",s.content)
    
    return s
def wrapper2(wrapped, instance, args, kwargs):
    s=  wrapped(*args, **kwargs)
    for x in s:
        print("HACK",x)
    return s

#wrapt.wrap_function_wrapper(http.client, 'HTTPResponse.read', wrapper)
#wrapt.wrap_function_wrapper(http.client, 'HTTPResponse._safe_read', wrapper)

import urllib3.response
#wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.read_chunk', wrapper)
#wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.stream', wrapper2)
#wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.__iter__', wrapper2)
import requests

if False:
    HTTPConnection.debuglevel = 1
    for method in ["get", "post", "put", "patch", "delete"]:
        wrapt.wrap_function_wrapper(requests,  method, wrapper)


# hack
#http.client.HTTPResponse = MyResponse

#import requests_debugger

import pprint
import logging
#logging.basicConfig(level=logging.DEBUG)

import contextlib

from http.client import HTTPConnection # py3



# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
# requests_log = logging.getLogger("requests.packages.urllib3.connectionpool")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
                                        

if __name__ == '__main__':
    import os
    import sys
    from pathlib import Path
    tokenfile = str(Path.home() / Path(".travis") / Path("token"))
    token = open(tokenfile).read().strip()

    from travispy import TravisPy
    t = TravisPy(token)
    print(token)
    user = t.user()
    print(user)
#    print(dir(user))
    #<travispy.entities.user.User object at 0x02C26C48>

    repos = user.repos()
    
    #repos = t.repos(member=user.login)

    #'id': 25345664, 'name': 'introspector-data-linux'
    #for x in repos['repositories']:
    #    if 
    #    print(x)
        
        # print (x.id)
        # print ("lastbuild",x.last_build)
        # print (x.last_build_number)
        # print (x.last_build_state)
        # print (x.slug)
        # print (x.description)

    #x = t.repo("25345664")[0]
    x = t.builds(repository_id="25345664")
    #print("getting builds",x)
    for build in x:
        print("build",build.id)
        b = t.build(build.id)

        print("jobids",b.jobs)
        for job in b.jobs:
            print("job",job.id)
            l = job.log
            for line in l['content'].split("\n"):
                print(line)
            
        #print("jobids",b.job_ids)
        #print(dir(b))
        
        #print(build.href)
    #pprint.pprint(x)
    #print (x.id)
    #print ("lastbuild",x.last_build)
    #print (x.last_build_number)
    #print (x.last_build_state)
    # print (x.slug)
    # print (x.description)
    # #print (x.slug)
    # print (dir(x))
    # #for f in dir(x):
    # #    print(f, getattr(x, f)())
    #     #pprint.pprint (x.__dict__)
    # build = t.build(repo.last_build_id)
