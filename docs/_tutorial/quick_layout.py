import gdstk
import numpy as np
import palgds.base_cells as bc
from palgds.pcell_library import DirectionalCoupler
import os 
from draw import draw

os.chdir(os.path.dirname(os.path.abspath(__file__)))

development = True
path = os.path.dirname(os.path.abspath(__file__)) + "/"




dc = DirectionalCoupler(name="Directional_Coupler")

dc.write_svg("Directional_Coupler.svg")
lib = gdstk.Library()
lib.add(dc, *dc.dependencies(True))
lib.write_gds("Directional_Coupler.gds", max_points=4000)

if development:
    draw(dc, path)


gc = bc.GDSCell(name="Grating_Coupler", filename='Grating_Coupler.gds', ports={"in": bc.Port((0, 0), 0, "op")})
