.. _features-variant:

##################################
Variant Type
##################################

Due to C++11 not having std::variant type, hsmcpp library comes with it's own
implementation of Variant container. It supports all basic types and
some variations of std containers.


Supported types
---------------

-  BYTE_1 (int8_t)
-  BYTE_2 (int16_t)
-  BYTE_4 (int32_t)
-  BYTE_8 (int64_t)
-  UBYTE_1 (uint8_t)
-  UBYTE_2 (uint16_t)
-  UBYTE_4 (uint32_t)
-  UBYTE_8 (uint64_t)
-  DOUBLE (double)
-  BOOL (bool)
-  STRING (std::string)
-  BYTEARRAY (std::vector)
-  LIST (std::list)
-  VECTOR (std::vector)
-  DICTIONARY (std::map<Variant, Variant>)
-  PAIR (std::pair<Variant, Variant>)


Working with Variant type
-------------------------

To create a Variant from a basic type:

.. code-block:: c++

   Variant v1(7);
   Variant v2 = Variant::make(7);

To get value our of Variant container you can use one of the toXXXXX()
functions or value():

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
value()        - fast                                         - unsafe
                                                              - users are responsible to make sure they are using correct data
                                                                type
============== ============================================== =================================================================
