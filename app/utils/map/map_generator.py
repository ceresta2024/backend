from random import choice
from math import floor

import app.utils.map.map_entities as map_entities
import app.utils.map.map_growth as map_growth


def init_map(gmap):
    map_x, map_y = gmap.size
    for cell_x in range(map_x):
        for cell_y in range(map_y):
            gmap.set_cell(map_entities.Field, cell_x, cell_y)


def generate_block(gmap, block_settings):
    map_growth.plant_seeds(
        gmap, map_entities.Field, block_settings.seeds_amount, map_entities.Pavement
    )

    characters = map_growth.create_characters(5, 2)

    map_growth.grow_seeds(
        gmap,
        characters,
        map_entities.Field,
        map_entities.Pavement,
        block_settings.growth_rate,
    )


def generate_pit(gmap, pit_settings):
    map_growth.plant_seeds(
        gmap,
        map_entities.Pit,
        pit_settings.seeds_amount,
        map_entities.Field,
    )

    characters = map_growth.create_characters(
        5, 2, directions=[(-1, 0), (0, 1), (-1, 1), (1, -1)]
    )

    map_growth.grow_seeds(
        gmap,
        characters,
        map_entities.Pit,
        map_entities.Field,
        pit_settings.growth_rate,
    )


def generate_tunnel(gmap, tunnel_settings):
    map_growth.plant_seeds(
        gmap,
        map_entities.Tunnel,
        tunnel_settings.seeds_amount,
        map_entities.Field,
    )

    characters = map_growth.create_characters(
        5, 2, directions=[(-1, 0), (0, 1), (-1, 1), (1, -1)]
    )

    map_growth.grow_seeds(
        gmap,
        characters,
        map_entities.Tunnel,
        map_entities.Field,
        tunnel_settings.growth_rate,
    )


def is_good_wall_direction(gmap, parent_cell, direction):
    cell_x = parent_cell[0] + direction[0]
    cell_y = parent_cell[1] + direction[1]

    if not map_growth.is_inside_map(gmap, cell_x, cell_y):
        return False

    is_good_neighbour_count = (
        map_growth.get_neighbors_count(gmap, map_entities.Wall, cell_x, cell_y) < 2
    )
    is_pavement = isinstance(gmap.map_objects[cell_x][cell_y], map_entities.Pavement)

    return is_good_neighbour_count and not is_pavement


def generate_wall(gmap, wall_settings):
    directions = [(1, -1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (-1, 1)]

    for _ in range(wall_settings.wall_seeds_count):
        fields = gmap.get_map_objects(map_entities.Field)
        if not fields:
            return
        field = choice(fields)
        cell_x = field[0]
        cell_y = field[1]

        gmap.set_cell(map_entities.Wall, cell_x, cell_y)

        for _ in range(wall_settings.wall_length):
            rand_direction = choice(directions)
            max_tries = 20
            tries_count = 0
            while not is_good_wall_direction(gmap, (cell_x, cell_y), rand_direction):
                rand_direction = choice(directions)
                tries_count = tries_count + 1
                if tries_count > max_tries:
                    break
            if tries_count > max_tries:
                break
            cell_x = cell_x + rand_direction[0]
            cell_y = cell_y + rand_direction[1]

            gmap.set_cell(map_entities.Wall, cell_x, cell_y)


def generate_grass(gmap, grass_settings):
    map_growth.plant_seeds_where(
        gmap,
        map_entities.Grass,
        floor(grass_settings.seeds_amount / 3 * 2),
        map_entities.Field,
        adjacent_types=[map_entities.Pit],
    )
    map_growth.plant_seeds_among(
        gmap,
        map_entities.Grass,
        floor(grass_settings.seeds_amount / 3 * 1),
        map_entities.Field,
        map_entities.Field,
    )

    characters = map_growth.create_characters(5, 4)

    map_growth.grow_seeds(
        gmap,
        characters,
        map_entities.Grass,
        map_entities.Field,
        grass_settings.growth_rate,
    )


def generate_thorn(gmap, thorn_settings):
    map_growth.plant_seeds_where(
        gmap,
        map_entities.Thorn,
        floor(thorn_settings.seeds_amount / 5 * 3),
        map_entities.Field,
        adjacent_types=[map_entities.Wall],
    )
    map_growth.plant_seeds_where(
        gmap,
        map_entities.Thorn,
        floor(thorn_settings.seeds_amount / 5 * 1),
        map_entities.Field,
        adjacent_types=[map_entities.Grass],
    )
    map_growth.plant_seeds_among(
        gmap,
        map_entities.Thorn,
        floor(thorn_settings.seeds_amount / 5 * 1),
        map_entities.Field,
        map_entities.Field,
    )

    characters = map_growth.create_characters(5, 6)

    map_growth.grow_seeds_random(
        gmap,
        characters,
        map_entities.Thorn,
        map_entities.Field,
        thorn_settings.growth_rate,
    )


def generate_map(map_settings):
    gmap = map_entities.GameMap(
        map_settings.name, map_settings.size[0], map_settings.size[1]
    )

    init_map(gmap)
    # generate_block(gmap, map_settings.block_settings)
    generate_wall(gmap, map_settings.wall_settings)
    generate_grass(gmap, map_settings.grass_settings)
    generate_pit(gmap, map_settings.pit_settings)
    generate_tunnel(gmap, map_settings.tunnel_settings)
    generate_thorn(gmap, map_settings.thorn_settings)

    return gmap


def get_gmap_array(map_settings):
    gmap = generate_map(map_settings)
    data = []
    height, width = map_settings.size
    for _ in range(width):
        data.append([0 for _ in range(height)])
    for map_objects_row in gmap.map_objects:
        for map_object in map_objects_row:
            y, x = map_object.position
            data[x][y] = map_settings.pos_type[map_object.name]
    return data
