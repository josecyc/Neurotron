#! /usr/bin/env python3
import sys, time, os
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
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
        print ('frame available')
        frame = controller.frame()
        print ("Frame id: {}, timestamp: {}, hands: {}, fingers: {}".format(frame.id, 
            frame.timestamp, len(frame.hands), len(frame.fingers)))
        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"
            arm = hand.arm
            print(handType)
            print('palm_position: {}'.format(hand.palm_position))

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
        print('Exiting...')
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
