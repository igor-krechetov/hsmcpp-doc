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
state machine. Any state can have substates added to it on the
following conditions:

-  any state can have only one parent;
-  there is no depth limitations when creating substates, but circle
   inclusion is not allowed (A->B->C->A);
-  at least one entry point must be specified for states with substates.

Entering a substate is considered an atomic operation that can't be
interrupted.


Usage
=====

Adding a new substate is done using `registerSubstate() <../API#registersubstate>`__ API:

.. code-block::  c++

   hsm.registerSubstate(MyStates::ParentState, MyStates::StateB, true);
   hsm.registerSubstate(MyStates::ParentState, MyStates::StateC);

Note that **ParentState** must be a part of **MyStates** enum as any
other state.

.. _features-substates-entry_points:

Entry Points
============

Multiple entry points
---------------------

Composite states can have multiple entry points specified this can be useful in the
following cases:

- you want to have a different entry point depending on some condition;
- you want to activate multiple substates at the same time (see `parallel states() <parallel#features-parallel>`__)


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

There are 2 types of conditions that can be used:

================== ================================================= ============================================
Condition Type     Description
================== ================================================= ============================================
events filter      Evaluates to TRUE only if it matches with event   .. uml:: ./substates_entrypoint_event.pu
                   used to enter the parent state.                      :align: center
                                                                        :alt: Entry points with event condition
condition callback Evaluates to TRUE only if value returned from     .. uml:: ./substates_entrypoint_callback.pu
                   callback matches expected value.                     :align: center
                                                                        :alt: Entry points with callback condition
================== ================================================= ============================================

.. note:: Only one condition of each type can be used for a single entry point,
          but you can apply both of them at the same time (so you can have both event
          and callback, but can't have 2 events defines for a single entry point).


Priority of multiple entry points
---------------------------------

When determining which entry point to activate, hsmcpp follows these
rules:

-  non-conditional entry points are always activated;
-  conditional entry points will be activated only if
   their conditions are evaluated as TRUE. Conditions will
   be evaluated in the same order as transitions were registered;

Here are examples of different cases of multiple entry points.
Green color indicates which substates will be activated when event is triggered.

Entry points without specified events:

.. uml:: ./entrypoint_priority_noevents.pu
   :align: center
   :alt: Conditional entry points without events

Entry points with specified events:

.. uml:: ./entrypoint_priority_events.pu
   :align: center
   :alt: Conditional entry points with events


.. _features-substates-final_state:

Final State
============

.. warning:: TODO: add description