import gdstk
from palgds.utils import read_ports_from_txt_file

# long term To-Do: Class definitions for ports

class PCell(gdstk.Cell):

    def __init__(self, name, ports=None):
        super().__init__(name)
        self.ports = ports if ports is not None else {}

    def _create_elements(self, *args, **kwargs):
        pass

    def _create_ports(self, *args, **kwargs):
        pass

    def __repr__(self):
        rep = 'PCell name: ' + self.name + ' --- Ports: ' + str(len(self.ports))+ \
              ' --- Type: ' + str(type(self).__name__)
        return rep

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
        self.ports.update({"in": (points[0][0], points[0][1], 180, port_type),
                           "out": (points[-1][0], points[-1][1], 0, port_type)})

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
            self.ports.update(read_ports_from_txt_file(ports_filename))

class GDSRawCell(gdstk.RawCell):
    # To be implemented later ...
    def __init__(self, filename, cell_name, ports=None, ports_filename=None):
        # self._create_elements(filename, cell_name)
        # ports = self._create_ports(ports, ports_filename)
        super().__init__(cell_name)
        pass

    def _create_elements(self, filename, cell_name):
        self._raw_cells = gdstk.read_rawcells(filename)
        return self._raw_cells[cell_name]

    def _create_ports(self, ports, ports_filename):
        if ports is not None:
            return ports
        elif ports_filename is None:
            return {}
        else:
            return read_ports_from_txt_file(ports_filename)



