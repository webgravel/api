import sys
import os

sys.path.append('/gravel/pkg/gravel-common')

import subprocess
import json

import cmd_util
import gravelrpc
import api_db
import api_config

from api_db import PermissionDenied

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

        uid = int(master_call(['user', 'add', '%d' % uid], func=subprocess.check_output))
        master_call(['storage', 'add', 'u%d' % uid, 'file', 'uid=%d' % uid])

        api_db.set_owner('user', uid, self.client_id)
        api_db.set_owner('storage', 'u%d' % uid, self.client_id)

        return uid

    def method_get_custom(self, uid, name):
        api_db.verify_owner('user', uid, self.client_id)

        data = master_call(['user', 'custom', '--get', '--', '%d' % uid, name],
                           func=subprocess.check_output)
        return json.loads(data)

    def method_set_custom(self, uid, name, data):
        api_db.verify_owner('user', uid, self.client_id)

        if name not in api_config.ALLOW_CUSTOMS[self.client_id]:
            raise PermissionDenied('editing %r not allowed' % name)

        master_call(['user', 'custom', '--set', '--', '%d' % uid, name],
                    func=cmd_util.call_with_stdin,
                    stdin_data=json.dumps(data))

def master_call(args, **kwargs):
    return cmd_util.generic_call(api_config.MASTER_PREFIX + args, **kwargs)

if __name__ == '__main__':
    Handler.main(('localhost', 4443), gravelrpc.ThreadingSSLServer)
