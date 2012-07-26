'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os
import pygame
from pygame import *
from pygame.image import *

#data_py = os.path.abspath(os.path.dirname(__file__))
#data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))
data_dir = 'data'

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)


def load_image(name):
	global pygame
	fullname = os.path.join('data',name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
		print 'Cannot load image:',fullname
		raise SystemExit, message
	image.set_colorkey((0,255,0))
	return image
