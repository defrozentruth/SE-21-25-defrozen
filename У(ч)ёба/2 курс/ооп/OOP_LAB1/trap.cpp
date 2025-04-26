    #include "trap.hpp"
    
    void Trap::changePlayer(Player& player){
        if(player.retAgility() < this->lvl){
            std::cout << "You fell into a pit and broke your leg!\n";
            player.decHP(this->lvl);
            if (player.retHP() <= 0)
                player.changeWinState(LOSE);
        }else{
            std::cout << "You noticed a pit and jumped over it. You gain agility";
            player.incAgility(this->lvl);
        }
    }

    char Trap::retName(){
        return 'T';
    }

    Trap* Trap::clone(){
        return new Trap(*this);
    }