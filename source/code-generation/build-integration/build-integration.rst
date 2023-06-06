.. _code-generation-build:

##################################
Build Integration
##################################

.. contents::
   :local:

Integrating code generation to project
======================================

Ideally, state machine code generation should be integrated into your build process to
prevent any need for copy-pasting. This can be achieved using scxml2gen tool. Example of how to do it can be found
in :repo-link:`/examples/02_generated`.

To make invoking scxml2gen during build more convenient a couple of CMake functions are provided:

+------------------------+------------------------------+-----------------------------------------------------------------------------------------------+
| Function               | Description                  | Arguments                                                                                     |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | Name                 | Description                                                            |
+========================+==============================+======================+========================================================================+
| **generateHsm**        | Generates hpp and cpp file   | *genTarget*          | new target name (used later for add_dependencies() call)               |
|                        | in destDirectory.            |                      |                                                                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *scxml*              | path to scxml file                                                     |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *className*          | class name to use when generating code (default suffix will be added)  |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *destDirectory*      | path to directory where to save generated files                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *outSrcVariableName* | name of the variable where to store path to generated cpp file         |
+------------------------+------------------------------+----------------------+------------------------------------------------------------------------+
| **generateHsmEx**      | Extended version of          | *genTarget*          | new target name (used later for add_dependencies() call)               |
|                        | generateHsm which allows to  |                      |                                                                        |
|                        | provide custom template and  |                      |                                                                        |
|                        | destination files path       |                      |                                                                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *scxml*              | path to scxml file                                                     |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *className*          | class name to use when generating code (default suffix will be added)  |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *classSuffix*        | suffix to append to class name when generating code                    |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *destDirectory*      | path to directory where to save generated files                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *templateHpp*        | path to HPP and CPP templates                                          |
|                        |                              | *templateCpp*        |                                                                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *destHpp*            | destination path for generated HPP and CPP files                       |
|                        |                              | *destCpp*            |                                                                        |
+------------------------+------------------------------+----------------------+------------------------------------------------------------------------+
| **generateHsmDiagram** | Generates PlantUML state     | *genTarget*          | new target name (used later for add_dependencies() call)               |
|                        | diagram.                     |                      |                                                                        |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *scxml*              | path to scxml file                                                     |
|                        |                              +----------------------+------------------------------------------------------------------------+
|                        |                              | *destFile*           | path to file where to save generated diagram                           |
+------------------------+------------------------------+----------------------+------------------------------------------------------------------------+


They will be automatically available to you when including root
CMakeLists.txt file in your project.

Here is an example of CMake script to build generate and build a simple
HSM. Important points here are:

-  using **add_dependencies()**. **generateHsm()** just and a custom target, so
   without anyone depending on it nothing will be generated.
-  the last argument to generateHsm() must be a string with a variable
   name (not variable itself!).
-  adding generated cpp file to your executable.

.. literalinclude:: /hsmcpp/examples/02_generated/CMakeLists.txt
   :language: cmake

Implementation itself is very similar to a :ref:`gettingstarted-hello-world` example, but now we don't need to
manually register HSM structure.

**Suggestion:**

-  use *override* keyword for callbacks. This will save you a lot of
   effort if callback gets renamed/removed from HSM definition.
-  you can use protected inheritance for generated class (SwitchHsmBase)
   if you want to prevent clients (of SwitchHsm) to directly access HSM
   API.
-  you can generate your files anywhere, but doing it inside your build
   folder will prevent you from accidentally submitting them.

.. literalinclude:: /hsmcpp/examples/02_generated/02_generated.cpp
   :language: c++


Generating PlantUML diagrams
============================

`PlantUML <https://plantuml.com>`__ is an amazing tool that allows
creating a lot of different diagram types using text files. Since I
couldn't find any way to automatically generate images based on SCXML or
export them to PlantUML format I added additional functionality to
scxml2gen application.

To generate a PlantUML file from SCXML simply call:

.. code-block::  Shell

   python3 ./tools/scxml2gen/scxml2gen.py -plantuml -s ./tests/scxml/multilevel.scxml -o ./multilevel.plantuml

You can also use CMake function **generateHsmDiagram()** to do it
automatically during build. You can check example of its usage in :repo-link:`/examples/04_history/CMakeLists.txt`.
