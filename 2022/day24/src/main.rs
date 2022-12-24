use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone)]
enum Direction {
    Left,
    Right,
    Up,
    Down,
}

#[derive(Debug, Clone)]
enum Tile {
    Empty,
    Blizzard(Vec<Direction>),
}

type Position = (i64, i64);
type Map = HashMap<Position, Tile>;

fn get_target_position((x, y): Position, dir: Direction) -> Position {
    match dir {
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
    }
}

fn get_target_position_wrapped(
    (x, y): Position,
    dir: Direction,
    (min_x, min_y): &Position,
    (max_x, max_y): &Position,
) -> Position {
    let (target_x, target_y) = match dir {
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
    };

    if &target_x < min_x {
        (*max_x, target_y)
    } else if &target_x > max_x {
        (*min_x, target_y)
    } else if &target_y < min_y {
        (target_x, *max_y)
    } else if &target_y > max_y {
        (target_x, *min_y)
    } else {
        (target_x, target_y)
    }
}

fn update_map(old: Map, blizzard_max_position: &Position) -> Map {
    let mut new_map = Map::new();

    // Generate new map
    for (pos, tile) in &old {
        match tile {
            Tile::Empty => {
                if !new_map.contains_key(pos) {
                    new_map.insert(*pos, Tile::Empty);
                }
            }
            Tile::Blizzard(dirs) => {
                for dir in dirs {
                    let target_pos = get_target_position_wrapped(
                        *pos,
                        dir.clone(),
                        &(1, 1),
                        blizzard_max_position,
                    );

                    match new_map.get_mut(&target_pos) {
                        Some(Tile::Empty) | None => {
                            new_map.insert(target_pos, Tile::Blizzard(vec![dir.clone()]));
                        }
                        Some(Tile::Blizzard(dirs)) => {
                            dirs.push(dir.clone());
                        }
                    };

                    if !new_map.contains_key(pos) {
                        new_map.insert(*pos, Tile::Empty);
                    }
                }
            }
        }
    }

    new_map
}

fn possible_nexts(current_pos: &Position, map: &Map) -> Vec<Position> {
    [
        current_pos.clone(),
        get_target_position(current_pos.clone(), Direction::Up),
        get_target_position(current_pos.clone(), Direction::Down),
        get_target_position(current_pos.clone(), Direction::Left),
        get_target_position(current_pos.clone(), Direction::Right),
    ]
    .iter()
    .filter_map(|target_pos| match map.get(target_pos) {
        Some(Tile::Empty) => Some(target_pos.clone()),
        Some(Tile::Blizzard(_)) | None => None,
    })
    .collect()
}

fn simulate(start: Position, end: Position, map: &Map) -> usize {
    let mut players = HashSet::from([start]);
    let mut num_iterations = 0;
    let blizzard_max_position = (end.0, end.1 - 1);
    let mut map = map.clone();

    loop {
        num_iterations += 1;

        let mut new_players = HashSet::new();
        map = update_map(map, &blizzard_max_position);

        for player in players
            .iter()
            .flat_map(|player| possible_nexts(player, &map))
        {
            if player == end {
                return num_iterations;
            }

            new_players.insert(player);
        }

        players = new_players;
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let map = reader
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.unwrap()
                .chars()
                .enumerate()
                .filter_map(|(x, c)| {
                    let pos = (x as i64, y as i64);
                    let tile = match c {
                        '.' => Tile::Empty,
                        '>' => Tile::Blizzard(vec![Direction::Right]),
                        '<' => Tile::Blizzard(vec![Direction::Left]),
                        '^' => Tile::Blizzard(vec![Direction::Up]),
                        'v' => Tile::Blizzard(vec![Direction::Down]),
                        _ => return None,
                    };

                    return Some((pos, tile));
                })
                .collect::<Vec<_>>()
        })
        .collect::<HashMap<_, _>>();

    let start = map
        .iter()
        .min_by(|a, b| a.0 .1.cmp(&b.0 .1))
        .unwrap()
        .0
        .clone();
    let end = map
        .iter()
        .max_by(|a, b| a.0 .1.cmp(&b.0 .1))
        .unwrap()
        .0
        .clone();

    println!("{}", simulate(start, end, &map));

    Ok(())
}
