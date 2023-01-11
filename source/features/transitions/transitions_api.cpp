hsm.registerTransition(MyStates::StateA,
                        MyStates::StateB,
                        MyEvents::EVENT_1,
                        &hsmHandler,
                        &HandlerClass::on_event_1_transition,
                        &HandlerClass::event_1_condition,
                        true);
hsm.registerTransition(MyStates::StateA,
                        MyStates::StateB,
                        MyEvents::EVENT_1,
                        [](const VariantVector_t& args){ ... },
                        [](const VariantVector_t& args){ ... return true; },
                        true);