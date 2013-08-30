import graveldb

PATH = '/gravel/system/api'

class Ownership(graveldb.Table('ownerships', PATH)):
    default = dict(owner=None)

    @staticmethod
    def get(kind, ident):
        assert ':' not in kind
        return Ownership('%s:%s' % (kind, ident))

def set_owner(kind, ident, owner, overwrite=False):
    ownership = Ownership.get(kind, ident)
    if not overwrite and ownership.exists:
        raise ValueError('object %r already owned' % ownership.name)
    ownership.data.owner = owner
    ownership.save()

def verify_owner(kind, ident, owner):
    ownership = Ownership.get(kind, ident)
    if owner != ownership.data.owner:
        raise PermissionDenied()

class PermissionDenied(Exception):
    def __init__(self, msg='Permission denied'):
        Exception.__init__(self, msg)
