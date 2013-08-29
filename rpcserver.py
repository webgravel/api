import sys
import os

sys.path.append('/gravel/pkg/gravel-common')

import gravelrpc
import api_config

import api_db

secrets_file = 'api_secrets.txt'

assert os.stat(secrets_file).st_mode & 0o044 == 0
secrets = dict( line.strip().split('=', 1)
                for line in open(secrets_file, 'r')
                if line.strip() )

class Handler(gravelrpc.RPCHandler):
    key = api_config.KEY

    def _preprocess_args(self, *args, **kwargs):
        self.client_id = secrets[kwargs['auth']]
        if not self.client_id or kwargs['auth'].startswith('#'):
            raise RuntimeError('malformed secrets file')

    def method_create_user(self, name):
        pass

if __name__ == '__main__':
    Handler.main(('localhost', 4443), gravelrpc.ThreadingSSLServer)
