.. _features-timers:

##################################
Timers
##################################

.. warning:: TODO: fix API links


Overview
========

Timers are used to initiate transition logic from within HSM without any
additional code. Some common examples of timers usage are:

-  cancel ongoing operation due to timeout;
-  repeating operation after delay.


Usage
=====

To use a timer in your HSM you first need to register it using this API:

.. code-block::  c++

   void registerTimer(const TimerID_t timerID, const HsmEventEnum event);

-  timerID - can be any value, but must be unique withing this instance
   of HSM;
-  event - event which should be triggered when timer expires.

Interacting with timers is part of :ref:`features-states-actions` so
registerStateAction() API should be used. You can start, stop or restart
any of the registered timers.