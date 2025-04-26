#pragma once
#include "map_events.hpp"

class Overseer: public Map_Events{
public:
    Overseer();
    void changeField(Field& field);
    Overseer* clone() override;
    char retName();
};