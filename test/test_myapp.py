'''
   Default test for Boilerplate App
'''

from myapp.app import main


def test_main():
    '''
    Test of main function for default app
    '''
    return_phrase = 'hi'
    assert main() is return_phrase, f'{return_phrase} not returned'
