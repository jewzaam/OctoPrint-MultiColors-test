For: https://github.com/MoonshineSG/OctoPrint-MultiColors

# Purpose

Create this project with a python test to check that the regex gives me the output I want.  It was taking too long to use the plugin by uploading gcode, modifying, download, diff, and repeat.  This is hopefully going to make it much easier by plugging in the starting gcode, patter, replacement gcode, and expected results.

# Results: My Settings

I slice with Slic3r and have enabled verbose GCODE.  I found GOCDE to move the hot end off the print at a layer change (reference eludes me right now).  Wanted to share what I did with this OctoPrint plugin for my setup.

The trick is to get the retract, extrucsion reset, and Z change captured in a group so you can replay it.

My regex:  `(.*layer [(]{0}[)])\n(G1 X.*move.*)\n(G1 E([\d.]*) F([\d.]*)[; ]*.*unretract)`

My GCODE: 

```
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
; RESUME (retract, reset extruder, move XY, move Z, unretract)
G1 E-\5 F\6 ; retract
M82 ; Set extruder to Absolute Mode
G92 E0 ; reset extrusion distance
\3
\2
\4
```
