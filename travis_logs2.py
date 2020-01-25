import http.client
import wrapt
import os
import os.path
import requests
import sys
from pathlib import Path
import datetime
from travispy import TravisPy
import urllib3.response
import pprint
import logging
import contextlib
import click

    


def do_debug():
    from http.client import HTTPConnection # py3
    
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

    wrapt.wrap_function_wrapper(http.client, 'HTTPResponse.read', wrapper)
    wrapt.wrap_function_wrapper(http.client, 'HTTPResponse._safe_read', wrapper)
    wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.read_chunk', wrapper)
    wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.stream', wrapper2)
    wrapt.wrap_function_wrapper(urllib3.response, 'HTTPResponse.__iter__', wrapper2)

    HTTPConnection.debuglevel = 1
    for method in ["get", "post", "put", "patch", "delete"]:
        wrapt.wrap_function_wrapper(requests,  method, wrapper)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    for logger in ("requests.packages.urllib3","requests.packages.urllib3.connectionpool"):
        requests_log = logging.getLogger(logger)
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


def do_project(t, repository_id, monthcut, slug):
    x = t.builds(repository_id=repository_id)

    for build in x:        
        b = t.build(build.id)
        started = datetime.datetime.strptime(b.started_at,
                                   "%Y-%m-%dT%H:%M:%S%z") #.%f
        if started < monthcut:
            continue
        
        print("build",build.id, started)        
        cmt = b.commit

        for job in b.jobs:
            print("job",job.id, slug)
            l = job.log
            with open("logs/{}/{}".format(slug, job.id),'w') as of:
                of.write(l['content'])

                                        
@click.command()
@click.option('--days', default="20", type=int)
@click.option('--tokenfile', default=str(Path.home() / Path(".travis") / Path("token")))
@click.option('--project', default="")
@click.option('--debug/--no-debug', default=False)

def runit(days, tokenfile, project,debug):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    if debug:
        do_debug()
    
    monthcut = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(
        tzinfo=datetime.timezone.utc)
    token = open(tokenfile).read().strip()
    t = TravisPy(token)
    user = t.user()
    repos = user.repos()
    respository_id = None
    for x in repos['repositories']:
        print(x)
        print(x['name'])
        #print(dir(x))
        slug =x['slug']
        print (slug, x['id'])
        repo_id = x['id']

        
        ppath = "logs/" + slug
        if not os.path.exists(ppath):
            os.makedirs(ppath)

        if project == "":
            do_project(t, repo_id,monthcut, slug)
        elif project == x.slug:
            do_project(t, repo_id,monthcut, slug)
            return
        
if __name__ == '__main__':
    runit()
        



            
