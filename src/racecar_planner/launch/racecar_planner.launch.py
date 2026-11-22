from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    lifecycle_nodes = ["planner_server"]
    planner_dir = FindPackageShare("racecar_planner")

    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="true")

    planner_config_arg = DeclareLaunchArgument(
        "planner_config",
        default_value=PathJoinSubstitution([planner_dir, "config", "planner.yaml"]),
    )

    planner_config = LaunchConfiguration("planner_config")
    use_sim_time = LaunchConfiguration("use_sim_time")

    planner_server = Node(
        package="nav2_planner",
        executable="planner_server",
        name="planner_server",
        output="screen",
        parameters=[planner_config, {"use_sim_time": use_sim_time}],
    )

    nav2_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_planning",
        output="screen",
        parameters=[
            {"node_names": lifecycle_nodes},
            {"autostart": True},
            {"use_sim_time": use_sim_time},
        ],
    )

    ld = LaunchDescription()

    ld.add_action(use_sim_time_arg)
    ld.add_action(planner_config_arg)
    ld.add_action(planner_server)
    ld.add_action(nav2_lifecycle_manager)

    return ld
