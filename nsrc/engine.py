from ui.visuals import Renderer as rend
from rand_bot_model import RandBot as RB
from tunnelvision_bot_model import TunnelVision_bot as TVB
from minmax_bot_model import MinMaxBot as MMB
from player import Player as P
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
        self.i=0
        self.j=0
class Game_Engine():
    def __init__(self, p1, p2, looping, starter):
        """Init the needed values for starting the game
        """
        self.player_one=p1
        self.player_two=p2
        #adjust the size of the screen
        self.game_size=700
        #adjust the size of chess table (not guaranteed to work)
        self.table_size=8
        self.starter=starter
        self.threats=0
        self.tick_rate=20
        self.temp_save=None
        self.move_history=[]
        self.current_move=None
        self.curr_player=self.starter
        self.curr_turn=self.starter
        self.check_moves=[]
        self.perm_checks=[]
        self.tthreats=0
        self.current_move_list=[]
        self.type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
        self.tilesize=int(self.game_size/self.table_size)
        self.crit_list=[0,0,0,0,0,0,0,0]
        self.eat_count=0
        self.curr_loop=self.turn_handler
        self.king_move_list=[]
        self.p1_unitlist=[]
        self.p2_unitlist=[]
        self.running=looping
        self.bot_models=[RB, TVB, MMB]
        self.game_matrix=[]
        self.last_move=[0,0,0]
        self.init_game_matrix()
        self.init_king_track()
        self.Renderer=rend(self.table_size, self.tilesize, self.game_matrix, self.starter)
        self.init_players()
        self.update()
    def init_players(self):
        if self.player_one[0]=="bot":
            model=self.bot_models[self.player_one[1]]
            self.player_one=model(0, self.game_matrix, self.crit_list, self.p1_unitlist, self.last_move, self.Renderer)
        else: self.player_one=P()
        if self.player_two[0]=="bot":
            model=self.bot_models[self.player_two[1]]
            self.player_two=model(1, self.game_matrix, self.crit_list, self.p2_unitlist, self.last_move, self.Renderer)
        else: self.player_two=P()  
        if self.starter==0:
            self.curr_player=self.player_one
        else: self.curr_player=self.player_two      
    def init_game_matrix(self):
        """places the standard starting board on game_matrix
        """
        self.game_matrix=[]
        #0=none
        #1=pawn
        #2=bishop
        #3=knight
        #4=rook
        #5=queen
        #6=king
        if self.starter==0:
            self.white_id=0
            self.black_id=1
        else:
            self.white_id=1
            self.black_id=0
        self.game_matrix.append([Tile(4, 1, self.type_list), Tile(3, 1, self.type_list), Tile(2, 1, self.type_list), Tile(5, 1, self.type_list), Tile(6, 1, self.type_list), Tile(2, 1, self.type_list), Tile(3, 1, self.type_list),Tile(4, 1, self.type_list)])
        self.game_matrix.append([Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list), Tile(1, 1, self.type_list)])
        empty_row=[Tile(0, -1, self.type_list)]*self.table_size
        for _ in range(self.table_size-4):
            self.game_matrix.append(empty_row.copy())
        self.game_matrix.append([Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list)])
        self.game_matrix.append([Tile(4, 0, self.type_list), Tile(3, 0, self.type_list), Tile(2, 0, self.type_list), Tile(5, 0, self.type_list), Tile(6, 0, self.type_list), Tile(2, 0, self.type_list), Tile(3, 0, self.type_list),Tile(4, 0, self.type_list)])
        if self.table_size>8:
            for _ in range(self.table_size-8):
                self.game_matrix[0].append(Tile(0, -1, self.type_list))
                self.game_matrix[1].append(Tile(0, -1, self.type_list))
                self.game_matrix[self.table_size-2].append(Tile(0, -1, self.type_list))
                self.game_matrix[self.table_size-1].append(Tile(0, -1, self.type_list))
        #add the i and j cordinates to each tile
        for i in range(self.table_size):
            for j in range(self.table_size):
                self.game_matrix[i][j].i=i
                self.game_matrix[i][j].j=j
                #if self.game_matrix[i][j].team==1:
                #    self.p2_unitlist.append(self.game_matrix[i][j])
                #elif self.game_matrix[i][j].team==0:
                #    self.p1_unitlist.append(self.game_matrix[i][j])
    def init_king_track(self):
        """initiates the needed info for tracking the kings
        """
        #if self.starter==1:
        self.king_spots=[(7, 4), (0,4)]
        #else:
            #self.king_spots=[(0, 4), (7,4)]
    
    def update_king_track(self, tile, i, j):
        """updates the position of king as it is moved

        Args:
            tile (Tile()): the king piece
            i (int): y-axis position
            j (int): x-axis position
        """
        ind=tile.team
        #print("king id, cords",self.game_matrix[i][j].id, i, j)
        self.king_spots[ind]=(i,j)
    def bot_reset(self):
        if self.player_one.is_bot:
            self.player_one.game_matrix=self.game_matrix
            self.player_one.engine.game_matrix=self.game_matrix
        if self.player_two.is_bot:
            self.player_two.game_matrix=self.game_matrix
            self.player_two.engine.game_matrix=self.game_matrix    
    def reset_game(self):
        print("reset game")
        self.curr_turn=self.starter
        if self.starter==0:
            self.curr_player=self.player_one
        else: self.curr_player=self.player_two
        self.eat_count=0
        for value in self.last_move:
            value=0
        self.move_history=[]
        self.init_game_matrix()
        self.init_king_track()
        self.crit_reset()
        self.perm_checks=[]
        self.Renderer.game_matrix=self.game_matrix
        self.Renderer.whole_update_screen()
        self.bot_reset()
    def crit_reset(self):
        for tile in self.crit_list:
            if tile!=0:
                tile.is_crit=-1
            tile=0 
            for i in range(self.table_size):
                for j in range(self.table_size):
                    if self.game_matrix[i][j].is_crit>-1:
                        #print("rip", self.game_matrix[i][j].id)
                        self.game_matrix[i][j].is_crit=-1
    def update(self):
        """update function that contains the main loop running the game
        call turn_handler if game is running. if game has ended calls for checkmate_loop
        """
        while self.running:
            #self.Renderer.clock.tick(self.tick_rate)
            self.curr_loop()
            self.Renderer.update_screen()
    def turn_handler(self):
        """the first function ran every turn. checks if the current player is a bot or a player.
        if the current player is a bot, it gets its turn with gain_turn function, which is supposed to return the move to be made.
        has no legality check so we suppose the bot returns only legal moves.
        """
        if self.curr_player.is_bot:
            self.check_input()
            king_moves=self.king_moves(self.game_matrix[self.king_spots[self.curr_turn][0]][self.king_spots[self.curr_turn][1]], self.king_spots[self.curr_turn][0], self.king_spots[self.curr_turn][1])
            move=self.curr_player.gain_turn(self.perm_checks, self.game_matrix, king_moves, self.crit_list)  
            self.current_move=(move[2], move[3], move[4])
            self.move_maker(move[0], move[1])
        else: self.input_handler()     
    def input_handler(self):
        """player function
        the parent function for handling unit movement. takes info from input_handler and based on whether currently trying to
        move or not will call for find_moves or move_maker
        """
        info=self.Renderer.input_handler.current_input()
        if info!=None:
            if type(info)==tuple:
                if (info[1], info[0]) in self.current_move_list:
                    if self.current_move[0].id!=6 and self.tthreats>1:
                        return
                    self.move_maker(info[1], info[0])
                else:
                    
                    for move in self.current_move_list:
                        self.Renderer.reset_tile(move)
                    self.current_move=[]
                    self.current_move_list=[]
                    
                    if self.game_matrix[info[1]][info[0]].team==self.curr_turn:
                        move_list=self.find_moves(self.game_matrix[info[1]][info[0]], info[1], info[0])
                        if len(move_list)>0:
                            self.move_handler(self.game_matrix[info[1]][info[0]], move_list, info[1], info[0])
            elif info=="u":
                self.undo_last_moves()
            elif info=="r":
                self.reset_game()

    def move_handler(self, mover_tile, move_list, i, j):
        """aims to remove all illegal moves from possible moves

        Args:
            mover_tile (Tile()): the piece to be moved
            move_list (list): the possible moves
            i (int): y-axis position
            j (int): x-axis position
        """
        if self.tthreats>1 and mover_tile.id!=6:
            return
        print(move_list, "before crit check")
        if mover_tile.is_crit>-1:
            move_list=self.crit_check_handler(mover_tile, move_list, i, j)
            print(move_list, "after crit check")
        if len(self.perm_checks)>0 and mover_tile.id!=6:
            move_list=self.viable_moves(move_list, self.perm_checks) 
        print(move_list, "after check check", self.perm_checks)
        self.current_move=[mover_tile, i, j]
        self.current_move_list=move_list
        for move in move_list:
            self.Renderer.draw_possible_moves(move)  

    def pawn_to_queen(self, i, j):
        """turns a pawn to a queen as it reaches the enemy backline
        """
        if self.current_move[0].team==1 and self.current_move[1]==6:
            self.current_move[0].type=Queen()   
            self.current_move[0].id=5
        elif self.current_move[0].team==0 and self.current_move[1]==1: 
            self.current_move[0].type=Queen()
            self.current_move[0].id=5
        self.game_matrix[i][j]=self.current_move[0]
        self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list)     
    #def move_maker_handler(i, j):
    def towering_move(self, i, j):
        """commits towering if possible. if not a towering move just moves the king normally

        Args:
            i (_type_): _description_
            j (_type_): _description_
        """
        if j-self.current_move[2]==-2:
            self.move_history[-1].append((i, 0, self.game_matrix[i][0], self.game_matrix[i][0].moved, i, j+1, self.game_matrix[i][j+1], self.game_matrix[i][j+1].moved))
            self.game_matrix[i][j]=self.current_move[0]
            self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list) 
            self.game_matrix[i][j+1]=self.game_matrix[i][0]
            self.game_matrix[i][j+1].i=i
            self.game_matrix[i][j+1].j=j+1
            self.game_matrix[i][0]=Tile(0, -1, self.type_list) 
            self.Renderer.reset_tile((self.current_move[1],0)) 
            
        elif j-self.current_move[2]==2:
            self.move_history[-1].append((i, self.table_size-1, self.game_matrix[i][self.table_size-1], self.game_matrix[i][self.table_size-1].moved, i, j-1, self.game_matrix[i][j-1], self.game_matrix[i][j-1].moved))
            self.game_matrix[i][j]=self.current_move[0]
            self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list) 
            self.game_matrix[i][j-1]=self.game_matrix[i][self.table_size-1]
            self.game_matrix[i][j-1].i=i
            self.game_matrix[i][j-1].j=j-1
            self.game_matrix[i][self.table_size-1]=Tile(0, -1, self.type_list)
            self.Renderer.reset_tile((self.current_move[1],self.table_size-1)) 
        else: 
            self.game_matrix[i][j]=self.current_move[0]
            self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list)      
    def check_input(self):
        """function that checks if the player wants to reset game
        """
        info=self.Renderer.input_handler.current_input()
        if info!=None: 
            if info=="r":
                self.reset_game()
                
    def move_maker(self, i, j):
        """makes the actual legal move switching the tiles

        Args:
            i (int): y-axis position
            j (int): x-axis position
        """
        self.move_history.append([(self.current_move[1], self.current_move[2], self.current_move[0], self.current_move[0].moved, i, j, self.game_matrix[i][j], self.game_matrix[i][j].moved)])
        if self.game_matrix[i][j].id!=0:
            if self.game_matrix[i][j].id==6:
                print("i ate king! yum yum (.__.)", self.current_move, self.current_move[0].id, self.last_move)
            self.eat_count+=1 
        if self.current_move[0].id==1:
            self.pawn_to_queen(i, j)
        elif self.current_move[0].id==6:
            self.update_king_track(self.current_move[0], i, j) 
            #code for executing towering
            self.towering_move(i, j)
                
        else:
            self.game_matrix[i][j]=self.current_move[0]
            self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list) 
        self.Renderer.reset_tile((self.current_move[1],self.current_move[2]))  
        self.Renderer.reset_tile((i, j))
        
        for move in self.current_move_list:
            self.Renderer.reset_tile(move) 
        self.move_related_info_update(i,j)
        self.current_move=[]
        self.current_move_list=[]
        self.swap_turn()    
          
    def move_related_info_update(self, i, j): 
        """updates the information of unit position and removes the eaten piece (if piece is being eaten)

        Args:
            i (int): y axis index
            j (int): x axis index
        """
        self.last_move[1]=self.current_move[1]
        self.last_move[2]=self.current_move[2]
        self.last_move[0]=self.current_move[0]
        self.current_move[0].moved=True 
        self.current_move[0].i=i
        self.current_move[0].j=j
        self.game_matrix[i][j].i=i
        self.game_matrix[i][j].j=j
         
    def swap_turn(self):
        """gives the turn to the other player
        """
        if self.curr_turn==0:
            self.curr_turn=1
            self.curr_player=self.player_two
        else: 
            self.curr_turn=0 
            self.curr_player=self.player_one
        self.threats=self.tthreats=0
        self.check_moves=[]
        self.perm_checks=[]
        self.crit_reset()
        self.king_check()
    def undo_last_moves(self):
        """undoes the last 2 moves if there is enough history.
        uses the self.move_history and pops movehistory from it.
        """
        if len(self.move_history)>1:   
            for _ in range(2): 
                temp_list=self.move_history.pop()
                for last_move in temp_list:
                    
                    self.game_matrix[last_move[0]][last_move[1]]=last_move[2]
                    self.game_matrix[last_move[0]][last_move[1]].moved=last_move[3]
                    self.game_matrix[last_move[0]][last_move[1]].i=last_move[0]
                    self.game_matrix[last_move[0]][last_move[1]].j=last_move[1]
                    if last_move[6].id!=0:
                        self.eat_count-=1
                    self.game_matrix[last_move[4]][last_move[5]]=last_move[6]
                    self.game_matrix[last_move[4]][last_move[5]].moved=last_move[7]
                    self.game_matrix[last_move[4]][last_move[5]].i=last_move[4]
                    self.game_matrix[last_move[4]][last_move[5]].j=last_move[5]
                    
                    if last_move[2].id==6:
                        self.update_king_track(last_move[2], last_move[0], last_move[1])
                    if last_move[6].id==6:
                        self.update_king_track(last_move[6], last_move[4], last_move[5])
                    self.king_check()
                    
            print("undo")
            self.Renderer.whole_update_screen()
        else:
            print("not enough move history to undo, pls play")
    def player_can_move(self):
        """function for finding out whether a player can make a move or if the game is a draw

        Returns:
            bool: can move
        """
        for i in range(self.table_size):
            for j in range(self.table_size):
                if self.game_matrix[i][j].team==self.curr_turn:
                    moves=self.find_moves(self.game_matrix[i][j], i ,j)
                    if moves!=[]:
                        return True
        return False
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
    
    def crit_list_adder(self, tile, mi, mj):
        """function for adding a critical piece (a piece that protects the king from a certain column)
        to crit_list. this way we can easily check if moving the critical piece puts king at risk (illegal move)
        """
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
        is also used in general to find if a tile is in fact threatened or not

        Args:
            tile (Tile()): the moving tile
            i (int): y-axis position
            j (int): x-axis position

        Returns:
            list: list of threats
        """
        self.check_moves=[]
        enemy_id=self.give_enemy_id(tile)
        horsemoves=[(2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2)]
        queenmoves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]    
        for move in horsemoves:
            mi, mj=move[0], move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==enemy_id and self.game_matrix[i+mi][j+mj].id==3:
                    self.check_moves.append((i+move[0], j+move[1]))
                    self.threats+=1
        pi, pj=i,j
        for move in queenmoves:
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
                    elif tile.id==6:
                        self.crit_list_adder(self.game_matrix[i+mi][j+mj], mi, mj)
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
            if 0<=i-1:
                if 0<=j-1:
                    if self.game_matrix[i-1][j-1].id==1 and self.game_matrix[i-1][j-1].team==enemy_id and tile.id!=0:
                        self.check_moves.append((i-dist, j-1))
                        self.threats+=1
                if j+1<=7:
                    if self.game_matrix[i-1][j+1].id==1 and self.game_matrix[i-1][j+1].team==enemy_id and tile.id!=0:
                        self.check_moves.append((i-dist, j+1))
                        self.threats+=1
        else:
            if -1<i+1<=self.table_size-1:
                if 0<=j-1<self.table_size:
                    if self.game_matrix[i+1][j-1].id==1 and self.game_matrix[i+1][j-1].team==enemy_id and tile.id!=0:
                        self.check_moves.append((i+dist, j-1))
                        self.threats+=1
                if j+1<=self.table_size-1:
                    if self.game_matrix[i+1][j+1].id==1 and self.game_matrix[i+1][j+1].team==enemy_id and tile.id!=0:
                        self.check_moves.append((i+dist, j+1))
                        self.threats+=1
        if tile.id==6:
            pass
            for move in queenmoves:
                mi, mj=move[0], move[1]
                if 0<=i+mi<=7 and 0<=j+mj<=7:
                    if enemy_king_checks(i+mi, j+mj):
                        self.check_moves.append((i, j))
                        break  
        temp_negs=[] 
        return self.check_moves
    
    def give_enemy_id(self, tile):
        """a simple function to reduce copypaste in code. returns the enemy id, unless the tile given is empty.
        if so, return the id of current player (this is used only when we want to know if some character can save the king)

        Args:
            tile (Tile): given tile

        Returns:
            int: id of the enemy
        """
        if tile.team==0:
            enemy_id=1
        elif tile.team==1:
            enemy_id=0
        else:
            enemy_id=self.curr_turn
        return enemy_id
    
    def recursive_threat_find(self, enemy_id, formaat, i, j, temp_negs):
        """algorithm to find out if moving a piece in critical place would threaten own king (be illegal).
        for quickness each critical piece knows its format. (which direction the threat could come fom)

        Args:
            enemy_id (int): id of enemy team
            formaat (tuple): the direction enemy threat could come from
            i (int): y axis
            j (int): x axis
            temp_negs (list): list of possible threatening tiles that the current piece could go to without putting king at risk

        Returns:
            list: the threat tiles
        """
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
        self.game_matrix[y][x]=Tile(0, -1, self.type_list)
        format_list=[(-1,-1), (-1,0), (-1,1), (0,1), (1, 1), (1, 0), (1,-1), (0,-1)]
        formaat=format_list[tile.is_crit]
        temp_negs=[]
        enemy_id=self.give_enemy_id(tile)
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
        self.perm_checks=self.check_moves.copy()
        if self.check_moves==[]:
            if self.eat_count!=30:
                if self.player_can_move():
                    print(self.curr_turn, "can move")
                    return
                else:
                    print("cant move or check anymore: draw")
                    self.curr_loop=self.checkmate_loop
            else:        
                print("cant move or check anymore: draw, only kings")
                self.curr_loop=self.checkmate_loop
            return
        print("check")
        
        self.tthreats=self.threats
        self.king_move_list=self.king_moves(k_tile, ki, kj)
        self.check_moves=[]
        if self.king_move_list==[]:
            if self.tthreats>1:
                print("checkmate")
                self.curr_loop=self.checkmate_loop
            elif self.tthreats==1:
                enemy_id=self.give_enemy_id(k_tile)
                print(self.perm_checks, "perm checks, king cords", k_tile.i, k_tile.j)
                for move in self.perm_checks:
                    og_id=self.game_matrix[move[0]][move[1]].team
                    self.game_matrix[move[0]][move[1]].team=enemy_id
                    self.is_threatened(self.game_matrix[move[0]][move[1]], move[0], move[1])
                    self.game_matrix[move[0]][move[1]].team=og_id
                    if len(self.check_moves)>0:
                        print("winnable 1")
                        return
                print("checkmate")
                self.curr_loop=self.checkmate_loop
            else:
                print("winnable 2")
                    
        
    def checkmate_loop(self):
        self.Renderer.whole_update_screen()
        info=self.Renderer.input_handler.main_inputs()
        if info=="r":
            self.reset_game()
            self.curr_loop=self.turn_handler
            
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
        if tile.id==1:
            return self.pawn_moves(tile, i, j)
        valid_moves=[]
        original_tile=self.game_matrix[i][j]
        def recursive_move_find(i, j, format):
            mi=format[0]
            mj=format[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==-1:
                    valid_moves.append((i+mi, j+mj))
                    recursive_move_find(i+mi, j+mj, move)
                elif self.game_matrix[i+mi][j+mj].team!=original_tile.team:
                    valid_moves.append((i+mi, j+mj))
        for move in tile.type.moves:
            mi=move[0]
            mj=move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==-1 and original_tile.type.can_move_inf:
                    valid_moves.append((i+mi, j+mj))
                    recursive_move_find(i+mi, j+mj, move)
                elif self.game_matrix[i+mi][j+mj].team!=original_tile.team:
                    valid_moves.append((i+mi, j+mj))
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
        if not tile.moved and tile.id==6:
            if self.game_matrix[i][j-1].team==-1 and self.game_matrix[i][j-2].team==-1 and self.game_matrix[i][j-3].team==-1 and self.game_matrix[i][j-4].moved==False and self.game_matrix[i][j-4].id==4:
                temp_j=j-2
                self.is_threatened(tile, i, temp_j)
                if self.check_moves==[]:
                    moves.append((i, temp_j))
                self.check_moves=[]
            if self.game_matrix[i][j+1].team==-1 and self.game_matrix[i][j+2].team==-1 and self.game_matrix[i][j+3].moved==False and self.game_matrix[i][j+3].id==4:        
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
        if 0<i<self.table_size-1:
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
    
    
    
if __name__=="__main__":    
    #game=Game_Engine(("p", 0), ("bot", 2), True, 0)
    #game=Game_Engine(("p", 0), ("p", 0), True, 0)
    game=Game_Engine(("p", 0), ("bot", 2), True, 0)
