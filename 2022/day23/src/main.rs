use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

use enum_iterator::{all, cardinality, Sequence};

type Position = (i64, i64);

#[derive(Debug, Sequence, PartialEq, Eq, Hash)]
enum Direction {
    N,
    S,
    E,
    W,
    NW,
    NE,
    SW,
    SE,
}

fn get_rel_pos((x, y): Position, dir: &Direction) -> Position {
    match dir {
        Direction::N => (x, y - 1),
        Direction::S => (x, y + 1),
        Direction::E => (x + 1, y),
        Direction::W => (x - 1, y),
        Direction::NW => (x - 1, y - 1),
        Direction::NE => (x + 1, y - 1),
        Direction::SW => (x - 1, y + 1),
        Direction::SE => (x + 1, y + 1),
    }
}
static DIRECTION_PROPSITION_ORDER: &'static [(Direction, Direction, Direction)] = &[
    (Direction::N, Direction::NE, Direction::NW),
    (Direction::S, Direction::SE, Direction::SW),
    (Direction::W, Direction::NW, Direction::SW),
    (Direction::E, Direction::NE, Direction::SE),
];

fn do_round(
    elves: HashSet<Position>,
    round: usize,
) -> (HashSet<Position>, (i64, i64), (i64, i64), usize) {
    let mut result = HashSet::<Position>::new();
    let ((mut min_x, mut min_y), (mut max_x, mut max_y)) =
        (elves.iter().next().unwrap(), elves.iter().next().unwrap());
    let dir_proposition_start = (round - 1) % DIRECTION_PROPSITION_ORDER.len();
    let dir_proposition_order = (dir_proposition_start
        ..dir_proposition_start + DIRECTION_PROPSITION_ORDER.len())
        .map(|i| &DIRECTION_PROPSITION_ORDER[i % DIRECTION_PROPSITION_ORDER.len()]);

    fn add_elf(
        (elf_x, elf_y): Position,
        elves: &mut HashSet<Position>,
        min_x: &mut i64,
        min_y: &mut i64,
        max_x: &mut i64,
        max_y: &mut i64,
    ) {
        elves.insert((elf_x, elf_y));
        *min_x = elf_x.min(*min_x);
        *min_y = elf_y.min(*min_y);
        *max_x = elf_x.max(*max_x);
        *max_y = elf_y.max(*max_y);
    }

    let mut propositions = HashMap::<Position, Vec<Position>>::new();

    for (elf_x, elf_y) in elves.iter() {
        let open_adjacent_positions = all::<Direction>()
            .map(|dir| !elves.contains(&get_rel_pos((*elf_x, *elf_y), &dir)) as usize)
            .sum::<usize>();

        if open_adjacent_positions == cardinality::<Direction>() {
            add_elf(
                (*elf_x, *elf_y),
                &mut result,
                &mut min_x,
                &mut min_y,
                &mut max_x,
                &mut max_y,
            );
        } else {
            let mut proposition = None;

            for (a, b, c) in dir_proposition_order.clone() {
                let a = get_rel_pos((*elf_x, *elf_y), a);
                let b = get_rel_pos((*elf_x, *elf_y), b);
                let c = get_rel_pos((*elf_x, *elf_y), c);

                if !elves.contains(&a) && !elves.contains(&b) && !elves.contains(&c) {
                    proposition = Some(a);
                    break;
                }
            }

            if let Some(proposition) = proposition {
                if let Some(proposing_elves) = propositions.get_mut(&proposition) {
                    proposing_elves.push((*elf_x, *elf_y));
                } else {
                    propositions.insert(proposition, vec![(*elf_x, *elf_y)]);
                }
            } else {
                add_elf(
                    (*elf_x, *elf_y),
                    &mut result,
                    &mut min_x,
                    &mut min_y,
                    &mut max_x,
                    &mut max_y,
                );
            }
        }
    }

    let mut num_elves_moved = 0;

    for (proposition, proposing_elves) in propositions {
        match &proposing_elves[..] {
            [_] => {
                add_elf(
                    proposition,
                    &mut result,
                    &mut min_x,
                    &mut min_y,
                    &mut max_x,
                    &mut max_y,
                );

                num_elves_moved += 1;
            }
            elves => elves.iter().for_each(|elf| {
                add_elf(
                    *elf,
                    &mut result,
                    &mut min_x,
                    &mut min_y,
                    &mut max_x,
                    &mut max_y,
                )
            }),
        }
    }

    (result, (min_x, min_y), (max_x, max_y), num_elves_moved)
}

fn get_empty_tiles(
    elves: &HashSet<Position>,
    min_x: i64,
    min_y: i64,
    max_x: i64,
    max_y: i64,
) -> usize {
    (min_x..=max_x)
        .map(|x| {
            (min_y..=max_y)
                .map(|y| !elves.contains(&(x, y)) as usize)
                .sum::<usize>()
        })
        .sum::<usize>()
}

fn print_elves(elves: &HashSet<Position>, min_x: i64, min_y: i64, max_x: i64, max_y: i64) {
    (min_y..=max_y).for_each(|y| {
        let line = (min_x..=max_x)
            .map(|x| if elves.contains(&(x, y)) { '#' } else { '.' })
            .collect::<String>();

        println!("{line}");
    });
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut elves = reader
        .lines()
        .enumerate()
        .flat_map(|(i_line, line)| {
            line.unwrap()
                .chars()
                .enumerate()
                .filter_map(|(i_char, c)| {
                    if c == '#' {
                        Some((i_char as i64, i_line as i64))
                    } else {
                        None
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect::<HashSet<_>>();

    let (mut min_x, mut min_y, mut max_x, mut max_y);
    let mut round = 1;

    loop {
        let num_elves_moved;
        (elves, (min_x, min_y), (max_x, max_y), num_elves_moved) = do_round(elves, round);

        if round == 10 {
            println!("{}", get_empty_tiles(&elves, min_x, min_y, max_x, max_y));
        }
        
        if num_elves_moved == 0 {
            println!("{round}");
            break;
        }

        round += 1;
    }

    Ok(())
}
