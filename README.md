<h1 align="center">Autonomous Racecar</h1>

<p align="center">
  <strong>ROS 2-based autonomous Ackermann-steered vehicle exploring robotics navigation, mapping, path planning and control.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/ROS_2-Jazzy-blue" alt="ROS 2 Jazzy">
  <img src="https://img.shields.io/badge/Gazebo-Harmonic-orange" alt="Gazebo Harmonic">
  <img src="https://img.shields.io/badge/Status-V1.0.0-green" alt="V1.0.0">
</p>

---

## About

Autonomous Racecar is a personal robotics project focused on developing and exploring autonomous navigation algorithms using a small-scale Ackermann-steered vehicle.

The project provides a modular platform for experimenting with mapping, localisation, path planning, trajectory generation and vehicle control.

The first development milestone, **V1.0.0**, establishes a complete autonomous navigation pipeline using **ROS 2 Jazzy**, **Gazebo Harmonic** and **Nav2**.

The vehicle operates within a simulated warehouse environment containing shelves and obstacles. It uses LiDAR sensing, localisation, global path planning and path-following control to navigate towards user-defined goals.

The long-term objective is to transfer the system to a physical RC vehicle, integrating onboard computing, sensors and embedded control hardware.

---

## Demonstrations

Screenshots and videos demonstrating the current system to follow.

---

## Features

### V1.0.0 — Autonomous Navigation Foundation

- **Ackermann steering:** Vehicle modelling and steering control using `ros2_control`.
- **Gazebo simulation:** Simulated warehouse environment with shelving and obstacles.
- **LiDAR integration:** LaserScan data for environmental perception.
- **Odometry:** Extended Kalman Filter (EKF) for vehicle state estimation.
- **Mapping:** Occupancy-grid mapping and saved maps.
- **Localisation:** Adaptive Monte Carlo Localisation (AMCL).
- **Global path planning:** Smac Hybrid-A* with Ackermann turning-radius constraints.
- **Path following:** Regulated Pure Pursuit (RPP) controller.
- **Navigation orchestration:** Nav2 Behaviour Tree Navigator with periodic replanning.
- **Costmaps:** Global and local costmap configurations with obstacle and inflation layers.
- **Visualisation:** RViz for monitoring localisation, sensor data, planned paths and costmaps.

---

## Technologies

<table>
  <tr>
    <th colspan="2">Technologies Used</th>
  </tr>
  <tr><td>ROS 2 Jazzy</td><td>Gazebo Harmonic</td></tr>
  <tr><td>Nav2</td><td>ros2_control</td></tr>
  <tr><td>SLAM Toolbox</td><td>AMCL</td></tr>
  <tr><td>robot_localization</td><td>Python</td></tr>
  <tr><td>C++</td><td></td></tr>
</table>

## ROS 2 Packages

The project is organised into modular ROS 2 packages, each responsible for a specific part of the autonomous navigation system.

| Package | Description |
|---------|-------------|
| `racecar_description` | Defines the vehicle's URDF model, joints, geometry and coordinate frames. |
| `racecar_gazebo` | Provides the Gazebo simulation environment, vehicle spawning and simulated sensors. |
| `racecar_control` | Configures Ackermann steering, wheel control and the velocity command interface. |
| `racecar_localisation` | Provides mapping, EKF-based odometry and AMCL localisation. |
| `racecar_planner` | Configures the Nav2 Planner Server, Smac Hybrid-A* and global costmap. |
| `racecar_motion_controller` | Configures the Nav2 Controller Server, Regulated Pure Pursuit and local costmap. |
| `racecar_navigation` | Coordinates autonomous goal execution, global planning, path following and periodic replanning using Nav2 behaviour trees. |
| `racecar_bringup` | Provides the launch configuration for starting the integrated autonomous navigation system. |

---

## Navigation Architecture

The autonomous navigation system uses Nav2 to coordinate localisation, global planning and vehicle control.

### Localisation

The vehicle estimates its position using:

- Wheel odometry and an Extended Kalman Filter.
- LiDAR measurements.
- AMCL localisation against a previously generated occupancy-grid map.

### Global Path Planning

The **Smac Hybrid-A*** planner generates paths through the warehouse environment.

Unlike conventional grid-based planning, Hybrid-A* considers the vehicle's orientation and minimum turning radius, making it suitable for Ackermann-steered vehicles.

The global costmap represents the environment using static map information, obstacle observations and inflation layers.

### Motion Control

The **Regulated Pure Pursuit** controller generates velocity commands to follow the planned path.

The controller adjusts its behaviour based on path curvature and can perform collision checks using the local costmap.

These commands are forwarded to the vehicle's Ackermann steering controller through a velocity-command bridge.

### Navigation Orchestration

The **Nav2 Behaviour Tree Navigator** coordinates the navigation process.

The behaviour tree manages:

1. Global path calculation.
2. Path execution.
3. Periodic replanning.

This provides a modular foundation for future navigation behaviours and recovery strategies.

---

## Getting Started

### Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Nav2
- ros2_control
- robot_localization
- SLAM Toolbox

### Installation

Detailed dependency installation, workspace build and launch instructions will be added.
### Running the Simulation

Clone the repository into the `src` directory of a ROS 2 workspace.

From the workspace root, build the packages:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

Launch the complete simulation and autonomous navigation system:

```bash
ros2 launch racecar_bringup racecar_bringup.launch.py
```

This launches the integrated racecar simulation, including Gazebo, vehicle control, localisation, Nav2 and RViz.
---

## Known Limitations

V1.0.0 establishes the autonomous navigation foundation but is not intended to provide fully robust obstacle avoidance.

Current limitations include:

- Avoidance of newly introduced obstacles is not yet reliable.
- Global planning currently uses a forward-only Dubins motion model.
- Reverse manoeuvres are not enabled.
- Navigation may fail in constrained environments or when the vehicle cannot make sufficient progress.

These limitations provide a starting point for future development.

---

## Roadmap

### V1.0.0 — Autonomous Navigation Foundation

**Status: Complete**

Establish a modular ROS 2 autonomous navigation system capable of localisation, global path planning and autonomous goal execution in simulation.

### V2.0.0 — Robust Autonomous Navigation

**Status: Planned**

Potential development areas:

- Investigate custom path-planning algorithms, including A* and D* Lite.
- Improve navigation performance around dynamic and unexpected obstacles.

## Acknowledgements

This project is partially based on the original MIT RACECAR project, with components adapted and developed for ROS 2 Jazzy and Gazebo Harmonic.

---

<p align="center">
  <a href="#autonomous-racecar">Back to top</a>
</p>
