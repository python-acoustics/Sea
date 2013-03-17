.. _reference:

Reference
#########

.. toctree::
    :maxdepth: 2
    
This section is a reference of all available classes and functions in FreeCAD-SEA.


Gui
***
.. inheritance-diagram:: gui
.. automodule:: gui
   :show-inheritance:
   :members:

Analysis
======== 
.. inheritance-diagram:: gui.analysis
.. automodule:: gui.analysis
   :show-inheritance:
   :members:

.. inheritance-diagram:: gui.analysis.actions
.. automodule:: gui.analysis.actions
   :show-inheritance:
   :members:
   
Add item
======== 
.. inheritance-diagram:: gui.addItem
.. automodule:: gui.addItem
   :show-inheritance:
   :members:   
   
.. inheritance-diagram:: gui.addItem.actions
.. automodule:: gui.addItem.actions
   :show-inheritance:
   :members:
   
SEA
***
.. inheritance-diagram:: Sea
.. automodule:: Sea
   :show-inheritance:
   :members:
   
Model
=====
.. inheritance-diagram:: Sea.model
.. automodule:: Sea.model
   :show-inheritance:
   :members:

System
------
.. inheritance-diagram:: Sea.model.system
.. automodule:: Sea.model.system
   :show-inheritance:
   :members:

Base classes
------------
.. inheritance-diagram:: Sea.model.baseclasses
.. automodule:: Sea.model.baseclasses
   :show-inheritance:
   :members:


Connection
------------
.. inheritance-diagram:: Sea.model.connection
.. automodule:: Sea.model.connection
   :show-inheritance:
   :members:
   
Couplings
---------
.. inheritance-diagram:: Sea.model.couplings
.. automodule:: Sea.model.couplings
   :show-inheritance:
   :members:
   
Point
^^^^^   
.. inheritance-diagram:: Sea.model.couplings.coupling_1D_structural
.. automodule:: Sea.model.couplings.coupling_1D_structural
   :show-inheritance:
   :members:

Line
^^^^^   
.. inheritance-diagram:: Sea.model.couplings.coupling_2D_structural
.. automodule:: Sea.model.couplings.coupling_2D_structural
   :show-inheritance:
   :members:

Plate to Cavity
^^^^^^^^^^^^^^^^   
.. inheritance-diagram:: Sea.model.couplings.coupling_3D_platecavity
.. automodule:: Sea.model.couplings.coupling_3D_platecavity
   :show-inheritance:
   :members:
   
Cavity to Plate
^^^^^^^^^^^^^^^^
.. inheritance-diagram:: Sea.model.couplings.coupling_3D_cavityplate
.. automodule:: Sea.model.couplings.coupling_3D_cavityplate
   :show-inheritance:
   :members:
   
      
   
Excitations
-----------
.. inheritance-diagram:: Sea.model.excitations
.. automodule:: Sea.model.excitations
   :show-inheritance:
   :members:


Materials
---------
.. inheritance-diagram:: Sea.model.materials
.. automodule:: Sea.model.materials
   :show-inheritance:
   :members:

Components   
----------
.. inheritance-diagram:: Sea.model.components
.. automodule:: Sea.model.components
   :show-inheritance:
   :members:
   
Beam 
^^^^
.. inheritance-diagram:: Sea.model.components.structural_1D_beam
.. automodule:: Sea.model.components.structural_1D_beam
   :show-inheritance:
   :members: Component1DBeam, SubsystemLong, SubsystemBend, SubsystemShear
   
Plate
^^^^^
.. inheritance-diagram:: Sea.model.components.structural_2D_plate
.. automodule:: Sea.model.components.structural_2D_plate
   :show-inheritance:
   :members: Component2DPlate, SubsystemLong, SubsystemBend, SubsystemShear

Cavity2D
^^^^^^^^
.. inheritance-diagram:: Sea.model.components.cavity_2D
.. automodule:: Sea.model.components.cavity_2D
   :show-inheritance:
   :members: Component2DCavity, SubsystemLong

   
Cavity3D
^^^^^^^^
.. inheritance-diagram:: Sea.model.components.cavity_3D
.. automodule:: Sea.model.components.cavity_3D
   :show-inheritance:
   :members: Component3DCavity, SubsystemLong
   
   
   
