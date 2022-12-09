use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

type Position = (i64, i64);

fn update_tail(tail: &Position, head: &Position) -> Position {
    let direction = match (head.0 - tail.0, head.1 - tail.1) {
        (0, 0) | (1, 0) | (-1, 0) | (0, 1) | (0, -1) | (1, 1) | (-1, 1) | (-1, -1) | (1, -1) => {
            (0, 0)
        }
        (x, y) => (
            (x as f64 / 2.0).round() as i64,
            (y as f64 / 2.0).round() as i64,
        ),
    };

    (tail.0 + direction.0, tail.1 + direction.1)
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let start: Position = (0, 0);
    let mut head: Position = start.clone();
    let mut tail: Position = start.clone();
    let mut visited_by_tail: HashSet<Position> = HashSet::new();

    visited_by_tail.insert(tail);

    for line in reader.lines().map(|line| line.unwrap()) {
        let parts = line.split_whitespace().collect::<Vec<_>>();

        let direction = match parts[0] {
            "R" => (1, 0),
            "L" => (-1, 0),
            "U" => (0, 1),
            "D" => (0, -1),
            dir => panic!("Invalid direction: {dir}"),
        };

        let mut amt_to_move = parts[1].parse::<u64>().unwrap();

        while amt_to_move > 0 {
            head = (head.0 + direction.0, head.1 + direction.1);
            tail = update_tail(&tail, &head);

            visited_by_tail.insert(tail);
            amt_to_move -= 1;
        }
    }

    println!("{}", visited_by_tail.len());

    Ok(())
}
