#pragma once
#include <iostream>
#include "player_events.hpp"


class Trap:public Player_Events{
    int lvl;
public:
    Trap(int lvl = 1):lvl(lvl){};
    void changePlayer(Player& player);
    Trap* clone() override;
    char retName();
};