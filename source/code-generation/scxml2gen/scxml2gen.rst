.. _tools-scxml2gen:

##################################
scxml2gen
##################################


.. contents::
   :local:


Command line arguments
======================

scxml2gen works in two modes:

-  C++ code generation
-  plantuml state diagram generation

To get a list of supported arguments run:

.. literalinclude:: ./scxml2gen_usage.txt
   :language: bash


Code generation example
=======================

Let's look at the sample command to generate HSM from SCXML:

.. code-block::  Shell

   python3 ./tools/scxml2gen/scxml2gen.py -code -s ./examples/02_generated/02_generated.scxml -c SwitchHsm -thpp ./tools/scxml2gen/template.hpp -tcpp ./tools/scxml2gen/template.cpp -d ./

This will generate two files:


SwitchHsmBase.hpp
-----------------

.. literalinclude:: ./SwitchHsmBase.hpp
   :language: c++


SwitchHsmBase.cpp
-----------------

.. literalinclude:: ./SwitchHsmBase.cpp
   :language: c++


Using custom templates
======================

scxml2gen comes with a predefined template for hpp and cpp files:

- :repo-link:`/tools/scxml2gen/template.cpp`
- :repo-link:`/tools/scxml2gen/template.hpp`

It it doesnt satisfy your project needs you can define your own.
Currently scxml2gen supports following variables:

-  **CLASS_NAME**: name of generated class (constructed as class name +
   suffix provided as arguments)
-  **ENUM_STATES**: name of the enum containing HSM states (constructed
   as class name + "States")
-  **ENUM_EVENTS**: name of the enum containing HSM events (constructed
   as class name + "Events")
-  **ENUM_TIMERS**: name of the enum containing HSM timers (constructed
   as class name + "Timers")
-  **ENUM_STATES_ITEM**: (**BLOCK item**) list of state names
-  **ENUM_EVENTS_ITEM**: (**BLOCK item**) list of event names
-  **ENUM_TIMERS_ITEM**: (**BLOCK item**) list of timer names
-  **INITIAL_STATE**: name of the initial state
-  **HSM_STATE_ACTIONS**: declaration of HSM onStateChanged callbacks
   (each function is placed on a new line)
-  **HSM_STATE_ENTERING_ACTIONS**: declaration of HSM onEntering
   callbacks (each function is placed on a new line)
-  **HSM_STATE_EXITING_ACTIONS**: declaration of HSM onExit callbacks
   (each function is placed on a new line)
-  **HSM_TRANSITION_ACTIONS**: declaration of HSM transition callbacks
   (each function is placed on a new line)
-  **HSM_TRANSITION_CONDITIONS**: declaration of HSM condition callbacks
   (each function is placed on a new line)
-  **HPP_FILE**: hpp file name
-  **REGISTER_STATES**: code registering all HSM states
-  **REGISTER_SUBSTATES**: code registering all HSM substates
-  **REGISTER_TRANSITIONS**: code registering all HSM transitions
-  **REGISTER_TIMERS**: code registering all HSM timers
-  **REGISTER_ACTIONS**: code registering all HSM actions

Variables can be referenced in two ways:

-  **@VARIABLE@**: inserts variable as-is (for example: *@CLASS_NAME@ =>
   SwitchHsmBase*)
-  **%VARIABLE%**: inserts variable in upper case (for example:
   *%CLASS_NAME% => SWITCHHSMBASE*)

.. literalinclude:: ./variables_ref.hpp


.. warning:: TODO: describe how to use block item variables