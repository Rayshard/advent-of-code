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

#[derive(Debug)]
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

fn parse_map_and_path(reader: &mut BufReader<File>) -> io::Result<(Map, Path)> {
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

fn move_in_dir((x, y): (i64, i64), dir: &Direction, map: &Map) -> Option<(i64, i64)> {
    let target_pos = match dir {
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
    };

    let (target_pos, target_tile) = if let Some(tile) = map.tiles.get(&target_pos) {
        (&target_pos, tile)
    } else {
        match dir {
            Direction::Up => (0..map.num_rows)
                .rev()
                .find_map(|row| map.tiles.get_key_value(&(target_pos.0, row as i64)))
                .unwrap(),
            Direction::Down => (0..map.num_rows)
                .find_map(|row| map.tiles.get_key_value(&(target_pos.0, row as i64)))
                .unwrap(),
            Direction::Left => (0..map.num_columns)
                .rev()
                .find_map(|column| map.tiles.get_key_value(&(column as i64, target_pos.1)))
                .unwrap(),
            Direction::Right => (0..map.num_columns)
                .find_map(|column| map.tiles.get_key_value(&(column as i64, target_pos.1)))
                .unwrap(),
        }
    };

    match target_tile {
        Tile::Open => Some(*target_pos),
        Tile::Wall => None,
    }
}

fn trace(path: &Path, map: &Map) -> ((i64, i64), Direction) {
    let (mut position, mut direction) = (map.start, Direction::Right);

    //println!("{:?}", position);

    for action in path {
        match action {
            Movement::Walk(amount) => {
                for _ in 1..=*amount {
                    match move_in_dir(position, &direction, &map) {
                        Some(new_pos) => {
                            position = new_pos;
                            //println!("{:?}", position);
                        }
                        None => break,
                    }
                }
            }
            Movement::RotateClockwise => direction = direction.rotate_clockwise(),
            Movement::RotateCounterClockwise => direction = direction.rotate_counterclockwise(),
        }
    }

    (position, direction)
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let mut reader = BufReader::new(file);

    let (map, path) = parse_map_and_path(&mut reader)?;

    // Part 1
    let ((column, row), direction) = trace(&path, &map);
    let direction_value = match direction {
        Direction::Up => 3,
        Direction::Down => 1,
        Direction::Left => 2,
        Direction::Right => 0,
    };

    println!("{}", 1000 * (row + 1) + 4 * (column + 1) + direction_value);
    Ok(())
}
