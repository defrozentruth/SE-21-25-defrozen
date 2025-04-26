#pragma once

#define WIN 1
#define LOSE -1

class Player{
    int hp;
    int agility;
    int attack;
    int winState;
    public:
        Player(int hp = 10, int agility = 1, int atk = 1);
        void decHP(int hp);
        int retHP();
        int retAgility();
        int retAttack();
        void incHP(int hp);
        void incAgility(int ag);
        void incAttack(int atk);
        void changeWinState(int state);
        int retWinState();
};