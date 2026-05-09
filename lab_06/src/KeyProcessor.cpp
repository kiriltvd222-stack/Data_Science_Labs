#include "KeyProcessor.hpp"

bool KeyProcessor::processKey(int key) {
    if (key == 27 || key == 'q' || key == 'Q') return false; // ESC або Q для виходу
    
    switch (key) {
        case '1': currentMode = Mode::NORMAL; break;
        case '2': currentMode = Mode::INVERT; break;
        case '3': currentMode = Mode::BLUR; break;
        case '4': currentMode = Mode::CANNY; break;
        case '5': currentMode = Mode::GLITCH; break;
    }
    return true;
}