import gdstk
import palgds.base_cells as bc
import palgds.technology as tech
import palgds.utils as utils

TECH = tech.TECH

class Circuit(bc.PCell):

    def __init__(self, name, pcells, translations=None, rotations=None, reflections=None, links=None,
                 op_trace=None, op_bend_radius=None, el_trace=None, el_bend_radius=None):
        self.pcells = pcells
        self.translations = translations
        self.rotations = rotations
        self.reflections = reflections
        self.links = links
        self.op_trace = op_trace
        self.op_bend_radius = op_bend_radius
        self.el_trace = el_trace
        self.el_bend_radius = el_bend_radius

        self._preprocess_inputs()
        cell = self._create_cell(name)
        ports = self._create_ports()
        super().__init__(cell, ports)

    def _create_cell(self, name):
        cell = gdstk.Cell(name)
        for key in self.pcells:
            cell.add(gdstk.Reference(self.pcells[key].cell,
                                    origin=self.translations[key],
                                    x_reflection=self.reflections[key],
                                    rotation=self.rotations[key]))

        cells_of_links = self._create_cells_of_links(name)
        for _cell in cells_of_links:
            cell.add(gdstk.Reference(_cell))

        return cell

    def _preprocess_inputs(self):
        self.translations = {} if self.translations is None else self.translations
        self.rotations = {} if self.rotations is None else self.rotations
        self.reflections = {} if self.reflections is None else self.reflections
        self.links = [] if self.links is None else self.links
        self.op_trace = TECH.TRACE.OPTICAL_TRACE if self.op_trace is None else self.op_trace
        self.op_bend_radius = TECH.DIMENSION.BEND_RADIUS if self.op_bend_radius is None else self.op_bend_radius
        self.el_trace = TECH.TRACE.METAL_TRACE if self.el_trace is None else self.el_trace
        self.el_bend_radius = 0 if self.el_bend_radius is None else self.el_bend_radius

        for key in self.translations.keys():
            if key not in self.pcells.keys():
                print("There is no PCell '", key, "' in pcells to apply translation!", sep='')
                raise KeyError(key)
        for key in self.rotations.keys():
            if key not in self.pcells.keys():
                print("There is no PCell '", key, "' in pcells to apply rotation!", sep='')
                raise KeyError(key)
        for key in self.reflections.keys():
            if key not in self.pcells.keys():
                print("There is no PCell '", key, "' in pcells to apply reflection!", sep='')
                raise KeyError(key)
        for link in self.links:
            if link["from"][0] not in self.pcells.keys():
                print("There is no PCell '", link["from"][0], "' in pcells to create link!", sep='')
                raise KeyError(link["from"][0])
            if link["to"][0] not in self.pcells.keys():
                print("There is no PCell '", link["to"][0], "' in pcells to create link!", sep='')
                raise KeyError(link["to"][0])

        for key in self.pcells.keys():
            if key not in self.translations.keys():
                self.translations.update({key: (0, 0)})
            if key not in self.rotations.keys():
                self.rotations.update({key: 0})
            if key not in self.reflections.keys():
                self.reflections.update({key: False})

    def _create_cells_of_links(self, name):
        cells_of_links = []
        k = 0
        for link in self.links:
            port0 = self.pcells[link["from"][0]].ports[link["from"][1]]
            port1 = self.pcells[link["to"][0]].ports[link["to"][1]]

            print(port0[3], port1[3] )
            if port0[3] == port1[3] == "op":
                trace = self.op_trace
                bend_radius = self.op_bend_radius
            elif port0[3] == port1[3] == "el":
                trace = self.el_trace
                bend_radius = self.el_bend_radius
            else:
                raise ValueError("Trying to connect different port types!" +
                                 f" --- port0_type:{port0[3]} vs port1_type:{port1[3]}" )

            # Apply transformations to ports:
            port0 = utils.apply_transformation(port0,
                                               self.translations[link["from"][0]],
                                               self.rotations[link["from"][0]],
                                               self.reflections[link["from"][0]])

            port1 = utils.apply_transformation(port1,
                                               self.translations[link["to"][0]],
                                               self.rotations[link["to"][0]],
                                               self.reflections[link["to"][0]])


            points = utils.calculate_path_between_two_ports(port0=port0, port1=port1, bend_radius=bend_radius)
            link_cell = trace(name +'_link' + str(k), points, bend_radius=bend_radius)
            k += 1
            cells_of_links.append(link_cell.cell)

        return cells_of_links

    def _create_ports(self, *args, **kwargs):
        ports = {}
        k = 0
        for key in self.pcells:
            for i in self.pcells[key].ports:
                is_used = False
                for link in self.links:
                    if link["from"][0] == key and link["from"][1] == i:
                        is_used = True
                    if link["to"][0] == key and link["to"][1] == i:
                        is_used = True
                if not is_used:
                    _port = self.pcells[key].ports[i]
                    _port = utils.apply_transformation(_port, self.translations[key], self.rotations[key],
                                                       self.reflections[key])

                    ports.update({"port"+str(k):_port})
                    k += 1

        return ports