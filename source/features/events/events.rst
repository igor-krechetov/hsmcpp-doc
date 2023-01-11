.. _features-events:

##################################
Events
##################################

Events are defined as an enum in yoru code:

.. code-block::  c++

   enum class MyEvents
   {
       EVENT_1,
       EVENT_2,
       EVENT_3,
       EVENT_4
   };

They could be later used when registering transitions.