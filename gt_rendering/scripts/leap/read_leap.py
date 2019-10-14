#! /usr/bin/env python3
import sys, time, os
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
import pandas as pd
import argparse

class LeapMotionListener(Leap.Listener):
	data = []
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

	def on_init(self, controller):
		print ("Leap : Initialized")

	def on_connect(self, controller):
		print ("Leap : Motion Sensor Connected")
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print ("Leap : Motion Sensor Disconnected")

	def on_exit(self, controller):
		print ("Leap : Exited")

	def on_frame(self, controller):
		frame = controller.frame()
		print ("Frame id: {}, timestamp: {}, hands: {}, fingers: {}".format(frame.id, 
			frame.timestamp, len(frame.hands), len(frame.fingers)))
		for hand in frame.hands:
			if hand.is_right:
				handType = "Left Hand" if hand.is_left else "Right Hand"
				arm = hand.arm
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
				self.data.append(np.array([time.time(), frame.timestamp,
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
					pinky_tip_rel[0], pinky_tip_rel[1], pinky_tip_rel[2]]))
				print(handType)
				print('palm_position: {}'.format(hand.palm_position))
				print('fingertips: {} {} {} {} {}'.format(thumb_tip_rel, index_tip_rel, middle_tip_rel, ring_tip_rel, pinky_tip_rel))

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('name')
	parser.add_argument('nbr')
	return parser.parse_args()

def main():
	args = parse()
	listener = LeapMotionListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	print ("Leap - Press enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		sys.stdout.flush()
		print('Leap - Exiting...')
		print ("Data dump: {} points".format(len(listener.data)))
		df = pd.DataFrame(data=listener.data, columns=listener.columns)
		df.to_csv("leap_data_{}_{}.csv".format(args.name, args.nbr), index=False)
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()
