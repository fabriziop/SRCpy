#!/usr/bin/python3
# .+
# .context    : SRCpy, RAI coded signal (SRC)
# .title      : package __init__
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	9-Apr-2021
# .copyright  :	(c) 2021 Fabrizio Pollastri
# .license    : GNU Lesser General Public License
# .-


from os.path import splitext,join,basename,dirname
from glob import glob
from importlib import import_module

# this import works for a module structure with one function for each
# module (each '*.py' file), where module and function have the same name.
# import all modules (*.py files in __init__.py dir) except __init__.py.
#files=[splitext(f)[0] for f in glob(join(dirname(__file__), '*.py')) 
for path in glob(join(dirname(__file__), '*.py')):
    # strip file extension and directory path
    module = basename(splitext(path)[0])
    # skip __init__.py (this file)
    if module == '__init__':
        continue
    # import current module as srcpy.<module>
    import_module("." + module,"srcpy")
    # strip one id level (skip common.py module): module.module becomes module
    if module == 'common':
        continue
    globals()[module] = getattr(globals()[module],module)
    
#### END
