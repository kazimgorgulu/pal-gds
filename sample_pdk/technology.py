import palgds.technology as tech
import palgds.base_cells as bc

TECH = tech.TECH
TECH.clear_technology()
TECH.name = 'Sample Technology'

class WaveguideTrace(bc.Trace):
    """Trace template for optical routes"""

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=[0.45, 4.45], bend_radius=bend_radius, layer=[0, 1], datatype=[0, 0], port_type='op')
        

class WireTrace(bc.Trace):
    """Trace template for electrical routes"""

    def __init__(self, name, points, bend_radius=0):
        super().__init__(name, points, width=1.5, bend_radius=bend_radius, layer=10, datatype=0, port_type='el')
        

# Traces
TECH.TRACE = tech.TechnologySubGroup('TRACE')
TECH.TRACE.WAVEGUIDE_TRACE = WaveguideTrace
TECH.TRACE.WIRE_TRACE = WireTrace

# Layers - in the form of: (LAYER, DATATYPE)
TECH.LAYER = tech.TechnologySubGroup('LAYER')
TECH.LAYER.CORE = (0, 0)
TECH.LAYER.CLD = (1, 0)

# Dimensions
TECH.DIMENSION = tech.TechnologySubGroup('DIMENSION')
TECH.DIMENSION.BEND_RADIUS = 5
TECH.DIMENSION.WG_WIDTH = 0.45