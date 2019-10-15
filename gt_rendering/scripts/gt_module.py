import json
#from serial.tools.list_ports import comport
import socket
# For importing modules outside root
#import sys
#sys.path.insert(1, '../gt_rendering/scripts')

UDP_IP = '127.0.0.1'
UDP_PORT = 4242
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

'''
Converts predictions to a dictionary that is sent to Godot via a socket
The Godot program has to be listening, which is done by running the 
main scene of the 'project.godot' file
'''
def send_to_godot(raw_preds):
        # reformat raw_preds accordingly
		# preds = raw_preds[0].astype(float)
		# print(type(float(preds[0])))
		preds = raw_preds / 10
		dic_preds = {
				'wrist': [preds[0], preds[1], preds[2]],
				'thumb_p': [preds[3], preds[4], preds[5]],
				'thumb_i': [preds[6], preds[7], preds[8]],
				'thumb_d': [preds[9], preds[10], preds[11]],
				'thumb_t': [preds[12], preds[13], preds[14]],
				'index_p':[preds[15], preds[16], preds[17]],
				'index_i': [preds[18], preds[19], preds[20]],
				'index_d': [preds[21], preds[22], preds[23]],
				'index_t': [preds[24], preds[25], preds[26]],
				'middle_p': [preds[27], preds[28], preds[29]],
				'middle_i': [preds[30], preds[31], preds[32]],
				'middle_d': [preds[33], preds[34], preds[35]],
				'middle_t': [preds[36], preds[37], preds[38]],
				'ring_p': [preds[39], preds[40], preds[41]],
				'ring_i': [preds[42], preds[43], preds[44]],
				'ring_d': [preds[45], preds[46], preds[47]],
				'ring_t': [preds[48], preds[49], preds[50]],
				'pinky_p': [preds[51], preds[52], preds[53]],
				'pinky_i': [preds[54], preds[55], preds[56]],
				'pinky_d': [preds[57], preds[58], preds[59]],
				'pinky_t': [preds[60], preds[61], preds[62]],
				'exit': 2
				}
		print('preds', dic_preds)
		MESSAGE = dic_preds
		sock.sendto(json.dumps(MESSAGE).encode('ascii'), (UDP_IP, UDP_PORT))