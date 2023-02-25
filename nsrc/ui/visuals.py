import pygame
from ui.input import Input_Handler as inputs
class Renderer():
    def __init__(self, size, tilesize, matrix, starter):
        self.size=size
        self.tile_size=tilesize
        self.sprite_size=int((tilesize-20)/10)
        self.game_matrix=matrix
        self.input_handler=inputs(self.tile_size)
        self.starter=starter
        self.clock=pygame.time.Clock()
        self.define_colors()
        self.define_sprite_shapes()
        self.screen=pygame.display.set_mode((self.size*self.tile_size, self.size*self.tile_size))
        self.whole_update_screen()
    def define_colors(self):
        self.white="#dedad7"
        self.white_border="#c4bbb5"
        self.black="#050505"
        self.black_border="#1c1a18"
        self.light_bg="#ab6b33"
        self.dark_bg="#5c3614"
    def bg_col_picker(self, i, j):
        """generates the zigzag color pattern
        """
        if i%2==0:
            if j%2==0:
                return self.light_bg
            return self.dark_bg
        else:
            if j%2==0:
                return self.dark_bg
            return self.light_bg
        
    def tile_draw(self, height, width):
        """ draws the square in the given cords with correct color
        """
        col=self.bg_col_picker(height, width)
        pygame.draw.rect(self.screen, col,[width*self.tile_size, height*self.tile_size, self.tile_size, self.tile_size])
    
    def piece_draw(self, piece_id, team_id, height, width):
        """ draws the correct piece based on id, team and cords given. Draws the piece based on the matrix given in self.sprite_list
        """
        def sprite_draw(i, j, col):
            pygame.draw.rect(self.screen, col,[(width)*self.tile_size+j*self.sprite_size+10, (height)*self.tile_size+i*self.sprite_size+10, self.sprite_size, self.sprite_size])
        if team_id==self.starter:
            col=self.white
            bcol=self.white_border
        else:
            col=self.black
            bcol=self.black_border
        i,j=0,0
        for row in self.sprite_list[piece_id]:
            j=0
            for val in row:
                if val==1:
                    sprite_draw(i, j, col)
                elif val==2:
                    sprite_draw(i, j, bcol)
                j+=1
            i+=1
    def whole_update_screen(self):
        """ draws the entire chessboard
        """
        i,j=0,0
        for row in self.game_matrix:
            j=0
            
            for tile in row:
                if tile.id!=0:
                    
                    self.tile_draw(i, j)
                    self.piece_draw(tile.id, tile.team, i, j)
                else:
                    self.tile_draw(i, j)
                j+=1
            i+=1
        self.update_screen()
    
    
        
    def draw_possible_moves(self, move):
        """ draws a centered circle in the given cords
        """
        pygame.draw.circle(self.screen, "#363433",[int(move[1]*self.tile_size+self.tile_size/2), int(move[0]*self.tile_size+self.tile_size/2)], int(self.tile_size/8))
        
    def reset_tile(self, cords):
        """ used to remove move indicators from board or to update wanted tiles adter move
        """
        i=cords[0]
        j=cords[1]
        tile=self.game_matrix[i][j]
        if tile.id!=0:
                    
            self.tile_draw(i, j)
            self.piece_draw(tile.id, tile.team, i, j)
        else:
            self.tile_draw(i, j)
    def update_screen(self):
        """used to update the screen or to give response to pygame so that it doesnt keep freezing (annoying)
        """
        pygame.display.update()
        
    
    
    
    
    def define_sprite_shapes(self):
        #long list for chess pieces
        self.sprite_list=[
            0,
            #PAWN
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 1, 0, 0, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
            ],
            #BISHOP
            [
                [0, 0, 0, 2, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 2, 0, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 1, 0, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],
            ],
            #KNIGHT
            [
                [0, 0, 0, 0, 2, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 1, 1, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 1, 0],
                [0, 0, 0, 2, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
            ],
            #ROOK
            [
                [0, 2, 2, 0, 2, 2, 0, 2, 2, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 2, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 2, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 2, 1, 0, 0, 0, 0, 1, 1, 0],
            ],
            #QUEEN
            [
                [0, 0, 2, 0, 2, 1, 0, 2, 0, 0],
                [0, 2, 0, 0, 2, 1, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],
            ],
            #KING
            [
                [2, 0, 0, 0, 2, 1, 0, 0, 0, 2],
                [0, 2, 0, 2, 1, 1, 1, 0, 2, 0],
                [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 1, 0],
            ]
        ]
                
    
