#pragma once
#include "event.hpp"
#include "player.hpp"

class Player_Events:public Event{
public:
    virtual void changeField(Field& field) final;
};