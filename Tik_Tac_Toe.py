
import sys
import time
import pygame as pg
from pygame.locals import *

#initializing variables
XO = 'o'
winner = None
draw = None

#board building variables
black = (0, 0, 0)
black = (0, 0, 0)
lines = (255, 255, 255)
width = 500
height = 500
board = [[None]*4, [None]*4, [None]*4]
