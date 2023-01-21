import sys
sys.setrecursionlimit(10000)
import random as r
import math as m
from heapq import heappush, heappop
import pygame
import time
class Tile():
    def __init__(self, i, j):
        self.minebool=False
        self.cords=(i,j)
        self.id=0
        self.flagged=False
        self.cleared=False
        
class Renderer():
    def __init__(self, botb):
        pygame.init()
        self.mtable=[]
        self.gamesize=33
        self.rest=[]
        riv=[1]*(self.gamesize+1)
        for _ in range(self.gamesize+1):
            self.rest.append(riv.copy())
        self.update_speed=10
        self.flagcount=0
        self.clearcount=0
        self.meaningfuls=[]
        self.need=False
        pygame.display.set_caption("minefield")
        self.minecol="#cf2013"
        self.search=self.wmassclear
        self.minecornercol="#400c08"
        self.mineamount=200
        self.tilesize=int(1000/self.gamesize)
        self.size=self.gamesize*self.tilesize
        self.screen=pygame.display.set_mode((self.size, self.size))
        self.mouse=pygame.mouse
        self.clock=pygame.time.Clock()
        self.clock2=pygame.time.Clock()
        self.font=pygame.font.SysFont("comicsans",round(self.tilesize/2)+1)
        self.color="#2f3640"
        id_riv=[]
        self.help_id_list=[]
        for _ in range(self.size+1):
            id_riv.append([])
        for _ in range(self.size):
            self.help_id_list.append(id_riv.copy())
        self.solvebool=botb
        self.flbool=True
        self.lastuncs=[]
        self.cornercolor="#1f2329"
        self.flagcolor="#963315"
        self.loop=True
        self.setup()
        self.screening()
        pygame.display.update() 
        self.update()
    def flipmass(self):
         
        if self.search==self.dmassclear:
            print("flip width") 
            self.search=self.wmassclear 
        else:
            print("flip depth") 
            self.search=self.dmassclear
    def setup(self):
        for i in range(self.gamesize):
            self.mtable.append([])
            for j in range(self.gamesize):
                self.mtable[i].append(Tile(i, j))
        self.miner()   
    def remine(self):
        y=r.randint(0,self.gamesize-1)            
        x=r.randint(0,self.gamesize-1)
        if self.mtable[y][x].minebool:
                self.remine()
        else: self.mtable[y][x].minebool=True
    def miner(self):
        for i in range(self.mineamount):
            y=r.randint(0,self.gamesize-1)            
            x=r.randint(0,self.gamesize-1)
            if self.mtable[y][x].minebool:
                self.remine()
            self.mtable[y][x].minebool=True
        self.idcalc()
        
    def idcalc(self):
        for i in range(self.gamesize):
            for j in range(self.gamesize):
                if self.mtable[i][j].minebool==False:
                    if i>0 and j>0:
                        if self.mtable[i-1][j-1].minebool: 
                            self.mtable[i][j].id+=1
                    if i>0:
                        if self.mtable[i-1][j].minebool: 
                            self.mtable[i][j].id+=1
                    if j>0:
                        if self.mtable[i][j-1].minebool: 
                            self.mtable[i][j].id+=1
                    if i>0 and j<self.gamesize-1:
                        if self.mtable[i-1][j+1].minebool: 
                            self.mtable[i][j].id+=1
                    if j<self.gamesize-1:
                        if self.mtable[i][j+1].minebool: 
                            self.mtable[i][j].id+=1
                    if i<self.gamesize-1:
                        if self.mtable[i+1][j].minebool: 
                            self.mtable[i][j].id+=1
                    if i<self.gamesize-1 and j<self.gamesize-1:
                        if self.mtable[i+1][j+1].minebool: 
                            self.mtable[i][j].id+=1
                    if j>0 and i<self.gamesize-1:
                        if self.mtable[i+1][j-1].minebool: 
                            self.mtable[i][j].id+=1
                        
    def flag(self, y, x):
        if self.mtable[y][x].cleared==False and self.mtable[y][x].flagged==False:
            self.rest[y][x]=0
            self.mtable[y][x].flagged=True
            self.flagcount+=1
        elif self.mtable[y][x].flagged:
            self.mtable[y][x].flagged=False
            self.rest[y][x]=1
            self.flagcount-=1
        self.single_screening(y, x)
    def helpclear(self, x, y):
        if x>0 and y>0:
            if self.mtable[y-1][x-1].cleared==False and self.mtable[y-1][x-1].minebool==False:
                self.mclearer(y-1, x-1)
                if self.mtable[y-1][x-1].id==0:
                    self.dmassclear(x-1, y-1)
        if x<self.gamesize-1 and y>0:
            if self.mtable[y-1][x+1].cleared==False and self.mtable[y-1][x+1].minebool==False:
                self.mclearer(y-1, x+1)
                if self.mtable[y-1][x+1].id==0:
                    self.dmassclear(x+1, y-1)
        if x<self.gamesize-1 and y<self.gamesize-1:
            if self.mtable[y+1][x+1].cleared==False and self.mtable[y+1][x+1].minebool==False:
                self.mclearer(y+1, x+1)
                if self.mtable[y+1][x+1].id==0:
                    self.dmassclear(x+1, y+1)
        if x>0 and y<self.gamesize-1:
            if self.mtable[y+1][x-1].cleared==False and self.mtable[y+1][x-1].minebool==False:
                self.mclearer(y+1, x-1)
                if self.mtable[y+1][x-1].id==0:
                    self.dmassclear(x-1, y+1)
    def wmassclear(self, x, y):
        
        todos=[]
        i=0
        heappush(todos, (i,y, x))
        while len(todos)>0:
            
            todo=heappop(todos)
            i=todo[0]
            y=todo[1]
            x=todo[2]
            if self.mtable[y][x].flagged:
                self.mtable[y][x].flagged=False
                self.flagcount-=1
            if self.gamesize-1>x:
                #print(r)
                if self.mtable[y][x+1].cleared==False and self.mtable[y][x+1].minebool==False:
                    self.mclearer(y, x+1)
                    if self.mtable[y][x+1].id==0:
                        heappush(todos,(i+1,y,x+1))
                      
                        
            if self.gamesize-1>y:
                if self.mtable[y+1][x].cleared==False and self.mtable[y+1][x].minebool==False:
                    self.mclearer(y+1, x)
                    if self.mtable[y+1][x].id==0:
                     
                       heappush(todos, (i+1,y+1,x))
                      
            if y>0:
                if self.mtable[y-1][x].cleared==False and self.mtable[y-1][x].minebool==False:
                    self.mclearer(y-1, x)
                    if self.mtable[y-1][x].id==0:
                      
                        heappush(todos, (i+1,y-1,x))
                        
            if x>0:
                if self.mtable[y][x-1].cleared==False and self.mtable[y][x-1].minebool==False:
                    self.mclearer(y, x-1)
                    if self.mtable[y][x-1].id==0:
                       
                        heappush(todos, (i+1,y,x-1))
                       
            
            if x>0 and y>0:
                if self.mtable[y-1][x-1].cleared==False and self.mtable[y-1][x-1].minebool==False:
                    self.mclearer(y-1, x-1)
                    if self.mtable[y-1][x-1].id==0:
                      
                        heappush(todos, (i+1,y-1,x-1))
                     
            if x<self.gamesize-1 and y>0:
                if self.mtable[y-1][x+1].cleared==False and self.mtable[y-1][x+1].minebool==False:
                    self.mclearer(y-1, x+1)
                    if self.mtable[y-1][x+1].id==0:
                     
                        heappush(todos, (i+1,y-1,x+1))
                     
            if x<self.gamesize-1 and y<self.gamesize-1:
                if self.mtable[y+1][x+1].cleared==False and self.mtable[y+1][x+1].minebool==False:
                    self.mclearer(y+1, x+1)
                    if self.mtable[y+1][x+1].id==0:
                     
                        heappush(todos, (i+1,y+1,x+1))
                     
            if x>0 and y<self.gamesize-1:
                if self.mtable[y+1][x-1].cleared==False and self.mtable[y+1][x-1].minebool==False:
                    self.mclearer(y+1, x-1)
                    if self.mtable[y+1][x-1].id==0:
                      
                        heappush(todos, (i+1,y+1,x-1))
                      
    def dmassclear(self, x, y):
        if self.mtable[y][x].flagged:
            self.mtable[y][x].flagged=False
            self.flagcount-=1
        if self.gamesize-1>x:
            #print(r)
            if self.mtable[y][x+1].cleared==False and self.mtable[y][x+1].minebool==False:
                self.mclearer(y, x+1)
                if self.mtable[y][x+1].id==0:
                    self.dmassclear(x+1,y)
                    
        if self.gamesize-1>y:
            if self.mtable[y+1][x].cleared==False and self.mtable[y+1][x].minebool==False:
                self.mclearer(y+1, x)
                if self.mtable[y+1][x].id==0:
                    self.dmassclear(x,y+1)
        if y>0:
            if self.mtable[y-1][x].cleared==False and self.mtable[y-1][x].minebool==False:
                self.mclearer(y-1, x)
                if self.mtable[y-1][x].id==0:
                    self.dmassclear(x,y-1)
        if x>0:
            if self.mtable[y][x-1].cleared==False and self.mtable[y][x-1].minebool==False:
                self.mclearer(y, x-1)
                if self.mtable[y][x-1].id==0:
                    self.dmassclear(x-1,y)
        if self.mtable[y][x].id==0:
            self.helpclear(x, y)
    def mclearer(self, y, x):
        if self.mtable[y][x].cleared==False:
                    self.rest[y][x]=0
                    if self.mtable[y][x].flagged:
                        self.flagcount-=1
                        self.mtable[y][x].flagged=False
                    self.mtable[y][x].cleared=True
                    self.clearcount+=1
                    if self.mtable[y][x].minebool==True:
                        self.minereveal()
                    if self.mtable[y][x].id>0:
                        self.meaningfuls.append((y, x)) 
                    self.single_screening(y, x)
    def clearer(self, y, x):
        if self.mtable[y][x].cleared==False:
                    self.rest[y][x]=0
                    if self.mtable[y][x].flagged:
                        self.flagcount-=1
                        self.mtable[y][x].flagged=False
                    self.mtable[y][x].cleared=True
                    self.clearcount+=1
                    if self.mtable[y][x].minebool==True:
                        self.minereveal(y, x)
                    
                    if self.mtable[y][x].id==0:
                        self.search(x, y)  
                    else: self.meaningfuls.append((y, x))    
                    self.single_screening(y, x) 
                    pygame.display.update()        
    def inputs(self):
        pos=self.mouse.get_pos()
        y=m.floor(pos[1]/self.tilesize)
        x=m.floor(pos[0]/self.tilesize)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    self.clearer(y, x)

                    return True
                elif event.button==3:
                    self.flag(y, x)
                    return True
            if event.type==pygame.KEYDOWN and event.key==pygame.K_c:
                self.wholeclear()
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                self.loop=False
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_s:
                self.solvebool=not self.solvebool
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_f:
                self.flipmass()
        return False 
    def minereveal(self, y, x):
        for i in range(self.gamesize):
            for j in range(self.gamesize):
                if self.mtable[i][j].minebool:
                    self.mtable[i][j].cleared=True
        looop=True
        self.screening()
        self.single_screening(y, x)
        alk=time.time()
        while looop:
            lop=time.time()
            pygame.display.update()
            self.clock.tick(10)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_c:
                    self.wholeclear()
                    
                if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                    self.loop=False
                    looop=False
                if (event.type==pygame.KEYDOWN and event.key==pygame.K_r) or (lop-alk>=1 and self.solvebool):
                        self.loop=False
                        looop=False
    def wholeclear(self):
        for i in range(self.gamesize):
            for j in range(self.gamesize):
                self.mtable[i][j].cleared=True
        self.screening()
        pygame.display.update()
    def numbergiver(self, i, j):
        ident=self.mtable[i][j].id
        def numberdrawer(col):
            txt = self.font.render(str(ident), True, col)
            self.screen.blit(txt, (j*self.tilesize+round(self.tilesize/3), i*self.tilesize+round(self.tilesize/4)))
        if ident==1:
            numberdrawer("#074beb")
        if ident==2:
            numberdrawer("#16ba0d")
        if ident==3:
            numberdrawer("#cbcf13")
        if ident==4:
            numberdrawer("#cfa013")
        if ident==5:
            numberdrawer("#cf7113")
        if ident==6:
            numberdrawer("#cf4813")
        if ident==7:
            numberdrawer("#cf2013")
        if ident==8:
            numberdrawer("#eb0793")
        
    def cleardraw(self, height, width):
        if self.mtable[height][width].minebool:
            pygame.draw.rect(self.screen, self.minecol,[width*self.tilesize-1, height*self.tilesize-1, self.tilesize-1, self.tilesize-1])
        else: pygame.draw.rect(self.screen, self.color,[width*self.tilesize-1, height*self.tilesize-1, self.tilesize-1, self.tilesize-1])
        
    def tiledraw(self, height, width, col, cornercol):
        pygame.draw.rect(self.screen, col,[width+1, height+1, self.tilesize-1, self.tilesize-1])
        pygame.draw.rect(self.screen, cornercol, [width, height, self.tilesize, self.tilesize], 5, 3)           
    def single_screening(self, i, j):
        pygame.draw.rect(self.screen, self.color, (j*self.tilesize, i*self.tilesize,self.tilesize,self.tilesize))
        if self.mtable[i][j].cleared:
            if self.mtable[i][j].minebool:
                self.tiledraw(i*self.tilesize, j*self.tilesize, "#a61299", "#610b59")
            else:
                self.cleardraw(i, j)
                if self.mtable[i][j].id>0:
                    self.numbergiver(i, j)
        elif self.mtable[i][j].flagged:
            self.tiledraw(i*self.tilesize, j*self.tilesize, self.flagcolor, self.minecornercol)    
        else:
            self.tiledraw(i*self.tilesize, j*self.tilesize, self.color, self.cornercolor)
        pygame.display.update()
    def screening(self):
        self.screen.fill(self.color)
        for i in range(self.gamesize):
            for j in range(self.gamesize):
                if self.mtable[i][j].cleared:
                    self.cleardraw(i, j)
                    if self.mtable[i][j].id>0:
                        self.numbergiver(i, j)
                elif self.mtable[i][j].flagged:
                    self.tiledraw(i*self.tilesize, j*self.tilesize, self.flagcolor, self.minecornercol)    
                else:
                    self.tiledraw(i*self.tilesize, j*self.tilesize, self.color, self.cornercolor)
        pygame.display.update() 
        #print(self.flagcount, self.clearcount)
    def wcheck(self):
        if self.clearcount+self.flagcount==self.gamesize*self.gamesize and self.flagcount==self.mineamount:
            pygame.draw.rect(self.screen, "green", (int(self.tilesize*self.gamesize/2),int(self.tilesize*self.gamesize/2), 300, 300)) 
            txt = self.font.render("iso W", True, "black")
            self.screen.blit(txt, (int(self.gamesize/2*self.tilesize), int(self.gamesize/2*self.tilesize)))
            looop=True
            alk=time.time()
            while looop:
                lop=time.time()
                pygame.display.update()
                self.clock.tick(10)
                if lop-alk>=2 and self.solvebool:
                    self.loop=False
                    looop=False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if (event.type==pygame.KEYDOWN and event.key==pygame.K_r) or (lop-alk>=1 and self.solvebool):
                        self.loop=False
                        looop=False
    ###################################################
    #MAIN LOOP#        
    def update(self):
        while self.loop:
            self.clock.tick(self.update_speed)
            self.need=self.inputs()
            #if self.need:
                #self.screening()
                
            if self.solvebool:
                self.SolverBot()
            self.wcheck()
            pygame.display.update()
            
            
            
    def is_meaningful(self, y, x):
        uncleared=0
        mines=0
        uncleared_ind=[]
        pos_mine_ind=[]
        if self.gamesize-1>x:
            if self.mtable[y][x+1].flagged:
                mines+=1
            elif self.mtable[y][x+1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y, x+1))
            
                    
        if self.gamesize-1>y:
            if self.mtable[y+1][x].flagged:
                mines+=1
            elif self.mtable[y+1][x].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y+1, x))
            
        if y>0:
            if self.mtable[y-1][x].flagged:
                mines+=1
            elif self.mtable[y-1][x].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y-1, x))
            

        if x>0:
            if self.mtable[y][x-1].flagged:
                mines+=1
            elif self.mtable[y][x-1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y, x-1))
            
        if x>0 and y>0:
            if self.mtable[y-1][x-1].flagged:
                mines+=1
            elif self.mtable[y-1][x-1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y-1, x-1))
            

        if x<self.gamesize-1 and y>0:
            if self.mtable[y-1][x+1].flagged:
                mines+=1
            elif self.mtable[y-1][x+1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y-1, x+1))
            

        if x<self.gamesize-1 and y<self.gamesize-1:
            if self.mtable[y+1][x+1].flagged:
                mines+=1
            elif self.mtable[y+1][x+1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y+1, x+1))
            

        if x>0 and y<self.gamesize-1:
            if self.mtable[y+1][x-1].flagged:
                mines+=1
            elif self.mtable[y+1][x-1].cleared==False:
                uncleared+=1
                pos_mine_ind.append((y+1, x-1))
                
        ind=self.mtable[y][x].id-mines
        if uncleared==ind:
            for cords in pos_mine_ind:
                self.flag(cords[0], cords[1])
            return True
        elif ind==0:
            for cords in pos_mine_ind:
                self.clearer(cords[0], cords[1])
            return True
        
        return False
                
    def rand_click(self):
        
        y=r.randint(0,self.gamesize-1)            
        x=r.randint(0,self.gamesize-1)
        if self.rest[y][x]>=1:   
            print("guessing")
            self.clearer(y, x) 
        else: self.rand_click()
    def firstlast(self):
        id_riv=[]
        self.lastuncs=[]
        for _ in range(self.size+1):
            id_riv.append([])
        for _ in range(self.size):
            self.help_id_list.append(id_riv.copy())
        for i in range(self.gamesize):
            for j in range(self.gamesize):  
                if self.mtable[i][j].flagged:
                    self.rest[i][j]=0 
                elif self.rest[i][j]>=1:
                    self.rest[i][j]=1
                    self.lastuncs.append((i,j))
    def foundmorethan2(self, y, x):
        if self.gamesize-1>x:
            if self.rest[y][x+1]==3:
                return True
                      
        if self.gamesize-1>y:
            if self.rest[y+1][x]==3:
                return True
            
        if y>0:
            if self.rest[y-1][x]==3:
                return True
            
        if x>0:
            if self.rest[y][x-1]==3:
                return True
        return False
    def lastclear(self):
        found=False
        for cords in self.meaningfuls:
            y=cords[0]
            x=cords[1]
            uncleared=0
            mines=0

            pos_mine_ind=[]
            if self.gamesize-1>x:
                if self.mtable[y][x+1].flagged:
                    mines+=1
                elif self.mtable[y][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y, x+1))
                
                        
            if self.gamesize-1>y:
                if self.mtable[y+1][x].flagged:
                    mines+=1
                elif self.mtable[y+1][x].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x))
                
            if y>0:
                if self.mtable[y-1][x].flagged:
                    mines+=1
                elif self.mtable[y-1][x].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x))
                

            if x>0:
                if self.mtable[y][x-1].flagged:
                    mines+=1
                elif self.mtable[y][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y, x-1))
                
            if x>0 and y>0:
                if self.mtable[y-1][x-1].flagged:
                    mines+=1
                elif self.mtable[y-1][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x-1))
                

            if x<self.gamesize-1 and y>0:
                if self.mtable[y-1][x+1].flagged:
                    mines+=1
                elif self.mtable[y-1][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x+1))
                

            if x<self.gamesize-1 and y<self.gamesize-1:
                if self.mtable[y+1][x+1].flagged:
                    mines+=1
                elif self.mtable[y+1][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x+1))
                

            if x>0 and y<self.gamesize-1:
                if self.mtable[y+1][x-1].flagged:
                    mines+=1
                elif self.mtable[y+1][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x-1))
                    
            ind=self.mtable[y][x].id-mines
            for cords in pos_mine_ind:
                if self.rest[cords[0]][cords[1]]==1:
                    self.rest[cords[0]][cords[1]]=2
            if uncleared==2 and ind==1:
                eka=pos_mine_ind[0]
                toka=pos_mine_ind[1]
                if eka!=toka:
                    self.rest[eka[0]][eka[1]]=3
                    self.help_id_list[eka[0]][eka[1]].append((cords[0], cords[1], toka))
                    self.rest[toka[0]][toka[1]]=3
                    self.help_id_list[toka[0]][toka[1]].append((cords[0], cords[1], eka))
                
        for cords in self.meaningfuls:
            y=cords[0]
            x=cords[1]
            uncleared=0
            mines=0
            pos_mine_ind=[]
            if self.gamesize-1>x:
                if self.mtable[y][x+1].flagged:
                    mines+=1
                elif self.mtable[y][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y, x+1))
                
                        
            if self.gamesize-1>y:
                if self.mtable[y+1][x].flagged:
                    mines+=1
                elif self.mtable[y+1][x].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x))
                
            if y>0:
                if self.mtable[y-1][x].flagged:
                    mines+=1
                elif self.mtable[y-1][x].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x))
                

            if x>0:
                if self.mtable[y][x-1].flagged:
                    mines+=1
                elif self.mtable[y][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y, x-1))
                
            if x>0 and y>0:
                if self.mtable[y-1][x-1].flagged:
                    mines+=1
                elif self.mtable[y-1][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x-1))
                

            if x<self.gamesize-1 and y>0:
                if self.mtable[y-1][x+1].flagged:
                    mines+=1
                elif self.mtable[y-1][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y-1, x+1))
                

            if x<self.gamesize-1 and y<self.gamesize-1:
                if self.mtable[y+1][x+1].flagged:
                    mines+=1
                elif self.mtable[y+1][x+1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x+1))
                

            if x>0 and y<self.gamesize-1:
                if self.mtable[y+1][x-1].flagged:
                    mines+=1
                elif self.mtable[y+1][x-1].cleared==False:
                    uncleared+=1
                    pos_mine_ind.append((y+1, x-1))
                    
            ind=self.mtable[y][x].id-mines  
            if len(pos_mine_ind)>=3 and ind==1:
                for cords in pos_mine_ind:
                    if self.rest[cords[0]][cords[1]]==3 and found==False:
                        for val in self.help_id_list[cords[0]][cords[1]]:
                            if val[2] in pos_mine_ind:
                                print(cords[0],cords[1],val[2][0],val[2][1])
                                for another in self.help_id_list[val[2][0]][val[2][1]]:
                                    if another[2]!=val[2]:
                                        if found==False and val[0]==another[0] and val[1]==another[1] and another[2] in  pos_mine_ind:
                                            print(val[2], another[2])
                                            pos_mine_ind.remove(val[2])
                                            pos_mine_ind.remove(another[2])
                                            print("didit")
                                            found=True
                                            print(pos_mine_ind)
                                            for rest in pos_mine_ind:
                                                self.clearer(rest[0], rest[1])
        
            if found==False and  len(pos_mine_ind)>=3 and ind+1==uncleared:
                for cords in pos_mine_ind:
                    if self.rest[cords[0]][cords[1]]==3 and found==False:
                        for val in self.help_id_list[cords[0]][cords[1]]:
                            if val[2] in pos_mine_ind:
                                print(cords[0],cords[1],val[2][0],val[2][1])
                                for another in self.help_id_list[val[2][0]][val[2][1]]:
                                    if another[2]!=val[2]:
                                        if found==False and val[0]==another[0] and val[1]==another[1] and another[2] in  pos_mine_ind:
                                            print(val[2], another[2])
                                            pos_mine_ind.remove(val[2])
                                            pos_mine_ind.remove(another[2])
                                            print("didit mine")
                                            found=True
                                            print(pos_mine_ind)
                                            for rest in pos_mine_ind:
                                                self.flag(rest[0], rest[1])
            if found==False and len(pos_mine_ind)==3:
                calc=0
                for val in pos_mine_ind:
                    if self.rest[val[0]][val[1]]==3:
                        calc+=1
                if calc==3:
                    print("triple cope")
                    pos_mine_ind=sorted(pos_mine_ind)
                    if ind==2:
                        temp=pos_mine_ind.pop(0)
                        self.flag(temp[0], temp[1])   
                        temp=pos_mine_ind.pop(0)
                        self.clearer(temp[0], temp[1])  
                        temp=pos_mine_ind.pop(0)
                        self.flag(temp[0], temp[1])   
                    elif ind==1:
                        temp=pos_mine_ind.pop(0)
                        self.clearer(temp[0], temp[1])   
                        temp=pos_mine_ind.pop(0)
                        self.flag(temp[0], temp[1])  
                        temp=pos_mine_ind.pop(0)
                        self.clearer(temp[0], temp[1])   
                    found=True
                        
                
                                    
                            
        if found:
            return
        
        #print(self.lastuncs)
        if self.flagcount>=int(self.mineamount/2):
            print("guessing")
            pygame.time.wait(1000)
            for value in self.lastuncs:
                if self.rest[value[0]][value[1]]==1:
                    self.clearer(value[0],value[1])
                    return
            for value in self.lastuncs:
                if self.rest[value[0]][value[1]]==2:
                    self.clearer(value[0],value[1])
                    return
        else: self.rand_click()
        print("random choice")
        cords=r.choice(self.lastuncs)
        self.clearer(cords[0], cords[1])                
                
            
              
    def SolverBot(self):
        i=0
        no_change=True
        while i <= len(self.meaningfuls)-1:
            
            
            ret=self.is_meaningful(self.meaningfuls[i][0], self.meaningfuls[i][1])
            if ret:
                
                self.meaningfuls.pop(i)
                i-=1
                no_change=False
                self.flbool=True
            i+=1
            #self.screening()
        self.flbool=True
        if no_change:
            
                if self.flbool:
                    self.flbool=False
                    self.firstlast()
                    
                self.lastclear()
        #print(len(self.meaningfuls))
botbool=True

while True:               
    peli=Renderer(botbool)
        

          
        