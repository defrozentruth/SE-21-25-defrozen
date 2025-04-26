
#include "fieldview.hpp"


    void FieldView::printField(Field& field){
        Cell** temp = field.getField();
        for(int i = 0; i < field.getHeight(); i++) {
            for (int j = 0; j < field.getWidth(); j++) {
                if(temp[i][j].isPassable()){
                    if(i == field.getPlayerY() && j == field.getPlayerX()){
                        std::cout << "[@]";
                    }else{
                        if(temp[i][j].haveEvent() == true){
                            if(temp[i][j].eventAccess()->retName() == 'E' || temp[i][j].eventAccess()->retName() == 'W')
                                {if(temp[i][j].eventAccess()->retName() == 'E')
                                    std::cout << "[T]";
                                if(temp[i][j].eventAccess()->retName() == 'W')
                                    if (field.retOverseer())
                                    std::cout << "[%]";
                                    else
                                    std::cout << "[?]";}

                            else{
                                std::cout << "[?]";
                            }
                        }else{
                            std::cout << "[ ]";
                        }
                    }
                }
                else{
                    std::cout << "[#]";
                }
            }
            std::cout << '\n';
        }
    }
