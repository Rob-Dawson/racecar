from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Package directories
    racecar_bringup_dir = FindPackageShare("racecar_bringup")
    racecar_control_dir = FindPackageShare("racecar_control")
    racecar_state_estimation_dir = FindPackageShare("racecar_state_estimation")
    racecar_mapping_dir = FindPackageShare("racecar_mapping")
    racecar_localisation_dir = FindPackageShare("racecar_localisation")
    racecar_planner_dir = FindPackageShare("racecar_planner")
    racecar_motion_controller_dir = FindPackageShare("racecar_motion_controller")
    racecar_navigation_dir = FindPackageShare("racecar_navigation")

    # Launch arguments
    environment_arg = DeclareLaunchArgument(
        "environment",
        default_value="gazebo",
        description="Select the execution environment",
    )

    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz2",
    )

    environment = LaunchConfiguration("environment")
    use_rviz = LaunchConfiguration("use_rviz")

    # Environment conditions
    is_gazebo = IfCondition(PythonExpression(["'", environment, "' == 'gazebo'"]))

    sim_mode = PythonExpression(["'true' if '", environment, "' == 'gazebo' else 'false'"])

    # Robot description
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_bringup_dir, "launch", "rsp.launch.py"])
        ),
        launch_arguments={
            "sim_mode": sim_mode,
        }.items(),
    )

    # Gazebo simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_bringup_dir, "launch", "gazebo.launch.py"])
        ),
        condition=is_gazebo,
    )

    # RViz visualisation
    rviz_config = PathJoinSubstitution([racecar_bringup_dir, "rviz", "display.rviz"])

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config],
        output="screen",
        condition=IfCondition(use_rviz),
    )

    # Racecar control
    racecar_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_control_dir, "launch", "racecar_control.launch.py"])
        ),
        condition=is_gazebo,
    )

    # Racecar pose estimation
    racecar_state_estimation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [racecar_state_estimation_dir, "launch", "racecar_state_estimation.launch.py"]
            )
        )
    )

    # SLAM mapping
    racecar_mapping = IncludeLaunchDescription(  # noqa: F841
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_mapping_dir, "launch", "racecar_mapping.launch.py"])
        )
    )

    # Racecar localisation within a map
    racecar_localisation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [racecar_localisation_dir, "launch", "racecar_localisation.launch.py"]
            )
        )
    )

    # Racecar motion controller for Nav2
    racecar_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_navigation_dir, "launch", "racecar_navigation.launch.py"])
        )
    )

    # Racecar path planner
    racecar_planner = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([racecar_planner_dir, "launch", "racecar_planner.launch.py"])
        )
    )

    # Racecar motion controller for Nav2
    racecar_motion_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [racecar_motion_controller_dir, "launch", "racecar_motion_controller.launch.py"]
            )
        )
    )

    # Launch description
    ld = LaunchDescription()

    ld.add_action(environment_arg)
    ld.add_action(use_rviz_arg)

    ld.add_action(rsp)

    ld.add_action(gazebo)
    ld.add_action(rviz)

    ld.add_action(racecar_control)
    ld.add_action(racecar_state_estimation)

    # ld.add_action(racecar_mapping)

    ld.add_action(racecar_localisation)

    ld.add_action(racecar_navigation)
    ld.add_action(racecar_planner)
    ld.add_action(racecar_motion_controller)

    return ld
