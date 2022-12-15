use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufRead, BufReader},
};

fn consolidate_ranges(ranges: &mut Vec<(i64, i64)>) -> Vec<(i64, i64)> {
    ranges.sort_by(|a, b| a.0.cmp(&b.0));

    let mut result = Vec::new();
    if let Some(range) = ranges.get(0) {
        result.push(*range);
    }

    for (min, max) in &ranges[1..] {
        let (_, prev_max) = result.last_mut().unwrap();

        if min <= &(*prev_max + 1) {
            if max <= prev_max {
                continue;
            } else {
                *prev_max = *max;
            }
        } else {
            result.push((*min, *max));
        }
    }

    result
}

fn get_invalid_ranges_in_row(row: i64, map: &HashMap<(i64, i64), (i64, i64)>) -> Vec<(i64, i64)> {
    let mut invalid_ranges = Vec::<(i64, i64)>::new();

    for ((sensor_x, sensor_y), (beacon_x, beacon_y)) in map {
        let dist_to_beacon = (sensor_x - beacon_x).abs() + (sensor_y - beacon_y).abs();
        let dist_to_row = (sensor_y - row).abs();

        if dist_to_row > dist_to_beacon {
            continue;
        }

        let remaining_dist = dist_to_beacon - dist_to_row;
        let range = (sensor_x - remaining_dist, sensor_x + remaining_dist);

        // if the beacon is in the row, we need to remove it
        if beacon_y == &row && (sensor_x - beacon_x).abs() <= remaining_dist {
            if range.0 == range.1 {
                continue;
            } else if beacon_x == &range.0 {
                invalid_ranges.push((range.0 + 1, range.1));
            } else {
                invalid_ranges.push((range.0, range.1 - 1));
            }
        } else {
            invalid_ranges.push(range);
        }
    }

    consolidate_ranges(&mut invalid_ranges)
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

    // Part 1
    {
        let num_invalid_positions = get_invalid_ranges_in_row(2000000, &map)
            .iter()
            .fold(0, |acc, (min, max)| acc + (max - min + 1));

        println!("{:#?}", num_invalid_positions);
    }

    // Part 2
    let mut row_beacons = HashMap::<i64, HashSet<i64>>::new();
    for (x, row) in map.values() {
        if row_beacons.contains_key(row) {
            row_beacons.get_mut(row).unwrap().insert(*x);
        } else {
            row_beacons.insert(*row, HashSet::from([*x]));
        }
    }

    for row in 0..=4000000 {
        let invalid_ranges_in_row = get_invalid_ranges_in_row(row, &map);

        match &invalid_ranges_in_row[..] {
            // the whole row is invalid
            [_] => continue,

            // the row has one valid position (which may be a good beacon)
            [(_, left), (right, _)] if *right == left + 2 => {
                let x = left + 1;

                // skip if the valid position is a good beacon
                if let Some(beacons) = row_beacons.get(&row) {
                    if beacons.contains(&x) {
                        continue;
                    }
                }

                println!("{x}, {row}, {}", x * 4000000 + row);
                break;
            }

            // I did something wrong lol
            ranges => panic!("A row has weird ranges: {ranges:?}"),
        }
    }

    Ok(())
}
