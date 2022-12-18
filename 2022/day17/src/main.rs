use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

const MAP_WIDTH: i32 = 7;
pub type Position = (i32, i32);
pub enum Direction {
    Down,
    Left,
    Right,
}

pub enum Rock {
    Horizontal,
    Cross,
    BackwardL,
    Vertical,
    Box,
}

impl From<usize> for Rock {
    fn from(value: usize) -> Rock {
        match value % 5 {
            0 => Rock::Horizontal,
            1 => Rock::Cross,
            2 => Rock::BackwardL,
            3 => Rock::Vertical,
            4 => Rock::Box,
            _ => panic!(),
        }
    }
}

pub fn get_covered_tiles(x: i32, y: i32, rock: &Rock) -> Vec<Position> {
    match rock {
        Rock::Horizontal => vec![(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
        Rock::Cross => vec![
            (x + 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x + 2, y + 1),
            (x + 1, y + 2),
        ],
        Rock::BackwardL => vec![
            (x, y),
            (x + 1, y),
            (x + 2, y),
            (x + 2, y + 1),
            (x + 2, y + 2),
        ],
        Rock::Vertical => vec![(x, y), (x, y + 1), (x, y + 2), (x, y + 3)],
        Rock::Box => vec![(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)],
    }
}

pub fn get_ceiling(y: i32, rock: &Rock) -> i32 {
    match rock {
        Rock::Horizontal => y,
        Rock::Cross => y + 2,
        Rock::BackwardL => y + 2,
        Rock::Vertical => y + 3,
        Rock::Box => y + 1,
    }
}

pub fn try_move(
    rock: &Rock,
    position: Position,
    dir: Direction,
    map: &HashSet<Position>,
) -> Option<Position> {
    let (desired_x, desired_y) = match dir {
        Direction::Down => (position.0, position.1 - 1),
        Direction::Left => (position.0 - 1, position.1),
        Direction::Right => (position.0 + 1, position.1),
    };

    for pos in get_covered_tiles(desired_x, desired_y, rock) {
        if pos.0 < 0 || pos.0 >= MAP_WIDTH || pos.1 < 0 || map.contains(&pos) {
            return None;
        }
    }

    Some((desired_x, desired_y))
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);
    let mut map = HashSet::<Position>::new();
    let mut greatest_height = 0;
    let vents = reader
        .lines()
        .next()
        .unwrap()
        .unwrap()
        .chars()
        .collect::<Vec<_>>();

    let mut cur_rock_position = (2, 3);
    let mut num_resting_rocks = 0;
    let mut iteration = 0;

    while num_resting_rocks != 2022 {
        let rock = Rock::from(num_resting_rocks);
        let vent_dir = match vents.get(iteration % vents.len()).unwrap() {
            '>' => Direction::Right,
            '<' => Direction::Left,
            c => panic!("Invalid char: {c}"),
        };

        if let Some(new_pos) = try_move(&rock, cur_rock_position, vent_dir, &map) {
            cur_rock_position = new_pos;
        }

        if let Some(new_pos) = try_move(&rock, cur_rock_position, Direction::Down, &map) {
            cur_rock_position = new_pos;
        } else {
            map.extend(get_covered_tiles(
                cur_rock_position.0,
                cur_rock_position.1,
                &rock,
            ));

            greatest_height = greatest_height.max(get_ceiling(cur_rock_position.1, &rock) + 1);
            cur_rock_position = (2, greatest_height + 3);
            num_resting_rocks += 1;
        }

        iteration += 1;
    }

    println!("{greatest_height}");

    Ok(())
}
