import unittest
from tools.tactics import Battle, Regiment, Side, Terrain, demo


class BattleTests(unittest.TestCase):
    def test_demo_map(self):
        self.assertIn("B", demo().render())
        self.assertIn("R", demo().render())

    def test_movement_and_limits(self):
        b = demo()
        b.move("Blue Infantry", 2, 2)
        self.assertEqual(b.units["Blue Infantry"].x, 2)
        with self.assertRaises(ValueError):
            b.move("Blue Infantry", 4, 0)

    def test_occupied_tile_rejected(self):
        b = demo()
        with self.assertRaises(ValueError):
            b.move("Blue Infantry", 1, 1)

    def test_river_blocks_slow_unit(self):
        b = Battle([[Terrain.PLAIN, Terrain.RIVER]],
                   {"A": Regiment("A", Side.BLUE, 0, 0, 200, movement=2)})
        with self.assertRaises(ValueError):
            b.move("A", 1, 0)

    def test_attack_has_casualties_and_morale(self):
        b = demo()
        before = b.units["Red Infantry"].morale
        casualties, _ = b.attack("Blue Infantry", "Red Infantry")
        self.assertGreater(casualties, 0)
        self.assertLess(b.units["Red Infantry"].morale, before)

    def test_charge_exposes_attacker(self):
        b = demo()
        b.attack("Blue Cavalry", "Red Archers", charge=True)
        self.assertEqual(b.units["Blue Cavalry"].morale, 96)

    def test_positional_flanking(self):
        t = [[Terrain.PLAIN] * 3 for _ in range(3)]
        b = Battle(t, {
            "A": Regiment("A", Side.BLUE, 0, 1, 400),
            "B": Regiment("B", Side.BLUE, 1, 0, 400),
            "X": Regiment("X", Side.RED, 1, 1, 500),
        })
        self.assertTrue(b.attack("A", "X")[1])

    def test_no_friendly_fire(self):
        b = demo()
        with self.assertRaises(ValueError):
            b.attack("Blue Infantry", "Blue Cavalry")

    def test_reproducible(self):
        a, b = demo(), demo()
        self.assertEqual(a.attack("Blue Infantry", "Red Infantry"),
                         b.attack("Blue Infantry", "Red Infantry"))

    def test_winner_after_rout(self):
        b = demo()
        self.assertIsNone(b.winner())
        for u in b.units.values():
            if u.side == Side.RED:
                u.routed = True
        self.assertEqual(b.winner(), Side.BLUE)

    def test_ai_turn(self):
        b = demo()
        b.ai_turn(Side.RED)
        self.assertEqual(b.turn, 2)


if __name__ == "__main__":
    unittest.main()
