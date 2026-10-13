// Content of this file was generated

#include "SwitchHsmBase.hpp"

SwitchHsmBase::SwitchHsmBase()
    : HierarchicalStateMachine<SwitchHsmStates, SwitchHsmEvents>(SwitchHsmStates::On)
{
    configureHsm();
}

SwitchHsmBase::~SwitchHsmBase()
{}

void SwitchHsmBase::configureHsm()
{
    registerState<SwitchHsmBase>(SwitchHsmStates::On, this, &SwitchHsmBase::onOn, nullptr, nullptr);
    registerState<SwitchHsmBase>(SwitchHsmStates::Off, this, &SwitchHsmBase::onOff, nullptr, nullptr);


    registerTransition<SwitchHsmBase>(SwitchHsmStates::On, SwitchHsmStates::Off, SwitchHsmEvents::SWITCH, this, nullptr);
    registerTransition<SwitchHsmBase>(SwitchHsmStates::Off, SwitchHsmStates::On, SwitchHsmEvents::SWITCH, this, nullptr);
}
