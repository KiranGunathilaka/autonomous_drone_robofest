from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to SITL using UDP/TCP
print("Connecting to vehicle...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)

print("Connected successfully!")
print(f"Autopilot version: {vehicle.version}")
print(f"Vehicle mode: {vehicle.mode}")

print("Setting parameters to allow arming without GPS/IMU checks...")
vehicle.parameters['ARMING_CHECK'] = 0

# Arm and take off
def arm_and_takeoff(aTargetAltitude):
    print("Setting parameters to allow arming without GPS/IMU checks...")
    vehicle.parameters['ARMING_CHECK'] = 0

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    # Wait until target altitude is reached
    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {alt:.2f} m")
        if alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Start mission
arm_and_takeoff(5)

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
time.sleep(10)

# Close connection
vehicle.close()
print("Mission complete")
