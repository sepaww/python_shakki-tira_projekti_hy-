from false_engine import FalseEngine as FE
from time import time
from heapq import heappush, heappop
import random as r
class MinMaxBot():
    def __init__(self, team, matrix, crit_list, piece_list, last_move, renderer):
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
        self.renderer=renderer
        self.board_size=8
        self.best_moves=[]
        self.own_value=0
        self.times=[]
        self.enemy_value=0
        self.engine=FE(self.game_matrix, crit_list)
        self.last_move=last_move
        self.weights=[0,10,30,30,50,90,900]
    def gain_turn(self, check_list, game_matrix, king_moves, crit_list):
        """called from engine.py and initiates the move finding process. takes in some update information
        of game state

        Args:
            check_list (_type_): _description_
            game_matrix (_type_): _description_
            king_moves (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.turn_initiator(game_matrix)
        
        #if self.turn_count<1:
        #    return self.static_start()
        
        self.minmax_init()
        
        #print(self.best_moves)
        ret_info=heappop(self.best_moves)
        #print(ret_info)
        move=(ret_info[2][0], ret_info[2][1], ret_info[3], ret_info[3].i, ret_info[3].j)
        return move
    
    def depth_setter(self, depth):
        """setter function for changing depth (mainly used in tests)

        Args:
            depth (int): depth to be calculated
        """
        self.depth=depth
        
    def turn_initiator(self, game_matrix):
        """updates info for minmax

        Args:
            game_matrix (list): _description_
            check_list (list): _description_
        """
        self.piece_list=[]
        self.best_moves=[]
        self.counter=0
        self.init_board_values()
        self.game_matrix=game_matrix
        temp_matrix=[]
        for row in self.game_matrix:
            temp_matrix.append(row.copy())
        self.game_matrix=temp_matrix
        
    def static_start(self):
        """gives a standard opening to make sure more pieces are available to the minmax
        not used in current version

        Returns:
            tuple: the stadard move tuple
        """
        self.turn_count+=1
        if self.team==0:
            return (4, 4, self.game_matrix[6][4], 6, 4)
        return (3, 4, self.game_matrix[1][4], 1, 4)
    def find_pieces(self, team):
        """finds all the pieces of the wanted team
        adds the pieces found into heapq to make sure the most important pices
        are gone through first in minmax to reduce going through
        irrelevant or bad moves

        Args:
            team (int): the wanted teams id

        Returns:
            list: list of found pieces of the team
        """
        sort_list=[]
        c=0
        for i in range(self.board_size):
            for j in range(self.board_size):
                val=0
                if self.game_matrix[i][j].team==team:
                    if j in [3,4]:
                        if self.game_matrix[i][j].id==1 and not self.game_matrix[i][j].moved:
                            val-=8
                    if self.game_matrix[i][j].id==2 or self.game_matrix[i][j].id==3:
                        val-=7
                        if not self.game_matrix[i][j].moved:
                            val-=2
                    elif self.game_matrix[i][j].id==6:
                        val+=3
                    else: val-=self.game_matrix[i][j].id
                    heappush(sort_list, (val, c, self.game_matrix[i][j]))
                    c+=1
        piece_list=[]
        while sort_list!=[]:
            val=heappop(sort_list)
            piece_list.append(val[2])        
        return piece_list
                    
    def minmax_init(self):
        """initiator function for minmax. currenlty doesnt really do anything. could be used if multiple minmaxes were wanted.
        """   
        #start=time()   
        self.minmax(True, self.depth, -1000000, 100000, [], [])
        #stop=time()
        #self.times.append(stop-start)
        #print(sum(self.times)/len(self.times))

    
    def minmax(self, evil_maxxing, depth, alpha, beta, own_loss, enemy_loss):
        """minmax function that recursively finds the best move by brute
        forcing through all possible moves withn the given depth and calculating 
        the heuristic value of the gamestate we end up in.
        
        finds all the possible moves (moves are found in false_engine.py) and iterates throught them,
        going through all possibilities unless alpha-beta erasing confirms that no matter what move
        is chose it will be worse/better than some already found move.
        Adds the best possible move for each piece in the starting depth to self.best_moves (heapq).

        Args:
            evil_maxxing (bool): boolian for flipping between finding own best move and best enemy move
            depth (int): calculating depth
            alpha (int): max value for alpha-beta erasing
            beta (int): min value for alpha-beta erasing
            own_loss (list): list of own losses made with past iterations of minmax
            enemy_loss (list): list of enemy losses made with past iterations of minmax

        Returns:
            int: value of the best move
        """
        if depth==0:
            return self.board_evaluator(own_loss, enemy_loss)
        elif evil_maxxing:
            value=-9999
            all_moves=self.get_legal_moves(self.team)
            
            for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    ate_bool=False
                    temp_move=self.game_matrix[move[0]][move[1]]
                    if piece.id==1 and move[0] in [0,7]:
                        ate_bool=True
                        enemy_loss.append(5)
                    elif temp_move.id!=0:
                        ate_bool=True
                        enemy_loss.append(temp_move.id)
                    
                    og_spot=(piece.i, piece.j)
                    moved_bool=piece.moved
                    self.make_move( move, piece)
                    
                    value=max(value, self.minmax(False, depth-1, alpha, beta, own_loss, enemy_loss))
                    
                    if depth == self.depth:
                        self.renderer.update_screen()
                        self.renderer.input_handler.response_inputs()
                        self.counter+=1
                        c=self.counter
                        if value==9999:
                            value=0
                        heappush(self.best_moves,(-1*value,c, move, piece))
                        
                    self.unmake_move(temp_move, og_spot, piece, moved_bool)
                    if ate_bool:
                        enemy_loss.pop()
                        
                    alpha = max(alpha, value)
                    if value >= beta:
                        break
            return value
        else:
            value=9999
            all_moves=self.get_legal_moves(self.enemy_id)
            
            for moves in all_moves:
                piece=moves[0]
                movess=moves[1]
                for move in movess:
                    ate_bool=False
                    temp_move=self.game_matrix[move[0]][move[1]]
                    if piece.id==1 and move[0] in [0,7]:
                        ate_bool=True
                        own_loss.append(5)
                    elif temp_move.id!=0:
                        if temp_move.id==6:
                            return -4048*depth
                        ate_bool=True
                        own_loss.append(temp_move.id)
                    og_spot=(piece.i, piece.j)
                    moved_bool=piece.moved
                    self.make_move(move, piece)
                    
                    value=min(value, self.minmax(True, depth-1, alpha, beta, own_loss, enemy_loss))
                    
                    self.unmake_move(temp_move, og_spot, piece, moved_bool)
                    if ate_bool:
                        own_loss.pop()
                        
                    beta = min(beta, value)
                    if value <= alpha:
                        break
            return value
        
        
        
    def board_evaluator(self, own, enemy):
        """heuristic evaluator of the current game state

        Args:
            own (list): own losses leading to current situation
            enemy (list): enemy losses leading to current situation

        Returns:
            int: the heuristic value of the game state
        """
        own_val=self.own_value
        enemy_val=self.enemy_value
        for val in own:
            own_val-=self.weights[val]
        for val in enemy:
            enemy_val-=self.weights[val]
        # to refrain from trading kings:
        if own_val<900:
            return -4048
        return own_val-enemy_val
        
        
    def get_legal_moves(self,team):
        """provides a semi ideally sorted list of possible moves for the wanted team

        Args:
            team (int): id of the wanted team

        Returns:
            list: list (matrix) of possible moves
        """
        piece_list=self.find_pieces(team)
        moves=self.engine.engine_operator(1, piece_list,self.game_matrix,0, 0)  
        return moves
    
    def make_move(self,move, piece):
        """makes the wanted move in minmax's wanted position.
        also updates the piece's info

        Args:
            move (tuple): the place the piece is to be moved
            piece (Tile()): the piece to be moved
        """
        i=piece.i
        j=piece.j
        piece.i=move[0]
        piece.j=move[1]
        piece.moved=True
        self.game_matrix[move[0]][move[1]]=piece
        self.engine.empty_tiler(i, j, self.game_matrix)
         
    def unmake_move(self, temp_move, og_spot, piece, moved_bool):
        """unmakes the move made in move_make() and resets the piece info

        Args:
            temp_move (Tile()): temporary save of the piece that was in the place make_move moved the piece to
            og_spot (tuple): original position of piece
            piece (Tile()): the piece whose move is about to get unmade
            moved_bool (bool): bool to find out if the piece was not moved before the last move
        """
        self.game_matrix[piece.i][piece.j]=temp_move
        self.game_matrix[og_spot[0]][og_spot[1]]=piece
        piece.i=og_spot[0] 
        piece.j=og_spot[1]   
        piece.moved=moved_bool
    
    def init_board_values(self):
        """initiates the current game states value to be used after minmax has reached depth 0
        by calculating the heuristic value before minmaxing we can reduce greatly the time
        it takes to calculate the heuristic value in board_evaluator
        """
        self.own_value=self.enemy_value=0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.game_matrix[i][j].team==self.team:
                    self.own_value+=self.weights[self.game_matrix[i][j].id]
                elif self.game_matrix[i][j].team==self.enemy_id:
                    self.enemy_value+=self.weights[self.game_matrix[i][j].id]
