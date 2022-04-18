import gdstk
from palgds.utils import read_ports_from_txt_file


class PCell:
    def __init__(self, cell, ports=None):
        self._validate_inputs(cell, ports)
        self.cell = cell
        self.ports = ports if ports is not None else {}

    def _validate_inputs(self, cell, ports):
        pass

    def _generate_cell(self, *args, **kwargs):
        pass

    def _generate_ports(self, *args, **kwargs):
        pass

    @property
    def name(self):
        return self.cell.name

    def __repr__(self):
        rep = 'PCell name: ' + self.name + ' --- Ports: ' + str(len(self.ports))+ \
              ' --- Type: ' + str(type(self).__name__)
        return rep

class Trace(PCell):

    def __init__(self, name, points, width=0.45, offset=0, bend_radius=5, layer=0, datatype=0):
        cell = self._generate_cell(name, points, width, offset, bend_radius, layer, datatype)
        ports = {"in": (points[0][0], points[0][1], 180), "out": (points[-1][0], points[-1][1], 0)}
        super().__init__(cell, ports)

    def _generate_cell(self, name, points, width, offset, bend_radius, layer, datatype):
        cell = gdstk.Cell(name)
        shape = gdstk.FlexPath(points, width, offset, bend_radius=bend_radius, layer=layer, datatype=datatype,
                                   tolerance=2e-4)
        cell.add(shape)
        return cell

    def _generate_ports(self, *args, **kwargs):
        pass

class TextCell(PCell):
    def __init__(self, name, text, size=35, position=(0,0), vertical=False, layer=100, datatype=0):
        text_polygons = gdstk.text(text, size, position, vertical, layer, datatype)
        cell = gdstk.Cell(name)
        cell.add(*text_polygons)
        super(TextCell, self).__init__(cell)

    def _generate_cell(self, *args, **kwargs):
        pass

    def _generate_ports(self, *args, **kwargs):
        pass

class GDSCell(PCell):
    def __init__(self, filename, cell_name=None, rename=None, prefix_subcells=True, ports=None, ports_filename=None):
        cell = self._generate_cell(filename, cell_name, rename, prefix_subcells)
        ports = self._generate_ports(ports, ports_filename)
        super(GDSCell, self).__init__(cell, ports)

    def _generate_cell(self, filename, cell_name, rename, prefix_subcells):
        temp_lib = gdstk.read_gds(filename)
        cell = None

        if cell_name is None:
            cell = temp_lib.top_level()[0]
        else:
            for c in temp_lib.cells:
                if c.name == cell_name:
                    cell = c

        if rename is not None:
            cell.name = rename

        if prefix_subcells:
            for i in cell.dependencies(True):
                i.name = cell.name + '_' + i.name
        return cell

    def _generate_ports(self, ports, ports_filename):
        if ports is not None:
            return ports
        elif ports_filename is None:
            return {}
        else:
            return read_ports_from_txt_file(ports_filename)

class GDSRawCell(PCell):
    def __init__(self, filename, cell_name, ports=None, ports_filename=None):
        cell = self._generate_cell(filename, cell_name)
        ports = self._generate_ports(ports, ports_filename)
        super(GDSRawCell, self).__init__(cell, ports)

    def _generate_cell(self, filename, cell_name):
        self._raw_cells = gdstk.read_rawcells(filename)
        return self._raw_cells[cell_name]

    def _generate_ports(self, ports, ports_filename):
        if ports is not None:
            return ports
        elif ports_filename is None:
            return {}
        else:
            return read_ports_from_txt_file(ports_filename)



