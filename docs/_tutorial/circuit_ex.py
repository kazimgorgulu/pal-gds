import gdstk
import numpy as np
from draw import draw
import palgds.base_cells as bc
from palgds.pcell_library import RingResonator
from palgds.circuit import Circuit


import os 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

development = True
#path = os.path.dirname(os.path.abspath(__file__)) + "/"
path = "../_source_files/"


### Basic Circuit ###

ring_res = RingResonator(name="RingResonator", radius=10, gap=0.2, width=0.45)
gc = bc.GDSCell(name="GC", filename=path + 'GC.gds', ports={"in": bc.Port((0, 0), 0, "op")})

ring_res_circuit = Circuit(name='RingResCircuit',
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

if development:
    draw(ring_res_circuit, path, scaling=12)

# lib = gdstk.Library()
# lib.add(ring_res_circuit, *ring_res_circuit.dependencies(True))
# lib.write_gds(path + "Ring_Res_Circuit.gds", max_points=4000)



### Advanced Circuit ###

mmi = bc.GDSCell(name="MMI", filename=path+'MMI.gds', ports_filename=path+"MMI.txt")

if development:
       draw(mmi, path, scaling=9)

class CustomTrace(bc.Trace):

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=[0.5], bend_radius=bend_radius,
                         layer=[0], datatype=[0], port_type='op')
        
# End of trace class

straight_wg = CustomTrace(name='Trace', points=[(0, 0), (10, 0)])
if development:   
       draw(straight_wg, path, scaling=9)


mzi_no_routes = Circuit(name='MZI_no_routes',
                        pcells={"mmi1": mmi, "mmi2": mmi, "wg":straight_wg},
                        translations={"mmi1": (0, 0),
                                      "mmi2": (90, 0),
                                      "wg": (40, 15)
                                      },
                        rotations={"mmi2":np.pi},
                        reflections={"mmi2":True},
                        )
# end of mzi


if development:
       draw(mzi_no_routes, path, scaling=9)


mzi = Circuit(name='MZI',
              pcells={"mmi1": mmi, "mmi2": mmi, "wg":straight_wg},
              translations={"mmi1": (0, 0),
                            "mmi2": (90, 0),
                            "wg": (40, 15)
                            },
              rotations={"mmi2":np.pi},
              reflections={"mmi2":True},
              links=[{"from": ("mmi1", "out1"), "to": ("wg", "in")},
                     {"from": ("wg", "out"), "to": ("mmi2", "out1")},
                     {"from": ("mmi1", "out2"), "to": ("mmi2", "out2")},
                     ],
              op_trace=CustomTrace
              )
# end of mzi

if development:
       draw(mzi, path, scaling=9)

# lib = gdstk.Library()
# lib.add(balanced_mzi, *balanced_mzi.dependencies(True))
# lib.write_gds(path + "balanced_mzi.gds", max_points=4000)
# draw(balanced_mzi, path, scale=10)


