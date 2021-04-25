import os
import utils
from message import Message
from data import Data

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
input_path = project_path + "/data/mini_trace.trc"

raw_data = open(input_path, "r")
input_lines = raw_data.readlines()

messages= []
for line in input_lines:
    raw_msg = line.split()
    if not raw_msg[0].isdigit():
        continue
    if raw_msg[4] == "Tx":
        continue
    """
    msg = Message(raw_msg)
    
    msg = {"seq": int(raw_msg[0]),
           "time": float(raw_msg[1]),
           "type": int(raw_msg[3], base=16),
           "size": int(raw_msg[5])}
    data = []
    for i in range(msg['size']):
        d = []
        tmp =int(raw_msg[6+i], base=16)
        for j in range(8):
            d.append(tmp % 2)
            tmp = tmp / 2
        data.append(d)
    msg["data"] = data
    """
    messages.append(Message(raw_msg))

N = len(messages)
cur_seq = 0
cur_time = 0
data = []
data_unit = []
for i in range(N):
    if messages[i].type == utils.INIT:
        if cur_seq > 0:
            data.append(Data(cur_seq, cur_time, data_unit))
        
        cur_seq = cur_seq + 1
        cur_time = messages[i].time
        data_unit = []
    data_unit.append(messages[i])

N = len(data)

for i in range(N):
    data[i].decode_data()

save_path = project_path + "/save.pkl"
#save(data, save_path)