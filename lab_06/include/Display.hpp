#pragma once
#include <opencv2/opencv.hpp>
#include <string>
#include "FrameProcessor.hpp"

class Display {
public:
    std::string windowName;
    Display(const std::string& name);
    void show(const cv::Mat& frame);
    void setupCallbacks(FrameProcessor* processor);

    // Статичні функції для callbacks (вимога OpenCV)
    static void onMouse(int event, int x, int y, int flags, void* userdata);
    static void onTrackbar(int pos, void* userdata);
};