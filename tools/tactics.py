"""Deterministic miniature combat rules lab. Not connected to CK3 runtime."""
from dataclasses import dataclass, field
from enum import Enum
from random import Random


class Terrain(str, Enum):
    PLAIN = "plain"
    FOREST = "forest"
    HILL = "hill"
    RIVER = "river"


class Side(str, Enum):
    BLUE = "blue"
    RED = "red"


DEFENSE = {Terrain.PLAIN: 0, Terrain.FOREST: 2, Terrain.HILL: 3, Terrain.RIVER: 1}
COST = {Terrain.PLAIN: 1, Terrain.FOREST: 2, Terrain.HILL: 2, Terrain.RIVER: 3}


@dataclass
class Regiment:
    name: str
    side: Side
    x: int
    y: int
    soldiers: int
    attack: int = 8
    defense: int = 6
    morale: int = 100
    movement: int = 2
    commander: bool = False
    routed: bool = False

    @property
    def active(self):
        return self.soldiers > 0 and self.morale > 0 and not self.routed


@dataclass
class Battle:
    tiles: list[list[Terrain]]
    units: dict[str, Regiment]
    seed: int = 0
    turn: int = 1
    logs: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.tiles or not self.tiles[0] or any(len(r) != len(self.tiles[0]) for r in self.tiles):
            raise ValueError("invalid map")
        self.rng = Random(self.seed)
        occupied = set()
        for name, unit in self.units.items():
            if name != unit.name or not self.inside(unit.x, unit.y):
                raise ValueError("invalid unit placement")
            if (unit.x, unit.y) in occupied:
                raise ValueError("overlapping regiments")
            occupied.add((unit.x, unit.y))

    def inside(self, x, y):
        return 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[0])

    def occupant(self, x, y):
        return next((u for u in self.units.values()
                     if u.active and (u.x, u.y) == (x, y)), None)

    def distance(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def move(self, name, x, y):
        u = self.units[name]
        if not u.active or not self.inside(x, y):
            raise ValueError("invalid movement")
        if self.distance(u, Regiment("_", u.side, x, y, 1)) != 1:
            raise ValueError("only adjacent cardinal moves")
        if self.occupant(x, y) or COST[self.tiles[y][x]] > u.movement:
            raise ValueError("blocked or expensive tile")
        u.x, u.y = x, y
        self.logs.append(f"{name} -> {x},{y}")

    def hold(self, name):
        u = self.units[name]
        if not u.active:
            raise ValueError("inactive regiment")
        u.morale = min(100, u.morale + 5)
        self.logs.append(f"{name} holds")

    def attack(self, source, target, charge=False):
        a, d = self.units[source], self.units[target]
        if not a.active or not d.active or a.side == d.side or self.distance(a, d) != 1:
            raise ValueError("invalid attack")
        flank = any(u.name != a.name and u.side == a.side and u.active
                    and self.distance(u, d) == 1 for u in self.units.values())
        pressure = a.attack + self.rng.randint(0, 2) + (3 if flank else 0)
        pressure += (2 if charge else 0) + (1 if a.commander else 0)
        resistance = d.defense + DEFENSE[self.tiles[d.y][d.x]]
        casualties = min(d.soldiers, max(1, pressure - resistance) * max(1, a.soldiers // 100))
        d.soldiers -= casualties
        d.morale = max(0, d.morale - max(2, casualties // 15) - (5 if flank else 0))
        d.routed = d.morale == 0 or d.soldiers == 0
        if charge:
            a.morale = max(0, a.morale - 4)
            a.routed = a.morale == 0
        self.logs.append(f"{source} -> {target}: {casualties} casualties")
        return casualties, flank

    def winner(self):
        living = {u.side for u in self.units.values() if u.active}
        return next(iter(living)) if len(living) == 1 else None

    def ai_turn(self, side):
        for u in list(self.units.values()):
            if not u.active or u.side != side:
                continue
            enemies = sorted([e for e in self.units.values() if e.side != side and e.active],
                             key=lambda e: (self.distance(u, e), e.name))
            if enemies and self.distance(u, enemies[0]) == 1:
                self.attack(u.name, enemies[0].name)
            elif enemies:
                self.hold(u.name)
        self.turn += 1

    def render(self):
        marks = {Terrain.PLAIN: ".", Terrain.FOREST: "F", Terrain.HILL: "^", Terrain.RIVER: "~"}
        board = [[marks[t] for t in row] for row in self.tiles]
        for u in self.units.values():
            if u.active:
                board[u.y][u.x] = "B" if u.side == Side.BLUE else "R"
        return "\n".join(" ".join(row) for row in board)


def demo():
    tiles = [
        [Terrain.FOREST, Terrain.PLAIN, Terrain.HILL, Terrain.PLAIN, Terrain.FOREST],
        [Terrain.PLAIN, Terrain.PLAIN, Terrain.HILL, Terrain.PLAIN, Terrain.PLAIN],
        [Terrain.PLAIN, Terrain.PLAIN, Terrain.PLAIN, Terrain.PLAIN, Terrain.PLAIN],
    ]
    return Battle(tiles, {
        "Blue Infantry": Regiment("Blue Infantry", Side.BLUE, 1, 2, 360, commander=True),
        "Blue Cavalry": Regiment("Blue Cavalry", Side.BLUE, 3, 2, 140, attack=11),
        "Red Infantry": Regiment("Red Infantry", Side.RED, 1, 1, 500),
        "Red Archers": Regiment("Red Archers", Side.RED, 3, 1, 240),
    }, seed=42)


if __name__ == "__main__":
    b = demo()
    print("VVV RULES LAB (NOT IN CK3)")
    print(b.render())
    print("Infantry attack:", b.attack("Blue Infantry", "Red Infantry"))
    print("Cavalry charge:", b.attack("Blue Cavalry", "Red Archers", charge=True))
    print(b.render())
