import argparse

class Test(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values)