// Content of this file was generated

#ifndef __GEN_HSM_SWITCHHSMBASE__
#define __GEN_HSM_SWITCHHSMBASE__

#include <hsmcpp/hsm.hpp>

enum class SwitchHsmStates
{
    On,
    Off,
};

enum class SwitchHsmEvents
{
    SWITCH,
};

class SwitchHsmBase: public HierarchicalStateMachine<SwitchHsmStates, SwitchHsmEvents>
{
public:
    SwitchHsmBase();
    virtual ~SwitchHsmBase();

protected:
    void configureHsm();

// HSM state changed callbacks
protected:
    virtual void onOff(const VariantList_t& args) = 0;
    virtual void onOn(const VariantList_t& args) = 0;

// HSM state entering callbacks
protected:

// HSM state exiting callbacks
protected:

// HSM transition callbacks
protected:

// HSM transition condition callbacks
protected:
};

#endif // __GEN_HSM_SWITCHHSMBASE__
