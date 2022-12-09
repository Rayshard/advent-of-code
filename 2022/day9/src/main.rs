use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

type Position = (i64, i64);

fn get_new_position(leader: &Position, follower: &Position) -> Position {
    let direction = match (leader.0 - follower.0, leader.1 - follower.1) {
        (0, 0) | (1, 0) | (-1, 0) | (0, 1) | (0, -1) | (1, 1) | (-1, 1) | (-1, -1) | (1, -1) => {
            (0, 0)
        }
        (x, y) => (
            (x as f64 / 2.0).round() as i64,
            (y as f64 / 2.0).round() as i64,
        ),
    };

    (follower.0 + direction.0, follower.1 + direction.1)
}

fn update_rope(rope: &mut [Position], direction: &(i64, i64)) {
    let (head_x, head_y) = rope[0];
    rope[0] = (head_x + direction.0, head_y + direction.1);

    for i in 1..rope.len() {
        rope[i] = get_new_position(&rope[i - 1], &rope[i]);
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let start: Position = (0, 0);
    let mut rope1 = [start.clone(); 2];
    let mut rope2 = [start.clone(); 10];
    let mut visited_by_tail1: HashSet<Position> = HashSet::from([*rope1.last().unwrap()]);
    let mut visited_by_tail2: HashSet<Position> = HashSet::from([*rope2.last().unwrap()]);


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
            update_rope(&mut rope1, &direction);
            visited_by_tail1.insert(rope1.last().unwrap().clone());

            update_rope(&mut rope2, &direction);
            visited_by_tail2.insert(rope2.last().unwrap().clone());

            amt_to_move -= 1;
        }
    }

    println!("{}", visited_by_tail1.len());
    println!("{}", visited_by_tail2.len());

    Ok(())
}
