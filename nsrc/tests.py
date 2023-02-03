import unittest
from engine import Game_Engine as GE
from ui.visuals import Renderer
class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.game_engine = GE()

    def test_get_piece_at(self):
        piece = self.game_engine.get_piece_at(0, 0)
        self.assertEqual(piece.id, 1)
        self.assertEqual(piece.team, 0)

    def test_valid_move(self):
        valid_move = self.game_engine.valid_move(0, 0, 2, 0)
        self.assertTrue(valid_move)

        invalid_move = self.game_engine.valid_move(0, 0, 3, 3)
        self.assertFalse(invalid_move)

    def test_make_move(self):
        self.game_engine.make_move(0, 0, 2, 0)
        piece = self.game_engine.get_piece_at(2, 0)
        self.assertEqual(piece.id, 1)
        self.assertEqual(piece.team, 0)

        piece = self.game_engine.get_piece_at(0, 0)
        self.assertEqual(piece, None)

if __name__ == '__main__':
    unittest.main()
    

from ui.visuals import Renderer

class TestRenderer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.renderer = Renderer(10, 100, [[None for _ in range(10)] for _ in range(10)], 0)

    def test_bg_col_picker(self):
        col = self.renderer.bg_col_picker(0, 0)
        self.assertEqual(col, self.renderer.light_bg)

        col = self.renderer.bg_col_picker(0, 1)
        self.assertEqual(col, self.renderer.dark_bg)

        col = self.renderer.bg_col_picker(1, 0)
        self.assertEqual(col, self.renderer.dark_bg)

    def test_piece_draw(self):
        # Add piece to matrix and check if piece is drawn correctly
        # (Test requires manual inspection of the display window)
        pass

    def test_reset_tile(self):
        # Add piece to matrix, reset the tile, and check if it's removed
        # (Test requires manual inspection of the display window)
        pass