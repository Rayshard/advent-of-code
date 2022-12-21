use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

struct Blueprint {
    ore_robot_cost: u64,
    clay_robot_cost: u64,
    obsidian_robot_ore_cost: u64,
    obsidian_robot_clay_cost: u64,
    geode_robot_ore_cost: u64,
    geode_robot_clay_cost: u64,
}

fn determine_max_number_geodes(blueprint: &Blueprint) -> u64 {
    todo!()
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let result = reader
        .lines()
        .enumerate()
        .map(|(i, line)| {
            let line = line.unwrap();
            let parts = line.split_whitespace().collect::<Vec<_>>();

            let blueprint = Blueprint {
                ore_robot_cost: parts[6].parse().unwrap(),
                clay_robot_cost: parts[12].parse().unwrap(),
                obsidian_robot_ore_cost: parts[18].parse().unwrap(),
                obsidian_robot_clay_cost: parts[21].parse().unwrap(),
                geode_robot_ore_cost: parts[27].parse().unwrap(),
                geode_robot_clay_cost: parts[30].parse().unwrap(),
            };

            (i + 1) * determine_max_number_geodes(&blueprint) as usize
        })
        .sum::<usize>();

    println!("{result}");

    Ok(())
}
