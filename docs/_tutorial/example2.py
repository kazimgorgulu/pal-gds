import gdstk
import numpy as np
from palgds.circuit import Circuit
import palgds.base_cells as bc
import os 

def draw(pcell, path):
    """ svg export function from gdstk library."""
    bb = pcell.bounding_box()
    scaling = 300 / (1.1 * (bb[1][0] - bb[0][0]))
    name = path + pcell.name + ".svg"
    pcell.write_svg(
        name,
        scaling=scaling,
        background="none",
        shape_style={(0, 0): {"fill": "darkorange", "stroke": "chocolate"}},
        label_style={(3, 2): {"stroke": "red", "fill": "none", "font-size": "32px"}},
        pad="5%",
    )
    

path = os.path.dirname(os.path.abspath(__file__)) + "/"
ybranch = bc.GDSCell(name="YBranch", filename='YBranch.gds', ports_filename="YBranch.txt")
draw(ybranch, path)

# Create a PCell of a grating coupler device from GDSCell. Here we will read the ports from the text file.
# Please check the txt file format when creating your own txt files for ports. txt file has ports in following form:
# (name,xpos,ypos,orientation) - orientation should be one of one of these letters R,L,U,D. These then will be converted
# to radian angles automatically (R: 0, L: pi, U: pi/2 D: 3/2*pi).
device = bc.GDSCell(name="L1", filename='devices/L1.gds', ports_filename='devices/L1.txt')

# Now we will create a circuit of this device by connecting grating couplers to all ports.
circuit = Circuit(name='example2_circuit',
                  pcells={"dev": device, "gc1": ybranch, "gc2": ybranch, "gc3": ybranch, "gc4": ybranch,},
                  translations={"dev": (0, 0),
                                "gc1": (-100, 50),
                                "gc2": (-100, -50),
                                "gc3": (1000, 50),
                                "gc4": (1000, -50),
                                },
                  rotations={"gc3": np.pi, "gc4": np.pi},
                  links=[{"from": ("dev", "in1"), "to": ("gc1", "in")},
                         {"from": ("dev", "in2"), "to": ("gc2", "in")},
                         {"from": ("dev", "out1"), "to": ("gc3", "in")},
                         {"from": ("dev", "out2"), "to": ("gc4", "in")},
                         ]
                  )

lib = gdstk.Library()
lib.add(circuit, *circuit.dependencies(True))
lib.write_gds("example2_circuit.gds",max_points=4000)