.. _features-states:

##################################
States
##################################

.. contents::
   :local:


Overview
========

.. uml:: ./simple_state.pu
   :align: center
   :alt: Simple state example

States are defined as an enum:

.. code-block::  c++

   enum class MyStates
   {
       StateA,
       StateB,
       StateC
   };


State callbacks are optional and include:

-  *entering*

   -  called right before changing a state
   -  transition is canceled if callback returns FALSE

-  *state changed*

   -  called when HSM already changed its current state

-  *exiting*

   -  called for previous state before starting to transition to a new
      state
   -  transition is canceled if callback returns FALSE


Usage
=====

Assuming we create HSM as a separate object, here are possible ways to
register a state:

.. literalinclude:: state_api.cpp
   :language: c++

Note that if you explicitly need to pass nullptr (as in the last
example) you will need to provide class name as a template parameter.


.. _features-states-actions:

State actions
=============

Besides implementing logic inside HSM callbacks it's possible to define
some operations as state actions. These actions are built-in commands
that are executed automatically based on HSM activity.

Actions could be added using:

.. code-block::  c++

   bool registerStateAction(const HsmStateEnum state,
                            const StateActionTrigger actionTrigger,
                            const StateAction action,
                            Args... args);

At the moment two triggers are supported:

.. code-block::  c++

   enum class StateActionTrigger {
       ON_STATE_ENTRY,
       ON_STATE_EXIT
   };

-  *StateActionTrigger::ON_STATE_ENTRY* will execute action when *entering* a state;
-  *StateActionTrigger::ON_STATE_EXIT* will execute action when *exiting* a state.

.. note:: actions will be executed *only if* ongoing transition wasn't blocked by entry/exit callbacks.

Supported actions are:

==============================  ============================================= ==========================================================================================
Action                          Arguments                                     Description
==============================  ============================================= ==========================================================================================
**StateAction::START_TIMER**    - int timerID                                 -  starts a singleshot or repeating timer. singleshot timer will
                                - int intervalMs                                 fire only once and then will stay idle until started again;
                                - bool singleshot                             -  does nothing if timerID or interval are invalid;
                                                                              -  does nothing if requested timer is already running;
**StateAction::STOP_TIMER**     - int timerID                                 -  stops running timer without trigerring anything;
                                                                              -  does nothing if requested timer is not running;
**StateAction::RESTART_TIMER**  - int timerID                                 -  restarts timer with the same interval and mode (singleshot or
                                                                                 repeating) as were specified in start timer;
                                                                              -  does nothing if timer is not running;

                                                                              .. note:: trying to restart expired singleshot timer will do
                                                                                 nothing since this timer is considered as "not running". Use
                                                                                 "start timer" action instead.
**StateAction::TRANSITION**     - int eventID                                 -  add specified event with it's arguments to the end of transition queue;
                                - {arg1, arg2, ...}
==============================  ============================================= ==========================================================================================

See :ref:`features-timers` for details regarding their usage.