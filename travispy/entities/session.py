#import requests_debugger 
import requests


class Session(requests.Session):
    '''
    Internet session created to perform requests to |travisci|.

    :param str uri:
        URI where session will start.
    '''

    def __init__(self, uri):
        requests.Session.__init__(self)
        self.uri = uri
        #import pdb
        #pdb.set_trace()
        #requests_debugger.my_apply(self)
    # def post(self, *args, **kwargs):
    #     print(args, kwargs)
    #     ret = requests.Session.post(self, args, kwargs)
    #     print(ret)
    #     return ret
