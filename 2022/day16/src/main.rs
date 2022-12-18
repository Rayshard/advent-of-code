use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

type Graph = HashMap<String, (u64, Vec<String>)>;

trait GraphTrait {
    fn get_rate(&self, valve: &str) -> u64;
    fn get_tunnels(&self, valve: &str) -> &Vec<String>;
}

impl GraphTrait for Graph {
    fn get_rate(&self, valve: &str) -> u64 {
        self.get(valve).unwrap().0
    }

    fn get_tunnels(&self, valve: &str) -> &Vec<String> {
        &self.get(valve).unwrap().1
    }
}

fn calculate(graph: &Graph, visited: &mut HashSet<String>, start_valve: &String) -> u64 {
    let mut to_move_to: Option<&String> = Some(start_valve);
    let mut to_open: Option<&String> = None;
    let mut opened = HashSet::<&String>::new();
    let mut total = 0;

    for minute in 1..=30 {
        if let Some(valve) = to_open {
            opened.insert(valve);
            total += (minute + 1) * graph.get_rate(valve);
        }

        to_open = to_move_to;
        to_move_to = None;
    }

    total
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
                .parse::<u64>()
                .unwrap();
            let tunnels = parts
                .skip(4)
                .map(|tunnel| tunnel.trim_end_matches(',').to_string())
                .collect::<Vec<_>>();

            (valve, (rate, tunnels))
        })
        .collect::<HashMap<_, _>>();

    let most_pressure = graph
        .keys()
        .map(|valve| calculate(&graph, &mut HashSet::new(), valve))
        .max()
        .unwrap();

    println!("{most_pressure}");

    Ok(())
}
