use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

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
    prv_pairs: &HashMap<(String, String), i64>,
    pressure_releasing_valves_to_visit: &HashSet<String>,
    minutes_remaining: i64,
) -> i64 {
    let mut max = 0i64;

    for prv in pressure_releasing_valves_to_visit {
        let required_minutes_to_open = (prv_pairs
            .get(&(start_valve.clone(), prv.to_string()))
            .unwrap()
            + 1) as i64;
        if required_minutes_to_open >= minutes_remaining {
            continue;
        }

        let num_minutes_releasing = minutes_remaining - required_minutes_to_open;
        let new_prv_to_visit = pressure_releasing_valves_to_visit
            .difference(&HashSet::from([prv.clone()]))
            .map(|prv| prv.clone())
            .collect::<HashSet<_>>();
        max = max.max(
            num_minutes_releasing * graph.get_rate(prv)
                + calculate(
                    prv,
                    graph,
                    prv_pairs,
                    &new_prv_to_visit,
                    num_minutes_releasing,
                ),
        );
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

    let pressure_releasing_values = graph
        .iter()
        .filter_map(|(valve, (rate, _))| if rate != &0 { Some(valve) } else { None })
        .collect::<HashSet<_>>();

    let pairs = get_pairs(&graph);

    let most_pressure = pairs
        .iter()
        .filter_map(|((from, to), required_minutes)| {
            if from == "AA" && pressure_releasing_values.contains(to) {
                let valve = to;
                let remaining_prv_to_visit = pressure_releasing_values
                    .difference(&HashSet::from([valve]))
                    .map(|prv| prv.to_string())
                    .collect::<HashSet<_>>();

                let minutes_remaining = 30 - required_minutes - 1;
                Some(
                    graph.get_rate(valve) * minutes_remaining
                        + calculate(
                            valve,
                            &graph,
                            &pairs,
                            &remaining_prv_to_visit,
                            minutes_remaining,
                        ),
                )
            } else {
                None
            }
        })
        .max()
        .unwrap();

    println!("{most_pressure}");

    Ok(())
}
