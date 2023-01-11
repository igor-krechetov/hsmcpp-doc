.. _features-history:

##################################
History
##################################

.. contents::
   :local:

.. warning:: TODO: Add Usage section

A history element is used to record current state of a parent state. Stored information can be used
to restore previously active elements when reentering parent state. The following diagram, describing
a simple washing machine logic, illustrates the use of history element.

.. uml:: ./history_sample.pu
   :align: center
   :alt: Example of HSM with history element

In this state machine, when a washing machine is running, it will
progress from **"Washing"** through **"Rinsing"** to **"Spinning"**. If there is a
power cut, the washing machine will stop running and will go to the
**"Power Off"** state. Then when the power is restored, the Running state is
entered at the **"History State"** symbol meaning that it should resume
where it last left-off.

Each history state can have default transitions defined. This transition
is used when a composite state had never been active before (therefore
it's history being empty).

Two types of history are supported:

-  shallow
-  deep

.. note:: It's important to keep in mind, that, when restoring history,
          all corresponding callbacks will be executed (on enter, on state, on
          exit).


Shallow history
---------------

Shallow history pseudostate represents the most recent active substate
of its parent state (but not the substates of that substate). A
composite state can have at most one shallow history vertex. A
transition coming into the shallow history state is equivalent to a
transition coming into the most recent active substate of a state. The
entry action of the state represented by the shallow history is
performed.

A shallow history is indicated by a small circle containing an **"H"**.
It applies to the state that contains it.

Let's look at the example. Let's say we have this state machine with
**StateE** being currently active:

.. uml:: ./history_shallow_01.pu
   :align: center
   :alt: Sample HSM transition

After **E1** transition active state will become **StateD**:

.. uml:: ./history_shallow_02.pu
   :align: center
   :alt: Sample HSM transition

Since we are using shallow history type, HSM will remember **Parent2** as a
history target for **Parent1**:

.. uml:: ./history_shallow_03.pu
   :align: center
   :alt: Sample HSM transition

Since **Parent2** has substates entry transition will be automatically
executed and **StateC** will become active:

.. uml:: ./history_shallow_04.pu
   :align: center
   :alt: Sample HSM transition


Deep history
------------

Deep history pseudostate represents the most recent active configuration
of the composite state that directly contains this pseudostate (e.g.,
the state configuration that was active when the composite state was
last exited). A composite state can have at most one deep history
element.

Deep history is indicated by a small circle containing an **"H*"**. It
applies to the state that contains it.

Let's look at the example. We have exactly same state machine, but now
history type is set to "deep":

.. uml:: ./history_deep_01.pu
   :align: center
   :alt: Sample HSM transition

While moving to **StateD**, HSM will save **StateE** as a history target
for **Parent1**:

.. uml:: ./history_deep_02.pu
   :align: center
   :alt: Sample HSM transition

So after **E2** transition to history state, our HSM will look exactly same
as it's initial version:

.. uml:: ./history_deep_01.pu
   :align: center
   :alt: Sample HSM transition