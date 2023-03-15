.. _platforms:

##################################
Platforms
##################################

.. contents::
   :local:


.. |ok| replace:: |:white_check_mark:|
.. |na| replace:: |:x:|


.. warning:: TODO: add API links

Most of the hsmcpp library's functionality is platform independent. But implementation of events dispatching, timers and multi-threading support highly depends on underlying OS. To allow support of various execution environments platform and framework specific parts were separated into an abstraction layer. Required abstractions include:

- mutex
- critical section
- semaphore


Supported Platforms
===================

Platform selection is done using HSMBUILD_PLATFORM build setting. Depending on the provided value, some
dispatchers might not be available:

+----------+----------------------------+-----------------+----------+--------------------------------------------------------------+
| Value    | Supported Dispatchers      | Multi Threading |Interrupts| Description                                                  |
+==========+============================+=================+==========+==============================================================+
| posix    | STD                        | |ok|            | |ok|     | This is the default implementation of OS specific primitives |
|          +----------------------------+-----------------+----------+ based on standard C++ library. Any platform, that has a full |
|          | Glib                       | |ok|            | |ok|     | set of std features available (specifically threads and      |
|          +----------------------------+-----------------+----------+ synchronization) and is POSIX compliant, can be covered      |
|          | Glibmm                     | |ok|            | |ok|     | by this implementation.                                      |
|          +----------------------------+-----------------+----------+ For example: Linux, QNX, Integrity, etc.                     |
|          | Qt                         | |ok|            | |ok|     |                                                              |
+----------+----------------------------+-----------------+----------+--------------------------------------------------------------+
| windows  | STD                        | |ok|            | |na|     | Same as POSIX based implementation, but doesn't include      |
|          +----------------------------+-----------------+----------+ support for interrupts/signals.                              |
|          | Qt                         | |ok|            | |na|     |                                                              |
+----------+----------------------------+-----------------+----------+--------------------------------------------------------------+
| arduino  | Arduino                    | |na|            | |ok|     | Arduino doesn't provide any multi-process or multi-threading |
|          |                            |                 |          | support. So abstraction layer for this platform merely       |
|          |                            |                 |          | provides an empty stub for a common logic to compile. All    |
|          |                            |                 |          | dispatching and callbacks execution is done sequentially and |
|          |                            |                 |          | no synchronization is required.                              |
+----------+----------------------------+-----------------+----------+--------------------------------------------------------------+
| freertos | FreeRTOS                   | |ok|            | |ok|     | Even  though FreeRTOS comes with a basic implementation of   |
|          |                            |                 |          | std library, it lacks threads related functionality due to   |
|          |                            |                 |          | a bit different approach to concurrency (Tasks and           |
|          |                            |                 |          | Interrupts instead of threads).                              |
+----------+----------------------------+-----------------+----------+--------------------------------------------------------------+


Dispatchers Overview
======================

hsmcpp library is asynchronous by design. All transitions within it are
handled through events queue. To make things asynchronous, processing of
this queue must be done on a separate thread or some kind of event loop.
Since requirements to such processing mechanism will be different from
project to project, it was decided to make it an additional abstraction
(*IHsmEventDispatcher*) which could be replaced based on your specific
needs.

*IHsmEventDispatcher* responsibilities include:

-  asynchronously invoke listeners callback after receiving event was
   emitted;
-  provide thread-safe way to emit events;
-  provide interrupts-safe way to emit events;
-  start/stop/restart timers;
-  maintain a list of listeners.

When initializing HSM object it's required to provide an instance of
IHsmEventDispatcher. Unless you keep a copy of shared_ptr with
dispatcher instance, it will be distroyed automatically during HSM
object destruction. Clients can use on of the built-in dispatchers or
implement their own.

Built-in dispatchers
====================

Currently hsmcpp includes the following dispatchers:

-  **HsmEventDispatcherSTD**

   -  internally starts std::thread and uses it to dispatch HSM events

-  **HsmEventDispatcherGlib**

   -  dispatches hsm events through Glib main loop. No additional
      threads are created.

