cmake_minimum_required(VERSION 3.8)
project(practica3)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    launch
    urdf
    meshes
    rviz
    robots
    config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()