#include "overseer.hpp"

    void Overseer::changeField(Field& field){
        field.changeOverseer(true);
    }

    char Overseer::retName(){
        return 'O';
    }

    Overseer* Overseer::clone(){
        return new Overseer(*this);