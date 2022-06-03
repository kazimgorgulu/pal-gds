Quick Layout
-----------------

In this section we will create a simple circuit layout with a directional coupler and grating couplers. We will first create 
individual component cells and then create circuit by connecting these components. 
We will use parametric cell definition of directional coupler existing 
in ``pcell_library`` in ``palgds`` to keep tutorial short. 

Let's start by importing following packages:

.. literalinclude:: _tutorial/quick_layout.py
    :start-at: import gdstk
    :end-at: from palgds.pcell_library import DirectionalCoupler


Now, let's create a directional coupler cell with 0.45 um wide waveguides, 10 um coupling length, 0.2 um gap, and y-span of 4 um.



.. code-block:: python

    dc = DirectionalCoupler(name="DC", Lc=10, width=0.45, Ls=8, y_span=4, layer=0, datatype=0)

For visualization we can export to svg by using `write_svg` function.

.. code-block:: python

    dc.write_svg("DC.svg")

.. image:: _tutorial/DC.svg
    :align: center


We will grating coupler PCell by reading an existing  GDS file. Make sure you download and put "Grating_Coupler.gds" 
file into your working directory. Here, we are manually providing the port of the grating coupler.

.. code-block:: python

    gc = bc.GDSCell(name="GC", filename='GC.gds',  ports={"in": bc.Port((1, 0), 0, "op")})

.. image:: _tutorial/GC.svg
    :align: center

Now, we will create the circuit using these components. Here, ``pcells`` is the dict of cells that compose the circuit. ``translation`` (default: ``(0, 0)``) and
``rotation`` (default: ``0`` in radians) are transformations of individual components. Connections between ports are provided
with ``links``.


.. literalinclude:: _tutorial/quick_layout.py
    :start-at: circuit = Circuit(name='DC_Circuit',
    :end-before: # end of dc_circuit


.. image:: _tutorial/DC_Circuit.svg
    :align: center


In order to export to GDSII file we need to create a ``gdstk.Library`` and then add ``dc_circuit`` cell to it:

.. code-block:: python

    lib = gdstk.Library()
    lib.add(dc_circuit, *dc_circuit.dependencies(True))
    lib.write_gds("DC_Circuit.gds", max_points=4000)

