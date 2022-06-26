import palgds.base_cells as bc


class WaveguideTrace(bc.Trace):
    """Trace template for optical routes"""

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=0.45, bend_radius=bend_radius, layer=0, datatype=0, port_type='op')


class WireTrace(bc.Trace):
    """Trace template for electrical routes"""

    def __init__(self, name, points, bend_radius=0):
        super().__init__(name, points, width=2, bend_radius=bend_radius, layer=21, datatype=0, port_type='el')


class Technology:

    def __init__(self):
        self.name = 'Default Technology'

    def clear_technology(self):
        keys_list = list(self.__dict__.keys())
        for i in keys_list:
            delattr(self, i)

class TechnologySubGroup:

    def __init__(self, name):
        self.name = name


TECH = Technology()

# Traces
TECH.TRACE = TechnologySubGroup('TRACE')
TECH.TRACE.WAVEGUIDE_TRACE = WaveguideTrace
TECH.TRACE.WIRE_TRACE = WireTrace

# Layers - (LAYER, DATATYPE)
TECH.LAYER = TechnologySubGroup('LAYER')
TECH.LAYER.CORE = (0, 0)

# Dimensions
TECH.DIMENSION = TechnologySubGroup('DIMENSION')
TECH.DIMENSION.BEND_RADIUS = 5
TECH.DIMENSION.WG_WIDTH = 0.45








