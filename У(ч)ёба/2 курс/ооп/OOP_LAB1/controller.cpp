
#include "controller.hpp"
        void Controller::mover(char movement, Field& field, Player& player){
                movement = tolower(movement);
                switch (movement){
                case 'w':
                    field.movePlayer(0, -1, player);
                break;
                case 'a':
                    field.movePlayer(-1, 0, player);
                break;
                case 's':
                    field.movePlayer(0, 1, player);
                break;
                case 'd':
                    field.movePlayer(1, 0, player);
                break;
                }
        }
