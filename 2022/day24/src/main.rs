use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
enum Direction {
    Left,
    Right,
    Up,
    Down,
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum Tile {
    Empty,
    Blizzard(Vec<Direction>),
}

type Position = (i64, i64);

#[derive(Clone, PartialEq, Eq)]
struct Map {
    tiles: HashMap<Position, Tile>,
}

impl Map {
    pub fn new() -> Self {
        Self {
            tiles: HashMap::new(),
        }
    }
}

impl std::hash::Hash for Map {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        todo!()
    }
}

#[derive(Hash, Eq, PartialEq)]
struct State {
    player: Position,
    map: Map,
}

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

fn possible_nexts(state: &State, blizzard_max_position: &Position) -> Vec<State> {
    let mut new_map = Map::new();

    // Generate new map
    for (pos, tile) in &state.map.tiles {
        match tile {
            Tile::Empty => {
                if !new_map.tiles.contains_key(pos) {
                    new_map.tiles.insert(*pos, Tile::Empty);
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

                    match new_map.tiles.get_mut(&target_pos) {
                        Some(Tile::Empty) | None => {
                            new_map
                                .tiles
                                .insert(target_pos, Tile::Blizzard(vec![dir.clone()]));

                            if !new_map.tiles.contains_key(pos) {
                                new_map.tiles.insert(*pos, Tile::Empty);
                            }
                        }
                        Some(Tile::Blizzard(dirs)) => {
                            dirs.push(dir.clone());
                        }
                    };
                }
            }
        }
    }

    // Get possible next positions
    [
        state.player.clone(),
        get_target_position(state.player.clone(), Direction::Up),
        get_target_position(state.player.clone(), Direction::Down),
        get_target_position(state.player.clone(), Direction::Left),
        get_target_position(state.player.clone(), Direction::Right),
    ]
    .iter()
    .filter_map(|target_pos| match new_map.tiles.get(target_pos) {
        Some(Tile::Empty) => Some(State {
            player: target_pos.clone(),
            map: new_map.clone(),
        }),
        Some(Tile::Blizzard(_)) | None => None,
    })
    .collect()
}

fn simulate(states: Vec<State>, end: Position) -> usize {
    let mut states = states;
    let mut num_iterations = 0;
    let blizzard_max_position = (end.0, end.1 - 1);

    let seen_states = HashSet::<State>::new();

    loop {
        num_iterations += 1;

        let mut new_states = vec![];

        for state in states
            .iter()
            .flat_map(|state| possible_nexts(state, &blizzard_max_position))
        {
            if state.player == end {
                return num_iterations;
            } else if !seen_states.contains(&state) {
                new_states.push(state);
            }
        }

        states = new_states;
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let tiles = reader
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

    let start = tiles
        .iter()
        .min_by(|a, b| a.0 .1.cmp(&b.0 .1))
        .unwrap()
        .0
        .clone();
    let end = tiles
        .iter()
        .max_by(|a, b| a.0 .1.cmp(&b.0 .1))
        .unwrap()
        .0
        .clone();

    println!("{}", simulate(vec![State { player: start, map: Map { tiles } }], end));

    Ok(())
}
