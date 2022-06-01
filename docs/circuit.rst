Creating Circuits
-----------------


``Circuit`` class in ``palgds`` is used for creating automated layouts of complex photonic circuits.
The designer provides the individidual components and the links between their ports. The optical or 
electrical routes automatically generated in ``Circuit`` class. 


Circuit Layout 1: Basics
***************************

In this section we will create a simple circuit with a ring resonator and grating couplers. For this, we will use the same ring
resonator PCell definition that we used in previous section.

.. code-block:: python
    
    import gdstk
    import numpy as np
    import palgds.base_cells as bc
    from palgds.circuit import Circuit


    ring_res = RingResonator(name="RingRes", radius=10, gap=0.2, width=0.45)


We will grating coupler PCell by reading an existing  GDS file. Make sure you download and put "Grating_Coupler.gds" 
file into your working directory. Here, we are manually providing the port of the grating coupler.

.. code-block:: python

    gc = bc.GDSCell(name="Grating_Coupler", filename='Grating_Coupler.gds',
                    ports={"in": bc.Port((1, 0), 0, "op")})



Now, we will create the circuit using these components. Here, ``pcells`` is the dict of cells that compose the circuit. ``translation`` (default: ``(0, 0)``) and
``rotation`` (default: ``0`` in radians) are transformations of individual components. Connections between ports are provided
with ``links``. Waveguide routes between the connected ports will be created with default trace with 450 nm wide waveguides. 

.. literalinclude:: _tutorial/example1.py
    :start-at: circuit = Circuit(name='RingResCircuit',
    :end-before: # end of circuit

Then, export layout:

.. code-block:: python

    lib = gdstk.Library()
    lib.add(circuit, *circuit.dependencies(True))
    lib.write_gds("RingResCircuit.gds", max_points=4000)

.. image:: _tutorial/RingResCircuit.svg
    :align: center



Circuit Layout 2: Advanced
************************************

In this section, we will build the layout of balanced and unbalanced Mach-Zehnder interferometer circuits. 
We will first create a directional coupler and then create a custom ``Trace`` to be 
used as routing template in the  circuit.

Parametric definition of a directional coupler exists in ``pcell_library`` of ``palgds``. Therefore, start with
following imports and create directional coupler:

.. code-block:: python

    import gdstk
    import numpy as np
    import palgds.base_cells as bc
    from palgds.circuit import Circuit

    from palgds.pcell_library import DirectionalCoupler

    dc = DirectionalCoupler(name="Directional_Coupler", Lc=10, width=0.45, gap=0.2, y_span=4)

.. image:: _tutorial/Directional_Coupler.svg
    :align: center


Default waveguide trace in ``palgds`` is a 450 nm wide waveguide with a layer number of '0'. Let's create 
a custom trace template with two layers representing a waveguide with core and cladding:


.. literalinclude:: _tutorial/example1.py
    :start-at: class CustomTrace(bc.Trace):
    :end-before: # End of trace class


Let's create a sample waveguide layout with this trace.

.. code-block:: python

    trace = CustomTrace(name='Trace', points=[(0, 0), (20, 0), (20, 10), (40, 10)])

.. image:: _tutorial/Trace.svg
    :align: center


Now, we will create a balanced Mach-Zehnder interferometer circuit:

.. literalinclude:: _tutorial/example1.py
    :start-at: balanced_mzi = Circuit(name='Balanced_MZI',
    :end-before: # end of balanced mzi


.. image:: _tutorial/Balanced_MZI.svg
    :align: center



