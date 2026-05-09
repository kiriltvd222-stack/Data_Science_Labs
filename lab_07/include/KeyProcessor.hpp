#pragma once

enum class Mode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    GLITCH,
    FACE_DETECT
};

class KeyProcessor {
public:
    Mode processKey(char key, Mode currentMode);
};