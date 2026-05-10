#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;
    std::thread worker;
    std::mutex mtx;
    std::atomic<bool> isRunning;
    std::atomic<bool> hasNewFrame;
    
    cv::Mat frameForDetection;
    std::vector<cv::Rect> faces;

    void detectLoop();

public:
    FaceDetector(const std::string& prototxt, const std::string& model);
    ~FaceDetector();

    void start();
    void stop();
    void setFrame(const cv::Mat& frame);
    std::vector<cv::Rect> getFaces();
};