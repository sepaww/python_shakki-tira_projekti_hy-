from ui.visuals import Renderer as rend

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
class Game_Engine():
    def __init__(self):
        self.game_size=800
        self.table_size=8
        self.starter=0
        self.threats=0
        self.temp_save=None
        self.current_move=None
        self.curr_player=self.starter
        self.curr_turn=self.starter
        self.check_moves=[]
        self.current_move_list=[]
        self.type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
        self.tilesize=int(self.game_size/self.table_size)
        self.running=True
        self.game_matrix=[]
        self.init_game_matrix()
        self.init_king_track()
        self.Renderer=rend(self.table_size, self.tilesize, self.game_matrix, self.curr_player)
        self.update()
    def init_game_matrix(self):
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
        empty_row=[Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list), Tile(0, -1, self.type_list)]
        for _ in range(4):
            self.game_matrix.append(empty_row.copy())
        self.game_matrix.append([Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list), Tile(1, 0, self.type_list)])
        self.game_matrix.append([Tile(4, 0, self.type_list), Tile(3, 0, self.type_list), Tile(2, 0, self.type_list), Tile(5, 0, self.type_list), Tile(6, 0, self.type_list), Tile(2, 0, self.type_list), Tile(3, 0, self.type_list),Tile(4, 0, self.type_list)])
    
    def init_king_track(self):
        #if self.starter==1:
        self.king_spots=[(7, 4), (0,4)]
        #else:
            #self.king_spots=[(0, 4), (7,4)]
    
    def update_king_track(self, tile, i, j):
        ind=tile.team
        self.king_spots[ind]=(i,j)
       
    def update(self):
        while self.running:
            self.Renderer.clock.tick(20)
            self.input_handler()
            self.Renderer.update_screen()
    def input_handler(self):
        info=self.Renderer.input_handler.current_input()
        if info!=None:
            if (info[1], info[0]) in self.current_move_list:
                if self.current_move[0].id!=6 and self.threats>1:
                    return
                self.move_maker(info[1], info[0])
            else:
                self.threats=0
                for move in self.current_move_list:
                    self.Renderer.reset_tile(move)
                self.current_move=[]
                self.current_move_list=[]
                
                if self.game_matrix[info[1]][info[0]].team==self.curr_turn:
                    move_list=self.find_moves(self.game_matrix[info[1]][info[0]], info[1], info[0])
                    if len(move_list)>0:
                        print(move_list)
                        self.move_handler(self.game_matrix[info[1]][info[0]], move_list, info[1], info[0])

    def move_handler(self, mover_tile, move_list, i, j):
        print("nyt", move_list)
        move_list=self.own_check(mover_tile, move_list, i, j)
        print("jalk", move_list)
        if self.threats>1 and mover_tile.id!=6:
            return
        self.current_move=[mover_tile, i, j]
        self.current_move_list=move_list
        for move in move_list:
            self.Renderer.draw_possible_moves(move)  

    def pawn_to_queen(self):
        if self.current_move[0].team==1 and self.current_move[1]==6:
            print(self.current_move)
            self.current_move[0].type=Queen()   
            self.current_move[0].id=5
        elif self.current_move[0].team==0 and self.current_move[1]==1: 
            print(self.current_move)
            self.current_move[0].type=Queen()
            self.current_move[0].id=5
    #def move_maker_handler(i, j):        
    def move_maker(self, i, j):
        self.current_move[0].moved=True 
        if self.current_move[0].id==1:
            self.pawn_to_queen()
        elif self.current_move[0].id==6:
            self.update_king_track(self.current_move[0], i, j) 
        self.game_matrix[i][j]=self.current_move[0]
        self.game_matrix[self.current_move[1]][self.current_move[2]]=Tile(0, -1, self.type_list) 
    
        
        self.Renderer.reset_tile((self.current_move[1],self.current_move[2]))  
        self.current_move=[]
        
        for move in self.current_move_list:
            self.Renderer.reset_tile(move) 
        self.current_move_list=[]
        self.swap_turn()      
                    
    def swap_turn(self):
        if self.curr_turn==0:
            self.curr_turn=1
        else: self.curr_turn=0 
    def king_help_moves(self, move_list):
        i=0 
        while i < len(move_list):
            if move_list[i] in self.check_moves:  
                move_list.pop(i)
                i-=1
            i+=1
        return move_list
    def mash_negs_together(self, temp_negs):
        for value in temp_negs:
            self.check_moves.append(value)
            
    def viable_moves(self, move_list):
        viable_moves=[]
        print(self.check_moves, move_list)
        if len(self.check_moves)==0:
            return move_list
        for check in self.check_moves:
            if check in move_list:
                viable_moves.append(check)
        return viable_moves
    
    def is_threatened(self, tile, i, j):
        if tile.team==0:
            enemy_id=1
        else: enemy_id=0
        if tile.id!=6:
            i,j=self.king_spots[tile.team][0], self.king_spots[tile.team][1]
        print("kingcords", i, j)
        horsemoves=[(2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2)]
        queenmoves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]    
        for move in horsemoves:
            mi, mj=move[0], move[1]
            if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                if self.game_matrix[i+mi][j+mj].team==enemy_id and self.game_matrix[i+mi][j+mj].id==3:
                    self.check_moves.append((i+move[0], j+move[1]))
                    self.threats+=1
        for move in queenmoves:
            temp_negs=[]
            def recursive_move_find(i, j, format):
                mi=format[0]
                mj=format[1]
                if 0<=i+mi<self.table_size and 0<=j+mj<self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==-1:
                        #print("did", i+mi, j+mj)
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
            recursive_move_find(i, j, move)
        def enemy_king_checks(i, j):
            if self.game_matrix[i][j].id==6 and self.game_matrix[i][j].team==enemy_id:
                return True
            return False
        if tile.id==6:
            dist=0
        else: 
            dist=1
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
            for move in queenmoves:
                mi, mj=move[0], move[1]
                if 0<=i+mi<=7 and 0<=j+mj<=7:
                    if enemy_king_checks(i+mi, j+mj):
                        self.check_moves.append((i, j))
                        break   
        return self.check_moves
            
    def own_check(self, tile, move_list, y, x):
        print("tileid", tile.id)
        if tile.id==6:
            return move_list
        self.temp_save=tile
        self.game_matrix[y][x]=Tile(0, -1, self.type_list)
        self.check_moves=[]
        i,j=self.king_spots[tile.team][0], self.king_spots[tile.team][1]
        self.check_moves=self.is_threatened(tile, i, j)
        self.game_matrix[y][x]=self.temp_save
        self.temp_save=None
        #if tile.id==6:
            #return self.king_help_moves(move_list)
        return self.viable_moves(move_list)
    
    def find_moves(self, tile, i, j):
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
                        print(self.check_moves, i+mi, j+mj)
                        king_moves.append((i+mi, j+mj))
        self.game_matrix[i][j]=self.temp_save
        self.temp_save=None
        return king_moves
                    
                    
    def pawn_moves(self, tile, i, j):
        print("pwn")
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
game=Game_Engine()