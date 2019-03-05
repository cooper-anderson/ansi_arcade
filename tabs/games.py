#!/usr/bin/env python3
# -*- coding: utf8 -*-

import braille
import dithering
import puzzle
import bpuzzle

games = ["2D Rubik's Cube", "Dithering", "Braille", "BPuzzle"]
descriptions = {"2D Rubik's Cube": "Slide letters and numbers to reorganize", "Dithering": "Render geometry with dithering", "Braille": "Learn Braille", "BPuzzle": "The 2D Rubik's Cube but with Braille letters"}
executables = {"2D Rubik's Cube": puzzle.Puzzle, "Dithering": dithering.Braille, "Braille": braille.Braille, "BPuzzle": bpuzzle.BPuzzle}
games.sort()

