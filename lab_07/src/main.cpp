#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "FaceDetector.hpp"
#include <iostream>

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
        return -1;
    }

    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;
    
    // Ініціалізація нейронки та запуск фонового потоку
    FaceDetector faceDetector("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    faceDetector.start();

    Mode currentMode = Mode::NORMAL;

    // Створюємо вікно заздалегідь
    cv::namedWindow("Lab 7 - AI & Threads");

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        if (currentMode == Mode::FACE_DETECT) {
            // Відправляємо кадр нейромережі
            faceDetector.setFrame(frame);

            // Забираємо останні координати та малюємо
            std::vector<cv::Rect> faces = faceDetector.getFaces();
            for (const auto& face : faces) {
                cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
                cv::putText(frame, "Face", cv::Point(face.x, face.y - 10),
                            cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
            }
            
            // Напис для зручності
            cv::putText(frame, "AI Mode: ON (Threaded)", cv::Point(10, 30), 
                        cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 255, 255), 2);
        } 
        else {
            // Звичайна обробка фільтрами з 6-ї лаби
            frame = frameProcessor.process(frame, currentMode); 
        }

        cv::imshow("Lab 7 - AI & Threads", frame);

        char key = (char)cv::waitKey(1);
        if (key == 27 || key == 'q') break;

        currentMode = keyProcessor.processKey(key, currentMode);
    }

    // Зупиняємо фоновий потік перед виходом
    faceDetector.stop();
    return 0;
}