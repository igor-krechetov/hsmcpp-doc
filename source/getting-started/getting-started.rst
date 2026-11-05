##################################
Getting Started
##################################

.. contents::
   :local:


Overview
========

There are 2 ways to add hsmcpp library to your project:

* compile, install and use library through pkg-config;
* add hsmcpp repository as a git submodule and compile it together with your project.

.. tip:: To design and edit your state machines visually, the recommended tool is
         :ref:`code-generation-hsm-ide` -- a desktop editor built specifically around
         hsmcpp.


Building the library
====================

Requirements
------------

* CMake 3.16+
* C++11 compatible compiler
* Python 3.8+ (only needed for the :ref:`code generator <code-generation-scxml>`)


Linux
-------------------

.. code-block::  bash

   git clone https://github.com/igor-krechetov/hsmcpp.git
   cd ./hsmcpp
   cmake -S . -B ./build -DCMAKE_BUILD_TYPE=Release
   cmake --build ./build -j
   cmake --install ./build        # optional, may require sudo

By default this builds the library, unit tests and examples, and only the STD based dispatcher
is enabled. Use build options to change that (see `Possible build options`_).
The default value of **HSMBUILD_PLATFORM** is *posix* (see :ref:`platforms`).


Windows
-------

You can use any toolchain supported by CMake (Visual Studio 2015 or newer, MinGW, etc.). Platform
must be set explicitly since *posix* is the default:

.. code-block::  bat

   git clone https://github.com/igor-krechetov/hsmcpp.git
   cd hsmcpp
   cmake -S . -B build -DHSMBUILD_PLATFORM=windows
   cmake --build build --config Release

To enable the Qt based dispatcher add **-DHSMBUILD_DISPATCHER_QT=ON** and make sure CMake can find Qt
(for example by setting **CMAKE_PREFIX_PATH** to your Qt directory):

.. code-block::  bat

   cmake -S . -B build -DHSMBUILD_PLATFORM=windows -DHSMBUILD_DISPATCHER_QT=ON -DCMAKE_PREFIX_PATH=C:\Qt\6.8.3\msvc2022_64

GLib and GLibmm based dispatchers are not available on Windows.


FreeRTOS and Arduino
--------------------

These platforms have additional requirements. See :ref:`platforms-dispatcher-freertos` and
:ref:`platforms-dispatcher-arduino`.


.. _gettingstarted-build-options:

Possible build options
----------------------

============================================= ==============================================================================================================
Option                                        Description
============================================= ==============================================================================================================
**HSMBUILD_PLATFORM**                         Target platform. Possible values: *posix* (default), *windows*, *qnx*, *freertos*, *arduino*. See :ref:`platforms`
**HSMBUILD_TARGET**                           Desired build output. Possible values: *library* (default), *platformio*, *arduinoide*
**HSMBUILD_VERBOSE**                          Enable/disable HSM verbosity (usually OFF since it's only needed for hsmcpp development)
**HSMBUILD_STRUCTURE_VALIDATION**             Enable/disable HSM structure validation (default ON)
**HSMBUILD_THREAD_SAFETY**                    Enable/disable HSM thread safety (default ON)
**HSMBUILD_DEBUGGING**                        Enable/disable support for HSM debugging using hsmdebugger (default ON, recommended to turn off in production build)
**HSMBUILD_DISPATCHER_GLIB**                  Enable GLib dispatcher
**HSMBUILD_DISPATCHER_GLIBMM**                Enable GLibmm dispatcher
**HSMBUILD_DISPATCHER_STD**                   Enable std::thread based dispatcher (default ON)
**HSMBUILD_DISPATCHER_QT**                    Enable Qt based dispatcher
**HSMBUILD_DISPATCHER_FREERTOS**              Enable FreeRTOS based dispatcher
**HSMBUILD_FREERTOS_ROOT**                    FreeRTOS sources root folder (freertos platform only)
**HSMBUILD_FREERTOS_CONFIG_FILE_DIRECTORY**   Path to folder with FreeRTOSConfig.h (freertos platform only)
**HSMBUILD_FREERTOS_DEFAULT_ISR_DETECT**      Enable default xPortIsInsideInterrupt implementation (freertos platform only)
**HSMBUILD_TESTS**                            Build unittests (default ON)
**HSMBUILD_EXAMPLES**                         Build examples (default ON)
**HSMBUILD_CODECOVERAGE**                     Build with code coverage instrumentation
**HSMBUILD_CLANGTIDY**                        Enable validation with clang-tidy (if available)
============================================= ==============================================================================================================

Options can be applied when running cmake:

.. code-block::  bash

   cmake -DHSMBUILD_PLATFORM=posix -DHSMBUILD_TESTS=OFF -DHSMBUILD_EXAMPLES=OFF ..


.. _gettingstarted-hello-world:

Hello World!
============

Let's create the smallest state machine which would represent a switch button:

.. uml:: ./00_helloworld.pu
   :align: center
   :alt: HelloWorld state machine

For more complex examples see :repo-link:`/examples` folder.

For simplicity we are going to use STD dispatcher to avoid additional
dependencies. Source code is available in :repo-link:`/examples/00_helloworld/00_helloworld_std.cpp` .

.. literalinclude:: /hsmcpp/examples/00_helloworld/00_helloworld_std.cpp
   :language: c++


CMake script (pkg-config)
-------------------------

To use hsmcpp as a pkg-config module you can follow template: :repo-link:`/examples/07_build/using_pkgconfig/CMakeLists.txt`

.. literalinclude:: /hsmcpp/examples/07_build/using_pkgconfig/CMakeLists.txt
   :language: cmake


CMake script (as source code)
-----------------------------

To compile hsmcpp together with your project you can follow template: :repo-link:`/examples/07_build/using_code/CMakeLists.txt`

.. literalinclude:: /hsmcpp/examples/07_build/using_code/CMakeLists.txt
   :language: cmake


CMake script (download from GitHub)
-----------------------------------

Maybe the easiest option to use hsmcpp in your project is to download it
directly from GitHub and compile it together with your application. The
downsides of this approach are:

* dependency on Internet connection availability and GitHub;
* a bit longer clean build time due to the necessity to download hsmcpp library files (since files are stored in your temporary build folder).

You can use this CMake template: :repo-link:`/examples/07_build/using_fetch/CMakeLists.txt`

.. literalinclude:: /hsmcpp/examples/07_build/using_fetch/CMakeLists.txt
   :language: cmake
