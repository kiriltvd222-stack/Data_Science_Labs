#include "Display.hpp"

Display::Display(const std::string& name) : windowName(name) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
}

void Display::show(const cv::Mat& frame) {
    cv::imshow(windowName, frame);
}

void Display::setupCallbacks(FrameProcessor* processor) {
    cv::setMouseCallback(windowName, Display::onMouse, processor);
    cv::createTrackbar("Intensity", windowName, &(processor->sliderValue), 100, Display::onTrackbar, processor);
}

void Display::onMouse(int event, int x, int y, int flags, void* userdata) {
    FrameProcessor* fp = reinterpret_cast<FrameProcessor*>(userdata);
    if (event == cv::EVENT_LBUTTONDOWN) {
        fp->pt1 = cv::Point(x, y);
        fp->pt2 = fp->pt1;
        fp->isDrawing = true;
    } else if (event == cv::EVENT_MOUSEMOVE && fp->isDrawing) {
        fp->pt2 = cv::Point(x, y);
    } else if (event == cv::EVENT_LBUTTONUP) {
        fp->pt2 = cv::Point(x, y);
        fp->isDrawing = false;
    }
}

void Display::onTrackbar(int pos, void* userdata) {
    FrameProcessor* fp = reinterpret_cast<FrameProcessor*>(userdata);
    fp->sliderValue = pos;
}