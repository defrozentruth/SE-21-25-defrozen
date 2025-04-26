#pragma once

#include "map_events.hpp"


class Win: public Map_Events{
public:
    Win();
    void changeField(Field& field);
    Win* clone() override;
    char retName();
};