#pragma once
#include <iostream>
#include <utility>
#include "event.hpp"
#include "cell.hpp"
#include "win.hpp"
#include "overseer.hpp"
#include "enemy.hpp"
#include "trap.hpp"
#include "map_events.hpp"
#include "player_events.hpp"




#define BASE_VALUE 20
#define WIN 1
#define LOSE -1

class Field{
    Cell** map;
    int size_x;
    int size_y;
    int player_x;
    int player_y;
    bool overseer;
    int winState;
    public:
        Field(int x = BASE_VALUE, int y = BASE_VALUE, int player_x = 0, int player_y = 0);
        void movePlayer(int x, int y, Player& player);
        Cell** getField();
        int getHeight();
        int getWidth();
        int getPlayerX();
        int getPlayerY();
        bool retOverseer();
        void changeOverseer(bool overseer);
        int retWinState();
        void changeWinState(int state);
        Field(const Field& fieldObj);
        void swap(Field &fieldObj);
        Field& operator=(const Field& fieldObj);
        Field(Field&& fieldObj);
        Field& operator=(Field&& filedObj);
        
};