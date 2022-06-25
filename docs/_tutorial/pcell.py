import gdstk
import numpy as np

import palgds.base_cells as bc
from palgds.circuit import Circuit
from draw import draw

import os 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

development = True
#path = os.path.dirname(os.path.abspath(__file__)) + "/"
path = "../_source_files/"

# RingResonator PCell class example:
class RingResonator(bc.PCell):
    def __init__(self, name, radius, gap, width, layer=0, datatype=0):
        super().__init__(name)
        self._create_elements(radius, gap, width, layer, datatype)
        self._create_ports(radius)

    def _create_elements(self, radius, gap, width, layer, datatype):
        center = (0, radius+gap+width)
        ring = gdstk.ellipse(center, radius+width/2, radius-width/2, layer=layer, datatype=datatype, tolerance=2e-4)
        straight_waveguide = gdstk.rectangle((-radius, -width/2), (radius, width/2), layer=layer, datatype=datatype)
        self.add(ring, straight_waveguide)

    def _create_ports(self, radius):
        self.ports.update({"in": bc.Port((-radius, 0), np.pi, "op"),
                           "out": bc.Port((radius, 0), 0, "op"),})


ring_res = RingResonator(name="RingRes", radius=5, gap=0.2, width=0.45)
if development:
    draw(ring_res, path, scaling=12)


print(ring_res)
print(ring_res.ports)






