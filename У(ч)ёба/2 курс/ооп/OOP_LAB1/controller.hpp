#pragma once
#include "field.hpp"
#include "player.hpp"

class Controller{
    public:
        void mover(char movement, Field& field, Player& player);
};