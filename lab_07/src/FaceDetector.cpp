#include "FaceDetector.hpp"
#include <chrono>

FaceDetector::FaceDetector(const std::string& prototxt, const std::string& model) {
    net = cv::dnn::readNetFromCaffe(prototxt, model);
    isRunning = false;
    hasNewFrame = false;
}

FaceDetector::~FaceDetector() {
    stop();
}

void FaceDetector::start() {
    if (!isRunning) {
        isRunning = true;
        worker = std::thread(&FaceDetector::detectLoop, this);
    }
}

void FaceDetector::stop() {
    isRunning = false;
    if (worker.joinable()) {
        worker.join();
    }
}

void FaceDetector::setFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    frame.copyTo(frameForDetection);
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return faces;
}

void FaceDetector::detectLoop() {
    while (isRunning) {
        cv::Mat localFrame;
        bool processFrame = false;

        {
            std::lock_guard<std::mutex> lock(mtx);
            if (hasNewFrame && !frameForDetection.empty()) {
                frameForDetection.copyTo(localFrame);
                hasNewFrame = false;
                processFrame = true;
            }
        }

        if (processFrame) {
            cv::Mat blob = cv::dnn::blobFromImage(localFrame, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
            net.setInput(blob);
            
            cv::Mat detections = net.forward();
            cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

            std::vector<cv::Rect> localFaces;

            for (int i = 0; i < detectionMat.rows; i++) {
                float confidence = detectionMat.at<float>(i, 2);
                if (confidence > 0.5) {
                    int xLeftBottom = static_cast<int>(detectionMat.at<float>(i, 3) * localFrame.cols);
                    int yLeftBottom = static_cast<int>(detectionMat.at<float>(i, 4) * localFrame.rows);
                    int xRightTop = static_cast<int>(detectionMat.at<float>(i, 5) * localFrame.cols);
                    int yRightTop = static_cast<int>(detectionMat.at<float>(i, 6) * localFrame.rows);

                    localFaces.push_back(cv::Rect(xLeftBottom, yLeftBottom, 
                                                  xRightTop - xLeftBottom, 
                                                  yRightTop - yLeftBottom));
                }
            }

            {
                std::lock_guard<std::mutex> lock(mtx);
                faces = localFaces;
            }
            
            // Штучна затримка на 500мс для демонстрації багатопотоковості
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        } else {
            std::this_thread::sleep_for(std::chrono::milliseconds(10)); 
        }
    }
}