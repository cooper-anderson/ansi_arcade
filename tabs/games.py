#!/usr/bin/env python3
# -*- coding: utf8 -*-

import braille
import dithering
import puzzle

games = ["2D Rubics Cube", "Dithering", "Braille"]
descriptions = {"2D Rubics Cube": "Slide letters and numbers to reorganize", "Dithering": "Render geometry with dithering", "Braille": "Learn Braille"}
executables = {"2D Rubics Cube": puzzle.Puzzle, "Dithering": dithering.Braille, "Braille": braille.Braille}
games.sort()

