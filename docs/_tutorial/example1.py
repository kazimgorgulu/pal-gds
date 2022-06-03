import gdstk
import numpy as np

import palgds.base_cells as bc
from palgds.circuit import Circuit

import os 
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def draw(pcell, path, scale=300):
    """ svg export function from gdstk library."""
    bb = pcell.bounding_box()
    scaling = scale / (1.1 * (bb[1][0] - bb[0][0]))
    name = path + pcell.name + ".svg"
    pcell.write_svg(
        name,
        scaling=scaling,
        background="none",
        shape_style={(0, 0): {"fill": "darkorange", "stroke": "chocolate"}},
        label_style={(3, 2): {"stroke": "red", "fill": "none", "font-size": "32px"}},
        pad="5%",
    )
    # print(f"Saving {name} (scaling {scaling})")

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

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__)) + "/"
    ring_res = RingResonator(name="RingRes", radius=5, gap=0.2, width=0.45)
    # ring_res.write_svg(path + "RingRes.svg")
    # lib = gdstk.Library()
    # lib.add(ring_res, *ring_res.dependencies(True))
    # lib.write_gds(path + "RingRes.gds", max_points=4000)
    draw(ring_res, path)




###########################Circuit###################################
ring_res = RingResonator(name="RingResonator", radius=10, gap=0.2, width=0.45)
gc = bc.GDSCell(name="Grating_Coupler", filename='Grating_Coupler.gds', ports={"in": bc.Port((0, 0), 0, "op")})

circuit = Circuit(name='RingResCircuit',
                  pcells={"rr": ring_res, "gc1": gc, "gc2": gc},
                  translations={"rr": (0, 0),
                                "gc1": (-15, 0),
                                "gc2": (15, 0),
                                },
                  rotations={"gc2": np.pi},
                  links=[{"from": ("rr", "in"), "to": ("gc1", "in")},
                         {"from": ("rr", "out"), "to": ("gc2", "in")},
                         ]
                  )
# end of circuit

draw(circuit, path, scale=600)

ybranch = bc.GDSCell(name="YBranch", filename='YBranch.gds', ports_filename="YBranch.txt")
draw(ybranch, path, scale=250)

class CustomTrace(bc.Trace):

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=[0.45, 3], bend_radius=bend_radius,
                         layer=[0, 1], datatype=[0, 0], port_type='op')
        pass
# End of trace class

trace = CustomTrace(name='Trace', points=[(0, 0), (20, 0), (20, 10), (40, 10)])
draw(trace, path, scale=300)

circuit.add(gdstk.Reference(trace))

lib = gdstk.Library()
lib.add(circuit, *circuit.dependencies(True))
lib.write_gds(path + "circuit.gds", max_points=4000)


from palgds.pcell_library import DirectionalCoupler

dc = DirectionalCoupler(name="Directional_Coupler")
draw(dc, path)

lib = gdstk.Library()
lib.add(dc, *dc.dependencies(True))
lib.write_gds(path + "direc.gds", max_points=4000)


balanced_mzi = Circuit(name='Balanced_MZI',
                  pcells={"dc1": dc, "dc2": dc},
                  translations={"dc1": (0, 0),
                                "dc2": (50, 0),
                                },
                  links=[{"from": ("dc1", "out1"), "to": ("dc2", "in1")},
                         {"from": ("dc1", "out2"), "to": ("dc2", "in2")},
                         ],
                  op_trace=CustomTrace
                  )
# end of balanced mzi

lib = gdstk.Library()
lib.add(balanced_mzi, *balanced_mzi.dependencies(True))
lib.write_gds(path + "balanced_mzi.gds", max_points=4000)
draw(balanced_mzi, path, scale=600)





















# import os
# path = os.path.abspath('../../palgds-demo/samples/')
# print(path)
# gdscell = bc.GDSCell(name='MMI', filename=path+"/MMI.gds", rename="cccell")

# p = bc.Port((1,2.222), 3.33)
# print(p)
# ring_res = RingResonator(name="RingRes", radius=10, gap=0.2, width=0.45)
# lib = gdstk.Library()
# lib.add(ring_res.cell, *ring_res.cell.dependencies(True))
# lib.write_gds("ring_resonator.gds",max_points=4000)
#
#
#
# # In the following lines we will create connect two ring resonators in a circuit:
#
# circuit = Circuit(name='rr_cct',
#                   pcells={"dev1": ring_res, "dev2": ring_res, },
#                   translations={"dev1": (0, 0),
#                                 "dev2": (100, 50),},
#                   rotations={"dev1": 0, "dev2": 0},
#                   links=[{"from": ("dev1", "out"), "to": ("dev2", "out"), }]
#                   )
#
# lib = gdstk.Library()
# lib.add(circuit.cell, *circuit.cell.dependencies(True))
# lib.write_gds("ring_res_circuit.gds",max_points=4000)
#
# # In above circuit you will realize that the routing waveguide is not correct.
# # Layer number is not matching with the ring resonators. This is because Circuit class uses default Optical Trace
# # from technology file. So we will create a custom Trace and use it in ring resonator circuit:





