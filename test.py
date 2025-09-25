from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to SITL (default: ArduCopter on localhost:14550)
print("Connecting to vehicle...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)
print("Connected successfully!")

# Function to arm and takeoff
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to target altitude with GPS + EKF checks.
    """

    print("Performing basic pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    while vehicle.gps_0.fix_type < 3:
        print(" Waiting for GPS fix... (Current: %s)" % vehicle.gps_0.fix_type)
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Takeoff to target altitude

    # Wait until target altitude is reached
    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {alt:.2f} m")
        if abs(alt - aTargetAltitude) <= 0.5:
            print("Reached target altitude (within tolerance)")
            break
        time.sleep(1)

# 🚀 Start mission
arm_and_takeoff(3)


target = LocationGlobalRelative(vehicle.location.global_frame.lat,vehicle.location.global_frame.lon, 5)
vehicle.simple_goto(target)
time.sleep(10)

# Fly to waypoints
point1 = LocationGlobalRelative(-35.363261, 149.165230, 5)
print("Flying to point 1...")
vehicle.simple_goto(point1)
time.sleep(10)

point2 = LocationGlobalRelative(-35.364000, 149.166000, 5)
print("Flying to point 2...")
vehicle.simple_goto(point2)
time.sleep(10)

# Return to Launch
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Wait until landed
while vehicle.armed:
    print(" Waiting for landing...")
    time.sleep(2)

# Close connection
print("Mission complete")
vehicle.close()
