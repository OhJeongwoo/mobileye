from message import Message
from lane import Lane
from obstacle import Obstacle
import utils

class Data:
    def __init__(self, seq = None, time = None, messages = None):
        if messages:
            self.seq = seq
            self.time = time
            self.size = len(messages)
            self.messages =messages
        self.left_lane = Lane()
        self.right_lane = Lane()
        self.n_next_lane = 0
        self.next_lane = []

    def find_message(self, target):
        for msg in self.messages:
            if msg.type == target:
                return msg
        return None

    def decode_data(self):
        # decode left lane
        LaneA = self.find_message(utils.LEFT_LANE_A)
        LaneB = self.find_message(utils.LEFT_LANE_B)
        if LaneA is None or LaneB is None:
            utils.print_error_message(self.seq, "left_lane")
        else:
            self.left_lane = utils.decode_lane(LaneA, LaneB)
           
        # decode right lane
        LaneA = self.find_message(utils.RIGHT_LANE_A)
        LaneB = self.find_message(utils.RIGHT_LANE_B)
        if LaneA is None or LaneB is None:
            utils.print_error_message(self.seq, "right_lane")
        else:
            self.right_lane = utils.decode_lane(LaneA, LaneB)

        # decode next lane
        NextLaneInfo = self.find_message(utils.NEXT_LANE_INFO)
        if NextLaneInfo is None:
            utils.print_error_message(self.seq, "next lane info")
        else:
            self.n_next_lane = utils.decode_next_lane_info(NextLaneInfo)
        
        for i in range(self.n_next_lane):
            LaneA = self.find_message(utils.NEXT_LANE_A + 2 * i)
            LaneB = self.find_message(utils.NEXT_LANE_B + 2 * i)
            if LaneA is None or LaneB is None:
                utils.print_error_message(self.seq, str(i) + "-th next lane")
            else:
                self.next_lane.append(utils.decode_lane(LaneA, LaneB))
        
        print("Success to decode %d-th data" %(self.seq))