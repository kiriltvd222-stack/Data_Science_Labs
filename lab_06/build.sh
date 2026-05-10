#!/bin/bash
echo "Початок збірки проєкту..."
mkdir -p build
cd build
cmake ..
make 
echo "Збірку успішно завершено!"