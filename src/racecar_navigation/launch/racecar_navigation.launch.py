from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    lifecycle_nodes = ["bt_navigator"]

    navigation_dir = FindPackageShare("racecar_navigation")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
    )

    navigator_config_arg = DeclareLaunchArgument(
        "navigator_config",
        default_value=PathJoinSubstitution([navigation_dir, "config", "navigator.yaml"]),
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    navigator_config = LaunchConfiguration("navigator_config")
    behavior_tree = PathJoinSubstitution(
        [
            navigation_dir,
            "behavior_trees",
            "navigate_to_pose.xml",
        ]
    )
    bt_navigator = Node(
        package="nav2_bt_navigator",
        executable="bt_navigator",
        name="bt_navigator",
        output="screen",
        parameters=[
            navigator_config,
            {
                "use_sim_time": use_sim_time,
                "default_nav_to_pose_bt_xml": behavior_tree,
            },
        ],
    )

    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_navigation",
        output="screen",
        parameters=[
            {
                "node_names": lifecycle_nodes,
                "autostart": True,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    ld = LaunchDescription()

    ld.add_action(use_sim_time_arg)
    ld.add_action(navigator_config_arg)
    ld.add_action(bt_navigator)
    ld.add_action(lifecycle_manager)

    return ld
