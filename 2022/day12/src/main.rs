use std::{
    collections::{HashMap, VecDeque},
    fs::File,
    io::{self, BufRead, BufReader},
};

fn find_path(start: (i64, i64), end: (i64, i64), grid: &HashMap<(i64, i64), u64>) -> Option<u64> {
    let mut seen: HashMap<(i64, i64), u64> = HashMap::new();
    let mut to_visit: VecDeque<((i64, i64), u64)> = VecDeque::new();

    to_visit.push_back((start, 0));

    while !to_visit.is_empty() {
        let (cur_pos, cur_step) = to_visit.pop_front().unwrap();

        if cur_pos == end {
            continue;
        }

        let surrounding = [
            (cur_pos.0 + 1, cur_pos.1),
            (cur_pos.0 - 1, cur_pos.1),
            (cur_pos.0, cur_pos.1 + 1),
            (cur_pos.0, cur_pos.1 - 1),
        ];

        let next_step = cur_step + 1;

        for coord in surrounding {
            if seen.contains_key(&coord)
                || !grid.contains_key(&coord)
                || grid.get(&coord).unwrap() > &(grid.get(&cur_pos).unwrap() + 1)
            {
                continue;
            }

            seen.insert(coord, next_step);
            to_visit.push_back((coord, next_step));
        }
    }

    match seen.get(&end) {
        Some(value) => Some(*value),
        None => None
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut grid: HashMap<(i64, i64), u64> = HashMap::new();
    let mut start: (i64, i64) = (0, 0);
    let mut end: (i64, i64) = (0, 0);

    for (y, line) in reader.lines().map(|line| line.unwrap()).enumerate() {
        for (x, c) in line.chars().enumerate() {
            let coord = (x as i64, y as i64);

            grid.insert(
                coord,
                match c {
                    'S' => {
                        start = coord;
                        'a' as u64
                    }
                    'E' => {
                        end = coord;
                        'z' as u64
                    }
                    c => c as u64,
                },
            );
        }
    }

    println!("{}", find_path(start, end, &grid).unwrap());

    let mut path_lengths = grid
        .iter()
        .filter_map(|(key, value)| {
            if *value == 'a' as u64 {
                find_path(*key, end, &grid)
            } else {
                None
            }
        })
        .collect::<Vec<_>>();

    path_lengths.sort();
    println!("{}", path_lengths.first().unwrap());

    Ok(())
}
