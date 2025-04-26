#pragma once
#include "player_events.hpp"
#include "event.hpp"

class Enemy:public Player_Events{
    int lvl;
    int attack;
    int hp;
public:
    Enemy(int hp = 1, int attack = 1, int lvl = 1):hp(hp), attack(attack), lvl(lvl){};
    void changePlayer(Player& player);
    Enemy* clone() override;
    char retName();

};