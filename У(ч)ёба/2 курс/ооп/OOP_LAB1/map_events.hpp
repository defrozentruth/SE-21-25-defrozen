#pragma once
#include "event.hpp"

class Field;
#include "field.hpp"


class Map_Events : public Event{
    public:
        virtual void changePlayer(Player& player) final;
};