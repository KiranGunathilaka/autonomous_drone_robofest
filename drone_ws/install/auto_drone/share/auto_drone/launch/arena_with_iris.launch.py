from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_path
import os

def generate_launch_description():
    pkg      = get_package_share_path('auto_drone')
    world    = os.path.join(str(pkg), 'worlds', 'arena.world')
    iris_sdf = os.path.join(str(pkg), 'models', 'iris_drone', 'model.sdf')
    models   = os.path.join(str(pkg), 'models')

    # --- Pose arguments (THIS is the "DeclareLaunchArgument(...)" section)
    x = DeclareLaunchArgument('x', default_value='17.75')
    y = DeclareLaunchArgument('y', default_value='-14.75')
    z = DeclareLaunchArgument('z', default_value='1.0')
    R = DeclareLaunchArgument('R', default_value='0.0')
    P = DeclareLaunchArgument('P', default_value='0.0')
    Y = DeclareLaunchArgument('Y', default_value='0.0')

    # --- Environment (plugins / models / resources / OGRE / SW rendering)
    ensure_plugin_path = SetEnvironmentVariable(
        name='GAZEBO_PLUGIN_PATH',
        value=os.environ.get('GAZEBO_PLUGIN_PATH', '') + ':/opt/ros/foxy/lib'
    )
    ensure_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=os.environ.get('GAZEBO_MODEL_PATH', '') + f':{models}:/usr/share/gazebo-11/models'
    )
    ensure_resource_path = SetEnvironmentVariable(
        name='GAZEBO_RESOURCE_PATH',
        value=os.environ.get('GAZEBO_RESOURCE_PATH', '') + f':/usr/share/gazebo-11:{str(pkg)}:{models}'
    )
    ensure_ogre_path = SetEnvironmentVariable(
        name='OGRE_RESOURCE_PATH',
        value=os.environ.get('OGRE_RESOURCE_PATH', '') +
              ':/usr/lib/x86_64-linux-gnu/OGRE-1.9.0:/usr/lib/x86_64-linux-gnu/OGRE-1.12.9'
    )
    # avoid gzclient GPU issues in Docker
    sw_gl = SetEnvironmentVariable(name='LIBGL_ALWAYS_SOFTWARE', value='1')

    gzserver = ExecuteProcess(
        cmd=[
            'gzserver', '--verbose',
            '-s', '/opt/ros/foxy/lib/libgazebo_ros_init.so',
            '-s', '/opt/ros/foxy/lib/libgazebo_ros_factory.so',
            world
        ],
        output='screen'
    )

    # GUI (for headless, comment out)
    gzclient = ExecuteProcess(cmd=['gzclient'], output='screen')

    spawn_iris = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_iris',
        arguments=[
            '-entity', 'iris_demo',
            '-file', iris_sdf,
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
            '-R', LaunchConfiguration('R'),
            '-P', LaunchConfiguration('P'),
            '-Y', LaunchConfiguration('Y'),
        ],
        output='screen'
    )

    return LaunchDescription([
        # Put arguments first so they’re declared before nodes use them
        x, y, z, R, P, Y,
        # Then environment
        ensure_plugin_path, ensure_model_path, ensure_resource_path, ensure_ogre_path, sw_gl,
        # Processes
        gzserver, gzclient, spawn_iris
    ])
