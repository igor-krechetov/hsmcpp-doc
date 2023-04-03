.. _features-substates:

##################################
Substates
##################################

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

Adding a new substate is done using :hsmcpp:`HierarchicalStateMachine::registerSubstate` API:

.. code-block::  c++

   hsm.registerSubstate(MyStates::Parent, MyStates::StateC);

Note that **Parent** must be a part of **MyStates** enum as any other state.


.. _features-substates-entry_points:

Entry Points
============

Usage
-----

Adding an entry point is done using :hsmcpp:`HierarchicalStateMachine::registerSubstateEntryPoint` API.

.. code-block::  c++

   hsm.registerState(MyStates::StateA);
   hsm.registerSubstateEntryPoint(MyStates::Parent, MyStates::StateA);


Multiple entry points
---------------------

Composite states can have multiple entry points specified. This can be useful in the following cases:

- you want to have a different entry point depending on some condition;
- you want to activate multiple substates at the same time (see `parallel states <parallel#features-parallel>`__)

.. uml:: ./substates_entrypoint_multiple.pu
   :align: center
   :alt: Multiple entry points example

.. code-block::  c++

   hsm.registerSubstateEntryPoint(MyStates::Parent, MyStates::StateA);
   hsm.registerSubstateEntryPoint(MyStates::Parent, MyStates::StateB);


.. _features-substates-conditional_entry_points:

Conditional entry points
------------------------

It's quite common to have multiple ways to enter a parent state. But
sometimes you might have a situation when you would want to have a
different initial entry state depending on the triggering transition.

This could be done by specifying multiple entry points with conditions.

.. uml:: ./substates_cond_entries.pu
   :align: center
   :alt: Conditional entry points example

.. code-block::  c++

   hsm.registerSubstateEntryPoint(PlayerStates::Playback,
                                  PlayerStates::Paused,
                                  PlayerEvent::LOAD);
   hsm.registerSubstateEntryPoint(PlayerStates::Playback,
                                  PlayerStates::Playing,
                                  PlayerEvent::RESTART_DONE);

There are 2 types of conditions that can be used:

================== ================================================= ============================================
Condition Type     Description                                       Example
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

A "Final state" is a state that represents the end of the composite state execution. When the state machine transitions to a final state, it means that it has completed processing and has nothing more to do. Unline regular states, it's impossible to transition to other states directly from a final state. Final states can be used in:

- state machine's top level;
- composite state;
- parallel state.

Final states can generate an event when entered, which can trigger the state machine to react. This functionality can be used to notify outer states that a composite state has completed its processing and has entered its final substate.

For example, consider a composite state that controls an online ordering system. When an order is placed, the state machine may transition through various substates, such as "Processing", "Packaging", and "Shipping", before finally entering the final state, "Completed". When the state machine enters the "Completed" state, it can generate an event that allows the state machine to react to the “completion” of composite states.

Final State Types
-----------------

Top level final state
~~~~~~~~~~~~~~~~~~~~~

When defined in the top level, the final state is used as the ultimate end state of the state machine. For example, a state machine that controls a robotic arm may have a final state that represents the end of the arm's movement.

.. uml:: ./substates_final_top.pu
   :align: center
   :alt: Top level final state

