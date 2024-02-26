# pylint: disable=invalid-name
from random import randint, choice


class Character:
    def __init__(self, directions):
        self.directions = directions

    def get_directions(self):
        return self.directions


def create_characters(
    characters_amount,
    character_directions_amount,
    directions=None,
):
    directions = directions or [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (-1, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
    ]
    characters = []

    for _ in range(characters_amount):
        character_directions = []
        for _ in range(character_directions_amount):
            random_direction = randint(0, len(directions) - 1)
            character_directions.append(directions[random_direction])
        characters.append(Character(character_directions))

    return characters


def is_inside_map(gmap, x, y):
    if x < 0 or y < 0:
        return False

    map_size_x, map_size_y = gmap.size
    if (x > map_size_x - 1) or (y > map_size_y - 1):
        return False

    return True


def get_neighbors_count(gmap, map_object, x, y):
    neighbors_count = 0

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    for direction_x, direction_y in directions:
        neighbor_x = x + direction_x
        neighbor_y = y + direction_y
        if is_inside_map(gmap, neighbor_x, neighbor_y) and isinstance(
            gmap.map_objects[neighbor_x][neighbor_y], map_object
        ):
            neighbors_count += 1

    return neighbors_count


def throw_coin():
    if randint(0, 1) == 1:
        return True
    return False


def get_grow_directions(gmap, directions, seed_x, seed_y, field_type):
    grow_directions = []
    for direction_x, direction_y in directions:
        grow_x = seed_x + direction_x
        grow_y = seed_y + direction_y
        if is_inside_map(gmap, grow_x, grow_y) and isinstance(
            gmap.map_objects[grow_x][grow_y], field_type
        ):
            grow_directions.append((grow_x, grow_y))

    return grow_directions


def plant_seeds(gmap, seed_type, seeds_amount, field_type):
    planted_seeds = []

    for _ in range(seeds_amount):
        map_size_x, map_size_y = gmap.size
        random_pos_x = randint(1, map_size_x - 2)
        random_pos_y = randint(1, map_size_y - 2)
        while (
            not isinstance(gmap.map_objects[random_pos_x][random_pos_y], field_type)
            or (random_pos_x, random_pos_y) in planted_seeds
        ):
            random_pos_x = randint(1, map_size_x - 2)
            random_pos_y = randint(1, map_size_y - 2)
        gmap.set_cell(seed_type, random_pos_x, random_pos_y)
        planted_seeds.append((random_pos_x, random_pos_y))


def is_adjacent_to(gmap, x, y, adjacent_types):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]

    for adjacent_type in adjacent_types:
        is_adjacent_to_type = False

        for direction_x, direction_y in directions:
            neighbor_x = x + direction_x
            neighbor_y = y + direction_y
            if is_inside_map(gmap, neighbor_x, neighbor_y) and isinstance(
                gmap.map_objects[neighbor_x][neighbor_y], adjacent_type
            ):
                is_adjacent_to_type = True
                break

        if not is_adjacent_to_type:
            return False

    return True


def is_adjacent_only_to(gmap, x, y, adjacent_only_to_type):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]

    for direction_x, direction_y in directions:
        neighbor_x = x + direction_x
        neighbor_y = y + direction_y
        if is_inside_map(gmap, neighbor_x, neighbor_y) and not isinstance(
            gmap.map_objects[neighbor_x][neighbor_y], adjacent_only_to_type
        ):
            return False

    return True


def plant_seeds_among(gmap, seed_type, seeds_amount, field_type, among_type):
    for _ in range(seeds_amount):
        fields = gmap.get_map_objects(field_type)
        if not fields:
            return
        field = choice(fields)
        cell_x = field[0]
        cell_y = field[1]

        max_tries = 120
        tries_count = 0
        while not is_adjacent_only_to(gmap, cell_x, cell_y, among_type):
            field = choice(fields)
            cell_x = field[0]
            cell_y = field[1]
            tries_count += 1
            if tries_count > max_tries:
                break
        if tries_count > max_tries:
            break

        gmap.set_cell(seed_type, cell_x, cell_y)


def plant_seeds_where(
    gmap,
    seed_type,
    seeds_amount,
    field_type,
    adjacent_types=None,
    not_adjacent_types=None,
):
    adjacent_types = adjacent_types or []
    not_adjacent_types = not_adjacent_types or []

    for _ in range(seeds_amount):
        fields = gmap.get_map_objects(field_type)
        if not fields:
            return
        field = choice(fields)
        cell_x = field[0]
        cell_y = field[1]

        max_tries = 120
        tries_count = 0
        while (
            adjacent_types and not is_adjacent_to(gmap, cell_x, cell_y, adjacent_types)
        ) or (
            not_adjacent_types
            and is_adjacent_to(gmap, cell_x, cell_y, not_adjacent_types)
        ):
            field = choice(fields)
            cell_x = field[0]
            cell_y = field[1]
            tries_count += 1
            if tries_count > max_tries:
                break
        if tries_count > max_tries:
            break

        gmap.set_cell(seed_type, cell_x, cell_y)


def grow_seeds(gmap, characters, seed_type, field_type, grow_rate):
    for _ in range(grow_rate):
        for x, y in gmap.get_map_objects(seed_type):
            rand_character = randint(0, len(characters) - 1)
            grow_directions = get_grow_directions(
                gmap, characters[rand_character].get_directions(), x, y, field_type
            )
            if not grow_directions:
                continue

            rand_direction_index = randint(0, len(grow_directions) - 1)
            grow_x, grow_y = grow_directions[rand_direction_index]
            gmap.set_cell(seed_type, grow_x, grow_y)


def grow_seeds_random(gmap, characters, seed_type, field_type, grow_rate):
    for _ in range(grow_rate):
        for x, y in gmap.get_map_objects(seed_type):
            if throw_coin():
                continue
            rand_character = randint(0, len(characters) - 1)
            grow_directions = get_grow_directions(
                gmap, characters[rand_character].get_directions(), x, y, field_type
            )
            if not grow_directions:
                continue

            rand_direction_index = randint(0, len(grow_directions) - 1)
            grow_x, grow_y = grow_directions[rand_direction_index]
            gmap.set_cell(seed_type, grow_x, grow_y)
