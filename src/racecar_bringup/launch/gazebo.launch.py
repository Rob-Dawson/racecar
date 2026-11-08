from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    racecar_gazebo_dir = FindPackageShare("racecar_gazebo")
    default_world = PathJoinSubstitution([racecar_gazebo_dir, "worlds", "empty.sdf"])
    racecar_gazebo_share = FindPackageShare("racecar_description")

    gz_resource_path = PathJoinSubstitution(
        [
            racecar_gazebo_share,
            "..",
        ]
    )
    world_arg = DeclareLaunchArgument(
        "world", default_value=default_world, description="World to load"
    )

    world = LaunchConfiguration("world")

    gz_args = ["-r -v 4 ", world]
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={
            "gz_args": gz_args,
            "on_exit_shutdown": "true",
        }.items(),
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "/robot_description", "-name", "racecar", "-z", "0.1"],
        output="screen",
    )

    bridge_params = PathJoinSubstitution(
        [
            racecar_gazebo_dir,
            "config",
            "gz_bridge.yaml",
        ]
    )

    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{"config_file": bridge_params}],
        output="screen",
    )
    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            gz_resource_path,
            ":",
            EnvironmentVariable("GZ_SIM_RESOURCE_PATH", default_value=""),
        ],
    )
    ld = LaunchDescription()
    ld.add_action(world_arg)
    ld.add_action(gazebo_resource_path)
    ld.add_action(gazebo)
    ld.add_action(spawn_entity)
    ld.add_action(ros_gz_bridge)

    return ld
