.. _features-variant:

##################################
Variant Type
##################################

Overview
========

Due to C++11 not having std::variant type, hsmcpp library comes with it's own
implementation of Variant container. It supports all basic types and
some variations of std containers (see :hsmcpp:`Variant::Type` enum).


Supported types
===============

================= =============================================
Name              Underlying Type
================= =============================================
Type::BYTE_1      int8_t
Type::BYTE_2      int16_t
Type::BYTE_4      int32_t
Type::BYTE_8      int64_t
Type::UBYTE_1     uint8_t
Type::UBYTE_2     uint16_t
Type::UBYTE_4     uint32_t
Type::UBYTE_8     uint64_t
Type::DOUBLE      double
Type::BOOL        bool
Type::STRING      std::string
Type::BYTEARRAY   std::vector
Type::LIST        std::list
Type::VECTOR      std::vector
Type::DICTIONARY  std::map<hsmcpp::Variant, hsmcpp::Variant>
Type::PAIR        std::pair<hsmcpp::Variant, hsmcpp::Variant>
================= =============================================


Working with Variant type
=========================

To create a Variant from a basic type:

.. code-block:: c++

   Variant v1(7);
   Variant v2 = Variant::make(7);

To get value our of Variant container you can use one of the toXXXXX() functions (for example :hsmcpp:`Variant::toString`) or :hsmcpp:`Variant::value`:

.. code-block:: c++

   Variant v1("abc");
   std::string s1 = v1.toString();
   std::string s2 = *(v1.value<std::string>());

The difference between these two approaches is that toXXXXX() functions
also try to convert internal value to requested type while value()
returns a pointer to internal data.

============== ============================================== =================================================================
Approach       Pros                                           Cons
============== ============================================== =================================================================
toXXXXX()      - easy to use                                  - slower
               - automatically converts types (if possible)   - some types are not available (for example only toInt64() and
                                                                toUInt64() for numeric values)
value()        - fast                                         - **unsafe**
                                                              - users are responsible to make sure they are using correct data
                                                                type
============== ============================================== =================================================================
