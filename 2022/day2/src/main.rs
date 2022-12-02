use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Clone, Copy, PartialEq)]
enum Shape {
    Rock = 1,
    Paper = 2,
    Scissors = 3,
}

fn play(player1: &Shape, player2: &Shape) -> Option<Shape> {
    match (player1, player2) {
        (Shape::Rock, Shape::Paper) | (Shape::Paper, Shape::Rock) => Some(Shape::Paper),
        (Shape::Paper, Shape::Scissors) | (Shape::Scissors, Shape::Paper) => Some(Shape::Scissors),
        (Shape::Scissors, Shape::Rock) | (Shape::Rock, Shape::Scissors) => Some(Shape::Rock),
        _ => None,
    }
}

fn map_part1(player1: &str, player2: &str) -> (Shape, Shape) {
    let shape1 = match player1 {
        "A" => Shape::Rock,
        "B" => Shape::Paper,
        "C" => Shape::Scissors,
        _ => panic!("Invalid: {:?}", player1),
    };
    let shape2 = match player2 {
        "X" => Shape::Rock,
        "Y" => Shape::Paper,
        "Z" => Shape::Scissors,
        _ => panic!("Invalid: {:?}", player2),
    };

    return (shape1, shape2);
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut total = 0;

    for line in reader.lines() {
        let string = line.unwrap();

        if let [p1, p2] = string.split_whitespace().collect::<Vec<&str>>()[..] {
            let (player1, player2) = map_part1(p1, p2);
            let outcome = match play(&player1, &player2) {
                Some(shape) if shape == player2 => 6, // Win
                Some(_) => 0,                         // Lose
                None => 3,                            // Draw
            };

            total += (player2 as i32) + outcome;
        } else {
            panic!("Invalid round: {:?}", string)
        }
    }

    println!("{}", total);

    Ok(())
}
