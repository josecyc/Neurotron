import dongleless
import time


def sample_rate(times=[]):
    # Measure the sample rate by dividing 20 by the length of time between
    # 20 function calls, average is 20-25/.5s which is 50 hz
    # it can improve to 200 hz with the Myo Bluetooth protocol
    #    times.append(time.time())
    #    if len(times) > 20:
    #        print((len(times) - 1) / (times[-1] - times[0]))
    #        times.pop(0)

def imu_data(myo, quat, accel, gyro):
    #print("imu_data:", quat)
    return

def emg_data(myo, emg):
    #sample_rate()
    print("emg_data:", emg)

if '__name__' == '__main__':


    function_dict = {
    "imu_data":imu_data, #printing these gets really crowded, uncomment them if you want to use them.
    "emg_data":emg_data
    }
    dongleless.run(function_dict)
