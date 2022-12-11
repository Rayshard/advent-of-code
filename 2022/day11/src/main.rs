use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn read_line(reader: &mut BufReader<File>) -> String {
    let mut line = String::new();
    reader.read_line(&mut line);

    return line;
}

fn parse_last_as_u64_on_whitespace_split(reader: &mut BufReader<File>) -> u64 {
    read_line(reader)
        .split_whitespace()
        .last()
        .unwrap()
        .parse()
        .unwrap()
}

#[derive(Debug)]
enum Operation {
    Add(u64),
    Multiply(u64),
    Square,
}

#[derive(Debug)]
struct Test {
    divisibility_factor: u64,
    true_monkey: u64,
    false_monkey: u64,
}

impl Test {
    pub fn parse(reader: &mut BufReader<File>) -> Test {
        Test {
            divisibility_factor: parse_last_as_u64_on_whitespace_split(reader),
            true_monkey: parse_last_as_u64_on_whitespace_split(reader),
            false_monkey: parse_last_as_u64_on_whitespace_split(reader),
        }
    }
}

#[derive(Debug)]
struct Monkey {
    starting_items: Vec<u64>,
    operation: Operation,
    test: Test,
}

impl Monkey {
    fn parse_id(reader: &mut BufReader<File>) -> u64 {
        read_line(reader)
            .trim()
            .trim_end_matches(":")
            .split_whitespace()
            .last()
            .unwrap()
            .parse()
            .unwrap()
    }

    fn parse_starting_items(reader: &mut BufReader<File>) -> Vec<u64> {
        read_line(reader)
            .split(':')
            .last()
            .unwrap()
            .split(',')
            .map(|part| part.trim().parse().unwrap())
            .collect()
    }

    fn parse_operation(reader: &mut BufReader<File>) -> Operation {
        let line = read_line(reader);
        let parts = line.split_whitespace().skip(4).collect::<Vec<_>>();

        match &parts[..] {
            ["*", "old"] => Operation::Square,
            ["*", value] => Operation::Multiply(value.parse().unwrap()),
            ["+", value] => Operation::Add(value.parse().unwrap()),
            parts => panic!("Invalid: {parts:?}"),
        }
    }

    pub fn parse(reader: &mut BufReader<File>) -> (u64, Monkey) {
        let id = Monkey::parse_id(reader);
        let monkey = Monkey {
            starting_items: Monkey::parse_starting_items(reader),
            operation: Monkey::parse_operation(reader),
            test: Test::parse(reader),
        };

        (id, monkey)
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let mut reader = BufReader::new(file);

    let monkeys: Vec<Monkey> = Vec::new();

    loop {
        let (_, monkey) = Monkey::parse(&mut reader);
        println!("{monkey:?}");

        let mut trash = String::new();
        if reader.read_line(&mut trash).unwrap() == 0 {
            break;
        }
    }

    Ok(())
}
