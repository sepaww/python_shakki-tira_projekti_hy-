from false_engine import FalseEngine as FE
import random as r
class TunnelVision_bot():
    def __init__(self, team, matrix, crit_list, piece_list, last_move, renderer):
        self.game_matrix=matrix
        self.team=team
        self.piece_list=piece_list
        self.is_bot=True
        self.table_size=len(self.game_matrix)-1
        self.tuple=(0,0)
        self.engine=FE(self.game_matrix, crit_list)
        self.last_move=last_move
        self.value_init()
    def gain_turn(self, check_list, game_matrix, king_moves, crit_list):
        self.game_matrix=game_matrix
        self.piece_list=[]
        move=[]
        self.find_pieces()
        max=-9999999
        best_move=None
        for piece in self.piece_list:  
            if piece.id!=6:
                move=self.engine.engine_operator(0, piece, piece.i, piece.j, (check_list, crit_list))
                
            else: move=king_moves
            piece_spot_value=self.threat_values(piece, piece.i, piece.j)
            for way in move:
                value=0
                value=self.general_values(piece, way[0], way[1])
                #value+=self.value_list[piece.id][0]
                value-=self.value_list[piece.id][1]
                if self.game_matrix[way[0]][way[1]].team not in [self.team, -1]:
                    value+=(self.value_list[self.game_matrix[way[0]][way[1]].id][1]*5)
                    if self.game_matrix[way[0]][way[1]].id==6:
                        value-=1000000000
                print(value) 
                some_move=(way[0], way[1], piece, piece.i, piece.j)
                if value>piece_spot_value:   
                    if value>max:
                        max=value
                        best_move=(way[0], way[1], piece, piece.i, piece.j)
        if best_move==None:
            return some_move
        print(max)
        
        #print(move)
        return best_move
    def choose_piece(self):
        return r.choice(self.piece_list)
    def find_pieces(self):
        for i in range(self.table_size+1):
            for j in range(self.table_size+1):
                if self.game_matrix[i][j].team==self.team:
                    self.piece_list.append(self.game_matrix[i][j])
                    
    def value_init(self):
        self.value_list=[(0,0), (2,3), (4,4), (4,4), (5,5), (5,7), (0,20)]
        
        self.y_values=[-20,-10,3,5,5,3,-10,-20]
        self.x_values=[-20,-10,3,5,5,3,-10,-20]
    
    def pawn_values(self,tile, i,j):
        temp_add=0
        if not tile.moved:
            temp_add+=20
        if self.team==0:
            if i+1<=7:
                if j+1<=7:
                    if self.game_matrix[i+1][j+1].team==self.team and self.game_matrix[i+1][j+1].id==1:
                        temp_add+=1
                if j-1>=0:
                    if self.game_matrix[i+1][j-1].team==self.team and self.game_matrix[i+1][j-1].id==1:
                        temp_add+=1
            if i-1>=0:
                if j+1<=7:
                    if self.game_matrix[i-1][j+1].id!=0:
                        temp_add+=3
                if j-1>=0:
                    if self.game_matrix[i-1][j-1].id!=0:
                        temp_add+=3
        else:
            if i+1<=7:
                if j+1<=7:
                    if self.game_matrix[i+1][j+1].id!=0:
                        temp_add+=3
                if j-1>=0:
                    if self.game_matrix[i+1][j-1].id!=0:
                        temp_add+=3
            if i-1>=0:
                if j+1<=7:
                    if self.game_matrix[i-1][j+1].team==self.team and self.game_matrix[i-1][j+1].id==1:
                        temp_add+=1
                if j-1>=0:
                    if self.game_matrix[i-1][j-1].team==self.team and self.game_matrix[i-1][j-1].id==1:
                        temp_add+=1
        return temp_add
    
    def general_values(self, tile, i ,j):
        add=0
        if tile.id==1:
            add+=self.pawn_values(tile,i,j)
        else:
            add+=self.eat_values(tile, i ,j)
        add+=self.threat_values(tile, i ,j)
        add+=self.positional_value(i ,j)
        return add
    
    def eat_values(self,tile, i ,j):
        temp_add=0
        if tile.team==1:
            enemy_id=0
        else:
            enemy_id=1
        if not tile.moved:
            temp_add+=10
        pi, pj=i,j
        for move in tile.type.moves:
            i, j=pi,pj
            adder=[0]
            def recursive_move_find(i, j, format):
                mi=format[0]
                mj=format[1]
                if 0<=i+mi<=self.table_size and 0<=j+mj<=self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==-1:
                        recursive_move_find(i+mi, j+mj, move)
                    elif self.game_matrix[i+mi][j+mj].team==enemy_id:
                        adder[0]+=self.value_list[self.game_matrix[i+mi][j+mj].id][1]
                    elif self.game_matrix[i+mi][j+mj].team==tile.team:
                        adder[0]+=(self.value_list[self.game_matrix[i+mi][j+mj].id][0]*2)
            if tile.id not in [3,6]:
                recursive_move_find(i, j, move)
                temp_add+=adder[0]
            
            else:
                mi, mj=move[0], move[1]
                if 0<=i+mi<=self.table_size and 0<=j+mj<=self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==enemy_id:
                        temp_add+=self.value_list[self.game_matrix[i+mi][j+mj].id][1]
                    elif self.game_matrix[i+mi][j+mj].team==tile.team:
                        temp_add+=self.value_list[self.game_matrix[i+mi][j+mj].id][0]
        temp_add-=self.value_list[tile.id][0]
        
        return temp_add  
    
    def give_enemy_id(self, tile):
        if tile.team==0:
                enemy_id=1
        elif tile.team==1:
            enemy_id=0
        else:
            enemy_id=self.curr_turn
        return enemy_id 
     
    def threat_values(self, tile, i ,j):
        temp_add=0
        enemy_id=self.give_enemy_id(tile)
        horsemoves=[(2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2)]
        queenmoves=[(1,1), (1,-1), (-1, 1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1)]    
        for move in horsemoves:
            mi, mj=move[0], move[1]
            if 0<=i+mi<=self.table_size and 0<=j+mj<=self.table_size:
                if self.game_matrix[i+mi][j+mj].team==enemy_id and self.game_matrix[i+mi][j+mj].id==3:
                    temp_add-=(self.value_list[self.game_matrix[i+mi][j+mj].id][1]+self.value_list[tile.id][0]+self.value_list[tile.id][0])
                elif self.game_matrix[i+mi][j+mj].team==tile.team and self.game_matrix[i+mi][j+mj].id==3:  
                    temp_add+=self.value_list[self.game_matrix[i+mi][j+mj].id][0]  
        pi, pj=i,j
        for move in queenmoves:
            i, j=pi,pj
            adder=[0]
            def recursive_move_find(i, j, format):
                mi=format[0]
                mj=format[1]
                if 0<=i+mi<=self.table_size and 0<=j+mj<=self.table_size:
                    if self.game_matrix[i+mi][j+mj].team==-1:
                        recursive_move_find(i+mi, j+mj, move)
                    elif self.game_matrix[i+mi][j+mj].team==enemy_id:
                        if (abs(mi)+abs(mj))%2==0:
                            if self.game_matrix[i+mi][j+mj].id in [2,5]:
                                adder[0]-=(self.value_list[self.game_matrix[i+mi][j+mj].id][1]+self.value_list[tile.id][0]+self.value_list[tile.id][0])
                        elif self.game_matrix[i+mi][j+mj].id in [5,4]:
                            adder[0]-=(self.value_list[self.game_matrix[i+mi][j+mj].id][1]+self.value_list[tile.id][0]+self.value_list[tile.id][0])
                    elif self.game_matrix[i+mi][j+mj].team==tile.team:
                        if (abs(mi)+abs(mj))%2==0:
                            if self.game_matrix[i+mi][j+mj].id in [2,5]:
                                adder[0]+=self.value_list[self.game_matrix[i+mi][j+mj].id][0]
                        elif self.game_matrix[i+mi][j+mj].id in [5,4]:
                            adder[0]+=self.value_list[self.game_matrix[i+mi][j+mj].id][0]
            recursive_move_find(i, j, move)
            temp_add+=adder[0]
        
        if enemy_id==1:
            if 0<=i-1:
                if 0<=j-1:
                    if self.game_matrix[i-1][j-1].id==1:
                        if self.game_matrix[i-1][j-1].team==enemy_id and self.game_matrix[i-1][j-1].id==1:
                            temp_add-=self.value_list[1][1]+(self.value_list[tile.id][1]*2)
                        elif self.game_matrix[i-1][j-1].team==tile.team:
                            temp_add+=self.value_list[1][0]
                if j+1<=self.table_size:
                    if self.game_matrix[i-1][j+1].id==1:
                        if self.game_matrix[i-1][j+1].team==enemy_id and self.game_matrix[i-1][j+1].id==1:
                            temp_add-=self.value_list[1][1]+(self.value_list[tile.id][1]*2)
                        elif self.game_matrix[i-1][j+1].team==tile.team:
                            temp_add+=self.value_list[1][0]
        else:
            if 0<i+1<=self.table_size:
                if 0<=j-1<=self.table_size:
                    if self.game_matrix[i+1][j-1].id==1:
                        if self.game_matrix[i+1][j-1].team==enemy_id and self.game_matrix[i+1][j-1].id==1:
                            temp_add-=self.value_list[1][1]+(self.value_list[tile.id][1]*2)
                        elif self.game_matrix[i+1][j-1].team==tile.team:
                            temp_add+=self.value_list[1][0]
                if j+1<=self.table_size:
                    if self.game_matrix[i+1][j+1].id==1:
                        if self.game_matrix[i+1][j+1].team==enemy_id:
                            temp_add-=self.value_list[1][1]+(self.value_list[tile.id][1]*2)
                        elif self.game_matrix[i+1][j+1].team==tile.team:
                            temp_add+=self.value_list[1][0]

        return temp_add

    def positional_value(self,i ,j):
        temp_add=0
        temp_add+=self.x_values[j]
        temp_add+=self.y_values[i]
        return temp_add