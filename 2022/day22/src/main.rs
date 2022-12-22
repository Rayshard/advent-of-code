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

type Map = Vec<(i64, Vec<Tile>)>;
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

fn get_tile((x, y): (i64, i64), map: &Vec<(i64, Vec<Tile>)>) -> (Tile, (i64, i64)) {
    let y = if y < 0 {
        map.len() as i64 + y % map.len() as i64
    } else {
        y % map.len() as i64
    } as usize;

    let (row_start, row_tiles) = &map[y];

    let row_length = row_start + row_tiles.len() as i64;
    let x = if x < 0 {
        row_length + x % row_length
    } else {
        x % row_length
    } as usize
        % row_tiles.len();

    (row_tiles[x].clone(), (row_start + x as i64, y as i64))
}

fn parse_map_and_path(reader: &mut BufReader<File>) -> io::Result<(Map, Path)> {
    let mut map = Vec::<(i64, Vec<Tile>)>::new();
    let mut path = Vec::<Movement>::new();

    loop {
        let mut line = String::new();

        if reader.read_line(&mut line).unwrap() == 1 {
            reader.read_line(&mut line)?;

            path = line
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

            break;
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

            map.push((row[0].0, row.iter().map(|(_, tile)| tile.clone()).collect()));
        }
    }

    Ok((map, path))
}

fn move_in_dir((x, y): (i64, i64), dir: &Direction, map: &Map) -> Option<(i64, i64)> {
    let target = match dir {
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
    };

    match get_tile(target, &map) {
        (Tile::Open, target) => Some(target),
        (Tile::Wall, _) => None,
    }
}

fn trace(path: &Path, map: &Map) -> ((i64, i64), Direction) {
    let (mut position, mut direction) = ((map[0].0, 0), Direction::Right);

    println!("{:?}", position);

    for action in path {
        match action {
            Movement::Walk(amount) => {
                for _ in 1..=*amount {
                    match move_in_dir(position, &direction, &map) {
                        Some(new_pos) => {
                            position = new_pos;
                            println!("{:?}", position);
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

    println!("{:?}", trace(&path, &map));
    Ok(())
}
