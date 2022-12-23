use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

type Position = (i64, i64);
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

fn get_rel_pos((x, y): Position, dir: Direction) -> Position {
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

fn do_round(map: HashSet<Position>) -> (HashSet<Position>, (i64, i64), (i64, i64)) {
    let mut result = HashSet::<Position>::new();
    let ((mut min_x, mut min_y), (mut max_x, mut max_y)) =
        (map.iter().next().unwrap(), map.iter().next().unwrap());

    for (elf_x, elf_y) in map {
        result.insert((elf_x, elf_y));
        min_x = min_x.min(elf_x);
        min_y = min_y.min(elf_y);
        max_x = max_x.max(elf_x);
        max_y = max_y.max(elf_y);
    }

    (result, (min_x, min_y), (max_x, max_y))
}

fn get_empty_tiles(
    map: &HashSet<Position>,
    min_x: i64,
    min_y: i64,
    max_x: i64,
    max_y: i64,
) -> usize {
   (min_x..=max_x)
        .map(|x| {
            (min_y..=max_y)
                .map(|y| !map.contains(&(x, y)) as usize)
                .sum::<usize>()
        })
        .sum::<usize>()
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

    let (mut min_x, mut min_y, mut max_x, mut max_y) = (0, 0, 0, 0);

    for _ in 1..=10 {
        (elves, (min_x, min_y), (max_x, max_y)) = do_round(elves);
    }

    println!("{}", get_empty_tiles(&elves, min_x, min_y, max_x, max_y));

    Ok(())
}
