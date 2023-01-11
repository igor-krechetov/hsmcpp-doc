.. _platforms:

##################################
Platforms
##################################

.. contents::
   :local:


.. warning:: TODO: add API links


Supported Platforms
===================

.. warning:: TODO: add content


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
-  maintain a list of listeners;

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

Since these dispatchers have dependencies on external libraries and only
one of them is usually need, it's possible to disable them from
compilation using these CMake options:

-  HSMBUILD_DISPATCHER_GLIB
-  HSMBUILD_DISPATCHER_GLIBMM
-  HSMBUILD_DISPATCHER_STD
-  HSMBUILD_DISPATCHER_QT


HsmEventDispatcherSTD
---------------------

HsmEventDispatcherSTD is a simple thread based dispatcher. Internally it
uses std::thread to start a new thread.

Simplified logic:

.. image:: ./_gen/dispatchers_std.png
   :align: center
   :alt: Simplified events dispatcher logic

This dispatcher is compatible with all types of applications and should
not interfere with existing event loops from other frameworks. If
desirable it's also possible to use HsmEventDispatcherSTD as a
replacement of your application main loop. To do so you need to call
HsmEventDispatcherSTD::join() to prevent main thread from exiting. For
reference see :repo-link:`/examples/00_helloworld_std.cpp`.


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


HsmEventDispatcherQt
--------------------

HsmEventDispatcherQt utilizes QCoreApplication::postEvent() function for
posting events on Qt's main event loop. As a result all HSM callbacks
are executed on the same thread where event loop is running (usually
main thread).


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
