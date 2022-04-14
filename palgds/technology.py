import palgds.base_cells as bc


class OpticalTrace(bc.Trace):
    """Trace template for optical trace"""

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=0.5, bend_radius=bend_radius, offset=0, layer=0, datatype=0)
        pass

class MetalTrace(bc.Trace):
    """Trace template for metal trace"""

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=1.5, bend_radius=bend_radius, offset=0, layer=10, datatype=0)
        pass

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
TECH.TRACE.OPTICAL_TRACE = OpticalTrace
TECH.TRACE.METAL_TRACE = MetalTrace

# Layers - [LAYER, DATABASE]
TECH.LAYER = TechnologySubGroup('LAYER')
TECH.LAYER.CORE = [0, 0]
TECH.LAYER.CLD = [1, 0]

# Dimensions
TECH.DIMENSION = TechnologySubGroup('DIMENSION')
TECH.DIMENSION.BEND_RADIUS = 5
TECH.DIMENSION.WG_WIDTH = 0.45








