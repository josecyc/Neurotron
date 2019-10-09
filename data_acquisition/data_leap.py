import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
import pandas as pd
import time

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'];
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    columns = ["Unix Time", "Timestamp", "Palm x", "Palm y", "Palm z", "Wrist x", "Wrist y", "Wrist z",
            "Thumb Proximal x", "Thumb Proximal y", "Thumb Proximal z",
            "Thumb Intermediate x", "Thumb Intermediate y", "Thumb Intermediate z",
            "Thumb Distal x", "Thumb Distal y", "Thumb Distal z",
            "Thumb Tip x", "Thumb Tip y", "Thumb Tip z",
            "Index Proximal x", "Index Proximal y", "Index Proximal z",
            "Index Intermediate x", "Index Intermediate y", "Index Intermediate z",
            "Index Distal x", "Index Distal y", "Index Distal z",
            "Index Tip x", "Index Tip y", "Index Tip z",
            "Middle Proximal x", "Middle Proximal y", "Middle Proximal z",
            "Middle Intermediate x", "Middle Intermediate y", "Middle Intermediate z",
            "Middle Distal x", "Middle Distal y", "Middle Distal z",
            "Middle Tip x", "Middle Tip y", "Middle Tip z",
            "Ring Proximal x", "Ring Proximal y", "Ring Proximal z",
            "Ring Intermediate x", "Ring Intermediate y", "Ring Intermediate z",
            "Ring Distal x", "Ring Distal y", "Ring Distal z",
            "Ring Tip x", "Ring Tip y", "Ring Tip z",
            "Pinky Proximal x", "Pinky Proximal y", "Pinky Proximal z",
            "Pinky Intermediate x", "Pinky Intermediate y", "Pinky Intermediate z",
            "Pinky Distal x", "Pinky Distal y", "Pinky Distal z",
            "Pinky Tip x", "Pinky Tip y", "Pinky Tip z"]
    data = np.zeros((7000, 68))
    i = 0

    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Motion Sensor Connected")
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print ("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
	frame = controller.frame()
	"""print ("Frame ID: " + str(frame.id) \
		+ " Timestamp: " + str(frame.timestamp) \
		+ " # of Hands " + str(len(frame.hands)) \
		+ " # of Fingers " + str(len(frame.fingers)) \
		+ " # of Tools " + str(len(frame.tools)) \
		+ " # of Gestures " + str(len(frame.gestures())))"""

        for hand in frame.hands:
            """handType = "Left Hand" if hand.is_left else "Right Hand"
            print ("{} Hand ID: {} Palm Position {}".format(handType, str(hand.id), str(hand.palm_position)))
            normal = hand.palm_normal
            direction = hand.direction
            print ("Pitch: {} Roll: {} Yaw: {}".format(str(direction.pitch * Leap.RAD_TO_DEG), str(normal.roll * Leap.RAD_TO_DEG), str(direction.yaw * Leap.RAD_TO_DEG)))

            print ("Arm Direction: {} Wrist Position: {} Elbow Position {}".format(str(arm.direction), str(arm.wrist_position), str(arm.elbow_position)))"""

            
            handType = "Left Hand" if hand.is_left else "Right Hand"
            arm = hand.arm
            #print
            #print ("Timestamp: {} Unix time {}".format(frame.timestamp, time.time()))
            #print ("{} Hand ID: {} Palm Position {}".format(handType, hand.id, hand.palm_position))
            #print ("Wrist Position: {} Relative: {}".format(arm.wrist_position, arm.wrist_position - hand.palm_position))
            wrist_rel = arm.wrist_position - hand.palm_position
            thumb_proximal_rel = hand.fingers[0].bone(1).prev_joint - hand.palm_position
            thumb_intermediate_rel = hand.fingers[0].bone(2).prev_joint - hand.palm_position
            thumb_distal_rel = hand.fingers[0].bone(3).prev_joint - hand.palm_position
            thumb_tip_rel = hand.fingers[0].bone(3).next_joint - hand.palm_position
            index_proximal_rel = hand.fingers[1].bone(1).prev_joint - hand.palm_position
            index_intermediate_rel = hand.fingers[1].bone(2).prev_joint - hand.palm_position
            index_distal_rel = hand.fingers[1].bone(3).prev_joint - hand.palm_position
            index_tip_rel = hand.fingers[1].bone(3).next_joint - hand.palm_position
            middle_proximal_rel = hand.fingers[2].bone(1).prev_joint - hand.palm_position
            middle_intermediate_rel = hand.fingers[2].bone(2).prev_joint - hand.palm_position
            middle_distal_rel = hand.fingers[2].bone(3).prev_joint - hand.palm_position
            middle_tip_rel = hand.fingers[2].bone(3).next_joint - hand.palm_position
            ring_proximal_rel = hand.fingers[3].bone(1).prev_joint - hand.palm_position
            ring_intermediate_rel = hand.fingers[3].bone(2).prev_joint - hand.palm_position
            ring_distal_rel = hand.fingers[3].bone(3).prev_joint - hand.palm_position
            ring_tip_rel = hand.fingers[3].bone(3).next_joint - hand.palm_position
            pinky_proximal_rel = hand.fingers[4].bone(1).prev_joint - hand.palm_position
            pinky_intermediate_rel = hand.fingers[4].bone(2).prev_joint - hand.palm_position
            pinky_distal_rel = hand.fingers[4].bone(3).prev_joint - hand.palm_position
            pinky_tip_rel = hand.fingers[4].bone(3).next_joint - hand.palm_position
            self.data[self.i] = np.array([time.time(), frame.timestamp,
                hand.palm_position[0], hand.palm_position[1], hand.palm_position[2],
                wrist_rel[0], wrist_rel[1], wrist_rel[2],
                thumb_proximal_rel[0], thumb_proximal_rel[1], thumb_proximal_rel[2],
                thumb_intermediate_rel[0], thumb_intermediate_rel[1], thumb_intermediate_rel[2],
                thumb_distal_rel[0], thumb_distal_rel[1], thumb_distal_rel[2],
                thumb_tip_rel[0], thumb_tip_rel[1], thumb_tip_rel[2],
                index_proximal_rel[0], index_proximal_rel[1], index_proximal_rel[2],
                index_intermediate_rel[0], index_intermediate_rel[1], index_intermediate_rel[2],
                index_distal_rel[0], index_distal_rel[1], index_distal_rel[2],
                index_tip_rel[0], index_tip_rel[1], index_tip_rel[2],
                middle_proximal_rel[0], middle_proximal_rel[1], middle_proximal_rel[2],
                middle_intermediate_rel[0], middle_intermediate_rel[1], middle_intermediate_rel[2],
                middle_distal_rel[0], middle_distal_rel[1], middle_distal_rel[2],
                middle_tip_rel[0], middle_tip_rel[1], middle_tip_rel[2],
                ring_proximal_rel[0], ring_proximal_rel[1], ring_proximal_rel[2],
                ring_intermediate_rel[0], ring_intermediate_rel[1], ring_intermediate_rel[2],
                ring_distal_rel[0], ring_distal_rel[1], ring_distal_rel[2],
                ring_tip_rel[0], ring_tip_rel[1], ring_tip_rel[2],
                pinky_proximal_rel[0], pinky_proximal_rel[1], pinky_proximal_rel[2],
                pinky_intermediate_rel[0], pinky_intermediate_rel[1], pinky_intermediate_rel[2],
                pinky_distal_rel[0], pinky_distal_rel[1], pinky_distal_rel[2],
                pinky_tip_rel[0], pinky_tip_rel[1], pinky_tip_rel[2]])
            self.i += 1
            #print ("Updated stats i = {}".format(self.i))
            #for finger in hand.fingers:
            #    print ("Type: {} ID: {} Length (mm): {} Width (mm): {}".format(self.finger_names[finger.type], str(finger.id), str(finger.length), str(finger.width)))
                #print ("--------------------------------------------------------------------------")
                #print ("{} Finger - ID: {}".format(self.finger_names[finger.type], finger.id))
                #for b in range(1, 4):
                    #bone = finger.bone(b)
                    #print ("{}: {} Relative: {}".format(self.bone_names[bone.type], bone.prev_joint, bone.prev_joint - hand.palm_position))
                    #if (b == 3):
                        #print ("Tip: {} Relative {}".format(bone.next_joint, bone.next_joint - hand.palm_position))


def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print ("Press enter to quit")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        print ("Data dump:")
        print (listener.data)
        df = pd.DataFrame(data=listener.data, columns=listener.columns)
        df.to_csv("test.csv", index=False)
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
