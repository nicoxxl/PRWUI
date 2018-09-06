import json

def h(tag, props, *children):
    return {'type':tag, 'props':props, 'children':children}


class H:
    def __init__(self, tag, props=None):
        self.tag = tag
        if props is None:
            self.props={}
        else:
            self.props = props
    
    def __call__(self, *children, **extra_prop):
        return h(self.tag, {**self.props, **extra_prop}, *children)

class ComplexProp:
    def __init__(self, prefix):
        self._prefix = prefix
    def __getattr__(self, name):
        # I don't like that
        # TODO : a better way
        def _render(value):
            return {self._prefix+name:json.dumps(value, sort_keys=True)}
        return _render

on = ComplexProp('on')