After transitioning into a top level final state it will be impossible to interract with a state machine instance (since it's impossible to leave the state directly).


Final state in composite state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In composite states, a final state is used to represent the completion of all sub-states within the composite state. This can be useful for modeling complex systems where multiple sub-tasks must be completed before the overall task is considered complete.

For example, consider a composite state that models a coffee-making process. The composite state may contain sub-states for grinding the coffee beans, heating the water, and brewing the coffee. When all these sub-states have completed their processing, the composite state can transition to its final state, indicating that the coffee-making process is complete.

In composite states, the final state can also generate an event when entered, just like in regular states. This event can be used to trigger external actions or notify users that the composite state has completed its processing. For example, the coffee-making process may generate an event when it enters its final state to notify the user that their coffee is ready to be served.

.. uml:: ./substates_final_composite.pu
   :align: center
   :alt: Final state in composite state


Multiple final states
~~~~~~~~~~~~~~~~~~~~~
Since each final state has a unique ID, it's possible to register as manu final states as you need.

.. uml:: ./substates_final_multiple.pu
   :align: center
   :alt: Multiple final states


Final state in parallel state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In parallel states, the final state is used to represent the completion of all the parallel tasks. For example, a state machine that controls irrigation system can use parallel states to run multiple water pumps. Final state can be used here to wait for all of the pumps to finish  their work before transitioning back to idle state.

.. uml:: ./substates_final_parallel.pu
   :align: center
   :alt: Final state in parallel state


Usage
-----

Adding a new final state is done using :hsmcpp:`HierarchicalStateMachine::registerFinalState` API and then adding it as a substate to a composite state.

.. code-block::  c++

   hsm.registerFinalState(MyStates::Final1);
   hsm.registerSubstate(MyStates::Parent, MyStates::Final1);


Events generation
-----------------

When using composite state we sometimes want to notify state machine that all substates were processed and final state was reached. To achieve this, after entering a final state an event is generated. It can be processed by parent state to transition to a next outer state. This behavior is configurable and can be:

+----------------------------------------+---------------------------------------------+---------------------------------------------+
| Action                                 | Code                                        | Example                                     |
+========================================+=============================================+=============================================+
| generate same event the one            |.. code-block::  c++                         | .. uml:: ./substates_final_event_same.pu    |
| used to transition into the            |                                             |    :align: center                           |
| final state                            |   hsm.registerState(MyStates::StateB);      |    :alt: Final state event re-emit          |
|                                        |   // not providing a custom event will      |                                             |
|                                        |   // instruct HSM to re-emit event used     |                                             |
|                                        |   // for transition to final state          |                                             |
|                                        |   hsm.registerFinalState(MyStates::Final1); |                                             |
|                                        |   ...                                       |                                             |
|                                        |   hsm.registerSubstate(MyStates::Parent,    |                                             |
|                                        |                        MyStates::StateB);   |                                             |
|                                        |   hsm.registerSubstate(MyStates::Parent,    |                                             |
|                                        |                        MyStates::Final1);   |                                             |
|                                        |   ...                                       |                                             |
|                                        |   hsm.registerTransition(MyStates::StateB,  |                                             |
|                                        |                           MyStates::Final1, |                                             |
|                                        |                           MyEvents::E2);    |                                             |
|                                        |   hsm.registerTransition(MyStates::Parent,  |                                             |
|                                        |                          MyStates::StateC,  |                                             |
|                                        |                          MyEvents::E2);     |                                             |
+----------------------------------------+---------------------------------------------+---------------------------------------------+
| generate a custom event                |.. code-block::  c++                         | .. uml:: ./substates_final_event_custom.pu  |
|                                        |                                             |    :align: center                           |
|                                        |   hsm.registerState(MyStates::StateB);      |    :alt: Final state with custom event      |
|                                        |   // providing a custom event E3            |                                             |
|                                        |   // to be generated on entry to Final1     |                                             |
|                                        |   hsm.registerFinalState(MyStates::Final1,  |                                             |
|                                        |                          MyEvents::E3);     |                                             |
|                                        |   ...                                       |                                             |
|                                        |   hsm.registerSubstate(MyStates::Parent,    |                                             |
|                                        |                        MyStates::StateB);   |                                             |
|                                        |   hsm.registerSubstate(MyStates::Parent,    |                                             |
|                                        |                        MyStates::Final1);   |                                             |
|                                        |   ...                                       |                                             |
|                                        |   hsm.registerTransition(MyStates::StateB,  |                                             |
|                                        |                           MyStates::Final1, |                                             |
|                                        |                           MyEvents::E2);    |                                             |
|                                        |   hsm.registerTransition(MyStates::Parent,  |                                             |
|                                        |                          MyStates::StateC,  |                                             |
|                                        |                          MyEvents::E2);     |                                             |
+----------------------------------------+---------------------------------------------+---------------------------------------------+
