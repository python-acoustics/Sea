.. _freecad-sea:

SEA in FreeCAD
###############

.. toctree::
   :maxdepth: 2
   
   
The previous chapter explained what Statistical Energy Analysis is. 
In this chapter we will have a closer look on how SEA is implemented in FreeCAD-SEA.

An SEA model in FreeCAD-SEA is represented by the following objects

* System
* Component
* Subsystem
* Coupling
* Material
* Excitation

Additionaly, FreeCAD objects containing a Shape (like Part) are used for the geometry.

To perform an SEA analysis the document has to contain a geometry of the structure under investigation.
When the geometry is present, it is possible to add SEA objects manually, or to construct a model automatically from the geometry.
Rudimentary rules are used to decide what types of each object should be used. 
It is also possible to detect whether components collide and automatically add the relevent type of coupling. 

Next step is to set the properties of all the objects.
when all properties have been set, the modal energies can be solved. 
This can graphically be done by selecting an SEA System and then :menuselection:`Analysis --> Solve` or 
through Python by executing Sea.actions.solve(system) where system is the DocumentObject of the model to be solved. 
