import gdstk
import numpy as np
import palgds.base_cells as bc
from palgds.circuit import Circuit
from palgds.pcell_library import DirectionalCoupler
import os 
from draw import draw

os.chdir(os.path.dirname(os.path.abspath(__file__)))

development = True
#path = os.path.dirname(os.path.abspath(__file__)) + "/"
path = "../_source_files/"



dc = DirectionalCoupler(name="DC", Lc=10, width=0.45, Ls=8, y_span=4, layer=0, datatype=0)
dc.write_svg(path + "DC.svg")
if development:
    draw(dc, path, scaling=7)


gc = bc.GDSCell(name="GC", filename=path+'GC.gds', ports={"in": bc.Port((0, 0), 0, "op")})
if development:
    draw(gc, path, scaling=6)

dc_circuit = Circuit(name='DC_Circuit',
                  pcells={"dc": dc, "gc1": gc, "gc2": gc, "gc3": gc, "gc4": gc},
                  translations={"dc": (0, 0),
                                "gc1": (-15, 15),
                                "gc2": (-15, -15),
                                "gc3": (40, 15),
                                "gc4": (40, -15),
                                },
                  rotations={"gc3": np.pi, "gc4": np.pi},
                  links=[{"from": ("dc", "in1"), "to": ("gc1", "in")},
                         {"from": ("dc", "in2"), "to": ("gc2", "in")},
                         {"from": ("dc", "out1"), "to": ("gc3", "in")},
                         {"from": ("dc", "out2"), "to": ("gc4", "in")},
                         ]
                  )
# end of dc_circuit
        
if development:
    draw(dc_circuit, path, scaling=5)


# lib = gdstk.Library()
# lib.add(dc_circuit, *dc_circuit.dependencies(True))
# lib.write_gds(path + "DC_Circuit.gds", max_points=4000)

