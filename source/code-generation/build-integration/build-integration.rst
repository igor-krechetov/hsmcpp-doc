.. _code-generation-build:

##################################
Build Integration
##################################


Integrating code generation to project
======================================

Ideally, code generation should be integrated into a build process to
prevent any need for copy-pasting. Example of how to do so can be found
in `/examples/02_generated <../blob/main/examples/02_generated>`__.

To make invoking scxml2gen during build more convenient two CMake
functions are provided:

-  *function(*\ **generateHsm**\ *genTarget scxml className
   destDirectory outSrcVariableName)*

   -  Generates hpp and cpp file in destDirectory.
   -  **IN arguments**

      -  *genTarget*: new target name (used later for add_dependencies()
         call)
      -  *scxml*: path to scxml file
      -  *className*: class name to use when generating code (default
         suffix will be added)
      -  *destDirectory*: path to directory where to save generated
         files

   -  **OUT arguments**

      -  *outSrcVariableName*: name of the variable where to store path
         to generated cpp file

-  *function(*\ **generateHsmEx**\ *genTarget scxml className
   classSuffix templateHpp templateCpp destHpp destCpp)*

   -  Extended version of generateHsm which allows to provide custom
      template and destination files path
   -  **IN arguments**

      -  *genTarget*: new target name (used later for add_dependencies()
         call)
      -  *scxml*: path to scxml file
      -  *className*: class name to use when generating code (default
         suffix will be added)
      -  *classSuffix*: suffix to append to class name when generating
         code
      -  *destDirectory*: path to directory where to save generated
         files
      -  *templateHpp*, templateCpp: path to HPP and CPP templates
      -  *destHpp*, destCpp: destination path for generated HPP and CPP
         files

They will be automatically available to you when including root
CMakeLists.txt file in your project.

Here is an example CMake script to build generate and build a simple
HSM. Important points here are:

-  using add_dependencies(). generateHsm() just and a custom target, so
   without anyone depending on it nothing will be generated.
-  the last argument to generateHsm() must be a string with a variable
   name (not variable itself!).
-  adding generated cpp file to your executable.

.. code-block::  CMake

   set(BINARY_NAME_02 "02_generated")

   # create folder for generated files
   set(GEN_DIR ${CMAKE_BINARY_DIR}/gen)
   file(MAKE_DIRECTORY ${GEN_DIR})

   generateHsm(GEN_02_HSM ./02_generated.scxml "SwitchHsm" ${GEN_DIR} "GEN_OUT_SRC")

   add_executable(${BINARY_NAME_02} 02_generated.cpp ${GEN_OUT_SRC})
   add_dependencies(${BINARY_NAME_02} GEN_02_HSM)
   target_include_directories(${BINARY_NAME_02}
       PRIVATE
           ${HSMCPP_STD_INCLUDE}
           ${CMAKE_BINARY_DIR}
   )
   target_link_libraries(${BINARY_NAME_02} PRIVATE ${HSMCPP_STD_LIB})

Implementation itself is very similar to a `HelloWorld
example <../Getting-Started#hello-world>`__, but now we don't need to
manually register HSM structure.

**Suggestion:**

-  use *override* keyword for callbacks. This will save you a lot of
   effort if callback gets renamed/removed from HSM definition.
-  you can use protected inheritance for generated class (SwitchHsmBase)
   if you want to prevent clients (of SwitchHsm) to directly access HSM
   API.
-  you can generate your files anywhere, but doing it inside your build
   folder will prevent you from accidentally submitting them.

.. code-block::  C++

   #include <chrono>
   #include <thread>
   #include <hsmcpp/HsmEventDispatcherSTD.hpp>
   #include "gen/SwitchHsmBase.hpp"

   using namespace std::chrono_literals;

   class SwitchHsm: public SwitchHsmBase
   {
   public:
       virtual ~SwitchHsm(){}

   // HSM state changed callbacks
   protected:
       void onOff(const VariantList_t& args) override
       {
           printf("Off\n");
           std::this_thread::sleep_for(1000ms);
           transition(SwitchHsmEvents::SWITCH);
       }

       void onOn(const VariantList_t& args) override
       {
           printf("On\n");
           std::this_thread::sleep_for(1000ms);
           transition(SwitchHsmEvents::SWITCH);
       }
   };

   int main(const int argc, const char**argv)
   {
       std::shared_ptr<hsmcpp::HsmEventDispatcherSTD> dispatcher = std::make_shared<hsmcpp::HsmEventDispatcherSTD>();
       SwitchHsm hsm;

       hsm.initialize(dispatcher);
       hsm.transition(SwitchHsmEvents::SWITCH);

       dispatcher->join();

       return 0;
   }


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

You can also use CMake function generateHsmDiagram() to do it
automatically during build. You can check example of its usage in
`/examples/04_history/CMakeLists.txt <../blob/main/examples/04_history/CMakeLists.txt>`__.

.. |Editing HSM in Qt Creator| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/editor_qt.png
.. |Editing HSM in scxmlgui| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/editor_scxmlgui.png
.. |State callback| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_01_state_callback.png
.. |State entering callback| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_01_entering_callback.png
.. |State exiting callback| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_01_exiting_callback.png
.. |State exiting callback 2| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_01_transition_callback.png
.. |Timer start action| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_02_timer_action.png
.. |Timer transition| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_03_timer_transition.png
.. |Conditional transition| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_04_transition_cond.png
.. |Multiple entries| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_05_multiple_entriepoints_1.png
.. |Original XML| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_05_multiple_entriepoints_2.png
.. |Modified XML| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_05_multiple_entriepoints_3.png
.. |Conditional entry points| image:: https://github.com/igor-krechetov/hsmcpp/blob/main/doc/wiki/editors/qt_05_multiple_entriepoints_4.png