-  **HsmEventDispatcherGlibmm**

   -  same as HsmEventDispatcherGlib, but uses Glibmm (C++ wrapper over
      Glib) and Glib::Dispatcher to handle events. No additional threads
      are created.

-  **HsmEventDispatcherQt**

   -  dispatches hsm events through main Qt event loop. No additional
      threads are created.

-  **HsmEventDispatcherArduino**

   -  dispatches hsm events every time dispatchEvents() method is called in Arduino's loop() function. No additional
      threads are created.

-  **HsmEventDispatcherFreeRTOS**

   -  internally starts FreeRTOS task and uses it to dispatch HSM events

Since these dispatchers have dependencies on external libraries and only
one of them is usually needed, you need to explicitly enable them for
compilation using these CMake options:

- HSMBUILD_DISPATCHER_GLIB
- HSMBUILD_DISPATCHER_GLIBMM
- HSMBUILD_DISPATCHER_STD
- HSMBUILD_DISPATCHER_QT
- HSMBUILD_DISPATCHER_FREERTOS

.. _platforms-dispatcher-std:

HsmEventDispatcherSTD
---------------------

HsmEventDispatcherSTD is a simple thread based dispatcher. Internally it
uses std::thread to start a new thread.

Simplified logic:

.. uml:: ./dispatchers_std.pu
   :align: center
   :alt: Simplified events dispatcher logic

This dispatcher is compatible with all types of applications and should
not interfere with existing event loops from other frameworks. If
desirable it's also possible to use HsmEventDispatcherSTD as a
replacement of your application main loop. To do so you need to call
HsmEventDispatcherSTD::join() to prevent main thread from exiting. For
reference see :repo-link:`/examples/00_helloworld/00_helloworld_std.cpp`.

.. _platforms-dispatcher-glib:

HsmEventDispatcherGlib
----------------------

HsmEventDispatcherGlib utilizes GLib main loop and pipe to dispatch
events. Clients can specify which GLib context to use (if application
has multiple) by providing GMainContext to constructor:

.. code-block::  c++

   explicit HsmEventDispatcherGLib(GMainContext* context);

To use default GLib main loop just use default constructor:

.. code-block::  c++

   HsmEventDispatcherGLib();

.. _platforms-dispatcher-glibmm:

HsmEventDispatcherGlibmm
------------------------

In general is same as HsmEventDispatcherGlib, but it utilizes
GLib::Dispatcher class to handle events. Due to GLib::Dispatcher
implementation this applies some restrictions:

-  HsmEventDispatcherGLibmm must be constructred and destroyed in the
   receiver thread (the thread in whose main loop it will execute its
   connected slots)
-  registerEventHandler() must be called from the same thread where
   dispatcher was created.

For more details see: `Using
Glib::Dispatcher <https://developer.gnome.org/gtkmm-tutorial/stable/sec-using-glib-dispatcher.html.en>`__

Not following these rules will result in an occasional SIGSEGV crash
(usually when deleting dispatcher instance).

Unless you really have to, it's **always better to reuse a single
dispatcher instance for multiple HSMs** instead of creating/deliting
multiple ones(they will anyway handle events sequentially since they use
same Glib main loop).


.. _platforms-dispatcher-qt:

HsmEventDispatcherQt
--------------------

HsmEventDispatcherQt utilizes QCoreApplication::postEvent() function for
posting events on Qt's main event loop. As a result all HSM callbacks
are executed on the same thread where event loop is running (usually
main thread).


.. _platforms-dispatcher-arduino:

HsmEventDispatcherArduino
-------------------------

Dispatching  is done by periodically calling dispatchEvents() in the Arduino's loop() function. All transitions and callbaks
are processed within it. Therefore it's advised to avoid using blocking operations inside HSM callbacks
to make your software more responsive. Instead, utilization of async APIs is highly recommended.
When possible, try replacing calls to delay() with HSM timeouts.

.. note:: It's advised to allocate instances of dispatcher and HSM on heap.

