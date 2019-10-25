#typedef enum \{([^{]+?)\} myohw_(\w+)
#$2 : \{ $1 \}


### See myohw.h for more complete instructions on command structure, formats, etc.
 

services = {  #*********************chse - characteristic, service
    0x0001: "ControlService"                , #< Myo info service
    0x0101: "MyoInfoCharacteristic"         , #< Serial number for this Myo and various parameters which
                                            #< are specific to this firmware. Read-only attribute. 
                                            #< See myohw_fw_info_t.
    0x0201: "FirmwareVersionCharacteristic" , #< Current firmware version. Read-only characteristic.
                                            #< See myohw_fw_version_t.
    0x0401: "CommandCharacteristic"         , #< Issue commands to the Myo. Write-only characteristic.
                                            #< See myohw_command_t.

    0x0002: "ImuDataService"                , #< IMU service
    0x0402: "IMUDataCharacteristic"         , #< See myohw_imu_data_t. Notify-only characteristic. /*
    0x0a02: "MotionEventCharacteristic"     , #< Motion event data. Indicate-only characteristic. /*

    0x0003: "ClassifierService"             , #< Classifier event service.
    0x0103: "ClassifierEventCharacteristic" , #< Classifier event data. Indicate-only characteristic. See myohw_pose_t. /***

    0x0005: "EmgDataService"                , #< Raw EMG data service.
    0x0105: "EmgData Characteristic"        , #< Raw EMG data. Notify-only characteristic.
    0x0205: "EmgData Characteristic"        , #< Raw EMG data. Notify-only characteristic.
    0x0305: "EmgData Characteristic"        , #< Raw EMG data. Notify-only characteristic.
    0x0405: "EmgData Characteristic"        , #< Raw EMG data. Notify-only characteristic.
 }
pose = { 
    0x0000: "rest"           ,
    0x0001: "fist"           ,
    0x0002: "wave_in"        ,
    0x0003: "wave_out"       ,
    0x0004: "fingers_spread" ,
    0x0005: "double_tap"     ,
    0xffff: "unknown"        ,
    -1    : "unknown"        
 }
sku = { 
    0: "sku_unknown"   , #< Unknown SKU (default value for old firmwares)
    1: "sku_black_myo" , #< Black Myo
    2: "sku_white_myo"   #< White Myo
 }
hardware_rev = { 
    0: "hardware_rev_unknown" , #< Unknown hardware revision.
    1: "hardware_rev_revc"    , #< Myo Alpha (REV-C) hardware.
    2: "hardware_rev_revd"    , #< Myo (REV-D) hardware.
}
command = { 
    0x01: "command_set_mode"               , #< Set EMG and IMU modes. See myohw_command_set_mode_t.
    0x03: "command_vibrate"                , #< Vibrate. See myohw_command_vibrate_t.
    0x04: "command_deep_sleep"             , #< Put Myo into deep sleep. See myohw_command_deep_sleep_t.
    0x07: "command_vibrate2"               , #< Extended vibrate. See myohw_command_vibrate2_t.
    0x09: "command_set_sleep_mode"         , #< Set sleep mode. See myohw_command_set_sleep_mode_t.
    0x0a: "command_unlock"                 , #< Unlock Myo. See myohw_command_unlock_t.
    0x0b: "command_user_action"            , #< Notify user that an action has been recognized / confirmed.
                                                 #< See myohw_command_user_action_t.
 }
emg_mode = { 
    0x00: "emg_mode_none"         , #< Do not send EMG data.
    0x02: "emg_mode_send_emg"     , #< Send filtered EMG data.
    0x03: "emg_mode_send_emg_raw" , #< Send raw (unfiltered) EMG data.
 }
imu_mode = { 
    0x00: "imu_mode_none"        , #< Do not send IMU data or events.
    0x01: "imu_mode_send_data"   , #< Send IMU data streams (accelerometer, gyroscope, and orientation).
    0x02: "imu_mode_send_events" , #< Send motion events detected by the IMU (e.g. taps).
    0x03: "imu_mode_send_all"    , #< Send both IMU data streams and motion events.
    0x04: "imu_mode_send_raw"    , #< Send raw IMU data streams.
 }
classifier_mode = { 
    0x00: "classifier_mode_disabled" , #< Disable and reset the internal state of the onboard classifier.
    0x01: "classifier_mode_enabled"  , #< Send classifier events (poses and arm events).
 }
vibration_type = { 
    0x00: "none"   , #< Do not vibrate.
    0x01: "short"  , #< Vibrate for a short amount of time.
    0x02: "medium" , #< Vibrate for a medium amount of time.
    0x03: "long"   , #< Vibrate for a long amount of time.
 }
sleep_mode = { 
    0: "sleep_mode_normal"      , #< Normal sleep mode; Myo will sleep after a period of inactivity.
    1: "sleep_mode_never_sleep" , #< Never go to sleep.
 }
unlockype = { 
    0x00: "unlock_lock"  , #< Re-lock immediately.
    0x01: "unlock_timed" , #< Unlock now and re-lock after a fixed timeout.
    0x02: "unlock_hold"  , #< Unlock now and remain unlocked until a lock command is received.
 }
user_action_type = { 
    0: "user_action_single" , #< User did a single, discrete action, such as pausing a video.
 }
classifier_model_type = { 
    0: "classifier_model_builtin" , #< Model built into the classifier package.
    1: "classifier_model_custom"    #< Model based on personalized user data.
 }
motion_event_type = { 
    0x00: "motion_event_tap" ,
 }
classifier_event_type = { 
    0x01: "arm_synced"   ,
    0x02: "arm_unsynced" ,
    0x03: "pose"         ,
    0x04: "unlocked"     ,
    0x05: "locked"       ,
    0x06: "sync_failed"  ,
    0x07: "warmup_complete"
 }
arm = { 
    0x01: "arm_right"   ,
    0x02: "arm_left"    ,
    0xff: "arm_unknown" 
 }
x_direction = { 
    0x01: "x_direction_toward_wrist" ,
    0x02: "x_direction_toward_elbow" ,
    0xff: "x_direction_unknown"      
 }
sync_result = { 
    0x01: "sync_failed_too_hard" , #< Sync gesture was performed too hard.
 }
