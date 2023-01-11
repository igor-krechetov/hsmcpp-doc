.. _features-substates:

##################################
Substates
##################################

.. warning:: TODO: fix API links

.. contents::
   :local:

Imagine we have the following state machine:

.. uml:: ./substates_fsm_approach.pu
   :align: center
   :alt: FSM approach to substates

In this example **EVENT_CANCEL** must be added for any state except
**StateA**. With increasing complexity of your state machine, this can
become a significant issue for maintenance. So such logic could be
simplified using substates:

.. uml:: ./substates_sample.pu
   :align: center
   :alt: HSM approach to substates

Substates allow grouping of states to create a hierarchy inside your
state machine. Any state could have substates added to it on the
following conditions:

-  any state can have only one parent;
-  there is no depth limitations when creating substates, but circle
   inclusion is not allowed (A->B->C->A);
-  parent/composite states can't have callbacks (it's possible to
   register them, but they will be ignored);
-  when state has substates an entry point must be specified;
-  multiple entry points can be specified for each composite state.

Entering a substate is considered an atomic operation that can't be
interrupted.


Usage
-----

Adding a new substate is done using `registerSubstate() <../API#registersubstate>`__ API:

.. code-block::  c++

   hsm.registerSubstate(MyStates::ParentState, MyStates::StateB, true);
   hsm.registerSubstate(MyStates::ParentState, MyStates::StateC);

Note that **ParentState** must be a part of **MyStates** enum as any
other state.


Multiple entry points
---------------------

If you define multiple entry points without any additional conditions
they will automatically become parallel states and will get activated as
soon as HSM transitions to their parent state.


.. _features-substates-conditional_entry_points:

Conditional entry points
------------------------

It's quite common to have multiple ways to enter a parent state. But
sometimes you might have a situation when you would want to have a
different entry state depending on the triggering transition.

This could be done by specifying multiple entry points with conditions.

.. uml:: ./substates_cond_entries.pu
   :align: center
   :alt: Conditional entry points example

When determining which entry point to activate, hsmcpp follows these
rules:

-  if there are **no** conditional entry points -> activate all entry
   points;
-  if there is **one or more** conditional entry point -> check if outer
   transition event matches with entry point transition event;

   -  in case of multiple conditional entry points they will be checked
      in the same order as they were registered;

-  if there are multiple conditional entry points with the same matching
   event all of them will be activated;
-  non-conditional entry points will be ignored if there is **at least
   one** matching conditional entry point;
-  if none of the conditional entry points match outer transition ->
   non-conditional entry points will be activated.

Here is how above example will be treated by HSM:

-  when entering **Playback** state from **Idle** it will activate
   only **Paused** substate;
-  we have conditional transition, but LOAD != RESTART_DONE;
-  when entering **Playback** state from **Restart** it will
   activate only **Playing** substate;

   -  since there is a matching conditional entry point transition to
      **Paused** will be ignored.