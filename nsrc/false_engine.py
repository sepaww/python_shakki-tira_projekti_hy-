
from heapq import heappush, heappop
class King():
    def __init__(self):
        self.moves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]
        self.can_hop=False
        self.can_move_inf=False
class Queen():
    def __init__(self):
        self.moves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]
        self.can_hop=False
        self.can_move_inf=True
class Rook():
    def __init__(self):
        self.moves=[(1,0), (-1,0), (0, 1), (0,-1)]
        self.can_hop=False
        self.can_move_inf=True
class Bishop():
    def __init__(self):
        self.moves=[(1,1), (1,-1), (-1, 1), (-1,-1)]
        self.can_hop=False
        self.can_move_inf=True
class Knight():
    def __init__(self):
        self.moves=[(2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2)]
        self.can_hop=True
        self.can_move_inf=False
class Pawn():
    def __init__(self):
        self.moves=[(1,0)]
        self.eats=[(1,1), (1,-1)]
        self.can_hop=False
        self.can_move_inf=False
class Tile():
    def __init__(self, id, team, typelist):
        self.id=id
        self.team=team
        self.moved=False
        self.type=typelist[id]
        self.is_crit=-1
class FalseEngine():
    def __init__(self, matrix, crit_list):
        """Init the needed values for starting the game
        """
        self.game_matrix=matrix
        self.crit_list=crit_list
        self.check_moves=[]
        self.tthreats=0
        self.threats=0
        self.check_crit=False
        self.table_size=8
        self.horse_moves=[(2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2)]
        self.queen_moves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]   
        self.sort_values=[1, 0, -1, -2, -2, -1, 0, 1]
        self.type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
    def reset_engine(self):
        self.check_moves=[]
        self.tthreats=0
        self.threats=0   
         
    def engine_operator(self, command, tile, i, j, check_moves):
        self.reset_engine()
        self.check_moves=check_moves
        if command==0:
            self.check_crit=True
            self.crit_list=check_moves[1]
            self.check_moves=check_moves[0]
            moves=self.find_moves(tile, i, j)
            if len(check_moves)>0:
                if tile.id!=6:
                    moves=self.viable_moves(moves, self.check_moves)
                else:
                    moves=self.king_moves(tile, i, j)
            return moves
        elif command==1:
            self.check_crit=False
            self.check_moves=[]
            pieces=tile
            board=i
            all_moves=[]
            self.game_matrix=board
            for piece in pieces:
                moves=self.find_moves(piece, piece.i, piece.j)
                moves=self.sort_moves(moves)
                if moves!=[]:
                    all_moves.append((piece,moves.copy()))
            return all_moves   
            
    def sort_moves(self, moves):   
        new_moves=[]
        temp_que=[]
        for move in moves:
            val=self.sort_values[move[0]]+self.sort_values[move[1]]
            if self.game_matrix[move[0]][move[1]].id!=0:
                val-=5
            heappush(temp_que, (val, move))
        while temp_que!=[]:
            new_moves.append(heappop(temp_que)[1])
        return new_moves 
    def crit_reset(self):
        for tile in self.crit_list:
            if tile!=0:
                tile.is_crit=-1
        self.crit_list=[0,0,0,0,0,0,0,0]  
        
    
    def mash_negs_together(self, temp_negs):
        """adds all found threatening tiles to the permanent list

        Args:
            temp_negs (list): contains the tiles that can be blocked in order to stop the king being threatened
        """
        for value in temp_negs:
            self.check_moves.append(value)
            
    def viable_moves(self, move_list, negs):
        """removes all illegal moves from move_list

        Args:
            move_list (list): list of possible moves
            negs (list): list of check moves
        Returns:
            list: legal moves
        """
        viable_moves=[]
        if len(negs)==0:
            return move_list
        for check in negs:
            if check in move_list:
                viable_moves.append(check)
        return viable_moves
    
    def reverse_viable_moves(self, move_list, negs):
        """removes all illegal moves from move_list

        Args:
            move_list (list): list of possible moves
            negs (list): list of check moves
        Returns:
            list: legal moves
        """
        viable_moves=[]
        if len(negs)==0:
            return move_list
        for move in move_list:
            if move not in negs:
                viable_moves.append(move)
        return viable_moves
    
    def empty_tiler(self,i, j, board):
        board[i][j]=Tile(0, -1, self.type_list)
        return board
    
    def crit_list_adder(self, tile, mi, mj):
        # format_list=[(-1,-1), (-1,0), (-1,1), (0,1), (1, 1), (1, 0), (1,-1), (0,-1)]
        if mi==-1 and mj==-1:
            self.crit_list[0]=tile
            tile.is_crit=0
        elif mi==-1 and mj==0:
            self.crit_list[1]=tile
            tile.is_crit=1
        elif mi==-1 and mj==1:
            self.crit_list[2]=tile
            tile.is_crit=2
        elif mi==0 and mj==1:
            self.crit_list[3]=tile
            tile.is_crit=3
        elif mi==1 and mj==1:
            self.crit_list[4]=tile
            tile.is_crit=4
        elif mi==1 and mj==0:
            self.crit_list[5]=tile
            tile.is_crit=5
        elif mi==1 and mj==-1:
            self.crit_list[6]=tile
            tile.is_crit=6
        elif mi==0 and mj==-1:
            self.crit_list[7]=tile
            tile.is_crit=7
        
    def is_threatened(self, tile, i, j):
        """BLOATED algorithm that finds whether the king is being threatened, the amount of threats and the possible tiles to block the threat(s)

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position

        Returns:
            list: list of threats
        """
        enemy_id=self.give_enemy_id(tile)
          
        for move in self.horse_moves:
            mi, mj=move[0], move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==enemy_id and self.game_matrix[i+mi][j+mj].id==3:
                    self.check_moves.append((i+move[0], j+move[1]))
                    self.threats+=1
        pi, pj=i,j
        for move in self.queen_moves:
            i, j=pi,pj
            temp_negs=[]
            def recursive_move_find(i, j, format):
                mi=format[0]
                mj=format[1]
                if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==-1:

                        temp_negs.append((i+mi, j+mj))
                        recursive_move_find(i+mi, j+mj, move)
                    elif self.game_matrix[i+mi][j+mj].team==enemy_id:

                        if (abs(mi)+abs(mj))%2==0:
                            if self.game_matrix[i+mi][j+mj].id in [2,5]:
                                self.threats+=1
                                temp_negs.append((i+mi, j+mj))
                                self.mash_negs_together(temp_negs)
                        elif self.game_matrix[i+mi][j+mj].id in [5,4]:
                            self.threats+=1
                            temp_negs.append((i+mi, j+mj))
                            self.mash_negs_together(temp_negs)
                    #elif tile.id==6:
                        #self.crit_list_adder(self.game_matrix[i+mi][j+mj], mi, mj)
            recursive_move_find(i, j, move)
        def enemy_king_checks(i, j):
            if self.game_matrix[i][j].id==6 and self.game_matrix[i][j].team==enemy_id:
                return True
            return False
        if tile.id==6:
            dist=1
        else: 
            dist=0
        if enemy_id==1:
            if 0<=i-dist:
                if 0<=j-1:
                    if self.game_matrix[i-1][j-1].id==1 and self.game_matrix[i-1][j-1].team==enemy_id:
                        self.check_moves.append((i-dist, j-1))
                        self.threats+=1
                if j+1<=7:
                    if self.game_matrix[i-1][j+1].id==1 and self.game_matrix[i-1][j+1].team==enemy_id:
                        self.check_moves.append((i-dist, j+1))
                        self.threats+=1
        else:
            if i+dist<=7:
                if 0<=j-1:
                    if self.game_matrix[i+1][j-1].id==1 and self.game_matrix[i+1][j-1].team==enemy_id:
                        self.check_moves.append((i+dist, j-1))
                        self.threats+=1
                if j+1<=7:
                    if self.game_matrix[i+1][j+1].id==1 and self.game_matrix[i+1][j+1].team==enemy_id:
                        self.check_moves.append((i+dist, j+1))
                        self.threats+=1
        if tile.id==6:
            for move in self.queen_moves:
                mi, mj=move[0], move[1]
                if 0<=i+mi<=7 and 0<=j+mj<=7:
                    if enemy_king_checks(i+mi, j+mj):
                        self.check_moves.append((i, j))
                        break  
        temp_negs=[] 
        return self.check_moves
    
    def give_enemy_id(self, tile):
        if tile.team==0:
            enemy_id=1
        else: enemy_id=0
        return enemy_id
    
    def recursive_threat_find(self, enemy_id, formaat, i, j, temp_negs):
        mi, mj=formaat[0], formaat[1]
        if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==-1:

                        temp_negs.append((i+mi, j+mj))
                        return self.recursive_threat_find(enemy_id, formaat, i+mi, j+mj, temp_negs)
                    elif self.game_matrix[i+mi][j+mj].team==enemy_id:
                        if (abs(mi)+abs(mj))%2==0:
                            if self.game_matrix[i+mi][j+mj].id in [2,5]:
                                temp_negs.append((i+mi, j+mj))
                                return temp_negs
                        elif self.game_matrix[i+mi][j+mj].id in [5,4]:
                            temp_negs.append((i+mi, j+mj))
                            return temp_negs
                        
    def crit_check_handler(self, tile, move_list, y, x):
        """initialize for is_threatened. removes the piece to be moved to calculate whether moving it puts own king at risk.

        Args:
            tile (Tile()): the moving tile
            move_list (list): list of possible moves
            i (int): y-axis position
            j (int): x-axis position

        Returns:
            _type_: _description_
        """
        self.temp_save=tile
        print(tile.id, "temp_id", self.temp_save.id)
        self.game_matrix[y][x]=Tile(0, -1, self.type_list)
        format_list=[(-1,-1), (-1,0), (-1,1), (0,1), (1, 1), (1, 0), (1,-1), (0,-1)]
        formaat=format_list[tile.is_crit]
        temp_negs=[]
        enemy_id=self.give_enemy_id(self.temp_save)
        threat_tiles=self.recursive_threat_find(enemy_id, formaat, y, x, temp_negs)
        self.game_matrix[y][x]=self.temp_save
        self.temp_save=None
        if threat_tiles==None:
            return move_list
        return self.viable_moves(move_list, threat_tiles)
    
    def king_check(self):
        ki, kj=self.king_spots[self.curr_turn][0], self.king_spots[self.curr_turn][1]
        k_tile=self.game_matrix[ki][kj]
        self.is_threatened(k_tile, ki, kj)
        if self.check_moves==[]:
            return

        self.perm_checks=self.check_moves.copy()
        self.tthreats=self.threats
        self.king_move_list=self.king_moves(k_tile, ki, kj)
        self.check_moves=[]
        if self.king_move_list==[]:
            if self.tthreats>1:
                print("checkmate")
            elif self.tthreats==1:
                for move in self.perm_checks:
                    self.is_threatened(self.game_matrix[move[0]][move[1]], move[0], move[1])
                    if len(self.check_moves)>0:
                        return
                print("checkmate") 
            else:
                print("winnable")
                    
        
    
    def find_moves(self, tile, i, j):
        """calls for the correct function to calculate possible moves by figuring out if a special move finding algorithm is needed

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position

        Returns:
           list: list of possible moves
        """
        if tile.id==1:
            return self.pawn_moves(tile, i, j)      
        elif tile.id==6:
            return self.king_moves(tile, i, j)      
        else:
            return self.general_moves(tile, i, j)   
        
    def general_moves(self, tile, i, j):
        
        valid_moves=[]
        
        def recursive_move_find(i, j, format):
            mi=format[0]
            mj=format[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==-1:
                    valid_moves.append((i+mi, j+mj))
                    recursive_move_find(i+mi, j+mj, move)
                elif self.game_matrix[i+mi][j+mj].team!=tile.team:
                    valid_moves.append((i+mi, j+mj))
        for move in tile.type.moves:
            mi=move[0]
            mj=move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==-1 and tile.type.can_move_inf:
                    valid_moves.append((i+mi, j+mj))
                    recursive_move_find(i+mi, j+mj, move)
                elif self.game_matrix[i+mi][j+mj].team!=tile.team:
                    valid_moves.append((i+mi, j+mj))
        if self.check_crit:            
            if tile.is_crit>1:
                        valid_moves=self.crit_check_handler(tile, valid_moves, tile.i, tile.j)
        return valid_moves 
        
    def towering_check(self, tile, i, j, moves):
        """checks if towering is possible

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position
            moves (_type_): _description_

        Returns:
            list: list of possible towering moves
        """
        if self.game_matrix[i][j-1].team==-1 and self.game_matrix[i][j-2].team==-1 and self.game_matrix[i][j-3].team==-1 and self.game_matrix[i][j-4].moved==False:
            temp_j=j-2
            self.is_threatened(tile, i, temp_j)
            if self.check_moves==[]:
                moves.append((i, temp_j))
            self.check_moves=[]
        if self.game_matrix[i][j+1].team==-1 and self.game_matrix[i][j+2].team==-1 and self.game_matrix[i][j+3].moved==False:        
            temp_j=j+2
            self.is_threatened(tile, i, temp_j)
            if self.check_moves==[]:
                moves.append((i, temp_j))
        return moves
    
    def king_moves(self, tile, i, j):
        """calculates the possible moves for the king piece

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position

        Returns:
            list: list of possible moves
        """
        king_moves=[]
        if not tile.moved:
            king_moves=self.towering_check(tile, i, j, king_moves)
        self.temp_save=tile
        self.game_matrix[i][j]=Tile(0, -1, self.type_list)
        for move in tile.type.moves:
            mi,mj=move[0],move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team!=tile.team:
                    self.check_moves=[]
                    self.is_threatened(tile, i+mi, j+mj)
                    if self.check_moves==[]:
                        king_moves.append((i+mi, j+mj))
        self.game_matrix[i][j]=self.temp_save
        self.temp_save=None
        return king_moves
                            
    def pawn_moves(self, tile, i, j):
        """calculates all possible pawn moves

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position

        Returns:
            list: list of possible moves
        """
        valid_moves=[]
        flipper=1
        if tile.team==0:
            flipper=-1
        move=[tile.type.moves[0][0], tile.type.moves[0][1]]
        move[0]*=flipper
        eat=([tile.type.eats[0][0],tile.type.eats[0][1]], [tile.type.eats[1][0],tile.type.eats[1][1]])
        eat[0][0]*=flipper
        eat[1][0]*=flipper
        if 0<i<7:
            if self.game_matrix[i+move[0]][j].team==-1:
                valid_moves.append((i+move[0], j))
                if tile.moved==False:
                    if self.game_matrix[i+move[0]+move[0]][j].team==-1:
                        valid_moves.append((i+move[0]+move[0], j))
            if j<self.table_size-1:            
                if tile.team!=self.game_matrix[i+eat[0][0]][j+eat[0][1]].team and self.game_matrix[i+eat[0][0]][j+eat[0][1]].team!=-1:
                    valid_moves.append((i+eat[0][0], j+eat[0][1]))
            if 0<j: 
                if tile.team!=self.game_matrix[i+eat[1][0]][j+eat[1][1]].team and self.game_matrix[i+eat[1][0]][j+eat[1][1]].team!=-1:
                    valid_moves.append((i+eat[1][0], j+eat[1][1]))
        return valid_moves
    
