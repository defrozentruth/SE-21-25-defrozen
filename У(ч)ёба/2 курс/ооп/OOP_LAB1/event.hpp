#pragma once
#include "player.hpp"
#include "field.hpp"
#include <iostream>

class Event{
public:
    Event() = default;
    virtual Event* clone() = 0;
    virtual void changePlayer(Player& player) = 0;
    virtual void changeField(Field& field) = 0;
    virtual char retName() = 0;
};