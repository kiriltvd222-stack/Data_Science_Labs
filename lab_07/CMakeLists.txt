cmake_minimum_required(VERSION 3.10)
project(Lab7_OpenCV)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS} include)

file(GLOB SOURCES "src/*.cpp")

add_executable(lab7_opencv ${SOURCES})
target_link_libraries(lab7_opencv ${OpenCV_LIBS} Threads::Threads)