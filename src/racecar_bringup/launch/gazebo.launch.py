from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
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
    default_world = PathJoinSubstitution(
        [racecar_gazebo_dir, "worlds", "warehouse.sdf"]
    )
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
    camera_pose = """
    pose {
      position {
        x: -0.87632280588150024
        y: 0.082298040390014648
        z: 1.0596097707748413
      }
      orientation {
        x: 0
        y: 0.24740396440029144
        z: 0
        w: 0.96891242265701294
      }
    }
    """

    camera_command = (
        "for attempt in $(seq 1 60); do "
        "if gz service -l | grep -Fxq '/gui/move_to/pose'; then "
        "break; "
        "fi; "
        "sleep 0.5; "
        "done; "
        "if ! gz service -l | grep -Fxq '/gui/move_to/pose'; then "
        "echo 'Gazebo camera service unavailable'; "
        "exit 1; "
        "fi; "
        "for attempt in $(seq 1 5); do "
        "if gz service -s /gui/move_to/pose "
        "--reqtype gz.msgs.GUICamera "
        "--reptype gz.msgs.Boolean "
        "--timeout 5000 "
        f"--req '{camera_pose}' | grep -q 'data: true'; then "
        "echo 'Gazebo camera positioned successfully'; "
        "exit 0; "
        "fi; "
        "sleep 1; "
        "done; "
        "echo 'Failed to position Gazebo camera'; "
        "exit 1"
    )

    set_camera = ExecuteProcess(
        cmd=["bash", "-c", camera_command],
        output="screen",
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
    ld.add_action(set_camera)
    ld.add_action(spawn_entity)
    ld.add_action(ros_gz_bridge)

    return ld