Compiling
~~~~~~~~~

Arduino build is not supported in current CMake configuration. Recommended way of including hsmcpp
for Arduino software is by using `PlatformIO IDE <https://platformio.org/platformio-ide>`__
and `PlatformIO package <https://registry.platformio.org/libraries/igor-krechetov/hsmcpp>`__.


.. _platforms-dispatcher-freertos:

HsmEventDispatcherFreeRTOS
--------------------------

HsmEventDispatcherFreeRTOS utilizes a custom FreeRTOS Task to handle HSM events and callbacks.
Task is created and started during call to dispatcher's initialize()API.

.. note:: Creation and initialization of HSM and dispatcher should  be done inside of a Task and not main() function.


Compiling
~~~~~~~~~

hsmcpp library musts be compiled as part of your application's build. Make sure to set **HSMBUILD_FREERTOS_ROOT**
build option and specify path to your FreeRTOS root directory.
For reference see :repo-link:`/examples/08_freertos`


FreeRTOS configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to the specifics of the platfrom, you would usually need a FreeRTOS configuration file.
If you don't care much about specific settings, hsmcpp library already includes a default
configuration (though I do recommend to review it to avoid any unexpected behavior of your code).
In case a custom configuration is needed, it can be specified using **HSMBUILD_FREERTOS_CONFIG_FILE_DIRECTORY**
build opion. It should point to a folder containing your `FreeRTOSConfig.h <https://www.freertos.org/a00110.html>`__ file.

.. warning:: FreeRTOSConfig.h included in hsmcpp repository was tested only with POSIX simulation of FreeRTOS. It should be
             treated only as a reference and it's your responsibility to provide correct config for your specific HW.

Additionally, following FreeRTOS features must be enabled:

- INCLUDE_xTaskGetCurrentTaskHandle = 1
- configUSE_TASK_NOTIFICATIONS = 1
- configUSE_TIMERS = 1
- configUSE_MUTEXES = 1
- configSUPPORT_DYNAMIC_ALLOCATION = 1

If you are using interrupts (ISR) in your code, you must provide implementation for
xPortIsInsideInterrupt() API (usually provided by your FreeRTOS port; defined in portmacro.h). In case this
API is not available and your are not going to interact with HSM from within interrupts
handler, then you can enable default implementation of xPortIsInsideInterrupt() by turning
on **BUILD_FREERTOS_DEFAULT_ISR_DETECT** build option (default implementation simply always returns **FALSE**).

.. warning:: Using this option will make most calls to hsmcpp API from ISR unsafe and will result in undefined behavior (most often memory corruption and crash).



Implementing custom dispatchers
===============================

Even though STD based dispatcher will work in all situations, sometimes
it's not desirable or even impossible to have an additional unmanaged
thread running in the process (for example in case of RTOS systems which
often utilize watchdog mechanism). In this case it's possible to use
your own dispatcher by implementing **IHsmEventDispatcher** interface.
When doing so keeping the following things in mind:

-  emit() method should be thread-safe.
-  start() method is used by HSM to start event dispatching. It is
   called during initialize() and must be non blocking. Calling this
   method when dispatching is already ongoing should always return TRUE.
-  registerEventHandler must support multiple callbacks registration.
   This is needed to support sharing dispatcher between different HSM
   instances.

Even though you can implement **IHsmEventDispatcher** interface
directly, it's recommended to use **HsmEventDispatcherBase** as your
parent class.

I recommend checking existing dispatchers as a reference to get an idea
on how to implement your own:

-  :repo-link:`/src/HsmEventDispatcherGLib.cpp`
-  :repo-link:`/src/HsmEventDispatcherGLibmm.cpp`
-  :repo-link:`/src/HsmEventDispatcherSTD.cpp`
-  :repo-link:`/src/HsmEventDispatcherQt.cpp`
-  :repo-link:`/src/HsmEventDispatcherArduino.cpp`
-  :repo-link:`/src/HsmEventDispatcherFreeRTOS.cpp`
