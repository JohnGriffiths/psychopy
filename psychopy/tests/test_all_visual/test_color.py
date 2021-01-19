from psychopy.tests import utils
from psychopy import visual, colors
from pathlib import Path

"""All tests in this file involve rapidly changing colours, do not run these tests in a setting where you can view the 
output if you have photosensitive epilepsy"""

# Define expected values for different spaces
exemplars = [
    {'rgb': ( 1.00,  1.00,  1.00), 'rgb255': (255, 255, 255), 'hsv': (  0, 0.00, 1.00), 'hex': '#ffffff', 'named': 'white'}, # Pure white
    {'rgb': ( 0.00,  0.00,  0.00), 'rgb255': (128, 128, 128), 'hsv': (  0, 0.00, 0.50), 'hex': '#808080', 'named': 'gray'}, # Mid grey
    {'rgb': (-1.00, -1.00, -1.00), 'rgb255': (  0,   0,   0), 'hsv': (  0, 0.00, 0.00), 'hex': '#000000', 'named': 'black'}, # Pure black
    {'rgb': ( 1.00, -1.00, -1.00), 'rgb255': (255,   0,   0), 'hsv': (  0, 1.00, 1.00), 'hex': '#ff0000', 'named': 'red'}, # Pure red
    {'rgb': (-1.00,  1.00, -1.00), 'rgb255': (  0, 255,   0), 'hsv': (120, 1.00, 1.00), 'hex': '#00ff00', 'named': 'lime'}, # Pure green
    {'rgb': (-1.00, -1.00,  1.00), 'rgb255': (  0,   0, 255), 'hsv': (240, 1.00, 1.00), 'hex': '#0000ff', 'named': 'blue'}, # Pure blue
    # Psychopy colours
    {'rgb': (-0.20, -0.20, -0.14), 'rgb255': (102, 102, 110), 'hsv': (240, 0.07, 0.43), 'hex': '#66666e'}, # grey
    {'rgb': ( 0.35,  0.35,  0.38), 'rgb255': (172, 172, 176), 'hsv': (240, 0.02, 0.69), 'hex': '#acacb0'}, # light grey
    {'rgb': ( 0.90,  0.90,  0.90), 'rgb255': (242, 242, 242), 'hsv': (  0, 0.00, 0.95), 'hex': '#f2f2f2'}, # offwhite
    {'rgb': ( 0.90, -0.34, -0.29), 'rgb255': (242,  84,  91), 'hsv': (357, 0.65, 0.95), 'hex': '#f2545b'}, # red
    {'rgb': (-0.98,  0.33,  0.84), 'rgb255': (  2, 169, 234), 'hsv': (197, 0.99, 0.92), 'hex': '#02a9ea'}, # blue
    {'rgb': (-0.15,  0.60, -0.09), 'rgb255': (108, 204, 116), 'hsv': (125, 0.47, 0.80), 'hex': '#6ccc74'}, # green
    {'rgb': ( 0.85,  0.18, -0.98), 'rgb255': (236, 151,   3), 'hsv': ( 38, 0.99, 0.93), 'hex': '#ec9703'}, # orange
    {'rgb': ( 0.89,  0.65, -0.98), 'rgb255': (241, 211,   2), 'hsv': ( 52, 0.99, 0.95), 'hex': '#f1d302'}, # yellow
    {'rgb': ( 0.53,  0.49,  0.94), 'rgb255': (195, 190, 247), 'hsv': (245, 0.23, 0.97), 'hex': '#c3bef7'}, # violet
]
# A few values which are likely to mess things up
tykes = [
    {'rgba': ( 1.00,  1.00,  1.00, 0.50), 'rgba255': (255, 255, 255, 0.50), 'hsva': (  0, 0.00, 1.00, 0.50)}, # Make sure opacities work in every space
    {'rgba': "white", 'rgba255': "white", "hsva": "white", "hex": "white", "rgb255": "#ffffff"}, # Overriding colorSpace with hex or named values
    {'rgba': None, 'named': None, 'hex': None, 'hsva': None}, # None as a value
]

# Test window for visual objects
win = visual.Window([128, 128], pos=[50, 50], allowGUI=False, autoLog=False)

# Begin test
def test_colors():
    for colorSet in exemplars + tykes:
        # Construct matrix of space pairs
        spaceMatrix = []
        for space1 in colorSet:
            spaceMatrix.extend([[space1, space2] for space2 in colorSet if space2 != space1])
        # Compare each space pair for consistency
        for space1, space2 in spaceMatrix:
            col1 = colors.Color(colorSet[space1], space1)
            col2 = colors.Color(colorSet[space2], space2)
            closeEnough = all(abs(col1.rgba[i]-col2.rgba[i])<0.02 for i in range(4))
            # Check that valid color has been created
            assert bool(col1) and bool(col2)
            # Check setters
            assert col1 == col2 or closeEnough

def test_window_colors():
    # Iterate through color sets
    for colorSet in exemplars + tykes:
        for space in colorSet:
            # Set window color
            win.colorSpace = space
            win.color = colorSet[space]
            win.flip()
            utils.comparePixelColor(win, colors.Color(colorSet[space], space))

def test_shape_colors():
    # Create rectangle with chunky border
    obj = visual.Rect(win, units="pix", pos=(0,0), size=(128, 128), lineWidth=10)
    # Iterate through color sets
    for colorSet in exemplars + tykes:
        for space in colorSet:
            # Check border color
            obj.colorSpace = space
            obj.borderColor = colorSet[space]
            obj.fillColor = 'white'
            obj.opacity = 1  # Fix opacity at full as this is not what we're testing
            win.flip()
            obj.draw()
            utils.comparePixelColor(win, colors.Color(colorSet[space], space), coord=(1,1))
            utils.comparePixelColor(win, colors.Color('white'), coord=(50, 50))
            # Check fill color
            obj.colorSpace = space
            obj.fillColor = colorSet[space]
            obj.borderColor = 'white'
            obj.opacity = 1  # Fix opacity at full as this is not what we're testing
            win.flip()
            obj.draw()
            utils.comparePixelColor(win, colors.Color('white'), coord=(1,1))
            utils.comparePixelColor(win, colors.Color(colorSet[space], space), coord=(50, 50))