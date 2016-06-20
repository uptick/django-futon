import importlib


def import_class(module_string):
    cmpnts = module_string.split()
    mod_name = '.'.join(cmpnts[:-1])
    class_name = cmpnts[-1]
    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)
