"""PCell library for common photonic components."""
import gdstk
import numpy as np
import palgds.base_cells as bc


# Directional Coupler:
class DirectionalCoupler(bc.PCell):
    """Directional coupler cell."""
    def __init__(self, name, Lc=10, gap=0.2, width=0.45, Ls=8, y_span=4, layer=0, datatype=0, tolerance=1e-3):
        """

        :param name:
        :param Lc:
        :param gap:
        :param width:
        :param Ls:
        :param y_span:
        :param layer:
        :param datatype:
        :param tolerance:
        """
        super().__init__(name)
        self._create_elements(Lc, gap, width, Ls, y_span, layer=0, datatype=0, tolerance=1e-3)
        self._create_ports(Lc)

    def _create_elements(self, Lc, gap, width, Ls, y_span, layer=0, datatype=0, tolerance=1e-3):
        sbend_width = y_span/2 - gap/2 - width/2
        path1 = gdstk.RobustPath((0, -y_span/2), width, layer=0, datatype=0, tolerance=1e-3)
        path1.parametric(*self._s_bend(Ls, sbend_width), width=width)
        path1.segment((Lc+Ls, -gap/2-width/2))
        path1.parametric(*self._s_bend(Ls, -sbend_width), width=width)

        path2 = gdstk.RobustPath((0, y_span/2), width, layer=0, datatype=0, tolerance=1e-3)
        path2.parametric(*self._s_bend(Ls, -sbend_width), width=width)
        path2.segment((Lc + Ls, +gap / 2 + width / 2))
        path2.parametric(*self._s_bend(Ls, sbend_width), width=width)
        
        self.add(path1, path2)

    def _create_ports(self, Lc=10,  Ls=8, y_span=4):
        self.ports.update({"in1": bc.Port((0, y_span/2), np.pi, "op"),
                           "in2": bc.Port((0, -y_span/2), np.pi, "op"),
                           "out1": bc.Port((Lc + 2*Ls, y_span/2), 0, "op"),
                           "out2": bc.Port((Lc + 2*Ls, -y_span/2), 0, "op"), 
                           })

    def _s_bend(self, length, delta):
        func = lambda u: np.array((length * u, (1 - np.cos(np.pi * u)) / 2 * delta))
        grad = lambda u: np.array((length, np.sin(np.pi * u) / 2 * delta))
        return func, grad


# Ring Resonator:
class RingResonator(bc.PCell):
    """Ring resonator cell."""
    def __init__(self, name, radius, gap, width, layer=0, datatype=0):
        """
        :param name:
        :param radius:
        :param gap:
        :param width:
        :param layer:
        :param datatype:
        """
        super().__init__(name)
        self._create_elements(radius, gap, width, layer, datatype)
        self._create_ports(radius)

    def _create_elements(self, radius, gap, width, layer, datatype):
        center = (0, radius+gap+width)
        ring = gdstk.ellipse(center, radius+width/2, radius-width/2, layer=layer, datatype=datatype, tolerance=2e-4)
        straight_waveguide = gdstk.rectangle((-radius, -width/2), (radius, width/2), layer=layer, datatype=datatype)
        self.add(ring, straight_waveguide)

    def _create_ports(self, radius):
        self.ports.update({"in": bc.Port((-radius, 0), np.pi, "op"),
                           "out": bc.Port((radius, 0), 0, "op"),})
