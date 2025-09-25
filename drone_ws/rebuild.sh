#!/usr/bin/env bash
# clean + build + source for ROS2 Foxy colcon workspace

set -euo pipefail

# 1) Clean
rm -rf build/ install/ log/

# 2) Source ROS Foxy (disable -u so unbound vars don't break)
set +u
source /opt/ros/foxy/setup.bash
set -u

# 3) Build
colcon build --symlink-install

# 4) Source your local workspace
source install/setup.bash

echo "✅ Done."
