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


Building the library
====================

Requirements
------------

* CMake 3.14+
* Python 3


Ubuntu
------

Simplest way to build hsmcpp is to run build.sh script:

.. code-block::  bash

   git clone https://github.com/igor-krechetov/hsmcpp.git
   cd ./hsmcpp
   ./build.sh


Windows
-------

You can build hsmcpp with any tools that you have, but provided script
build_vs.cmd requires Visual Studio 2015 or newer. Make sure to set
correct path to your Visual Studio directory in build_vs.cmd:

.. code-block::  bash

   call "c:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x86

By default only STD based dispatcher is enabled. To enable Qt based one
uncomment following lines and change path to match your Qt directory:

.. code-block::  bash

   set Qt5_DIR=C:\Qt\5.9\5.9.2\msvc2015\lib\cmake\Qt5
   cmake -DHSMBUILD_DISPATCHER_GLIB=OFF -DHSMBUILD_DISPATCHER_GLIBMM=OFF ..

To build GLib and GLibmm based dispatchers you will need to provide
pkg-config and corresponding libraries yourself.


Possible build options
----------------------

================================= ==============================================================================================================
Option                            Description
================================= ==============================================================================================================
**HSMBUILD_VERBOSE**              Enable/disable HSM verbosity (usually OFF since it's only needed for hsmcpp development)
**HSMBUILD_STRUCTURE_VALIDATION** Enable/disable HSM structure validation
**HSMBUILD_THREAD_SAFETY**        Enable/disable HSM thread safety
**HSMBUILD_DEBUGGING**            Enable/disable support for HSM debugging using hsmdebugger (recommended to turn off in production build)
**HSMBUILD_DISPATCHER_GLIB**      Enable GLib dispatcher
**HSMBUILD_DISPATCHER_GLIBMM**    Enable GLibmm dispatcher
**HSMBUILD_DISPATCHER_STD**       Enable std::thread based dispatcher
**HSMBUILD_DISPATCHER_QT**        Enable Qt based dispatcher
**HSMBUILD_TESTS**                Build unittests
**HSMBUILD_EXAMPLES**             Build examples
================================= ==============================================================================================================

Options can be applied when calling cmake:

.. code-block::  bash

   cmake -DHSMBUILD_TESTS=OFF -DHSMBUILD_EXAMPLES=OFF ..


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
