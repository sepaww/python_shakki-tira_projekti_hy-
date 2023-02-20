import unittest
from engine import Game_Engine as GE
from engine import Tile, Queen, Knight, Bishop
from ui.visuals import Renderer
class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.game_engine = GE(("bot", 0), ("bot", 0), False, 0)
        self.starting_matrix_teams=[
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [-1,-1,-1,-1,-1,-1,-1,-1,],
            [-1,-1,-1,-1,-1,-1,-1,-1,],
            [-1,-1,-1,-1,-1,-1,-1,-1,],
            [-1,-1,-1,-1,-1,-1,-1,-1,],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]
        self.starting_matrix_ids=[
            [4,3,2,5,6,2,3,4],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [4,3,2,5,6,2,3,4]
        ]
    def test_starting_matrix(self):
        """testing if the starting matrix is initiated in the correct way
        """
        for i in range(8):
            print(self.game_engine.game_matrix[i])
            for j in range(8):
                self.assertEqual(self.game_engine.game_matrix[i][j].id, self.starting_matrix_ids[i][j])
                self.assertEqual(self.game_engine.game_matrix[i][j].team, self.starting_matrix_teams[i][j])
    def test_king_chec(self):
        """moves the king and enemy queen to the center of the board and checks if the threat to king is recognize and its moves are calculated correctly
        """
        self.game_engine
        self.assertEqual(self.game_engine.starter, 0)
        self.game_engine.current_move=(self.game_engine.game_matrix[7][4], 7, 4)
        self.game_engine.move_maker(3,2)
        self.game_engine.current_move=(self.game_engine.game_matrix[0][3], 0, 3)
        self.game_engine.move_maker(3, 3)
        self.assertEqual(self.game_engine.game_matrix[3][2].id, 6)
        self.assertEqual(self.game_engine.game_matrix[3][2].team, 0)
        self.assertEqual(self.game_engine.game_matrix[7][4].id, 0)
        self.assertEqual(self.game_engine.game_matrix[3][3].id, 5)
        self.assertEqual(self.game_engine.game_matrix[3][3].team, 1)
        self.assertEqual(self.game_engine.game_matrix[0][3].id, 0)
        self.assertEqual(self.game_engine.king_spots[0], (3,2))
        self.game_engine.king_check()
        self.assertEqual(self.game_engine.perm_checks, [(3,3)])
        self.assertEqual(self.game_engine.king_move_list, [(4,1),(3,3)])
        self.game_engine.current_move=(self.game_engine.game_matrix[3][2], 3, 2)
        self.game_engine.move_maker(3, 3)
        self.game_engine.current_move=(self.game_engine.game_matrix[1][0], 1, 0)
        self.game_engine.move_maker(2,0)
        self.game_engine.king_check()
        self.assertEqual(self.game_engine.perm_checks, [])
        

    def test_pawn_moves(self):
        """tests all possible pawn moves
        """
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[1][0], 1, 0)
        self.assertEqual(moves, [(2,0), (3,0)])
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[6][0], 6, 0)
        self.assertEqual(moves, [(5,0), (4,0)])
        self.game_engine.game_matrix[1][0].moved=True
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[1][0], 1, 0)
        self.assertEqual(moves, [(2,0)])
        self.game_engine.game_matrix[5][0].id=Tile(1, 1, self.game_engine.type_list)
        
        self.game_engine.game_matrix[5][2].id=Tile(1, 1, self.game_engine.type_list)
        #self.game_engine.game_matrix[5][1].team=-1
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[6][1], 6, 1)
        print(moves, self.game_engine.game_matrix[6][1].id)
        self.assertEqual(len(moves), 4)
        
    def test_general_moves(self):
        #tests the possible moves of other pieces than pawn and king
        self.game_engine.game_matrix[4][4]=Tile(3, 1, self.game_engine.type_list)
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[4][4], 4, 4)
        self.assertEqual(len(moves), 8)
        self.game_engine.game_matrix[4][4]=Tile(2, 1, self.game_engine.type_list)
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[4][4], 4, 4)
        self.assertEqual(len(moves), 8)
        self.game_engine.game_matrix[4][4]=Tile(4, 1, self.game_engine.type_list)
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[4][4], 4, 4)
        self.assertEqual(len(moves), 11)
        self.game_engine.game_matrix[4][4]=Tile(5, 1, self.game_engine.type_list)
        moves=self.game_engine.find_moves(self.game_engine.game_matrix[4][4], 4, 4)
        self.assertEqual(len(moves), 19)
    def test_make_move(self):
        pass

if __name__ == '__main__':
    unittest.main()
