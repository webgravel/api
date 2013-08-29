import graveldb

PATH = '/gravel/system/api'

class Ownership(graveldb.Table('ownerships', PATH)):
    default = dict(owner=None)
