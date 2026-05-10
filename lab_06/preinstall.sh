#!/bin/bash
echo "Оновлення пакетів та встановлення залежностей..."
sudo apt update
sudo apt install -y build-essential cmake gcc g++ libopencv-dev
echo "Встановлення завершено!"