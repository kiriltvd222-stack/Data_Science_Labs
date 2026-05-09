#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() : framesCount(0), fps(0.0) {
    startTick = cv::getTickCount();
}

void FrameProcessor::calculateFPS() {
    framesCount++;
    int64 currentTick = cv::getTickCount();
    double timePassed = (currentTick - startTick) / cv::getTickFrequency();
    if (timePassed >= 1.0) {
        fps = framesCount / timePassed;
        framesCount = 0;
        startTick = currentTick;
    }
}

cv::Mat FrameProcessor::process(const cv::Mat& input, Mode mode) {
    cv::Mat output = input.clone();

    switch (mode) {
        case Mode::INVERT:
            cv::bitwise_not(output, output);
            break;
        case Mode::BLUR:
            {
                int ksize = (sliderValue % 2 == 0) ? sliderValue + 1 : sliderValue;
                if (ksize < 1) ksize = 1;
                cv::GaussianBlur(output, output, cv::Size(ksize, ksize), 0);
            }
            break;
        case Mode::CANNY:
            {
                cv::Mat gray;
                cv::cvtColor(output, gray, cv::COLOR_BGR2GRAY);
                cv::Canny(gray, output, sliderValue, sliderValue * 3);
                cv::cvtColor(output, output, cv::COLOR_GRAY2BGR);
            }
            break;
        case Mode::GLITCH:
            {
                std::vector<cv::Mat> channels(3);
                cv::split(output, channels);
                cv::Mat shiftMat = cv::Mat::zeros(output.size(), CV_8UC1);
                // Зсуваємо червоний канал вправо
                cv::Mat roiRed = channels[2](cv::Rect(0, 0, output.cols - 15, output.rows));
                roiRed.copyTo(shiftMat(cv::Rect(15, 0, output.cols - 15, output.rows)));
                channels[2] = shiftMat.clone();
                cv::merge(channels, output);
            }
            break;
        default:
            break;
    }

    calculateFPS();
    drawOverlay(output);
    return output;
}

void FrameProcessor::drawOverlay(cv::Mat& frame) {
    // Малюємо FPS
    std::string fpsText = "FPS: " + std::to_string((int)fps);
    cv::putText(frame, fpsText, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);

    // Малюємо прямокутник мишкою
    if (isDrawing || (pt1.x != 0 && pt2.x != 0)) {
        cv::rectangle(frame, pt1, pt2, cv::Scalar(0, 0, 255), 2);
    }
}