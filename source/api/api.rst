.. _api:

##################################
API Reference
##################################

.. contents::
   :local:
   :depth: 2


Overview
========

Developers are supposed to utilize template class
HierarchicalStateMachine to use HSM in their projects. The simplest
approach is to create your own handler class that derives from
HierarchicalStateMachine:

.. code-block::  c++

   class MyHandler: protected HierarchicalStateMachine<MyStates, MyEvents, MyHandler>
   { ... };

From here it becomes possible to utilize provided API and configure HSM structure.


API details
===========

(constructor)
-------------

parameters
~~~~~~~~~~

============ ================== ======= ===============================
Name         Type               Default Description
============ ================== ======= ===============================
initialState const HsmStateEnum         Specifies initial state for HSM
============ ================== ======= ===============================

thread safety
~~~~~~~~~~~~~

Can be created on any thread without limitations, but in general it's
recommented to do it on the same thread where dispatcher was created.

(destructor)
------------

.. _thread-safety-1:

thread safety
~~~~~~~~~~~~~

Since it uses unregisterEventHandler() method of event dispatcher it
depends on it's implementation. Some dispatchers require their methods
to be called from a single thread. General recomendation would be to
create and destroy HSM from a single thread.

initialize
----------

Registers HSM object with provided event dispatcher. If dispatcher is
not running yet it will be automatically started. All HSM callbacks will
be executed in the context provided by dispatcher.

.. _parameters-1:

parameters
~~~~~~~~~~

+------------+---------------------+---------+---------------------+
| Name       | Type                | Default | Description         |
+============+=====================+=========+=====================+
| dispatcher | const               |         | event dispatcher to |
|            | std::shared_ptr&    |         | use for HSM         |
|            |                     |         | transitions         |
|            |                     |         | mechanism           |
+------------+---------------------+---------+---------------------+

return value
~~~~~~~~~~~~

*bool*: Returns FALSE in case of an error during HSM initialization.
Possible reasons could be:

-  dispatcher not provided
-  failed to start dispatcher

.. _thread-safety-2:

thread safety
~~~~~~~~~~~~~

Not thread safe. Recommended to call from the same thread where
dispatcher was created.

registerState
-------------

Registers HSM state and its handler callbacks. Does nothing if no
callbacks are provided.

*Note*: if you want to use HSM_ENABLE_SAFE_STRUCTURE flag to validate
HSM structure then all states must be registered (even if they dont have
callbacks).

.. _parameters-2:

parameters
~~~~~~~~~~

Prototype 1 \| Name \| Type \| Default \| Description \|
\|---\|:---:\|:---\|:---\| \| state \| const HsmStateEnum \| \| state to
register \| \| handler \| HsmHandlerClass\* \| nullptr \| object that
implements callbacks \| \| onStateChanged \|
HsmStateChangedCallbackPtr_t \| nullptr \| "state changed" callback \|
\| onEntering \| HsmStateEnterCallbackPtr_t \| nullptr \| "entering
state" callback \| \| onExiting \| HsmStateExitCallbackPtr_t \| nullptr
\| "exiting state" callback \|

Prototype 2 \| Name \| Type \| Default \| Description \|
\|---\|:---:\|:---\|:---\| \| state \| const HsmStateEnum \| \| state to
register \| \| onStateChanged \| HsmStateChangedCallback_t \| nullptr \|
"state changed" callback \| \| onEntering \| HsmStateEnterCallback_t \|
nullptr \| "entering state" callback \| \| onExiting \|
HsmStateExitCallback_t \| nullptr \| "exiting state" callback \|

.. _thread-safety-3:

thread safety
~~~~~~~~~~~~~

Not thread safe.

registerSubstate
----------------

Registers a state as a substate. This imposes a couple of restrictions:

-  each parent state must have only one entry point

   -  first call to this method must have *isEntryPoint* parameter set
      to *true* (per each parent)
   -  if multiple entry points are specified only the last one will be
      applied

-  callbacks provided in `registerState() <#registerstate>`__ for parent
   states will be ignored
-  single state can't be added as a substate to multiple parents
-  state can't be added as a substate multiple times

Provides additional structure validation if HSM_ENABLE_SAFE_STRUCTURE
flag is set.

.. _parameters-3:

parameters
~~~~~~~~~~

+--------------+--------------------+---------+--------------------+
| Name         | Type               | Default | Description        |
+==============+====================+=========+====================+
| parent       | const HsmStateEnum |         | parent state where |
|              |                    |         | a substate should  |
|              |                    |         | be added           |
+--------------+--------------------+---------+--------------------+
| substate     | const HsmStateEnum |         | state which should |
|              |                    |         | be registered as a |
|              |                    |         | substate           |
+--------------+--------------------+---------+--------------------+
| isEntryPoint | const bool         | false   | substate will be   |
|              |                    |         | treated as an      |
|              |                    |         | entry point if     |
|              |                    |         | TRUE is specified  |
+--------------+--------------------+---------+--------------------+

