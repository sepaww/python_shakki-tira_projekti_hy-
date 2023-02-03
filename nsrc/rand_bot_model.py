from false_engine import FalseEngine as FE
import random as r
class RandBot():
    def __init__(self, team, matrix, crit_list):
        self.game_matrix=matrix
        self.team=team
        self.piece_list=[]
        self.is_bot=True
        self.engine=FE(self.game_matrix, crit_list)
    def gain_turn(self, check_list):
        self.piece_list=[]
        self.find_pieces()
        move=[]
        self.choose_piece()
        while move==[]:
            piece=self.choose_piece()    
            move=self.engine.engine_operator(0, piece[0], piece[1], piece[2], check_list)
        move=r.choice(move)
        move=(move[0], move[1], piece[0], piece[1], piece[2])
        #print(move)
        return move
    def find_pieces(self):
        for i in range(len(self.game_matrix)):
            for j in range(len(self.game_matrix)):
                if self.game_matrix[i][j].team==self.team:
                    self.piece_list.append((self.game_matrix[i][j], i, j))
    def choose_piece(self):
        return r.choice(self.piece_list)
                