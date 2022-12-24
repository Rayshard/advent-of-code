use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

use rayon::prelude::*;

struct Blueprint {
    ore_robot_ore_cost: usize,
    clay_robot_ore_cost: usize,
    obsidian_robot_ore_cost: usize,
    obsidian_robot_clay_cost: usize,
    geode_robot_ore_cost: usize,
    geode_robot_obsidian_cost: usize,
    max_needed_ore_robots: usize,
}

impl Blueprint {
    pub fn new(
        ore_robot_ore_cost: usize,
        clay_robot_ore_cost: usize,
        obsidian_robot_ore_cost: usize,
        obsidian_robot_clay_cost: usize,
        geode_robot_ore_cost: usize,
        geode_robot_obsidian_cost: usize,
    ) -> Self {
        Self {
            ore_robot_ore_cost,
            clay_robot_ore_cost,
            obsidian_robot_ore_cost,
            obsidian_robot_clay_cost,
            geode_robot_ore_cost,
            geode_robot_obsidian_cost,
            max_needed_ore_robots: ore_robot_ore_cost
                .max(clay_robot_ore_cost)
                .max(obsidian_robot_ore_cost)
                .max(geode_robot_ore_cost),
        }
    }
}

#[derive(Clone)]
struct State {
    num_ore_robots: usize,
    num_ore: usize,
    num_clay_robots: usize,
    num_clay: usize,
    num_obsidian_robots: usize,
    num_obsidian: usize,
    num_geode_robots: usize,
    num_geodes: usize,
}

impl State {
    pub fn new() -> State {
        State {
            num_ore_robots: 1,
            num_ore: 0,
            num_clay_robots: 0,
            num_clay: 0,
            num_obsidian_robots: 0,
            num_obsidian: 0,
            num_geode_robots: 0,
            num_geodes: 0,
        }
    }

    pub fn possible_nexts(&self, blueprint: &Blueprint) -> Vec<State> {
        let mut result = vec![State {
            num_ore_robots: self.num_ore_robots,
            num_ore: self.num_ore + self.num_ore_robots,
            num_clay_robots: self.num_clay_robots,
            num_clay: self.num_clay + self.num_clay_robots,
            num_obsidian_robots: self.num_obsidian_robots,
            num_obsidian: self.num_obsidian + self.num_obsidian_robots,
            num_geode_robots: self.num_geode_robots,
            num_geodes: self.num_geodes + self.num_geode_robots,
        }];

        if self.num_ore >= blueprint.geode_robot_ore_cost
            && self.num_obsidian >= blueprint.geode_robot_obsidian_cost
        {
            result.push(State {
                num_ore_robots: self.num_ore_robots,
                num_ore: self.num_ore + self.num_ore_robots - blueprint.geode_robot_ore_cost,
                num_clay_robots: self.num_clay_robots,
                num_clay: self.num_clay + self.num_clay_robots,
                num_obsidian_robots: self.num_obsidian_robots,
                num_obsidian: self.num_obsidian + self.num_obsidian_robots
                    - blueprint.geode_robot_obsidian_cost,
                num_geode_robots: self.num_geode_robots + 1,
                num_geodes: self.num_geodes + self.num_geode_robots,
            });
        } else if self.num_ore >= blueprint.obsidian_robot_ore_cost
            && self.num_clay >= blueprint.obsidian_robot_clay_cost && self.num_obsidian_robots < blueprint.geode_robot_obsidian_cost
        {
                result.push(State {
                    num_ore_robots: self.num_ore_robots,
                    num_ore: self.num_ore + self.num_ore_robots - blueprint.obsidian_robot_ore_cost,
                    num_clay_robots: self.num_clay_robots,
                    num_clay: self.num_clay + self.num_clay_robots
                        - blueprint.obsidian_robot_clay_cost,
                    num_obsidian_robots: self.num_obsidian_robots + 1,
                    num_obsidian: self.num_obsidian + self.num_obsidian_robots,
                    num_geode_robots: self.num_geode_robots,
                    num_geodes: self.num_geodes + self.num_geode_robots,
                });
        } else {
            if self.num_ore >= blueprint.clay_robot_ore_cost
                && self.num_clay_robots < blueprint.obsidian_robot_clay_cost
            {
                result.push(State {
                    num_ore_robots: self.num_ore_robots,
                    num_ore: self.num_ore + self.num_ore_robots - blueprint.clay_robot_ore_cost,
                    num_clay_robots: self.num_clay_robots + 1,
                    num_clay: self.num_clay + self.num_clay_robots,
                    num_obsidian_robots: self.num_obsidian_robots,
                    num_obsidian: self.num_obsidian + self.num_obsidian_robots,
                    num_geode_robots: self.num_geode_robots,
                    num_geodes: self.num_geodes + self.num_geode_robots,
                });
            }

            if self.num_ore >= blueprint.ore_robot_ore_cost
                && self.num_ore_robots < blueprint.max_needed_ore_robots
            {
                result.push(State {
                    num_ore_robots: self.num_ore_robots + 1,
                    num_ore: self.num_ore + self.num_ore_robots - blueprint.ore_robot_ore_cost,
                    num_clay_robots: self.num_clay_robots,
                    num_clay: self.num_clay + self.num_clay_robots,
                    num_obsidian_robots: self.num_obsidian_robots,
                    num_obsidian: self.num_obsidian + self.num_obsidian_robots,
                    num_geode_robots: self.num_geode_robots,
                    num_geodes: self.num_geodes + self.num_geode_robots,
                });
            }
        }

        result
    }
}

fn determine_max_number_geodes(blueprint: &Blueprint, allowed_minutes: usize) -> usize {
    let mut states = vec![State::new()];

    for _ in 1..=allowed_minutes - 2 {
        states = states
            .iter()
            .flat_map(|state| state.possible_nexts(blueprint))
            .collect();
    }

    let best = states
        .par_iter()
        .map(|state| {
            state
                .possible_nexts(blueprint)
                .iter()
                .map(|state| state.num_geodes + state.num_geode_robots)
                .max()
                .unwrap()
        })
        .max()
        .unwrap();

    best
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let blueprints = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let parts = line.split_whitespace().collect::<Vec<_>>();

            Blueprint::new(
                parts[6].parse().unwrap(),
                parts[12].parse().unwrap(),
                parts[18].parse().unwrap(),
                parts[21].parse().unwrap(),
                parts[27].parse().unwrap(),
                parts[30].parse().unwrap(),
            )
        })
        .collect::<Vec<_>>();

    // Part 1
    let result = blueprints
        .iter()
        .enumerate()
        .map(|(i, blueprint)| (i + 1) * determine_max_number_geodes(&blueprint, 24) as usize)
        .sum::<usize>();

    println!("{result}");

    // Part 2
    let result = blueprints
        .iter()
        .take(3)
        .map(|blueprint| determine_max_number_geodes(&blueprint, 32))
        .product::<usize>();

    println!("{result}");

    Ok(())
}
