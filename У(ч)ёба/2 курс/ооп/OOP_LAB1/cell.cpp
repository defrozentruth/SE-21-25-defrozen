#include "cell.hpp"


        Cell::Cell(bool access, bool playerOn, Event* event){
            this->access = access;
            this->event = event;
            this->playerOn = playerOn;
            if (event != nullptr){
                this->event = event->clone();
                this->changeEventPresence(true);
            }else{
                this->event = nullptr;
            }
        }

        void Cell::changeEvent(Event* event){
            if(event != nullptr)
            this->event = event->clone();
            else
            this->event = nullptr;
        };

        void Cell::changeAccess(bool new_access){
            this->access = new_access;
        }

        bool Cell::isPassable(){
            return access;
        }

        void Cell::playerVisit(){
            if(playerOn){
                playerOn = false;
            }
            else
                playerOn = true;
        }

        void Cell::swap(Cell &obj){
            std::swap(access, obj.access);
            std::swap(playerOn, obj.playerOn);
            std::swap(event, obj.event);
        }
        Cell& Cell::operator=(Cell& obj){
            if(this != &obj){
                this->access = obj.access;
                this->playerOn = obj.playerOn;
                this->eventPresence = obj.eventPresence;
                this->event = obj.event->clone();
            }
            return *this;
        }

        Event* Cell::eventAccess(){
            if (this->event != nullptr) return this->event;
            return nullptr;
        }

        bool Cell::haveEvent(){
            return this->eventPresence;
        }

        void Cell::changeEventPresence(bool state){
            this->eventPresence = state;
        }