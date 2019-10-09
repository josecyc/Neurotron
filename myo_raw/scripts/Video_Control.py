scriptTitle = "Video Control"
scriptDescription = "A simple script to control video players"

def onPoseEdge(pose, edge):
	# active at all times
	if (pose == "waveOut"):
		if (edge == "on"): 
			myo.keyboard("right_arrow","down","")
			myo.unlock("hold")
		if (edge == "off"): 
			myo.keyboard("right_arrow","up","")
			myo.unlock("timed")			
	if (pose == "waveIn"):
		if (edge == "on"): 
			myo.keyboard("left_arrow","down","")
			myo.unlock("hold")
		if (edge == "off"): 
			myo.keyboard("left_arrow","up","")
			myo.unlock("timed")			
	if (pose == "fist") and (edge == "on"): 
		myo.keyboard("space","press","")



