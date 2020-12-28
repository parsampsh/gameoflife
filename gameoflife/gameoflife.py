#!/usr/bin/env python3
from os import popen
from random import random
from time import sleep as time_sleep
from copy import deepcopy
from sys import argv, exit

class GameOfLife:
    """
    The Game of life Emulator

    The Game of Life, also known simply as Life, is a cellular automaton devised by the British
    mathematician John Horton Conway in 1970. It is a zero-player game, meaning that
    its evolution is determined by its initial state, requiring no further input.
    One interacts with the Game of Life by creating an initial configuration
    and observing how it evolves. It is Turing complete and can simulate
    a universal constructor or any other Turing machine.

    More information on wikipedia: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

    This emulator is created by parsa shahmaleki.
    (c) 2020 parsa shahmaleki <parsampsh@gmail.com>
    Licensed Under GPL-v3

    Cli Usage:
        python3 -m gameoflife --option1=value --option2=value ...

    Code Usage:
        gol = GameOfLife(option1=value, option2=value...)
        gol.start()

    Options:
        you can customize the emulator using this options

        `width`         width of the world. default: width of the terminal
        `height`        hegith of the world. default: height of the terminal
        `live_char`     symbol of the live cell. default: `+`
        `dead_char`     symbol of the dead cell. default: ` `
        `sleep_time`    sleep time between world frames(secounds). default: `0.05`
        `border_char`   the world border chars. default: `#`
        `title`         a title of the head of the world. default: `Conway's Game of life`
        `random_har`    how much initialized live cells. every more means harder. default: `3`

    Cli Example:
        gameoflife --width=100 --height=40 --live_char='@' --sleep_time=0.2 --title='my gameoflife'

    Code Example:
        GameOfLife(width=100, live_char='@' sleep_time=0.2, title="something").start()
    """
    def __init__(self, height=None, width=None, live_char='+', dead_char=' ', sleep_time=0.05, border_char='#', title='Conway\'s Game of life', random_hard=3):
        # set the configuration
        self.world = []
        terminal_height, terminal_width = popen('stty size', 'r').read().split()
        if height == None:
            self.h = int(int(terminal_height)/1.5)
        else:
            self.h = int(height)
        if width == None:
            self.w = int(int(terminal_width)/1.1)
        else:
            self.w = int(width)
        self.live_char = live_char
        self.dead_char = dead_char
        self.sleep_time = float(sleep_time)
        self.border_char = border_char
        self.random_hard = int(random_hard)
        self.title = title
        self.footer = 'By parsampsh <parsampsh@gmail.com>'
        self.years = 0

        # initialize the world
        i = 0
        while i < self.h:
            j = 0
            self.world.append([])
            while j < self.w:
                self.world[-1].append(self.rand_number())
                j += 1
            i += 1

    def start(self):
        """ Starts running game of life """
        while True:
            self.print_world()
            self.eval_world()
            time_sleep(self.sleep_time)

    def rand_number(self):
        """ Generates a random boolean """
        try:
            num = int(str(random()).replace('.', ''))
            num = num % self.random_hard
            if num == 0:
                return 1
            return 0
        except:
            return self.rand_number()

    def get_nbors(self, i, j):
        """ Returns neiboughrs of a cell """
        n = 0
        y = i-1
        while y <= i+1:
            x = j-1
            while x <= j+1:
                try:
                    current = self.world[y][x]
                except:
                    current = 0
                if current == 1:
                    n += 1
                x += 1
            y += 1
        if self.world[i][j] == 1:
            n -= 1
        return n

    def eval_world(self):
        """ Makes evalutions on world """
        world = self.world
        new_world = deepcopy(world)
        i = 0
        while i < len(world):
            j = 0
            while j < len(world[i]):
                n = self.get_nbors(i, j)
                if world[i][j] == 1:
                    if n == 2 or n == 3:
                        new_world[i][j] = 1
                    else:
                        new_world[i][j] = 0
                else:
                    if n == 3:
                        new_world[i][j] = 1
                    else:
                        new_world[i][j] = 0
                j += 1
            i += 1
        self.world = new_world
        self.years += 1

    def print_world(self):
        """ Prints the world on screen """
        output = '\033[H'
        the_width = len(self.world[0])
        white_space = ' ' * int(((the_width - len(self.title + ' (' + str(self.years) + ' years)')) / 2))
        output += white_space + self.title + ' (' + str(self.years) + ' years)' + white_space + '\n'
        white_space = ' ' * int(((the_width - len(self.footer)) / 2))
        footer = white_space + self.footer + white_space + '\n'
        i = 0
        while i < len(self.world):
            j = 0
            if i == 0:
                output += (self.border_char * (len(self.world[i]) + 2)) + '\n'
            output += (self.border_char)
            while j < len(self.world[i]):
                if self.world[i][j] == 1:
                    output += (self.live_char)
                else:
                    output += (self.dead_char)
                j += 1
            output += self.border_char + '\n'
            if i == len(self.world)-1:
                output += (self.border_char * (len(self.world[i]) + 2)) + '\n'
            i += 1
        output += footer
        print(output)

def cli_handle():
    if '--help' in argv:
        print(GameOfLife.__doc__)
        exit()
    options = {}
    for arg in argv:
        if len(arg) > 2:
            if arg[:2] == '--':
                value = arg.split('=', 1)
                if len(value) > 1:
                    options[value[0][2:]] = value[-1]
    try:
        GameOfLife(**options).start()
    except TypeError as err:
        err_str = str(err)
        if err_str.startswith('__init__() got an unexpected keyword argument '):
            print('Error: Unknow option ' + err_str.replace('__init__() got an unexpected keyword argument ', ''))
        else:
            print('Error: ' + err_str)
    except KeyboardInterrupt as err:
        print('\nOh shit! God pressed CTRL+<some-fucking-key>! World was destroyed!')

if __name__ == '__main__':
    cli_handle()

