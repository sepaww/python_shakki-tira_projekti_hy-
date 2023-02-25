from false_engine import FalseEngine as FE
import random as r
class RandBot():
    def __init__(self, team, matrix, crit_list, piece_list, last_move, renderer):
        self.game_matrix=matrix
        self.team=team
        self.piece_list=[]
        self.is_bot=True
        self.engine=FE(self.game_matrix, crit_list)
        self.last_move=last_move
    def gain_turn(self, check_list, game_matrix, king_moves, crit_list):
        self.piece_list=[]
        self.game_matrix=game_matrix
        move=[]
        self.find_pieces()
        #print(crit_list)
        while move==[]:
            piece=self.choose_piece()  
            print("crit val", piece.is_crit, "id", piece.id) 
            #print("piece", piece.id, piece.i, piece.j) 
            move=self.engine.engine_operator(0, piece, piece.i, piece.j, (check_list, crit_list))
        move=r.choice(move)
        #print(move)
        ret_move=(move[0], move[1], piece, piece.i, piece.j)
        return ret_move
    def choose_piece(self):
        return r.choice(self.piece_list)
    def find_pieces(self):
        for i in range(len(self.game_matrix)):
            for j in range(len(self.game_matrix)):
                if self.game_matrix[i][j].team==self.team:
                    self.piece_list.append(self.game_matrix[i][j])