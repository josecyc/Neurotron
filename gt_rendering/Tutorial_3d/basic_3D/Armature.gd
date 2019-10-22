extends Skeleton
var armature

func _ready():
    skel = get_node("skel")
    var count = skel.get_bone_count()
    print("bone count:", count)

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
