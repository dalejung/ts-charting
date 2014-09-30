"""
Tools to shard logic into separate files like ohlc.py. 
"""
def merge(base, mixin, overrides=None):
    """
    Merge attributes from mixin class to base

    overrides : list of strings
        List of name that will be transferred regardless of previous checks.
        for the time being, this is only for double underscore names
    """
    if overrides is None:
        overrides = []


    for name, meth in mixin.__dict__.items():
        if name.startswith('__') and name not in overrides:
            continue

        if hasattr(base, name):
            # note that the base._mixins_ check should prevent us frogm
            # running the same mixin
            raise Exception("We should never replace an existing method. {0}".format(name))
        setattr(base, name, meth) 

def mixin(base, overrides=None):
    """
    Create mixin decorator for specific base class
    """
    def _mixin(mixin):
        mixin_name =  mixin.__name__
        _mixins_ = getattr(base, '_mixins_', [])
        if mixin_name in _mixins_:
            print('{mixin_name} already mixed'.format(mixin_name=mixin_name))
            return False
        _mixins_.append(mixin_name)
        setattr(base, '_mixins_', _mixins_)

        merge(base, mixin, overrides=overrides)
    return _mixin
