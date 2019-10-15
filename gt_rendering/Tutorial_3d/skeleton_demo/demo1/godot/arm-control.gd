
extends Spatial

# member variables here, example:
# var a=2
# var b="textvar"
var upperarm_angle = Vector3()
var lowerarm_angle = Vector3()
var skel

func _ready():
	skel = get_node("arm/Armature/Skeleton")
	set_process(true)
var bone = "upperarm"
var coordinate = 0
func set_bone_rot(bone, ang):
	var b = skel.find_bone(bone)
	var rest = skel.get_bone_rest(b)
	var newpose = rest.rotated(Vector3(1.0, 0.0, 0.0), ang.x)
	var newpose = newpose.rotated(Vector3(0.0, 1.0, 0.0), ang.y)
	var newpose = newpose.rotated(Vector3(0.0, 0.0, 1.0), ang.z)
	skel.set_bone_pose(b, newpose)

func _process(dt):
	if Input.is_action_pressed("select_x"):
		coordinate = 0
	elif Input.is_action_pressed("select_y"):
		coordinate = 1
	elif Input.is_action_pressed("select_z"):
		coordinate = 2
	elif Input.is_action_pressed("select_upperarm"):
		bone = "upperarm"
	elif Input.is_action_pressed("select_lowerarm"):
		bone = "lowerarm"
	elif Input.is_action_pressed("increment"):
		if bone == "lowerarm":
			lowerarm_angle[coordinate] += 1
		elif bone == "upperarm":
			upperarm_angle[coordinate] += 1
	elif Input.is_action_pressed("decrement"):
		if bone == "lowerarm":
			lowerarm_angle[coordinate] -= 1
		elif bone == "upperarm":
			upperarm_angle[coordinate] -= 1
	set_bone_rot("lowerarm", lowerarm_angle)
	set_bone_rot("upperarm", upperarm_angle)
	