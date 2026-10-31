"""Shared mechanical geometry for the pod board and its two mating tabs (electrode tab, charger tab).

All values in mm, KiCad board coordinates seen from the pod's TOP side (x right, y down), board
top-left corner at (100, 100). The tabs sit above the pod, same orientation, pads on their bottom
layer, so their pad and hole coordinates are the SAME numbers as the pod's pogo pins and holes.
"""

BOARD = (100.0, 100.0, 124.0, 130.0)          # 24 x 30 mm (150 mAh pouch is 19.75 x 26.02)

# 3 x 4 pogo grid, 3.0 mm pitch (Harwin P70-1000045R, pad 2.2). P11 VBUS + P12 GND share the
# bottom row's right end, so the charger tab touches only those two.
PITCH = 3.0
COLS = (102.2, 105.2, 108.2)
ROWS = (110.6, 113.6, 116.6, 119.6)
GRID = {}
for r, y in enumerate(ROWS):
    for c, x in enumerate(COLS):
        GRID["P%d" % (r * 3 + c + 1)] = (x, y)

# M2 NPTH clamp holes at both ends of the grid, 1.5 mm hole-to-edge (tabs screw down on 3.0 mm nylon spacers)
HOLES = ((105.2, 102.6), (105.2, 127.4))
SPACER_MM = 3.0                                 # pogo free 3.5 / working 2.9 / min 2.7

# NINA-B306 body 10 x 15, antenna end at the top board edge, 0.3 mm in from the edge
NINA_CENTRE = (116.5, 107.8)
NINA_BODY = (10.0, 15.0)


def antenna_keepout(centre=NINA_CENTRE):
    """No copper on any layer under the antenna end of the module, out to the board edge."""
    cx, cy = centre
    return (cx - 4.0, BOARD[1], cx + 4.0, cy - NINA_BODY[1] / 2 + 3.1)

NINA_ROT = 180      # footprint has the antenna at +y; 180 puts it at the board's top edge

# battery cartridge (rev 0.6): 20 x 20 x 4 mm pouch under the bottom face, clear of the H1 screw head, and the two
# cartridge contact pads in the strip it leaves at the bottom edge (pod coordinates, seen from the top)
CELL = (102.0, 104.8, 122.0, 124.8)
CART_PADS = {"BATT+": (110.9, 126.1), "BATT-": (112.4, 128.6)}
