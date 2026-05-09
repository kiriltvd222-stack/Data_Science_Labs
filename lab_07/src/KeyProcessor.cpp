#include "KeyProcessor.hpp"

Mode KeyProcessor::processKey(char key, Mode currentMode) {
    switch (key) {
        case '1': return Mode::NORMAL;
        case '2': return Mode::INVERT;
        case '3': return Mode::BLUR;
        case '4': return Mode::CANNY;
        case '5': return Mode::GLITCH;
        case 'f': 
        case 'F': return Mode::FACE_DETECT;
        default: return currentMode;
    }
}