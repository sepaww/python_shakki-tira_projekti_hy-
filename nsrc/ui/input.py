import pygame
import sys
class Input_Handler():
    def __init__(self, tilesize):
        self.current_input=self.main_inputs
        self.tile_size=tilesize
    def exit_input(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def main_inputs(self):
        mouse=pygame.mouse.get_pos()
        i=int(mouse[0]/self.tile_size)
        j=int(mouse[1]/self.tile_size)
        for event in pygame.event.get():
            self.exit_input(event)
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                return "r"
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_u:
                return "u"
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    return i, j
    def response_inputs(self):
        for event in pygame.event.get():
            self.exit_input(event)        
    def kill_self(self):
        pygame.quit()