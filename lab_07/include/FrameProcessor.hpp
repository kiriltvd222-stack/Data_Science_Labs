#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"
#include <string>

class FrameProcessor {
private:
    int64 startTick;
    int framesCount;
    double fps;

public:
    int sliderValue = 15; 
    bool isDrawing = false;
    cv::Point pt1, pt2;

    FrameProcessor();
    cv::Mat process(const cv::Mat& input, Mode mode);
    void drawOverlay(cv::Mat& frame);
    void calculateFPS();
};