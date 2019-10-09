scriptTitle = "LibreOffice Impress"
scriptDescription = "Control Impress presentations"

def onPoseEdge(pose, edge):
	# the next IF will be true for any LibreOffice product
	if myo.title_contains("LibreOffice"): 
		if (edge == "on"): # only check for new poses
			if (myo.getPoseSide() == "waveRight"): # next slide
				myo.keyboard("right_arrow","press","")
			if (myo.getPoseSide() == "waveLeft"): # prev slide
				myo.keyboard("left_arrow","press","")
		if pose == "doubleTap":
			myo.setLockingPolicy("standard")
			myo.unlock("timed")


