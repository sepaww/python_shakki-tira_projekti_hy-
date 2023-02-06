from false_engine import FalseEngine as FE
import random as r
class RandBot():
    def __init__(self, team, matrix, crit_list, piece_list, last_move):
        self.game_matrix=matrix
        self.team=team
        self.piece_list=[]
        self.is_bot=True
        self.engine=FE(self.game_matrix, crit_list)
        self.last_move=last_move
    def gain_turn(self, check_list, game_matrix, king_moves):
        self.piece_list=[]
        self.game_matrix=game_matrix
        move=[]
        self.find_pieces()
        
        while move==[]:
            piece=self.choose_piece()   
            print("piece", piece.id, piece.i, piece.j) 
            move=self.engine.engine_operator(0, piece, piece.i, piece.j, check_list)
        move=r.choice(move)
        print(move)
        move=(move[0], move[1], piece, piece.i, piece.j)
        #print(move)
        return move
    def choose_piece(self):
        return r.choice(self.piece_list)
    def find_pieces(self):
        for i in range(len(self.game_matrix)):
            for j in range(len(self.game_matrix)):
                print(self.game_matrix[i][j].i, i, self.game_matrix[i][j].j, j)
                if self.game_matrix[i][j].team==self.team:
                    self.piece_list.append(self.game_matrix[i][j])