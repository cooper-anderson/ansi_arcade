#!/usr/bin/env python3
# -*- coding: utf8 -*-

import braille
import dithering
import puzzle

games = ["2D Rubik's Cube", "Dithering", "Braille"]
descriptions = {"2D Rubik's Cube": "Slide letters and numbers to reorganize", "Dithering": "Render geometry with dithering", "Braille": "Learn Braille"}
executables = {"2D Rubik's Cube": puzzle.Puzzle, "Dithering": dithering.Braille, "Braille": braille.Braille}
games.sort()

