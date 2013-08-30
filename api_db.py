import graveldb

PATH = '/gravel/system/api'

class Ownership(graveldb.Table('ownerships', PATH)):
    default = dict(owner=None)

def set_owner(kind, ident, owner, overwrite=False):
    assert ':' not in kind
    ownership = Ownership('%s:%s' % (kind, ident))
    if not overwrite and ownership.exists:
        raise ValueError('object %r already owned' % ownership.name)
    ownership.data.owner = owner
    ownership.save()
