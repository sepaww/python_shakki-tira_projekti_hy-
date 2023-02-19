from engine import Game_Engine as GE 
import random as r
from time import time
import unittest
from engine import Tile, Queen, Knight, Bishop, Pawn, King, Rook

class TestMinMaxCorrectness(unittest.TestCase):
    def setUp(self):
        self.engine=GE(("bot", 2), ("bot", 2), False, 0)
        self.type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
        self.init_game_state_list()
        
    def game_state_giver(self, index):
        new_matrix=[]
        state=self.game_state_list[index]
        for i in range(len(state)):
            new_matrix.append([])
            for j in range(len(state[0])):
                new_matrix[i].append(Tile(state[i][j][0],state[i][j][1], self.type_list))
                new_matrix[i][j].i=i
                new_matrix[i][j].j=j
                new_matrix[i][j].moved=True
        self.engine.game_matrix=new_matrix
        self.engine.Renderer.whole_update_screen()
        
    def init_game_state_list(self):
        #insta mate for p1
        state_1=[[(4,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(6,0)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(2,0),(0,-1),(3,0)],
                 [(0,-1),(0,-1),(1,1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(1,1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(6,1),(0,-1),(0,-1),(0,-1),(4,0)]
                ]
        #mate in 1 for p1
        state_2=[[(0,-1),(2,0),(2,1),(0,-1),(0,-1),(0,-1),(2,0),(3,0)],
                 [(4,0),(0,-1),(0,-1),(1,0),(6,1),(0,-1),(0,-1),(4,1)],
                 [(0,-1),(5,0),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(2,0)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(5,1),(0,-1),(0,-1),(4,0)],
                 [(0,-1),(0,-1),(2,1),(3,0),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(0,-1),(0,-1),(0,-1),(5,0),(0,-1),(2,0),(6,0)],
                 [(0,-1),(1,1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(2,1),(5,1),(0,-1),(4,0),(0,-1),(4,1),(2,1)]
                ]
        #mate in 2 for p1
        state_3=[[(4,1),(0,-1),(2,1),(5,1),(0,-1),(0,-1),(4,1),(0,-1)],
                 [(2,1),(0,-1),(0,-1),(0,-1),(0,-1),(1,1),(6,1),(0,-1)],
                 [(1,1),(0,-1),(1,1),(1,1),(0,-1),(1,1),(0,-1),(0,-1)],
                 [(0,-1),(1,1),(0,-1),(0,-1),(1,1),(1,0),(0,-1),(0,-1)],
                 [(0,-1),(1,0),(0,-1),(0,-1),(1,0),(0,-1),(1,0),(2,0)],
                 [(0,-1),(0,-1),(0,-1),(1,0),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(0,-1),(1,0),(1,0),(5,0),(0,-1),(0,-1),(0,-1),(0,-1)],
                 [(4,0),(0,-1),(0,-1),(0,-1),(6,0),(0,-1),(0,-1),(4,0)]
                ]

        self.game_state_list=[state_1, state_2, state_3]
    
    def test_correctness(self):
        self.engine.player_one.depth_setter(2)
        self.game_state_giver(0)
        ret=self.engine.player_one.gain_turn(0, self.engine.game_matrix, 0, 0)
        self.assertEqual((ret[0], ret[1], ret[3], ret[4]), (7, 3, 7, 7))
        
        self.engine.player_one.depth_setter(3)
        self.game_state_giver(1)
        ret=self.engine.player_one.gain_turn(0, self.engine.game_matrix, 0, 0)
        self.assertEqual((ret[0], ret[1], ret[3], ret[4]), (5, 0, 5, 4))
        
        self.engine.player_one.depth_setter(5)
        self.game_state_giver(2)
        ret=self.engine.player_one.gain_turn(0, self.engine.game_matrix, 0, 0)
        self.assertEqual((ret[0], ret[1], ret[3], ret[4]), (2, 7, 6, 3))
        self.engine.Renderer.input_handler.kill_self()
if __name__ == "__main__":
    s=TestMinMaxCorrectness()