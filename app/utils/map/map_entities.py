from copy import copy


class GameMapObject:
    name = "map_object"

    def __init__(self, x, y):
        self.position = (x, y)


class Field(GameMapObject):
    name = "field"


class Pavement(GameMapObject):
    name = "pavement"


class Pit(GameMapObject):
    name = "pit"


class Tunnel(GameMapObject):
    name = "tunnel"


class Wall(GameMapObject):
    name = "wall"


class Grass(GameMapObject):
    name = "grass"


class Thorn(GameMapObject):
    name = "thorn"


class PitSettings:
    seeds_amount = 2
    growth_rate = 2


class TunnelSettings:
    seeds_amount = 2
    growth_rate = 2


class WallSettings:
    wall_seeds_count = 5
    wall_length = 30


class BlockSettings:
    seeds_amount = 2
    growth_rate = 2


class GrassSettings:
    seeds_amount = 2
    growth_rate = 2


class ThornSettings:
    seeds_amount = 4
    growth_rate = 3


class GameMap:
    def __init__(self, name, size_x, size_y):
        self.name = name
        self.size = (size_x, size_y)
        self.map_objects = []
        self.map_type_objects = {}

        for x_cord in range(size_x):
            map_objects_row = []
            for y_cord in range(size_y):
                map_objects_row.append(GameMapObject(x_cord, y_cord))

            self.map_objects.append(map_objects_row)

    def set_cell(self, cell_type, x_cord, y_cord):
        if (
            type(self.map_objects[x_cord][y_cord]) in self.map_type_objects
            and (x_cord, y_cord)
            in self.map_type_objects[type(self.map_objects[x_cord][y_cord])]
        ):
            self.map_type_objects[type(self.map_objects[x_cord][y_cord])].remove(
                (x_cord, y_cord)
            )
        if not cell_type in self.map_type_objects:
            self.map_type_objects[cell_type] = []
        self.map_type_objects[cell_type].append((x_cord, y_cord))

        self.map_objects[x_cord][y_cord] = cell_type(x_cord, y_cord)

    def get_map_objects(self, object_type):
        if not object_type in self.map_type_objects:
            return []

        return copy(self.map_type_objects[object_type])


class GameMapSettings:
    name = "Great Beet GameMap"
    size = (100, 100)
    block_settings = BlockSettings()
    wall_settings = WallSettings()
    grass_settings = GrassSettings()
    pit_settings = PitSettings()
    tunnel_settings = TunnelSettings()
    thorn_settings = ThornSettings()
