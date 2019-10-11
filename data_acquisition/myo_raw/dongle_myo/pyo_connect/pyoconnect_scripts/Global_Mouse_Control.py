
def onUnlock():
	myo.rotSetCenter()
	myo.unlock("hold")
	
def onPoseEdge(pose, edge):
	if (pose == 'fist') and (edge == "on"): 
		myo.mouse("left","click","")
	if (pose == 'fingersSpread') and (edge == "on"):
		myo.mouse("right","click","")


def onPeriodic():
	if myo.isUnlocked():
		myo.mouseMove(600+myo.rotYaw()*2000, 500-myo.rotPitch()*2000)



