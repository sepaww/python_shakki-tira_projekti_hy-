from false_engine import FalseEngine as FE
from heapq import heappush, heappop
import random as r
class MinMaxBot():
    def __init__(self, team, matrix, crit_list, piece_list, last_move):
        self.game_matrix=matrix
        self.team=team
        if self.team==1:
            self.enemy_id=0
        else: self.enemy_id=1
        self.piece_list=[]
        self.is_bot=True
        self.counter=0
        self.depth=4
        self.turn_count=0
        self.board_size=8
        self.best_moves=[]
        self.copes=[]
        self.engine=FE(self.game_matrix, crit_list)
        self.last_move=last_move
        self.weights=[0,10,30,30,50,90,900]
        self.y_values=[-2,-1,2,3,3,2,-1,-2]
        self.x_values=[-2,-1,2,3,3,2,-1,-2]
    def gain_turn(self, check_list, game_matrix, king_moves):
        self.piece_list=[]
        self.best_moves=[]
        self.counter=0
        self.game_matrix=game_matrix
        self.check_list=check_list
        if self.turn_count<1:
            self.turn_count+=1
            if self.team==0:
                return (4, 4, self.game_matrix[6][4], 6, 4)
            return (3, 4, self.game_matrix[1][4], 1, 4)
        
        self.minmax_init(self.game_matrix)
        print(self.best_moves)
        ret_info=heappop(self.best_moves)
        print(ret_info)
        #for i in range(len(self.copes)-1):
            #print("----------")
            #print(self.copes[i])
        move=(ret_info[2][0], ret_info[2][1], ret_info[3], ret_info[3].i, ret_info[3].j)
        #print(move)
        return move

    def find_pieces(self, board, team):
        piece_list=[]
        for i in range(self.board_size):
            for j in range(self.board_size):
                #print(self.game_matrix[i][j].i, i, self.game_matrix[i][j].j, j)
                if board[i][j].team==team:
                    piece_list.append(board[i][j])
        #print(len(piece_list))
        return piece_list
                    
    def minmax_init(self, board):
        board=self.board_copier(board)
        moves=self.get_legal_moves(board, self.team)   
                  
        self.minmax(True, self.depth, board, moves, -1000000, 100000)
        
    
    
    def board_copier(self, board):    
        new_c_board=[]
        c_board=board.copy()
        #print("----------")
        for row in c_board:
            #print(row)
            new_c_board.append(row.copy())
        #print("----------")
        return new_c_board
    
    
    def minmax(self, evil_maxxing, depth, board, all_moves, alpha, beta):
        if depth==0:
            #self.copes.append(board.copy())
            #if evil_maxxing:
            return self.board_evaluator(board, True)-self.board_evaluator(board, False)
            #else:
                #return self.board_evaluator(board, False)-self.board_evaluator(board, True)
        if evil_maxxing:
            value=-999999999
            for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    new_board=self.board_copier(board) 
                    new_board=self.make_move(new_board, move, piece)
                    #value=max(value,(self.board_evaluator(new_board, True) - self.board_evaluator(new_board, False)))
                    new_moves=self.get_legal_moves(new_board, self.enemy_id)
                    value=max(value, self.minmax(False, depth-1, new_board, new_moves, alpha, beta))
                    if depth == self.depth and piece.id!=6:
                        self.counter+=1
                        #print(self.counter)
                        c=self.counter
                        
                        heappush(self.best_moves,(-value,c, move, piece))
                    alpha = max(alpha, value)
                    if value >= beta:
                        break
            return value
        else:
            value=999999999
            for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    new_board2=self.board_copier(board) 
                    new_board2=self.make_move(new_board2, move, piece)
                    #value=min(value,(self.board_evaluator(new_board, False) - self.board_evaluator(new_board, True)))
                    new_moves=self.get_legal_moves(new_board2, self.team)
                    value=min(value, self.minmax(True, depth-1, new_board2, new_moves, alpha, beta))
                    beta = min(beta, value)
                    if value <= alpha:
                        break
            return value
        
        
        
    def board_evaluator(self,board, is_team):
        pos_val=0
        if is_team:
            curr_id=self.team
        else: curr_id=self.enemy_id
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j].team==curr_id:
                    pos_val+=self.weights[board[i][j].id]
                    #pos_val+=self.y_values[i]
                    #pos_val+=self.x_values[j]
        #print(pos_val)
        return pos_val        
        
    def get_legal_moves(self, board, team):
        piece_list=self.find_pieces(board, team)
        moves=self.engine.engine_operator(1, piece_list, board, 0, 0)  
        #print(moves)
        return moves
    
    def make_move(self, board, move, piece):
        i=piece.i
        j=piece.j
        board[move[0]][move[1]]=piece
        self.engine.empty_tiler(i, j, board)
        return board
        
        