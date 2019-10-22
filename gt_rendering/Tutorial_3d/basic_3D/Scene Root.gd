extends Spatial
var Armature

func _ready():
    Armature = get_node("Armature")
    var count = Armature.get_bone_count()
    print("bone count:", count)

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
#func _ready():
#	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
