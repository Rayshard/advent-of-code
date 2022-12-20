use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

use itertools::Itertools;

type Graph = HashMap<String, (i64, Vec<String>)>;

trait GraphTrait {
    fn get_rate(&self, valve: &str) -> i64;
    fn get_connecting_valves(&self, valve: &str) -> &Vec<String>;
}

impl GraphTrait for Graph {
    fn get_rate(&self, valve: &str) -> i64 {
        self.get(valve).unwrap().0
    }

    fn get_connecting_valves(&self, valve: &str) -> &Vec<String> {
        &self.get(valve).unwrap().1
    }
}

fn calculate(
    start_valve: &String,
    graph: &Graph,
    pairs: &HashMap<(String, String), i64>,
    pressure_releasing_valves_to_visit: &HashSet<&&String>,
    minutes_remaining: i64,
    current_pressure_to_be_released: i64,
) -> i64 {
    let mut max = 0i64;

    for prv in pressure_releasing_valves_to_visit {
        let required_minutes_to_open =
            (pairs.get(&(start_valve.clone(), prv.to_string())).unwrap() + 1) as i64;
        if required_minutes_to_open >= minutes_remaining {
            continue;
        }

        let num_minutes_releasing = minutes_remaining - required_minutes_to_open;
        let prv_as_set = HashSet::from([*prv]);
        let new_prv_to_visit = pressure_releasing_valves_to_visit
            .difference(&prv_as_set)
            .map(|prv| *prv)
            .collect::<HashSet<_>>();

        max = max.max(calculate(
            prv,
            graph,
            pairs,
            &new_prv_to_visit,
            num_minutes_releasing,
            num_minutes_releasing * graph.get_rate(prv),
        ));
    }

    current_pressure_to_be_released + max
}

fn calculate_part1(
    graph: &Graph,
    pairs: &HashMap<(String, String), i64>,
    pressure_releasing_values: &HashSet<&String>,
    num_minutes_to_complete: i64,
) -> i64 {
    pairs
        .iter()
        .filter_map(|((from, to), required_minutes)| {
            if from == "AA" && pressure_releasing_values.contains(to) {
                let valve = to;
                let valve_as_set = HashSet::from([valve]);
                let remaining_prv_to_visit = pressure_releasing_values
                    .difference(&valve_as_set)
                    .collect::<HashSet<_>>();

                let minutes_remaining = num_minutes_to_complete - required_minutes - 1;
                Some(calculate(
                    valve,
                    &graph,
                    &pairs,
                    &remaining_prv_to_visit,
                    minutes_remaining,
                    graph.get_rate(valve) * minutes_remaining,
                ))
            } else {
                None
            }
        })
        .max()
        .unwrap()
}

fn calculate_part2(
    graph: &Graph,
    pairs: &HashMap<(String, String), i64>,
    pressure_releasing_valves: &HashSet<&String>,
) -> i64 {
    let mut max = 0i64;

    for length in 1..=(pressure_releasing_valves.len() / 2) {
        for elephant_valves in pressure_releasing_valves.iter().combinations(length) {
            let elephant_valves = HashSet::from_iter(elephant_valves.iter().map(|prv| **prv));
            let elephant_best = calculate_part1(graph, pairs, &elephant_valves, 26);

            let my_valves = pressure_releasing_valves
                .difference(&elephant_valves)
                .map(|prv| *prv)
                .collect::<HashSet<_>>();
            let my_best = calculate_part1(graph, pairs, &my_valves, 26);

            max = max.max(elephant_best + my_best);
        }
    }

    max
}

fn search(valve: &String, graph: &Graph, seen: &mut HashMap<String, i64>, step: i64) {
    for connecting_valve in graph.get_connecting_valves(valve) {
        if let Some(last_step) = seen.get(connecting_valve) {
            if step >= *last_step {
                continue;
            }
        }

        seen.insert(connecting_valve.clone(), step);
        search(connecting_valve, graph, seen, step + 1);
    }
}

fn get_pairs(graph: &Graph) -> HashMap<(String, String), i64> {
    let mut result = HashMap::<(String, String), i64>::new();

    for valve in graph.keys() {
        let mut seen = HashMap::<String, i64>::new(); // a map from valve to how many steps it took to reach it
        search(valve, graph, &mut seen, 1);

        for (child, num_steps) in seen {
            result.insert((valve.to_string(), child), num_steps);
        }
    }

    result
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let graph = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let mut parts = line.split_whitespace();

            let valve = parts.nth(1).unwrap().to_string();
            let rate = parts
                .nth(2)
                .unwrap()
                .trim_end_matches(';')
                .split('=')
                .last()
                .unwrap()
                .parse::<i64>()
                .unwrap();
            let tunnels = parts
                .skip(4)
                .map(|tunnel| tunnel.trim_end_matches(',').to_string())
                .collect::<Vec<_>>();

            (valve, (rate, tunnels))
        })
        .collect::<HashMap<_, _>>();

    let pairs = get_pairs(&graph);
    let pressure_releasing_values = graph
        .iter()
        .filter_map(|(valve, (rate, _))| if rate != &0 { Some(valve) } else { None })
        .collect::<HashSet<_>>();

    println!(
        "{}",
        calculate_part1(&graph, &pairs, &pressure_releasing_values, 30)
    );

    println!(
        "{}",
        calculate_part2(&graph, &pairs, &pressure_releasing_values)
    );

    Ok(())
}
