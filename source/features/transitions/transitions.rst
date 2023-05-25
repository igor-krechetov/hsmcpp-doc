.. _features-transitions:

##################################
Transitions
##################################

.. contents::
   :local:

Overview
========

.. uml:: ./sample_transition.pu
   :align: center
   :alt: Sample HSM transition

Transition is an entity that allows changing current HSM state to a
different one. Its definition includes:

-  starting state: state from which transition is possible
-  target state: new state which HSM which have if transition is
   successful
-  triggering event: even which triggers transition
-  condition (optional): additional logic to restrict transition
-  callback (optional): will be called during transition

HSM applies following logic when trying to execute a transition:

.. uml:: ./callbacks_execution_order.pu
   :align: center
   :alt: Callbacks execution order

It is possible to define multiple transitions between two states. As a
general rule, these transitions should be exclusive, but HSM doesn't
enforce this. If multiple valid transitions are found for the same event
then the first applicable one will be used (based on registration
order). **But this situation should be treated by developers as a bug in
their code since it most probably will result in unpredictable
behavior.**

Usage
=====

To register transition use :hsmcpp:`HierarchicalStateMachine::registerTransition` API:

.. literalinclude:: transitions_api.cpp
   :language: c++

Call :hsmcpp:`HierarchicalStateMachine::transition` API to trigger a transition.

.. code-block::  c++

   hsm.transition(MyEvents::EVENT_1);

Normally if you try to send event which is not handled in current state
it will be just ignored by HSM without any notification. But sometimes
you might want to know in advance if transition would be possible or
not. You can use :hsmcpp:`HierarchicalStateMachine::isTransitionPossible` API for that.
It will check if provided event will be accepted by HSM taking in consideration:

-  current state
-  pending events
-  conditions assigned to transitions

.. note:: It is still possible for HSM to reject your event if after
          :hsmcpp:`HierarchicalStateMachine::isTransitionPossible` some other thread will manage to trigger
          another transition be careful when using it in multi-threaded
          environment.

.. _features-transitions-cancellation:

Cancelling pending transitions
------------------------------

By default, transitions are executed asynchronously and it's a
recommended way to use them. When multiple events are sent at the same
time they will be internally queued and executed sequentially.
Potentially it's possible to have multiple events queued when you need
to send a new event which will make previous events obsolete (for
example user want to cancel operation). In this case you can use
:hsmcpp:`HierarchicalStateMachine::transitionWithQueueClear` or
:hsmcpp:`HierarchicalStateMachine::transitionEx` to clear pending events:

.. code-block::  c++

   hsm.transitionWithQueueClear(MyEvents::EVENT_1);
   hsm.transitionEx(MyEvents::EVENT_1, true, false);

.. note:: Current ongoing transition can't be canceled.


.. _features-transitions-selftransitions:

Self transitions
================

Self-transitions are transitions for which starting and target states
are the same.

.. uml:: ./selftransition_simple.pu
   :align: center
   :alt: Simple self-transition

To register a self-transition use :hsmcpp:`HierarchicalStateMachine::registerSelfTransition` API:

.. literalinclude:: transitions_self_api.cpp
   :language: c++

.. note:: Though using :hsmcpp:`HierarchicalStateMachine::registerSelfTransition` is a recommended way for defining self-transitions, you can also use
          :hsmcpp:`HierarchicalStateMachine::registerTransition` API. Keep in mind that in this case transition type
          will be automatically set to **"external"**.

There are 2 types of self-transitions (see :hsmcpp:`TransitionType` enum):

=============== ================================================================
Transition Type Description
=============== ================================================================
**external**    During external transition, state machine exits current active
                state and returns back to it right away. This results in all
                entry, exit and state actions being invoked. This also affects
                substates if current state contains any.
**internal**    An internal transition does not allow the exit and entry actions
                to be executed. So only transition callback will be executed
                without any impact on active states.
=============== ================================================================

Difference between these two types can be demonstrated with this
example:

.. uml:: ./selftransition.pu
   :align: center
   :alt: Self-transition example

Let's assume **StateC** is currently active. If **EVENT_INTERNAL** is
triggered then only following callbacks will be executed:

.. uml:: ./selftransition_internal.pu
   :align: center
   :alt: Internal self-transition example

If **EVENT_EXTERNAL** is triggered then all corresponding exit/enter
callbacks will be processed:

.. uml:: ./selftransition_external.pu
   :align: center
   :alt: External self-transition example

.. note:: Notice how after external self-transition **StateB** became active. This happened due to state machine exiting from **ParentState_1** and, consequentially, exiting from it's substates too.

Conditional transitions
=======================

Sometimes transition should be executed only when a specific condition
is met. This could be achieved by setting condition callback and
expected value. Transition will be ignored if value returned by callback
doesnt match expected one.


.. _features-transitions-priority:

Priority of transitions
=======================

Ideally, when designing state machine, you should avoid having multiple
transitions which could be valid at the same time. This will make
understanding the logic and debugging easier. But if for some reason
your state machine will contain such transition, hsmcpp library will
still handle them in a deterministic and predictable manner:

-  all valid transitions will be executed if they are defined on the
   same level;
-  self transitions are always executed before any outgoing transitions;
-  if transitions are defined on multiple levels (for example between
   substates and on the same level as a parent):

   -  internal transitions between substates always have the highest
      priority. Outer transitions **will be ignored**;

Let's look at the following example:

.. uml:: ./transition_priorities.pu
   :align: center
   :alt: Transition priorities

-  If **StateA** is active and **EVENT_1** is triggered:

   -  first self transition for **StateA** will be executed;
   -  then both states B and C will be activated (see :ref:`features-parallel` section for details).

-  If **StateD** is active and **EVENT_3** is triggered:

   -  only StateD->StateE transition will be executed since internal transitions have higher priority.

-  If **StateE** is active and **EVENT_3** is triggered:

   -  first self transition for **ParentState** will be executed;
   -  then ParentState->StateF transition will be executed.

Synchronous transitions
=======================

.. warning:: It's **strongly discouraged** to usage synchronous transitions in production code. They were added mostly for testing purposes, since async unit tests are a headache to deal with.

Transitions can be executed synchronously using :hsmcpp:`HierarchicalStateMachine::transitionEx` API.
Please keep these things in mind when using synchronous transitions:

- Don't execute synchronous transitions from HSM callbacks:

   - all callbacks will still be executed on dispatcher's thread. So triggering a synchronous transition from HSM callback will result in a deadlock.

- When using Glib-based dispatcher, don't execute synchronous transitions from GLib thread that was assigned to dispatcher:

   - unless you specifically created a custom glib context, dispatcher will be running on a main thread of your application. Calling synchronous transition anywhere on this thread will result in a deadlock.