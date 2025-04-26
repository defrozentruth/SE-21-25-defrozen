#include "win.hpp"


    void Win::changeField(Field& field){
        field.changeWinState(WIN);
    }

    char Win::retName(){
        return 'W';
    }

    Win* Win::clone(){
        return new Win(*this);
    }