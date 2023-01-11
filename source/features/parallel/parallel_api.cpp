hsm.registerTransition(MyStates::StateA, MyStates::StateB, MyEvents::EVENT_1);
hsm.registerTransition(MyStates::StateA, MyStates::StateC, MyEvents::EVENT_1);

// or

hsm.registerTransition(MyStates::StateA,
                       MyStates::StateB,
                       MyEvents::EVENT_1,
                       &hsmHandler,
                       nullptr,
                       &HandlerClass::event_1_condition);
hsm.registerTransition(MyStates::StateA,
                       MyStates::StateC,
                       MyEvents::EVENT_1,
                       &hsmHandler,
                       nullptr,
                       &HandlerClass::event_1_condition);