HierarchicalStateMachine<MyStates, MyEvents> hsm;
HandlerClass hsmHandler;

hsm.registerState(MyStates::StateA);
hsm.registerState(MyStates::StateA, &hsmHandler, &HandlerClass::on_state_changed_a);
hsm.registerState(MyStates::StateA,
                    &hsmHandler,
                    &HandlerClass::on_state_changed_a,
                    &HandlerClass::on_entering_a);
hsm.registerState(MyStates::StateA,
                    &hsmHandler,
                    &HandlerClass::on_state_changed_a,
                    &HandlerClass::on_entering_a,
                    &HandlerClass::on_exiting_a);
hsm.registerState<HandlerClass>(MyStates::StateA,
                                &hsmHandler,
                                &HandlerClass::on_state_changed_a,
                                nullptr,
                                &HandlerClass::on_exiting_a);