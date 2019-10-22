extends Spatial
#extends Label

var socket = PacketPeerUDP.new()
var status = socket.listen(4242, "127.0.0.1")

func set_bone(origin, target, bone_):
	#$wrist_b.scale = Vector3($wrist_b.scale.x, $thumb_p.translation.distance_to($wrist.translation), $wrist_b.scale.z)
	#$wrist_b.translation = $thumb_p.translation + .5*($wrist.translation - $thumb_p.translation)
	print('scale:', bone_.scale)
	print('get scale:', bone_.get_scale())
	#bone_.set_scale(Vector3(bone_.scale.y, 20*target.translation.distance_to(origin.translation), bone_.scale.z))
	
	#bone_.set_scale(Vector3(20*target.translation.distance_to(origin.translation), 1, 1))
	print('scale:', bone_.scale)
	bone_.translation = target.translation + .5*(origin.translation - target.translation)
	#print(bone_.get_transform())
	bone_.look_at(target.translation, Vector3(0,1,0))
	bone_.set_scale(Vector3(1, 1, target.translation.distance_to(origin.translation)*.5))
	#bone_.look_at($thumb_p.translation, Vector3(1,0,0))
	#bone_.look_at($thumb_p.translation, Vector3(0,0,1))

func _process(delta):
	if status != OK:
		print("An error occurred listening on port 4242")
	if socket.get_available_packet_count() > 0:
		var data_parse = JSON.parse(socket.get_packet().get_string_from_ascii())
		if data_parse.error != OK:
			print("Error parsing JSON: Error " + str(data_parse.get_error()))
		else:
			var result = data_parse.get_result()
			if result["exit"] == 1:
				socket.close()
				get_tree().quit()
			else:
#				print(result["a"])
#				var pos = $Joint.translation
#				print(pos)
#				var vec = Vector3(result["a"][0], result["a"][1], result["a"][2])
#				$Joint.translation = vec
#				print($Joint.translation)
				$wrist.translation = Vector3(result["wrist"][0], result["wrist"][1], result["wrist"][2])
				
				#Thumb
				$thumb_p.translation = Vector3(result["thumb_p"][0], result["thumb_p"][1], result["thumb_p"][2])
				set_bone($wrist, $thumb_p, $thumb_p_b) 
				$thumb_i.translation = Vector3(result["thumb_i"][0], result["thumb_i"][1], result["thumb_i"][2])
				set_bone($thumb_p, $thumb_i, $thumb_i_b)
				$thumb_d.translation = Vector3(result["thumb_d"][0], result["thumb_d"][1], result["thumb_d"][2])
				set_bone($thumb_i, $thumb_d, $thumb_d_b)
				$thumb_t.translation = Vector3(result["thumb_t"][0], result["thumb_t"][1], result["thumb_t"][2])
				set_bone($thumb_d, $thumb_t, $thumb_t_b)
				
				#Index finger
				$index_p.translation = Vector3(result["index_p"][0], result["index_p"][1], result["index_p"][2])
				set_bone($thumb_p, $index_p, $index_p_b)
				set_bone($index_p, $middle_p, $index_p_m_b)
				$index_i.translation = Vector3(result["index_i"][0], result["index_i"][1], result["index_i"][2])
				set_bone($index_p, $index_i, $index_i_b)
				$index_d.translation = Vector3(result["index_d"][0], result["index_d"][1], result["index_d"][2])
				set_bone($index_i, $index_d, $index_d_b)
				$index_t.translation = Vector3(result["index_t"][0], result["index_t"][1], result["index_t"][2])
				set_bone($index_d, $index_t, $index_t_b)
				
				#Middle finger
				$middle_p.translation = Vector3(result["middle_p"][0], result["middle_p"][1], result["middle_p"][2])
				set_bone($middle_p, $ring_p, $middle_p_b)
				$middle_i.translation = Vector3(result["middle_i"][0], result["middle_i"][1], result["middle_i"][2])
				set_bone($middle_p, $middle_i, $middle_i_b)
				$middle_d.translation = Vector3(result["middle_d"][0], result["middle_d"][1], result["middle_d"][2])
				set_bone($middle_i, $middle_d, $middle_d_b)
				$middle_t.translation = Vector3(result["middle_t"][0], result["middle_t"][1], result["middle_t"][2])
				set_bone($middle_d, $middle_t, $middle_t_b)
				
				#Ring finger
				$ring_p.translation = Vector3(result["ring_p"][0], result["ring_p"][1], result["ring_p"][2])
				set_bone($ring_p, $pinky_p, $ring_p_b)
				$ring_i.translation = Vector3(result["ring_i"][0], result["ring_i"][1], result["ring_i"][2])
				set_bone($ring_p, $ring_i, $ring_i_p)
				$ring_d.translation = Vector3(result["ring_d"][0], result["ring_d"][1], result["ring_d"][2])
				set_bone($ring_i, $ring_d, $ring_d_b)
				$ring_t.translation = Vector3(result["ring_t"][0], result["ring_t"][1], result["ring_t"][2])
				set_bone($ring_d, $ring_t, $ring_t_b)
				
				#Pinky finger
				$pinky_p.translation = Vector3(result["pinky_p"][0], result["pinky_p"][1], result["pinky_p"][2])
				set_bone($wrist, $pinky_p, $pinky_p_b)
				$pinky_i.translation = Vector3(result["pinky_i"][0], result["pinky_i"][1], result["pinky_i"][2])
				set_bone($pinky_p, $pinky_i, $pinky_i_b)
				$pinky_d.translation = Vector3(result["pinky_d"][0], result["pinky_d"][1], result["pinky_d"][2])
				set_bone($pinky_i, $pinky_d, $pinky_d_b)
				$pinky_t.translation = Vector3(result["pinky_t"][0], result["pinky_t"][1], result["pinky_t"][2])
				set_bone($pinky_d, $pinky_t, $pinky_t_b)
				Engine.get_frames_per_second()    


				
				
				#$wrist_b.scale = Vector3($wrist_b.scale.x, $thumb_p.translation.distance_to($wrist.translation), $wrist_b.scale.z)
				#$wrist_b.translation = $thumb_p.translation + .5*($wrist.translation - $thumb_p.translation)
				#slerp
				
				#var t = $wrist_b.get_transform()
				#var lookDir = $thumb_p.get_transform().origin - t.origin
				#var rotTransform = t.looking_at(get_transform().origin+lookDir, Vector3(0, 1, 0))
				#var thisRotation = Quat(rotTransform.basis)
				#$wrist_b.set_transform(Transform(thisRotation, t.origin))
				
				#print($thumb_p.get_transform())
				
				#$wrist_b.look_at($thumb_p.translation, Vector3(0,1,0)) 
				
				#var t = $Bone.get_transform()
				#var lookPos = get_node($thumb_p.translation).get_transform().origin
				
				#$Bone.rotation = 
				#rotate($thumd_p.translation)
#extends Label

# Timestamps of frames rendered in the last second
#var times := []

# Frames per second
#var fps := 0


#func _process(_delta: float) -> void:
#	var now := OS.get_ticks_msec()

#	# Remove frames older than 1 second in the `times` array
#	while times.size() > 0 and times[0] <= now - 1000:
#		times.pop_front()

#	times.append(now)
#	fps = times.size()

#	# Display FPS in the label
#	text = str(fps) + " FPS"