Adapter
========

.. inheritance-diagram:: Sea.adapter
.. automodule:: Sea.adapter
   :show-inheritance:
   :members:

System
------
.. inheritance-diagram:: Sea.adapter.system
.. automodule:: Sea.adapter.system
   :show-inheritance:
   :members:


Base classes
------------
.. inheritance-diagram:: Sea.adapter.baseclasses
.. automodule:: Sea.adapter.baseclasses
   :show-inheritance:
   :members:

Connection
----------
.. inheritance-diagram:: Sea.adapter.connection
.. automodule:: Sea.adapter.connection
   :show-inheritance:
   :members:
   
Couplings
---------
.. inheritance-diagram:: Sea.adapter.couplings
.. automodule:: Sea.adapter.couplings
   :show-inheritance:
   :members:   


Point
^^^^^   
.. inheritance-diagram:: Sea.adapter.couplings.coupling_1D_structural
.. automodule:: Sea.adapter.couplings.coupling_1D_structural
   :show-inheritance:
   :members:

Line
^^^^^   
.. inheritance-diagram:: Sea.adapter.couplings.coupling_2D_structural
.. automodule:: Sea.adapter.couplings.coupling_2D_structural
   :show-inheritance:
   :members:

Plate to Cavity
^^^^^^^^^^^^^^^^   
.. inheritance-diagram:: Sea.adapter.couplings.coupling_3D_platecavity
.. automodule:: Sea.adapter.couplings.coupling_3D_platecavity
   :show-inheritance:
   :members:
   
Cavity to Plate
^^^^^^^^^^^^^^^^
.. inheritance-diagram:: Sea.adapter.couplings.coupling_3D_cavityplate
.. automodule:: Sea.adapter.couplings.coupling_3D_cavityplate
   :show-inheritance:
   :members:
      
   
   
   
Excitations
-----------
.. inheritance-diagram:: Sea.adapter.excitations
.. automodule:: Sea.adapter.excitations
   :show-inheritance:
   :members: 
   
Materials
-----------
.. inheritance-diagram:: Sea.adapter.materials
.. automodule:: Sea.adapter.materials
   :show-inheritance:
   :members: 
   
Components   
----------
.. inheritance-diagram:: Sea.adapter.components
.. automodule:: Sea.adapter.components
   :show-inheritance:
   :members:
   
Beam
^^^^^^^^^^^^^^
.. inheritance-diagram:: Sea.adapter.components.structural_1D_beam
.. automodule:: Sea.adapter.components.structural_1D_beam
   :show-inheritance:
   :members: 
   
Plate
^^^^^^^^^^^^^^
.. inheritance-diagram:: Sea.adapter.components.structural_2D_plate
.. automodule:: Sea.adapter.components.structural_2D_plate
   :show-inheritance:
   :members: 

Cavity2D
^^^^^^^^
.. inheritance-diagram:: Sea.adapter.components.cavity_2D
.. automodule:: Sea.adapter.components.cavity_2D
   :show-inheritance:
   :members: 

   
Cavity3D
^^^^^^^^
.. inheritance-diagram:: Sea.adapter.components.cavity_3D
.. automodule:: Sea.adapter.components.cavity_3D
   :show-inheritance:
   :members: 

   
   
Actions
========

.. automodule:: Sea.actions


General
---------

.. inheritance-diagram:: Sea.actions.actions
.. automodule:: Sea.actions.actions
   :show-inheritance:
   :members:
   
Factory
-----------
.. inheritance-diagram:: Sea.actions.factory
.. automodule:: Sea.actions.factory
   :show-inheritance:
   :members:

Document
-----------
.. inheritance-diagram:: Sea.actions.document
.. automodule:: Sea.actions.document
   :show-inheritance:
   :members:    

System
-----------
.. inheritance-diagram:: Sea.actions.system
.. automodule:: Sea.actions.system
   :show-inheritance:
   :members:    

Connection
-----------
.. inheritance-diagram:: Sea.actions.connection
.. automodule:: Sea.actions.connection
   :show-inheritance:
   :members:    
   
Component
-----------
.. inheritance-diagram:: Sea.actions.component
.. automodule:: Sea.actions.component
   :show-inheritance:
   :members:    

