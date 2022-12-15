use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_num_invalid_row_positions(row: i64, map: &HashMap<(i64, i64), (i64, i64)>) -> usize {
    let mut invalid_row_positions = HashSet::<i64>::new();

    for ((sensor_x, sensor_y), (beacon_x, beacon_y)) in map {
        let dist_to_beacon = (sensor_x - beacon_x).abs() + (sensor_y - beacon_y).abs();
        let dist_to_row = (sensor_y - row).abs();

        if dist_to_row > dist_to_beacon {
            continue;
        }

        let remaining_dist = dist_to_beacon - dist_to_row;
        let (min_x, max_x) = (sensor_x - remaining_dist, sensor_x + remaining_dist);

        for x in min_x..=max_x {
            invalid_row_positions.insert(x);
        }

        // if the beacon is in the row, we need to remove it
        if beacon_y == &row && invalid_row_positions.contains(beacon_x) {
            invalid_row_positions.remove(beacon_x);
        }
    }

    invalid_row_positions.len()
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    // a map of the sensor coords to the distance to their closest beacon
    let map = reader
        .lines()
        .map(|line| {
            let parts = line
                .unwrap()
                .split_whitespace()
                .filter_map(|part| {
                    if part.contains('=') {
                        let value = part
                            .trim_end_matches(&[':', ','])
                            .split('=')
                            .nth(1)
                            .unwrap()
                            .parse::<i64>()
                            .unwrap();

                        Some(value)
                    } else {
                        None
                    }
                })
                .collect::<Vec<_>>();

            ((parts[0], parts[1]), (parts[2], parts[3]))
        })
        .collect::<HashMap<_, _>>();

    println!("{}", get_num_invalid_row_positions(2000000, &map));

    Ok(())
}
