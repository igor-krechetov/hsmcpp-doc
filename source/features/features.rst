##################################
Features
##################################

Overview
========

**hsmcpp** library allows you to use a hierarchical state machine (HSM) in your
project without worrying about the mechanism itself. Instead developers can focus on
the structure and logic. The goal of this documentation is to explain how the **hsmcpp**
library can be used, so the basics of HSM will not be covered. If you are not familiar
with the state machine design pattern, you can familiarize yourself with the HSM concept and terminology here:

*  `Welcome to the world of Statecharts <https://statecharts.dev>`_
*  `Introduction to Hierarchical State Machines <https://barrgroup.com/embedded-systems/how-to/introduction-hierarchical-state-machines>`_
*  `Wikipedia: UML state machine <https://en.wikipedia.org/wiki/UML_state_machine>`_
*  `Hierarchical Finite State Machine for AI Acting Engine <https://towardsdatascience.com/hierarchical-finite-state-machine-for-ai-acting-engine-9b24efc66f2>`_

Since Finite State Machines (FSM) are just a simple case of HSM, those
could be also defined using **hsmcpp**.

Here is an example of a simple HSM which only contains states and
transitions:

.. uml:: ./transitions/sample_transition.pu
   :align: center
   :alt: Simple HSM Example


.. toctree::
   :caption: Content

   states/states
   events/events
   transitions/transitions
   substates/substates
   history/history
   parallel/parallel
   timers/timers
   variant/variant