import sys

from engine import Game_Engine as GE 
import random as r
from time import time
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

def random_game_state_generator(density, size):
    row=[0]*size
    matrix=[]
    type_list=[0, Pawn(), Bishop(), Knight(), Rook(), Queen(), King()]
    for _ in range(size):
        matrix.append(row.copy())
    matrix[0][3]=Tile(6, 1, type_list)
    matrix[0][3].moved=True
    matrix[7][3]=Tile(6, 0, type_list)
    matrix[7][3].moved=True
    for i in range(size):
        for j in range(size):
            def lottery():
                int=r.randint(0,density)
                if int in [0,1]:
                    int2=r.randint(1,5)
                    return (int, int2)
                else:
                    return (-1, 0)
            if matrix[i][j]==0:
                ret=lottery()
                team, id=ret[0], ret[1]
                matrix[i][j]=Tile(id, team, type_list)
                matrix[i][j].i=i
                matrix[i][j].j=j    
                matrix[i][j].moved=True
    for i in range(size):
        print(matrix[i])
    return matrix
                    
class Stress_tester():
    def __init__(self):
        self.engine=GE(("bot", 2), ("bot", 2), False, 0)
        self.density=15
        self.all_tests()
    def new_game_state(self):
        return random_game_state_generator(self.density, self.engine.table_size)
        
    def all_tests(self):
        times=[]
        for _ in range(5):
            times.append([])
        print(times)
        for _ in range(10):
            matrix=self.new_game_state()
            for i in range(1, 6):
                print(i)
                self.engine.player_one.depth_setter(i)
                start=time()
                self.engine.player_one.gain_turn([], matrix, [], [])
                stop=time()
                times[i-1].append(stop-start)
                print(times)
        sum_l=[]
        for row in times:
            sum_l.append(sum(row)/10)
        print(sum_l)
s=Stress_tester()