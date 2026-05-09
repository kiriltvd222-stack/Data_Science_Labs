#include <iostream>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
        return -1;
    }

    KeyProcessor keyProc;
    FrameProcessor frameProc;
    Display display("Lab 6 - OpenCV C++");

    display.setupCallbacks(&frameProc);

    std::cout << "Програма запущена. Натисніть 'q' або 'ESC' для виходу." << std::endl;
    std::cout << "Режими: 1(Normal), 2(Invert), 3(Blur), 4(Canny), 5(Glitch)." << std::endl;

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            std::cerr << "Помилка: Порожній кадр!" << std::endl;
            break;
        }

        cv::Mat processed = frameProc.process(frame, keyProc.currentMode);
        display.show(processed);

        int key = cv::waitKey(30);
        if (!keyProc.processKey(key)) break;
    }

    return 0;
}