hsm.registerSelfTransition(MyStates::StateA,
                            MyEvents::EVENT_1,
                            TransitionType::INTERNAL_TRANSITION,
                            &hsmHandler,
                            &HandlerClass::on_event_1_transition,
                            &HandlerClass::event_1_condition,
                            true);

hsm.registerSelfTransition(MyStates::StateA,
                            MyEvents::EVENT_1,
                            TransitionType::INTERNAL_TRANSITION,
                            [](const VariantVector_t& args){ ... },
                            [](const VariantVector_t& args){ ... return true; },
                            true);