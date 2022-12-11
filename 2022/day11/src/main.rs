use std::{
    collections::VecDeque,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn read_line(reader: &mut BufReader<File>) -> String {
    let mut line = String::new();
    reader.read_line(&mut line).unwrap();

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

#[derive(Debug, Clone)]
enum Operation {
    Add(u64),
    Multiply(u64),
    Square,
}

#[derive(Debug, Clone)]
struct Test {
    modulus: u64,
    true_monkey: usize,
    false_monkey: usize,
}

impl Test {
    pub fn parse(reader: &mut BufReader<File>) -> Test {
        Test {
            modulus: parse_last_as_u64_on_whitespace_split(reader),
            true_monkey: parse_last_as_u64_on_whitespace_split(reader) as usize,
            false_monkey: parse_last_as_u64_on_whitespace_split(reader) as usize,
        }
    }
}

#[derive(Debug, Clone)]
struct Monkey {
    starting_items: VecDeque<u64>,
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

    fn parse_starting_items(reader: &mut BufReader<File>) -> VecDeque<u64> {
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

fn process_monkey(
    monkey_id: usize,
    monkeys: &mut Vec<Monkey>,
    worry_supression_divisor: u64,
    modulus: u64,
) -> Vec<(usize, u64)> {
    let monkey = monkeys.get_mut(monkey_id).unwrap();
    let mut result = vec![];

    while !monkey.starting_items.is_empty() {
        let mut worry_level = monkey.starting_items.pop_front().unwrap();

        match monkey.operation {
            Operation::Add(value) => worry_level += value,
            Operation::Multiply(value) => worry_level *= value,
            Operation::Square => worry_level *= worry_level,
        }

        worry_level /= worry_supression_divisor;
        worry_level %= modulus;

        let next_monkey = if worry_level % monkey.test.modulus == 0 {
            monkey.test.true_monkey
        } else {
            monkey.test.false_monkey
        };

        result.push((next_monkey, worry_level));
    }

    result
}

fn process_monkeys(
    monkeys: &Vec<Monkey>,
    num_rounds: usize,
    worry_supression_divisor: u64,
) -> usize {
    let mut inspection_counts = vec![0; monkeys.len()];

    let mut monkeys = monkeys.clone();
    let modulus = monkeys
        .iter()
        .map(|m| m.test.modulus)
        .fold(1, |acc, d| acc * d);

    for _ in 0..num_rounds {
        for id in 0..monkeys.len() {
            let nexts = process_monkey(id, &mut monkeys, worry_supression_divisor, modulus);

            for (next_monkey, worry_level) in nexts.iter() {
                monkeys[*next_monkey]
                    .starting_items
                    .push_back(worry_level.clone());
            }

            inspection_counts[id] += nexts.len();
        }
    }

    inspection_counts.sort();
    let top_two = &inspection_counts[&inspection_counts.len() - 2..];

    top_two[0] * top_two[1]
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let mut reader = BufReader::new(file);
    let mut monkeys: Vec<Monkey> = Vec::new();

    loop {
        monkeys.push(Monkey::parse(&mut reader).1);

        let mut trash = String::new();
        if reader.read_line(&mut trash).unwrap() == 0 {
            break;
        }
    }

    println!("{}", process_monkeys(&monkeys, 20, 3));
    println!("{}", process_monkeys(&monkeys, 10000, 1));

    Ok(())
}
