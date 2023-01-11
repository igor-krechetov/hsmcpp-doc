.. _code-generation:

##################################
Code Generation
##################################


Overview
========

In general it's totally fine to define HSM structure manually in code.
But in real projects we often have to deal with:

-  state machine complexity (understanding states logic from code can
   becomes almost impossible even with as little as 10 different
   states);
-  synchronizing implementation and state diagrams for documentation;
-  copy-paste mistakes.

To help deal with these issues hsmcpp library comes with **scxml2gen**
utility. It uses state machines defined in SCXML format and allows to:

-  generate C++ code;
-  generate PlantUML state diagrams.


.. toctree::
   :caption: Content

   scxml/scxml
   editors/editors
   build-integration/build-integration
