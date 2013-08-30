import sys
import os

sys.path.append('/gravel/pkg/gravel-common')

import subprocess

import cmd_util
import gravelrpc
import api_db
import api_config

secrets_file = 'api_secrets.txt'

assert os.stat(secrets_file).st_mode & 0o044 == 0
secrets = dict( line.strip().split('=', 1)
                for line in open(secrets_file, 'r')
                if line.strip() )

class Handler(gravelrpc.RPCHandler):
    key = api_config.KEY

    def _preprocess_args(self, *args, **kwargs):
        try:
            self.client_id = secrets[kwargs['auth']]
        except KeyError:
            raise PermissionDenied('invalid auth key')
        if not self.client_id or kwargs['auth'].startswith('#'):
            raise RuntimeError('malformed secrets file')
        del kwargs['auth']
        return args, kwargs

    def method_create_user(self, uid):
        if self.client_id not in api_config.ALLOW_USER_CREATION:
            raise PermissionDenied()

        uid = int(master_call(['user', 'add', '%s' % uid], func=subprocess.check_output))
        master_call(['storage', 'add', 'u%d' % uid, 'file', 'uid=%d' % uid])

        api_db.set_owner('user', uid, self.client_id)

        return uid

def master_call(args, **kwargs):
    return cmd_util.generic_call(api_config.MASTER_PREFIX + args, **kwargs)

class PermissionDenied(Exception):
    def __init__(self, msg='Permission denied'):
        Exception.__init__(self, msg)

if __name__ == '__main__':
    Handler.main(('localhost', 4443), gravelrpc.ThreadingSSLServer)
