import dongleless
import time

def rest(myo):
    print("rest")

def fist(myo):
    print("fist")

def wave_in(myo):
    print("wave_in")

def wave_out(myo):
    print("wave_out")

def wave_left(myo):
    print("wave_left")

def wave_right(myo):
    print("wave_right")

def fingers_spread(myo):
    print("fingers_spread")

def double_tap(myo):
    print("double_tap")

def unknown(myo):
    print("unknown")

def arm_synced(myo, x_dir, arm):
    print("arm_synced")

def arm_unsynced(myo):
    print("arm_unsynced")

def imu_data(myo, quat, accel, gyro):
    #print("imu_data:", quat)
    return

def emg_data(myo, emg, times=[]):
#    times.append(time.time())

#    if len(times) > 20:
#        print((len(times) - 1) / (times[-1] - times[0]))
#        times.pop(0)
    print("emg_data:", emg)



function_dict = {
#"rest":rest,
#"fist":fist,
#"wave_in":wave_in,
#"wave_out":wave_out,
#"wave_left":wave_left,
#"wave_right":wave_right,
#"fingers_spread":fingers_spread,
#"double_tap":double_tap,
#"unknown":unknown,
#"arm_synced":arm_synced,
#"arm_unsynced":arm_unsynced,
"imu_data":imu_data, #printing these gets really crowded, uncomment them if you want to use them.
"emg_data":emg_data
}

dongleless.run(function_dict)
