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

fn play(player1: Shape, player2: Shape) -> i32 {
    let outcome = match (player1, player2) {
        (Shape::Rock, Shape::Paper) | (Shape::Paper, Shape::Rock) => Some(Shape::Paper),
        (Shape::Paper, Shape::Scissors) | (Shape::Scissors, Shape::Paper) => Some(Shape::Scissors),
        (Shape::Scissors, Shape::Rock) | (Shape::Rock, Shape::Scissors) => Some(Shape::Rock),
        _ => None,
    };

    match outcome {
        Some(shape) if shape == player2 => 6, // Win
        Some(_) => 0,                         // Lose
        None => 3,                            // Draw
    }
}

fn map_opponent(opponent: &str) -> Shape {
    match opponent {
        "A" => Shape::Rock,
        "B" => Shape::Paper,
        "C" => Shape::Scissors,
        _ => panic!("Invalid: {:?}", opponent),
    }
}

fn map_part1(player1: &str, player2: &str) -> (Shape, Shape) {
    let shape1 = map_opponent(player1);
    let shape2 = match player2 {
        "X" => Shape::Rock,
        "Y" => Shape::Paper,
        "Z" => Shape::Scissors,
        _ => panic!("Invalid: {:?}", player2),
    };

    return (shape1, shape2);
}

fn map_part2(player1: &str, player2: &str) -> (Shape, Shape) {
    let shape1 = map_opponent(player1);
    let shape2 = match (shape1, player2) {
        (Shape::Rock, "X") => Shape::Scissors,
        (Shape::Paper, "X") => Shape::Rock,
        (Shape::Scissors, "X") => Shape::Paper,
        (Shape::Rock, "Z") => Shape::Paper,
        (Shape::Paper, "Z") => Shape::Scissors,
        (Shape::Scissors, "Z") => Shape::Rock,
        (shape, "Y") => shape,
        _ => panic!("Invalid: {:?}", player2),
    };

    return (shape1, shape2);
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut total_part1 = 0;
    let mut total_part2 = 0;

    for line in reader.lines() {
        let string = line.unwrap();

        if let [p1, p2] = string.split_whitespace().collect::<Vec<&str>>()[..] {
            //Part 1
            {
                let (player1, player2) = map_part1(p1, p2);
                total_part1 += (player2 as i32) + play(player1, player2);
            }

            //Part 2
            {
                let (player1, player2) = map_part2(p1, p2);
                total_part2 += (player2 as i32) + play(player1, player2);
            }
        } else {
            panic!("Invalid round: {:?}", string)
        }
    }

    println!("{}", total_part1);
    println!("{}", total_part2);

    Ok(())
}
