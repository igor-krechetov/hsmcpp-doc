.. _features-timers:

##################################
Timers
##################################

Overview
========

Timers are used to initiate transition logic from within HSM without any
additional code. Some common examples of timers usage are:

-  cancel ongoing operation due to timeout;
-  repeating operation after delay.


Usage
=====

To use a timer in your HSM you first need to register it using :hsmcpp:`HierarchicalStateMachine::registerTimer` API:

.. code-block::  c++

   hsm.registerTimer(MyTimers::TIMER_1, MyEvents::ON_TIMER_1);

Interacting with timers is part of :ref:`features-states-actions` so
:hsmcpp:`HierarchicalStateMachine::registerStateAction` API should be used. You can also start, stop or restart
any of the registered timers directly using:

- :hsmcpp:`HierarchicalStateMachine::startTimer`
- :hsmcpp:`HierarchicalStateMachine::stopTimer`
- :hsmcpp:`HierarchicalStateMachine::restartTimer`
