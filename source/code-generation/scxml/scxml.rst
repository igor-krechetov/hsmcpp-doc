.. _code-generation-scxml:

######################
SCXML Format
######################

.. contents::
   :local:


Overview
========

*From* `Wikipedia <https://en.wikipedia.org/wiki/SCXML>`__ *:*

*SCXML stands for State Chart XML: State Machine Notation for Control
Abstraction. It is an XML-based markup language that provides a generic
state-machine-based execution environment based on Harel statecharts.*

*SCXML is able to describe complex finite state machines. For example,
it is possible to describe notations such as sub-states, parallel
states, synchronization, or concurrency, in SCXML.*

SCXML format specification can be found on `W3 official
website <https://www.w3.org/TR/scxml>`__.

SCXML format was designed to describe both structure and functionality
inside a single file. But since we are using it only to define structure,
some of SCXML features will be ignored.


Supported SCXML tags and attributes
===================================

.. |available| replace:: |:white_check_mark:| supported
.. |ignored| replace:: |:x:| ignored
.. |custom| replace:: |:heavy_plus_sign:| custom

+----------------------------------+----------+-----------+
|Tag                               |Attribute |Status     |
+==================================+==========+===========+
| .. centered:: **Core Constructs**                       |
+----------------------------------+----------+-----------+
|scxml                             |initial   ||available||
+                                  +----------+-----------+
|                                  |name      | |ignored| |
+                                  +----------+-----------+
|                                  |xmlns     ||available||
+                                  +----------+-----------+
|                                  |version   | |ignored| |
+                                  +----------+-----------+
|                                  |datamodel | |ignored| |
+                                  +----------+-----------+
|                                  |binding   | |ignored| |
+----------------------------------+----------+-----------+
| state                            | id       ||available||
+                                  +----------+-----------+
|                                  | initial  ||available||
+                                  +----------+-----------+
|                                  | src      | |custom|  |
+----------------------------------+----------+-----------+
| parallel                         | id       ||available||
+----------------------------------+----------+-----------+
| transition                       | event    ||available||
+                                  +----------+-----------+
|                                  | cond     ||available||
+                                  +----------+-----------+
|                                  | target   ||available||
+                                  +----------+-----------+
|                                  | type     ||available||
+----------------------------------+----------+-----------+
| initial                          |          ||available||
+----------------------------------+----------+-----------+
| final                            | id       ||available||
+----------------------------------+----------+-----------+
| onentry                          |          ||available||
+----------------------------------+----------+-----------+
| onexit                           |          ||available||
+----------------------------------+----------+-----------+
| history                          | id       ||available||
+                                  +----------+-----------+
|                                  | type     ||available||
+----------------------------------+----------+-----------+
| .. centered:: **Executable Content**                    |
+----------------------------------+----------+-----------+
| raise                            |          | |ignored| |
+----------------------------------+----------+-----------+
| if                               |          | |ignored| |
+----------------------------------+----------+-----------+
| elseif                           |          | |ignored| |
+----------------------------------+----------+-----------+
| else                             |          | |ignored| |
+----------------------------------+----------+-----------+
| foreach                          |          | |ignored| |
+----------------------------------+----------+-----------+
| log                              |          | |ignored| |
+----------------------------------+----------+-----------+
| .. centered:: **Data Model and Data Manipulation**      |
+----------------------------------+----------+-----------+
| datamodel                        |          | |ignored| |
+----------------------------------+----------+-----------+
| data                             |          | |ignored| |
+----------------------------------+----------+-----------+
| assign                           |          | |ignored| |
+----------------------------------+----------+-----------+
| donedata                         |          | |ignored| |
+----------------------------------+----------+-----------+
| content                          |          | |ignored| |
+----------------------------------+----------+-----------+
| param                            |          | |ignored| |
+----------------------------------+----------+-----------+
| script                           |          |  |custom| |
+----------------------------------+----------+-----------+
| .. centered:: **External Communications**               |
+----------------------------------+----------+-----------+
| send                             |          | |ignored| |
+----------------------------------+----------+-----------+
| cancel                           |          | |ignored| |
+----------------------------------+----------+-----------+
| invoke                           | type     | |ignored| |
+                                  +----------+-----------+
|                                  | typeexpr | |ignored| |
+                                  +----------+-----------+
|                                  | src      | |custom|  |
+                                  +----------+-----------+
|                                  | srcexpr  | |custom|  |
+                                  +----------+-----------+
|                                  | id       | |ignored| |
+                                  +----------+-----------+
|                                  |idlocation| |ignored| |
+                                  +----------+-----------+
|                                  | namelist | |ignored| |
+                                  +----------+-----------+
|                                  |autoforwad| |ignored| |
+----------------------------------+----------+-----------+
| finalize                         |          | |ignored| |
+----------------------------------+----------+-----------+
| .. centered:: **Extensions**                            |
+----------------------------------+----------+-----------+
| xi:include                       |          ||available||
+----------------------------------+----------+-----------+