.. _return-value-1:

return value
~~~~~~~~~~~~

*bool*: Returns TRUE if substate registration was successful.

.. _thread-safety-4:

thread safety
~~~~~~~~~~~~~

Not thread safe.

registerTransition
------------------

Registers transition between states.

.. _parameters-4:

parameters
~~~~~~~~~~

Prototype 1 \| Name \| Type \| Default \| Description \|
\|---\|:---:\|:---\|:---\| \| from \| const HsmStateEnum \| \| state
from which transition initiates \| \| to \| const HsmStateEnum \| \|
state to which transition leads \| \| onEvent \| const HsmEventEnum \|
\| event that should trigger transition \| \| handler \|
HsmHandlerClass\* \| nullptr \| object that implements callbacks \| \|
transitionCallback \| HsmTransitionCallbackPtr_t \| nullptr \| callback
that will be triggered during transition \| \| conditionCallback \|
HsmTransitionConditionCallbackPtr_t \| nullptr \| callback that will be
triggered before transition to check if it's allowed \|

Prototype 2 \| Name \| Type \| Default \| Description \|
\|---\|:---:\|:---\|:---\| \| from \| const HsmStateEnum \| \| state
from which transition initiates \| \| to \| const HsmStateEnum \| \|
state to which transition leads \| \| onEvent \| const HsmEventEnum \|
\| event that should trigger transition \| \| transitionCallback \|
HsmTransitionCallback_t \| nullptr \| callback that will be triggered
during transition \| \| conditionCallback \|
HsmTransitionConditionCallback_t \| nullptr \| callback that will be
triggered before transition to check if it's allowed \|

.. _thread-safety-5:

thread safety
~~~~~~~~~~~~~

Not thread safe.

getCurrentState
---------------

Returns current HSM state.

.. _return-value-2:

return value
~~~~~~~~~~~~

*HsmStateEnum*: current HSM state

.. _thread-safety-6:

thread safety
~~~~~~~~~~~~~

Thread safe.

transitionEx
------------

Sends event to HSM and tries to trigger a transition.

.. _parameters-5:

parameters
~~~~~~~~~~

+------------+--------------------+---------+---------------------+
| Name       | Type               | Default | Description         |
+============+====================+=========+=====================+
| event      | const HsmEventEnum |         | event to send to    |
|            |                    |         | HSM                 |
+------------+--------------------+---------+---------------------+
| clearQueue | const bool         |         | clear all pending   |
|            |                    |         | events before       |
|            |                    |         | sending a new event |
+------------+--------------------+---------+---------------------+
| sync       | const bool         |         | block execution and |
|            |                    |         | wait for transition |
|            |                    |         | to finish           |
+------------+--------------------+---------+---------------------+
| args       | Args...            |         | optional arguments  |
|            |                    |         | to pass to          |
|            |                    |         | callbacks           |
+------------+--------------------+---------+---------------------+

.. _return-value-3:

return value
~~~~~~~~~~~~

*bool*: for async transitions always returns TRUE; for SYNC transitions
returns TRUE only if transition was successfully finished, otherwise
returns FALSE.

.. _thread-safety-7:

thread safety
~~~~~~~~~~~~~

Safe to call from any thread.

transition
----------

Simple async transition. Wrapper over
`transitionEx() <#transitionex>`__.

.. _parameters-6:

parameters
~~~~~~~~~~

===== ================== ======= =======================================
Name  Type               Default Description
===== ================== ======= =======================================
event const HsmEventEnum         event to send to HSM
args  Args...                    optional arguments to pass to callbacks
===== ================== ======= =======================================

.. _thread-safety-8:

thread safety
~~~~~~~~~~~~~

Safe to call from any thread.

transitionWithQueueClear
------------------------

Async transition with clearing pending events queue. Wrapper over
`transitionEx() <#transitionex>`__.

.. _parameters-7:

parameters
~~~~~~~~~~

===== ================== ======= =======================================
Name  Type               Default Description
===== ================== ======= =======================================
event const HsmEventEnum         event to send to HSM
args  Args...                    optional arguments to pass to callbacks
===== ================== ======= =======================================

.. _thread-safety-9:

thread safety
~~~~~~~~~~~~~

Safe to call from any thread.

isTransitionPossible
--------------------

Checks if sending *event* will result in any transitions from current
HSM state. Method just simulates a transition and does not modify
anything in an HSM. *Note*: only transitions *conditionCallback* will be
triggered. Other handlers like state callbacks will not be invoked.

.. _parameters-8:

parameters
~~~~~~~~~~

===== ================== ======= =======================================
Name  Type               Default Description
===== ================== ======= =======================================
event const HsmEventEnum         event to send to HSM
args  Args...                    optional arguments to pass to callbacks
===== ================== ======= =======================================

.. _return-value-4:

return value
~~~~~~~~~~~~

*bool*: returns TRUE if transition is possible

.. _thread-safety-10:

thread safety
~~~~~~~~~~~~~

Safe to call from any thread.
