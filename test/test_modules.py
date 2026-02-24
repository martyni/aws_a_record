'''
   Testing module imports
'''
# pylint: disable=W0122
from os import listdir, chdir, path

ROOT = path.abspath('.')
TESTS_DIR = f'{ROOT}/test'
SRC = f'{ROOT}/src'
chdir(SRC)
MODULES = listdir()
print(MODULES)
chdir(ROOT)
SUBMODULES = []


def test_module_imports():
    '''
    Import modules
    '''
    for mod in MODULES:
        if 'egg-info' in mod:
            continue
        exec(f'import {mod}')
        assert exec('{mod}') is not False, f'Could not import {mod}'
    chdir(ROOT)


def test_coverage():
    '''
    Check each coverage
    '''
    tests = listdir(TESTS_DIR)
    print(MODULES)
    print(tests)
    mods_gen = (mod for mod in MODULES if 'egg-info' not in mod)
    for mod in mods_gen:
        print(f'test_{mod}.py in {tests}')
        assert f'test_{mod}.py' in tests


if __name__ == '__main__':
    test_module_imports()
    test_coverage()
