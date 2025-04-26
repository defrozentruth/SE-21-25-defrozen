#pragma once
#include "event.hpp"
#include <utility>


class Cell{
    bool access;
    bool playerOn;
    Event* event;
    bool eventPresence = false;
    public:
        Cell(bool access = true, bool playerOn = false, Event* event = nullptr);
        Cell(Cell& obj):access(obj.access), event(obj.event){};
        void swap(Cell &obj);
        Cell& operator=(Cell& obj);
        void changeEvent(Event* event);
        void changeAccess(bool new_access);
        bool isPassable();
        void playerVisit();
        Event* eventAccess();
        bool haveEvent();
        void changeEventPresence(bool state);
};