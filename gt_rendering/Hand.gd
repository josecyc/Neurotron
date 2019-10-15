extends Spatial
extends Label

var socket = PacketPeerUDP.new()
var status = socket.listen(4242, "127.0.0.1")

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
				$thumb_p.translation = Vector3(result["thumb_p"][0], result["thumb_p"][1], result["thumb_p"][2])
				$thumb_i.translation = Vector3(result["thumb_i"][0], result["thumb_i"][1], result["thumb_i"][2])
				$thumb_d.translation = Vector3(result["thumb_d"][0], result["thumb_d"][1], result["thumb_d"][2])
				$thumb_t.translation = Vector3(result["thumb_t"][0], result["thumb_t"][1], result["thumb_t"][2])
				$index_p.translation = Vector3(result["index_p"][0], result["index_p"][1], result["index_p"][2])
				$index_i.translation = Vector3(result["index_i"][0], result["index_i"][1], result["index_i"][2])
				$index_d.translation = Vector3(result["index_d"][0], result["index_d"][1], result["index_d"][2])
				$index_t.translation = Vector3(result["index_t"][0], result["index_t"][1], result["index_t"][2])
				$middle_p.translation = Vector3(result["middle_p"][0], result["middle_p"][1], result["middle_p"][2])
				$middle_i.translation = Vector3(result["middle_i"][0], result["middle_i"][1], result["middle_i"][2])
				$middle_d.translation = Vector3(result["middle_d"][0], result["middle_d"][1], result["middle_d"][2])
				$middle_t.translation = Vector3(result["middle_t"][0], result["middle_t"][1], result["middle_t"][2])
				$ring_p.translation = Vector3(result["ring_p"][0], result["ring_p"][1], result["ring_p"][2])
				$ring_i.translation = Vector3(result["ring_i"][0], result["ring_i"][1], result["ring_i"][2])
				$ring_d.translation = Vector3(result["ring_d"][0], result["ring_d"][1], result["ring_d"][2])
				$ring_t.translation = Vector3(result["ring_t"][0], result["ring_t"][1], result["ring_t"][2])
				$pinky_p.translation = Vector3(result["pinky_p"][0], result["pinky_p"][1], result["pinky_p"][2])
				$pinky_i.translation = Vector3(result["pinky_i"][0], result["pinky_i"][1], result["pinky_i"][2])
				$pinky_d.translation = Vector3(result["pinky_d"][0], result["pinky_d"][1], result["pinky_d"][2])
				$pinky_t.translation = Vector3(result["pinky_t"][0], result["pinky_t"][1], result["pinky_t"][2])
				Engine.get_frames_per_second()    

#extends Label

# Timestamps of frames rendered in the last second
var times := []

# Frames per second
var fps := 0


func _process(_delta: float) -> void:
	var now := OS.get_ticks_msec()

	# Remove frames older than 1 second in the `times` array
	while times.size() > 0 and times[0] <= now - 1000:
		times.pop_front()

	times.append(now)
	fps = times.size()

	# Display FPS in the label
	text = str(fps) + " FPS"