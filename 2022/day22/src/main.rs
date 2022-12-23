use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone)]
enum Tile {
    Open,
    Wall,
}

#[derive(Debug)]
enum Movement {
    Walk(usize),
    RotateClockwise,
    RotateCounterClockwise,
}

#[derive(Debug, Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

struct Map {
    tiles: HashMap<(i64, i64), Tile>,
    num_rows: usize,
    num_columns: usize,
    start: (i64, i64),
}

impl Map {
    pub fn new(rows: Vec<(i64, Vec<Tile>)>) -> Map {
        let start = (rows[0].0, 0);
        let num_rows = rows.len();
        let num_columns = rows
            .iter()
            .map(|(row_start, row_tiles)| *row_start as usize + row_tiles.len())
            .max()
            .unwrap();
        let tiles =
            rows.iter()
                .enumerate()
                .flat_map(|(y, (x_start, row_tiles))| {
                    row_tiles.iter().enumerate().map(move |(i_row, tile)| {
                        ((x_start + i_row as i64, y as i64), tile.clone())
                    })
                })
                .collect();

        Map {
            tiles,
            num_rows,
            num_columns,
            start,
        }
    }
}

type Path = Vec<Movement>;

impl Direction {
    pub fn rotate_clockwise(&self) -> Direction {
        match self {
            Direction::Up => Direction::Right,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
            Direction::Right => Direction::Down,
        }
    }

    pub fn rotate_counterclockwise(&self) -> Direction {
        match self {
            Direction::Up => Direction::Left,
            Direction::Down => Direction::Right,
            Direction::Left => Direction::Down,
            Direction::Right => Direction::Up,
        }
    }
}

fn parse_rows_and_path(reader: &mut BufReader<File>) -> io::Result<(Map, Path)> {
    let mut rows = Vec::<(i64, Vec<Tile>)>::new();
    let path = loop {
        let mut line = String::new();

        if reader.read_line(&mut line).unwrap() == 1 {
            reader.read_line(&mut line)?;

            break line
                .trim_start()
                .chars()
                .flat_map(|c| {
                    if c == 'R' || c == 'L' {
                        vec![',', c, ',']
                    } else {
                        vec![c]
                    }
                })
                .collect::<String>()
                .split(',')
                .map(|s| match s {
                    "R" => Movement::RotateClockwise,
                    "L" => Movement::RotateCounterClockwise,
                    s => Movement::Walk(s.parse().unwrap()),
                })
                .collect();
        } else {
            let row = line
                .chars()
                .enumerate()
                .filter_map(|(i, c)| match c {
                    '.' => Some((i as i64, Tile::Open)),
                    '#' => Some((i as i64, Tile::Wall)),
                    _ => None,
                })
                .collect::<Vec<_>>();

            rows.push((row[0].0, row.iter().map(|(_, tile)| tile.clone()).collect()));
        }
    };

    Ok((Map::new(rows), path))
}

type VoidTileMapper = fn((i64, i64), &Direction, &Map) -> ((i64, i64), Direction);

fn part1_void_tile_mapper(
    (target_column, target_row): (i64, i64),
    dir: &Direction,
    map: &Map,
) -> ((i64, i64), Direction) {
    let pos = match dir {
        Direction::Up => (0..map.num_rows)
            .rev()
            .find_map(|row| map.tiles.get_key_value(&(target_column, row as i64))),
        Direction::Down => {
            (0..map.num_rows).find_map(|row| map.tiles.get_key_value(&(target_column, row as i64)))
        }
        Direction::Left => (0..map.num_columns)
            .rev()
            .find_map(|column| map.tiles.get_key_value(&(column as i64, target_row))),
        Direction::Right => (0..map.num_columns)
            .find_map(|column| map.tiles.get_key_value(&(column as i64, target_row))),
    }
    .unwrap()
    .0;

    (*pos, dir.clone())
}

