use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

const MAP_WIDTH: i32 = 7;
pub type Position = (i32, i128);
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

impl From<i128> for Rock {
    fn from(value: i128) -> Rock {
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

pub fn get_covered_tiles(x: i32, y: i128, rock: &Rock) -> Vec<Position> {
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

pub fn get_ceiling(y: i128, rock: &Rock) -> i128 {
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

fn simulate(
    target_resting_rocks: i128,
    vents: &Vec<char>,
    starting_greatest_height: i128,
    starting_number_resting_rocks: i128,
    starting_iteration: i128,
) -> (
    i128,
    Option<i128>,
    Option<i128>,
    Option<i128>,
    Option<i128>,
    Option<i128>,
    Option<i128>,
) {
    let mut greatest_height = starting_greatest_height;
    let mut map = HashSet::<Position>::from([
        (0, greatest_height - 1),
        (1, greatest_height - 1),
        (2, greatest_height - 1),
        (3, greatest_height - 1),
        (4, greatest_height - 1),
        (5, greatest_height - 1),
        (6, greatest_height - 1),
    ]);

    let mut cur_rock_position = (2, greatest_height + 3);
    let mut num_resting_rocks = starting_number_resting_rocks;
    let mut iteration = starting_iteration;
    let mut last_purge_height = greatest_height;
    let mut last_purge_rocks = num_resting_rocks;
    let mut last_purge_iteration = iteration;

    let mut nrr_offset: Option<i128> = None;
    let mut gh_offset: Option<i128> = None;
    let mut i_offset: Option<i128> = None;
    let mut nrr_scalar: Option<i128> = None;
    let mut gh_scalar: Option<i128> = None;
    let mut i_scalar: Option<i128> = None;

    while num_resting_rocks != target_resting_rocks {
        let rock = Rock::from(num_resting_rocks);
        let vent_dir = match vents.get(iteration as usize % vents.len()).unwrap() {
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

            let top_row = (0..=6)
                .filter_map(|x| match map.get(&(x, greatest_height - 1)) {
                    Some(rock) => Some(*rock),
                    None => None,
                })
                .collect::<Vec<_>>();

            cur_rock_position = (2, greatest_height + 3);
            num_resting_rocks += 1;

            if top_row.len() == 7 {
                if nrr_offset.is_none() {
                    nrr_offset = Some(num_resting_rocks);
                } else {
                    nrr_scalar = Some(num_resting_rocks - last_purge_rocks);
                }

                if gh_offset.is_none() {
                    gh_offset = Some(greatest_height);
                } else {
                    gh_scalar = Some(greatest_height - last_purge_height);
                }

                if i_offset.is_none() {
                    i_offset = Some(iteration + 1);
                } else {
                    i_scalar = Some(iteration + 1 - last_purge_iteration);
                }

                last_purge_height = greatest_height;
                last_purge_rocks = num_resting_rocks;
                last_purge_iteration = iteration + 1;

                map.clear();
                map.extend(top_row);
            }
        }

        iteration += 1;
    }

    (
        greatest_height,
        nrr_offset,
        nrr_scalar,
        gh_offset,
        gh_scalar,
        i_offset,
        i_scalar,
    )
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);
    let vents = reader
        .lines()
        .next()
        .unwrap()
        .unwrap()
        .chars()
        .collect::<Vec<_>>();

    // Part 1
    println!("{}", simulate(2022, &vents, 0, 0, 0).0);

    // Part 2
    let (_, nrr_offset, nrr_scalar, gh_offset, gh_scalar, i_offset, i_scalar) = simulate(
        10000, // choose a big enough number so patterns emerge (program will crash otherwise)
        &vents, 0, 0, 0,
    );

    let target_resting_rocks = 1000000000000;
    let mut starting_number_resting_rocks = nrr_offset.unwrap();
    let mut starting_greatest_height = gh_offset.unwrap();
    let mut starting_iteration = i_offset.unwrap();

    let nrr_scalar = nrr_scalar.unwrap();
    let gh_scalar = gh_scalar.unwrap();
    let i_scalar = i_scalar.unwrap();

    loop {
        starting_number_resting_rocks += nrr_scalar;
        if starting_number_resting_rocks > target_resting_rocks {
            starting_number_resting_rocks -= nrr_scalar;
            break;
        }

        starting_greatest_height += gh_scalar;
        starting_iteration += i_scalar;
    }

    println!(
        "{}",
        simulate(
            target_resting_rocks,
            &vents,
            starting_greatest_height,
            starting_number_resting_rocks,
            starting_iteration
        ).0
    );

    Ok(())
}
