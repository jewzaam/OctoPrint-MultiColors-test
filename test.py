#!/usr/bin/env python

import re
import contextlib
import mmap

layer = 5

pattern = "(.*layer [(]{0}[)])\n(G1 X.*move.*)\n(G1 E([\d.]*) F([\d.]*)[; ]*.*unretract.*)".format(int(layer))

before = """G1 E260.93009 F1800.00000 ; retract extruder 0
G92 E0 ; reset extrusion distance
G1 Z1.400 F9600.000 ; move to next layer (5)
G1 X191.735 Y167.287 F9600.000 ; move to first perimeter point
G1 E1.90000 F1800.00000 ; unretract extruder 0
M204 S1200 ; adjust acceleration"""

gcode = """; PAUSE
M117 Color Change
G91 ; Set Relative Coordinates (Marlin also Extrusion)
M83 ; Set Relative Extrusion
G1 E-5.000000 F500 ; Retract 5mm
G1 Z15 F300 ; move Z up 15mm
G90 ; Set Absolute Coordinates
G1 X20 Y20 F9000 ; Move to hold position
G91 ; Set Relative Coordinates
G1 E-40 F500 ; Retract 40mm
M0 ; Idle Hold
G90 ; Set Absolute Coordinates
G1 F5000 ; Set speed limits
G28 X0 Y0 ; Home X Y
; RESUME (prepare for first unextract, reset extruder, layer change)
G1 E-\\5 F\\6 ; retract
M82 ; Set extruder to Absolute Mode
G92 E0 ; reset extrusion distance
\\3
\\2
\\4"""

expected = """G1 E260.93009 F1800.00000 ; retract extruder 0
G92 E0 ; reset extrusion distance
G1 Z1.400 F9600.000 ; move to next layer (5)
G1 X191.735 Y167.287 F9600.000 ; move to first perimeter point
G1 E1.90000 F1800.00000 ; unretract extruder 0
; multi color
; PAUSE
M117 Color Change
G91 ; Set Relative Coordinates (Marlin also Extrusion)
M83 ; Set Relative Extrusion
G1 E-5.000000 F500 ; Retract 5mm
G1 Z15 F300 ; move Z up 15mm
G90 ; Set Absolute Coordinates
G1 X20 Y20 F9000 ; Move to hold position
G91 ; Set Relative Coordinates
G1 E-40 F500 ; Retract 40mm
M0 ; Idle Hold
G90 ; Set Absolute Coordinates
G1 F5000 ; Set speed limits
G28 X0 Y0 ; Home X Y
; RESUME (prepare for first unextract, reset extruder, layer change)
G1 E-1.90000 F1800.00000 ; retract
M82 ; Set extruder to Absolute Mode
G92 E0 ; reset extrusion distance
G1 X191.735 Y167.287 F9600.000 ; move to first perimeter point
G1 Z1.400 F9600.000 ; move to next layer (5)
G1 E1.90000 F1800.00000 ; unretract extruder 0

M204 S1200 ; adjust acceleration"""




marker = "; multi color"

replace  = ur'\1\n{0}\n{1}\n'.format(marker, gcode)


def printdiff(expected, actual):
    """
    Helper function. Returns a string containing the unified diff of two multiline strings.
    """

    import difflib
    expected=expected.splitlines(1)
    actual=actual.splitlines(1)

    diff=difflib.unified_diff(expected, actual)

    output=''.join(diff)
    if len(output) == 0:
        print "No diff!"
    else:
        print output


c = re.compile(ur'({0}$)'.format(pattern), re.MULTILINE)

result = re.sub(c, replace, before)

printdiff(expected, result)


