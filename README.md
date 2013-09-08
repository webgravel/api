Gravel Master API
===================

This package exposes simple interface for use in client applications.

Installation
------------

```
gravelpkg install gravel-api
# create config
mkdir /gravel/system/apiconfig/
cd /gravel/system/apiconfig/
# generate API SSL key
openssl req -new -x509 -keyout key.pem -out key.pem -days 3650 -nodes
```

Example config:

`/gravel/system/apiconfig/api_config.py`
```
base = '/gravel/system/apiconfig'

SECRETS_FILE=base + '/secrets.txt'
MASTER_PREFIX = ['gravel']
KEY = base + '/key.pem'

ALLOW_CUSTOMS = {
    'test': ['web', 'ssh'],
}

ALLOW_USER_CREATION = {'test'}
```

`/gravel/system/apiconfig/secrets.txt`
```
randomstring1234567890=test
```
