# notes.py
from config import *

class Note:
    def __init__(self, lane, image, speed=None, note_type="tap"):
        self.lane      = lane
        self.image     = image
        self.note_type = note_type
        self.speed     = speed if speed is not None else NOTE_SPEED

        self.x = WIDTH

        self.hit_top     = False
        self.hit_bottom  = False
        self.dual_scored = False

        if lane == "top":
            self.y = TOP_LANE_Y
        elif lane == "bottom":
            self.y = BOTTOM_LANE_Y
        elif lane == "mid":
            self.y = DUAL_LANE_Y

    def update(self):
        self.x += self.speed   # speed is negative

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), self.y))