fn part2_void_tile_mapper(
    (target_column, target_row): (i64, i64),
    dir: &Direction,
    _: &Map,
) -> ((i64, i64), Direction) {
    println!("{:?}", (target_column, target_row, dir));

    match (target_column, target_row, dir) {
        (col, row, Direction::Up) if row == -1 && col >= 50 && col <= 99 => {
            ((0, 150 + col - 50), Direction::Right)
        }
        (col, row, Direction::Left) if col == -1 && row >= 150 && row <= 199 => {
            ((50 + row - 150, 0), Direction::Down)
        }
        (col, row, Direction::Up) if row == -1 && col >= 100 && col <= 149 => {
            ((col - 100, 199), Direction::Up)
        }
        (col, row, Direction::Down) if row == 200 && col >= 0 && col <= 49 => {
            ((100 + col, 0), Direction::Down)
        }
        (col, row, Direction::Right) if col == 150 && row >= 0 && row <= 49 => {
            ((99, 149 - row), Direction::Left)
        }
        (col, row, Direction::Right) if col == 100 && row >= 100 && row <= 149 => {
            ((149, 149 - row), Direction::Left)
        }
        (col, row, Direction::Down) if row == 50 && col >= 100 && col <= 149 => {
            ((99, 50 + col - 100), Direction::Left)
        }
        (col, row, Direction::Right) if col == 100 && row >= 50 && row <= 99 => {
            ((100 + row - 50, 49), Direction::Up)
        }
        (col, row, Direction::Left) if col == 49 && row >= 0 && row <= 49 => {
            ((0, 149 - row), Direction::Right)
        }
        (col, row, Direction::Left) if col == -1 && row >= 100 && row <= 149 => {
            ((50, 149 - row), Direction::Right)
        }
        (col, row, Direction::Left) if col == 49 && row >= 50 && row <= 99 => {
            ((row - 50, 100), Direction::Down)
        }
        (col, row, Direction::Up) if row == 99 && col >= 0 && col <= 49 => {
            ((50, col + 50), Direction::Right)
        }

        (col, row, Direction::Down) if row == 150 && col >= 50 && col <= 99 => {
            ((49, 150 + col - 50), Direction::Left)
        }
        (col, row, Direction::Right) if col == 50 && row >= 150 && row <= 199 => {
            ((50 + row - 150, 149), Direction::Up)
        }
        config => panic!("{config:?}"),
    }
}

fn move_in_dir(
    (x, y): (i64, i64),
    dir: &Direction,
    map: &Map,
    void_tile_mapper: VoidTileMapper,
) -> Option<((i64, i64), Direction)> {
    let target_pos = match dir {
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
    };

    let (target_pos, new_dir) = if map.tiles.contains_key(&target_pos) {
        (target_pos, dir.clone())
    } else {
        void_tile_mapper(target_pos, dir, &map)
    };

    match map.tiles.get(&target_pos) {
        Some(Tile::Open) => Some((target_pos, new_dir)),
        Some(Tile::Wall) => None,
        None => panic!("{target_pos:?}"),
    }
}

fn trace(path: &Path, map: &Map, void_tile_mapper: VoidTileMapper) -> i64 {
    let (mut position, mut direction) = (map.start, Direction::Right);

    for action in path {
        match action {
            Movement::Walk(amount) => {
                for _ in 1..=*amount {
                    match move_in_dir(position, &direction, &map, void_tile_mapper) {
                        Some((new_pos, new_dir)) => {
                            position = new_pos;
                            direction = new_dir;
                        }
                        None => break,
                    }
                }
            }
            Movement::RotateClockwise => direction = direction.rotate_clockwise(),
            Movement::RotateCounterClockwise => direction = direction.rotate_counterclockwise(),
        }
    }

    let direction_value = match direction {
        Direction::Up => 3,
        Direction::Down => 1,
        Direction::Left => 2,
        Direction::Right => 0,
    };

    1000 * (position.1 + 1) + 4 * (position.0 + 1) + direction_value
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let mut reader = BufReader::new(file);

    let (map, path) = parse_rows_and_path(&mut reader)?;

    println!("{}", trace(&path, &map, part1_void_tile_mapper));
    println!("{}", trace(&path, &map, part2_void_tile_mapper));

    Ok(())
}
