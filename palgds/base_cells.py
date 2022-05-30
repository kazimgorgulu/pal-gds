import gdstk
from palgds.utils import read_raw_ports_from_txt_file
import numpy as np


class PCell(gdstk.Cell):

    def __init__(self, name, ports=None):
        super().__init__(name)
        self.ports = ports if ports is not None else {}

    def _create_elements(self, *args, **kwargs):
        pass

    def _create_ports(self, *args, **kwargs):
        pass

    def __repr__(self):
        return object.__repr__(self) + " " + self.__dict__.__str__()

    def __str__(self):
        s = f"PCell <{type(self).__name__}> name:'{self.name}' with {len(self.ports)} ports, {len(self.polygons)}" \
            f" polygons, {len(self.paths)} paths, {len(self.references)} references, and {len(self.labels)} labels"
        return s

class Trace(PCell):
    # To-Do: Directional fix is required for ports.
    def __init__(self, name, points, width=0.45, offset=0, bend_radius=5, layer=0, datatype=0, port_type='op'):
        super().__init__(name)
        self._create_elements(points, width, offset, bend_radius, layer, datatype)
        self._create_ports(points, port_type)

    def _create_elements(self, points, width, offset, bend_radius, layer, datatype):
        shape = gdstk.FlexPath(points, width, offset, bend_radius=bend_radius, layer=layer, datatype=datatype,
                               tolerance=2e-4)
        self.add(shape)

    def _create_ports(self, points, port_type):
        self.ports.update({"in": Port((points[0][0], points[0][1]), np.pi , port_type),
                           "out": Port((points[-1][0], points[-1][1]), 0, port_type)})

class TextCell(PCell):
    def __init__(self, name, text, size=35, position=(0,0), vertical=False, layer=100, datatype=0):
        super().__init__(name)
        text_polygons = gdstk.text(text, size, position, vertical, layer, datatype)
        self.add(*text_polygons)

    def _create_elements(self, *args, **kwargs):
        pass

    def _create_ports(self, *args, **kwargs):
        pass

class GDSCell(PCell):
    def __init__(self, name, filename, rename=None, prefix_subcells=True, ports=None, ports_filename=None):
        super().__init__(name)
        self._create_elements(filename, name, rename, prefix_subcells)
        self._create_ports(ports, ports_filename)

    def _create_elements(self, filename, name, rename, prefix_subcells):
        temp_lib = gdstk.read_gds(filename)
        for c in temp_lib.cells:
            if c.name == name:
                self.add(*c.polygons,*c.paths, *c.labels, *c.references)

        if rename is not None:
            self.name = rename

        if prefix_subcells:
            for i in self.dependencies(True):
                i.name = self.name + '_' + i.name

    def _create_ports(self, ports, ports_filename):
        if ports is not None:
            self.ports.update(ports)
        elif ports_filename is None:
            pass
        else:
            raw_ports = read_raw_ports_from_txt_file(ports_filename)
            for key, value in raw_ports.items():
                self.ports.update({key: Port(value[:2], value[2], value[3])})

class Port:
    def __init__(self, position, angle, port_type="op"):
        self.position = position
        self.angle = angle
        self.port_type = port_type

    def __repr__(self):
        s = f'Port(position=({self.position[0]:.3f}, {self.position[1]:.3f}), angle={self.angle:.3f},' \
            f' port_type={self.port_type})'
        return s



