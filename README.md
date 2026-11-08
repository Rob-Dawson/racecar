<h1 align="center">Autonomous-Racecar</h1>
<h3>ROS 2-based autonomous vehicle platform exploring robotics navigation, mapping, path planning and control.</h3>

---

## About

Autonomous Racecar is a personal robotics project focused on developing and exploring autonomous navigation algorithms using a small-scale Ackermann-steered vehicle. The project aims to provide a modular platform for experimenting with mapping, localisation, path planning, trajectory generation and vehicle control.

Initial development uses ROS 2 and Gazebo Harmonic to simulate the vehicle, with `ros2_control` providing an interface for Ackermann steering and wheel control. Future development will introduce LiDAR-based mapping, autonomous navigation using Nav2, and custom C++ implementations of navigation algorithms.

The long-term goal is to transfer the system to a physical RC vehicle, integrating onboard computing, sensors and embedded control hardware.

---

## Technologies

| Robotics & Simulation | Software & Development |
|-----------------------|------------------------|
| ROS 2                 | C++                    |
| Gazebo Harmonic       | Python                 |
| ros2_control          | Git                    |
| SLAM Toolbox *(planned)* | CMake               |
| Nav2 *(planned)*      |                        |

---

## Getting Started

[Installation, build and launch instructions to be added.]

---

## Acknowledgements

This project is partially based on the original MIT RACECAR project, with components adapted and developed for ROS 2 and Gazebo Harmonic.

---

<a href="#top">Back to top</a>
