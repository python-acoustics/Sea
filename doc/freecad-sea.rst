.. _freecad-sea:

SEA in FreeCAD
###############

.. toctree::
   :maxdepth: 2
   
The previous chapter explained what Statistical Energy Analysis is. 
In this chapter we will have a closer look on how SEA is implemented in FreeCAD-SEA.

=========
Overview
=========

An SEA model in FreeCAD-SEA is represented by the descendents of the following abstract objects

* :class:`Sea.adapter.baseclasses.Component`
* :class:`Sea.adapter.baseclasses.Coupling`
* :class:`Sea.adapter.baseclasses.Material`
* :class:`Sea.adapter.baseclasses.Excitation`

as well as

* :class:`Sea.adapter.system.System`

Additionaly, :mod:`FreeCAD` objects containing a Shape (like :mod:`Part` classes) are used for the geometry.

Each :mod:`Sea.adapter` class has an attribute :attr:`model`, with which it refers to a :mod:`Sea.model` class of the same type.

.. blockdiag::

    blockdiag components {
      Adapter -> Model;
    }



To perform an SEA analysis the document has to contain a geometry of the
structure under investigation. When the geometry is present, it is possible to
add SEA objects manually, or to construct a model automatically from the
geometry. Rudimentary rules are used to decide what types of each object should
be used. It is also possible to detect whether components collide and
automatically add the relevent type of coupling. 

Next step is to set the properties of all the objects.
when all properties have been set, the modal energies can be solved. 
This can graphically be done by selecting an SEA System and then :menuselection:`Analysis --> Solve` or 
through Python by executing ``Sea.actions.solve(system)`` where system is the ``DocumentObject`` of the model to be solved. 

=============
Model classes
=============
The :mod:`Sea.model` classes describe the physics involved in SEA. The baseclasses describe properties that are common to all classes of that type.
For instance, :class:`Sea.model.baseclasses.Component` describes properties that are identical or mandatory for every component in :mod:`Sea.model.components`.

===============
Adapter classes
===============
The :mod:`Sea.adapter` classes give FreeCAD access to the physics described in the :mod:`Sea.model` classes.
The adapter objects all contain the attribute :attr:`model` which on initialization creates 
a :mod:`Sea.model` object of the respective class.

