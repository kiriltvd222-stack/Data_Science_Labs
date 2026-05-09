#pragma once

enum class Mode { NORMAL, INVERT, BLUR, CANNY, GLITCH };

class KeyProcessor {
public:
    Mode currentMode = Mode::NORMAL;
    bool processKey(int key);
};