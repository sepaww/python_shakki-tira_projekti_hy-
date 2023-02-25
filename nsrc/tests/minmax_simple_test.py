import unittest
from copy import deepcopy
from minmax_bot_model import MinMaxBot
from engine import Game_Engine as GE
from engine import Tile, Queen, Knight, Bishop, Pawn, King, Rook
class TestMinMaxBot(unittest.TestCase):
    """A couple of simple unittests to calculate if single functions work correctly
    """
    def setUp(self):
        self.type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
        self.engine= GE(("bot", 2), ("bot", 2), False, 0)
        self.table_size=8
        self.init_cases()
        self.bot=MinMaxBot(0, deepcopy(self.case_list[0]), [], [], [], None)
    def init_cases(self):
        case_1=[]
        case_1.append([Tile(4, 1, self.type_list), Tile(3, 1, self.type_list), Tile(2, 1, self.type_list), Tile(5, 1, self.type_list), Tile(6, 1, self.type_list), Tile(2, 1, self.type_list), Tile(3, 1, self.type_list),Tile(4, 1, self.type_list)])
        case_1.append([Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list)])
        empty_row=[Tile(0, -1, self.type_list)]*self.table_size
        for _ in range(4):
            case_1.append(empty_row.copy())
        case_1.append([Tile(0, -1, self.type_list), Tile(1, 0, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(1, 0, self.type_list), Tile(0, -1, self.type_list)])
        case_1.append([Tile(4, 0, self.type_list), Tile(3, 0, self.type_list), Tile(2, 0, self.type_list), Tile(5, 0, self.type_list), Tile(6, 0, self.type_list), Tile(2, 0, self.type_list), Tile(3, 0, self.type_list),Tile(4, 0, self.type_list)])
        for i in range(self.table_size):
            for j in range(self.table_size):
                case_1[i][j].i=i
                case_1[i][j].j=j
        self.case_list=[case_1]
    
    def test_heuristic_evaluator(self):
        """test if the board_evaluator avaluates the board correctly
        """
        self.bot.init_board_values()
        self.assertEqual(self.bot.own_value, 1230)
        self.assertEqual(self.bot.enemy_value, 1290)
        val=self.bot.board_evaluator([],[])
        self.assertEqual(val, -60)
        val=self.bot.board_evaluator([6],[])
        self.assertEqual(val, -4048)
        val=self.bot.board_evaluator([2,4,1,1],[5,2,1,1,3])
        self.assertEqual(val, 10)
        val=self.bot.board_evaluator([1,1,1,1,1],[])
        self.assertEqual(val, -110)
        val=self.bot.board_evaluator([],[1,2,3,4,5])
        self.assertEqual(val, 150)
        
    def test_get_legal_moves(self):
        """test if the minmax has access to all legal moves and not to illegal ones
        """
        moves=self.bot.get_legal_moves(0)
        count=0
        for val in moves:
            count+=len(val[1])
        self.assertEqual(count, 48)
        
        moves=self.bot.get_legal_moves(1)
        count=0
        for val in moves:
            count+=len(val[1])
        self.assertEqual(count, 20)
    def test_make_move_unmake_move(self):
        """test if the make_move and unmake_moves function accordingly and return the gamestate as it was before after all moves are done
        """
        def get_id_list(matrix):
            id_list=[]
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    id_list.append((matrix[i][j].id, matrix[i][j].i, matrix[i][j].j))
            return id_list
        og_id_list=get_id_list(self.case_list[0])
        all_moves=self.bot.get_legal_moves(0)
        for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    temp_move=self.bot.game_matrix[move[0]][move[1]] 
                    og_spot=(piece.i, piece.j)
                    moved_bool=piece.moved
                    self.bot.make_move( move, piece)
                    self.bot.unmake_move(temp_move, og_spot, piece, moved_bool)
        new_id_list=get_id_list(self.bot.game_matrix)
        print(new_id_list)
        print( og_id_list)
        self.assertEqual(new_id_list,og_id_list)
        all_moves=self.bot.get_legal_moves(1)
        for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    temp_move=self.bot.game_matrix[move[0]][move[1]] 
                    og_spot=(piece.i, piece.j)
                    moved_bool=piece.moved
                    self.bot.make_move( move, piece)
                    self.bot.unmake_move(temp_move, og_spot, piece, moved_bool)
        new_id_list=get_id_list(self.bot.game_matrix)
        self.assertEqual(new_id_list,og_id_list)
    def test_depth_setter(self):
        """ test if the depth_setter sets the depth to count to to correct level
        """
        self.bot.depth_setter(1)
        self.assertEqual(self.bot.depth, 1)
        self.bot.depth_setter(5)
        self.assertEqual(self.bot.depth, 5)
    
    
