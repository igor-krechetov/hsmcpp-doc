.. _features-events:

##################################
Events
##################################

Overview
========

Events are defined using `hsmcpp::EventID_t <../../api/api.html#typedefs>`__ type. Recommended way is to put definitions into a namespace:

.. code-block::  c++

    namespace MyEvents {
        constexpr hsmcpp::EventID_t EVENT_1 = 0;
        constexpr hsmcpp::EventID_t EVENT_2 = 1;
        constexpr hsmcpp::EventID_t EVENT_3 = 2;
        constexpr hsmcpp::EventID_t EVENT_4 = 3;
    }

They could be later used when registering transitions.