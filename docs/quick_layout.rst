Quick Layout
-----------------

In this section we will create a simple circuit layout with a directional coupler and grating couplers. We will first create 
individual component cells and then create circuit by connecting these components. 
We will use parametric cell definition of direcional coupler existing 
in ``pcell_library`` in ``palgds`` to keep tutorial short. 

Let's start by importing following packages:

.. literalinclude:: _tutorial/quick_layout.py
    :start-at: import gdstk
    :end-before: from palgds.pcell_library import DirectionalCoupler


Now, let's create a directional coupler cell with 0.45 um wide waveguides, 10 um coupling length, 0.2 um gap, and y-span of 4 um:



.. code-block:: python

    gc = bc.GDSCell(name="Grating_Coupler", filename='Grating_Coupler.gds',
                    ports={"in": bc.Port((1, 0), 0, "op")})
