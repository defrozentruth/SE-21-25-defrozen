#include "enemy.hpp"    

    void Enemy::changePlayer(Player& player){
        int playerHP = player.retHP();
        int enemyHP = this->hp;
        while(playerHP > 0 && enemyHP > 0){
            playerHP--;
            player.decHP(attack);
            enemyHP = enemyHP - player.retAttack();
        }
        if(enemyHP <= 0 ){
            std::cout << "You've won! You gain some points to your attack and hp!\n";
            player.incAttack(lvl);
            player.incHP(hp);
        }else{
            std::cout << "You have lost!\n";
            player.changeWinState(LOSE);
        }
    }

    char Enemy::retName(){
        return 'E';
    }

    Enemy* Enemy::clone(){
        return new Enemy(*this);
    }

