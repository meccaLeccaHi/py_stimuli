# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 12:04:55 2017

@author: root
"""

# http://www.fileformat.info/format/mpeg/sample/index.dir
import pygame, glob

FPS = 60

# Find movies matching wildcard search
videopath = '/home/adam/Desktop/virtBox_share/JonesStimset/identity1/'
videolist = glob.glob(videopath + '*.m4v')

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie(videolist[0])
screen = pygame.display.set_mode(movie.get_size())
movie_screen = pygame.Surface(movie.get_size()).convert()

movie.set_display(movie_screen)
movie.play()


playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            movie.stop()
            playing = False

    screen.blit(movie_screen,(0,0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()