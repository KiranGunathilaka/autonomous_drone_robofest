cmake_minimum_required(VERSION 3.5)
project(auto_drone)

# C standards
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# --- Install assets ---
install(DIRECTORY worlds DESTINATION share/${PROJECT_NAME})
install(DIRECTORY models DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(FILES
  package.xml
  DESTINATION share/${PROJECT_NAME}/
)

# Python nodes
# install(PROGRAMS scripts/my_node.py DESTINATION lib/${PROJECT_NAME})

# --- Env hook so model:// resolves inside this package ---
ament_environment_hooks(env_hooks/gazebo_model_path.dsv)

# Lint/testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
