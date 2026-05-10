#!/bin/bash
echo "Оновлення пакетів та встановлення залежностей..."
apt update
apt install -y libopencv-dev cmake g++ build-essential wget

echo "Завантаження моделей нейромережі (ResNet-10)..."
wget -q -N https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget -q -N https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel

echo "Залежності та моделі успішно встановлено!"