Callbacks Definition
====================

There are 5 types of callbacks that could be defined for HSM:

-  on state changed:

.. code-block::  xml

   <state id="state_1">
       <invoke srcexpr="onState1"/>
   </state>

-  on state entering:

.. code-block::  xml

   <state id="state_1">
       <onentry>
           <script>onEnteringState1</script>
       </onentry>
   </state>

-  on state exiting:

.. code-block::  xml

   <state id="state_1">
       <onexit>
           <script>onExitingState1</script>
       </onexit>
   </state>

-  on transition:

.. code-block::  xml

   <state id="state_1">
       <transition event="NEXT_STATE" target="state_2">
           <script>onNextStateTransition</script>
       </transition>
   </state>

-  on condition check:

.. code-block::  xml

   <state id="state_1">
       <transition event="NEXT_STATE" cond="checkNextStateTransition" target="state_2"/>
   </state>

Callback names should comply with C++ identifier naming rules.


Splitting SCXML files
==============================================

When defining your HSM structure you might want to reuse a state or a
group of states for some common logic (for example error handling).
Included file must comply with SCXML format and have a root node
**<scxml>** defined.

There are two ways to include another file inside of your scxml:

- using **<xi:include>** tag
- using **"src"** attribute of a state


Include using <xi:include>
--------------------------

This is a standard way which is compliant with W3 specification. For
this tag to work additional namespace must be added to your scxml:

.. code-block::  xml

   <scxml xmlns:xi="http://www.w3.org/2001/XInclude">

Restrictions and things to consider:

-  <xi:include> tag can only be a child of <scxml> or <state> nodes.
   It's not allowed to put it anywhere else.
-  availability of initial state in included file is optional, but your
   HSM will *usually* not work without one (validation was disabled on
   purpose to allow importing of a single state).
-  it's highly recommended to wrap <xi:include> into a <state> node
   which doesnt contain any other states or includes (transitions are
   allowed).

   -  in this case parent state will work like a namespace altering
      included state names to avoid name collision (if you want to
      include same file multiple times);
   -  exit transition can be defined

-  when using <xi:include> on the same level with other states or
   include keep in mid that:

   -  code will be inserted as-is. name collisions, incorrect initial
      states, non existent transitions will not be resolved;
   -  GUI editors don't allow to define exit/enter transitions (though
      it's possible to define them manually in XML you will loose
      ability to edit such file in GUI editor).


Using <xi:include> with a wrapper state
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:repo-link:`/examples/scxml/includes/xi_include_wrapped.scxml`

.. literalinclude:: ../../../hsmcpp/examples/scxml/includes/xi_include_wrapped.scxml
   :language: xml

:repo-link:`/examples/scxml/includes/substates1.scxml`

.. literalinclude:: ../../../hsmcpp/examples/scxml/includes/substates1.scxml
   :language: xml


**Result structure**

.. image:: ./_gen/xiinclude_wrapped.png
   :align: center
   :alt: Example of wrapped xi:include


Including <xi:include> directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:repo-link:`/examples/scxml/includes/xi_include_direct.scxml`

.. literalinclude:: ../../../hsmcpp/examples/scxml/includes/xi_include_direct.scxml
   :language: xml

Note how we define a transition to State1 even though it's not defined
in xi_include_direct.scxml. Transition will become valid after code from
state1.scxml will be included.

.. code-block::  xml

   <transition event="EVENT_1" target="State1"></transition>

:repo-link:`/examples/scxml/includes/state1.scxml`

.. literalinclude:: ../../../hsmcpp/examples/scxml/includes/state1.scxml
   :language: xml

Note how we define a transition to State2 even though it's not defined
in state1.scxml:

.. code-block::  xml

   <transition event="EVENT_2" target="State2"></transition>

**Result structure**

.. image:: ./_gen/xiinclude_direct.png
   :align: center
   :alt: Example of direct usage of xi:include

Include using "src" attribute of <state>
----------------------------------------

It's possible to reference external scxml files by using "src" attribute
of a <state>.

.. code-block::  xml

   <state id="..." src="file path">
       ...
   </state>

This will behave exactly same as a <xi:include> tag wrapped inside a
<state>.

Keep in mind that **this is not a part of W3 SCXML specification** and
was added only because it's supported by `scxmlgui <https://github.com/fmorbini/scxmlgui>`__.

:repo-link:`/examples/scxml/includes/state_src_include.scxml`

.. literalinclude:: ../../../hsmcpp/examples/scxml/includes/state_src_include.scxml
   :language: xml

**Result structure**

.. image:: ./_gen/state_src_include.png
   :align: center
   :alt: Example of using state::src
