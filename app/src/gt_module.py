import json
import socket
import numpy as np
# For importing modules outside root
#import sys
#sys.path.insert(1, '../gt_rendering/scripts')

UDP_IP = '127.0.0.1'
UDP_PORT = 4243
UDP_PORT_2 = 4244
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock_2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def send_to_godot(raw_preds, verbose=False):
		preds = raw_preds.astype(float)
		preds = preds / 10
		print(preds)
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
		if verbose:
			print('preds', dic_preds)
		MESSAGE = dic_preds
		sock.sendto(json.dumps(MESSAGE).encode('ascii'), (UDP_IP, UDP_PORT))

def send_to_godot_compare(raw_preds, verbose=False):
		preds = raw_preds.astype(float)
		preds = preds / 10
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
		if verbose:
			print('preds', dic_preds)
		MESSAGE = dic_preds
		sock_2.sendto(json.dumps(MESSAGE).encode('ascii'), (UDP_IP, UDP_PORT_2))


hand_dist = {
	'Index p i': 14.778511645692358,
	'Index i d': 9.218149359281258,
	'Index d t': 14.050259696092905,
	'Middle p i': 17.46476404618026,
	'Middle i d': 10.845685216672148,
	'Middle d t': 15.751066999164728,
	'Ring p i': 21.812003113455646,
	'Ring i d': 7.193333801590452,
	'Ring d t': 14.741174141707386,
	'Pinky p i': 20.81146413397682,
	'Pinky i d': 2.8004367046733867,
	'Pinky d t': 11.448140091060699
}

def angles_to_coords(angle_row, hand_ds):
    ls_row = []
    for i, key in zip(range(12), hand_ds):
        
        d = hand_ds[key]

        y = d*np.sin(np.degrees(angle_row[i]))

        ls_row.append(y)

    return ls_row

def send_to_godot_angles(raw_preds, verbose=False):
		preds = raw_preds.astype(float)
		preds = angles_to_coords(preds, hand_dist)
		preds = np.array(preds) / 10
		dic_preds = {
				'index_i': [preds[0]],
				'index_d': [preds[1]],
				'index_t': [preds[2]],
				'middle_i': [preds[3]],
				'middle_d': [preds[4]],
				'middle_t': [preds[5]],
				'ring_i': [preds[6]],
				'ring_d': [preds[7]],
				'ring_t': [preds[8]],
				'pinky_i': [preds[9]],
				'pinky_d': [preds[10]],
				'pinky_t': [preds[11]],
				'exit': 2
				}
		if verbose:
			print('preds', dic_preds)
		MESSAGE = dic_preds
		sock.sendto(json.dumps(MESSAGE).encode('ascii'), (UDP_IP, UDP_PORT))