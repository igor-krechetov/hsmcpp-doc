.. _faq:

##################################
FAQ
##################################

.. contents::
   :local:


Where and when should I create/delete events dispatcher?
########################################################
Usually you would create a dispatcher during your application startup and keep it until your programm is ready to finish. Platforms/framework integrations have different limitations as to where it's acceptable to create, init or delete dispatcher objects. You can refer to the table in :ref:`platforms-builtin-dispatchers` page for details.

I have multiple state machines and what them to be executed on different thread. How can I do this?
###################################################################################################
You would need to create a separate dispatcher for each of your state machines. Keep in mind that if dispatcher doesnt create it's own thread then you most probably will also need to create a custom event loop using tools provided by your framework/platform (for example glib, glibmm, Qt). You can refer to the table in :ref:`platforms-builtin-dispatchers` page to check if dispatcher creates a separate thread or not.


Why my application crashes when I delete instance of HSM / dispatcher?
######################################################################
There could be a couple reasons for the crash:
* deleting dispatcher in incorrect place;

   * Some dispatchers can be deleted only on the same thread where they were created (glib, glibmm, qt). Deleting them in a different thread will result in undefined behavior (which is usually a crash).

* having pending events in dispatcher at the moment of it's destruction.


I'm using synchronous transitions. Why does my application get stuck?
#####################################################################
Make sure you are not calling synchronous transitions from any of the HSM/dispatcher callbacks. Doing so would result in a dead-lock.