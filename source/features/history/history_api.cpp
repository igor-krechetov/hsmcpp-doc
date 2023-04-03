hsmcpp::HierarchicalStateMachine hsm;
HandlerClass hsmHandler;

...
hsm.registerState(MyStates::ParentState);
hsm.registerSubstateEntryPoint(MyStates::Parent, MyStates::StateA);
hsm.registerSubstate(MyStates::Parent, MyStates::StateB);
...

// to register history state with default parameters
hsm.registerHistory(MyStates::ParentState, MyStates::HistoryState1);

// to register deep history state
hsm.registerHistory(MyStates::ParentState, MyStates::HistoryState2, hsmcpp::HistoryType::DEEP);

// to register history state with custom default entry state
hsm.registerHistory(MyStates::ParentState, MyStates::HistoryState2,
                    hsmcpp::HistoryType::SHALLOW, MyStates::StateB);

// to register history state with custom callback
hsm.registerHistory(MyStates::ParentState, MyStates::HistoryState2,
                    hsmcpp::HistoryType::SHALLOW, INVALID_HSM_STATE_ID,
                    &hsmHandler, &HandlerClass::on_history_state,);