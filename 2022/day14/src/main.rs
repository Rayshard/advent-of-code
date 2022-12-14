use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone)]
enum Tile {
    Air,
    Rock,
    Sand,
}

type Map = HashMap<(i64, i64), Tile>;

fn get_tile(map: &Map, x: i64, y: i64) -> &Tile {
    map.get(&(x, y)).unwrap_or(&Tile::Air)
}

fn get_next_sand_pos(map: &Map, cur_pos: (i64, i64), floor: Option<i64>) -> (i64, i64) {
    let next_sand_pos = if matches!(get_tile(&map, cur_pos.0, cur_pos.1 + 1), Tile::Air) {
        (cur_pos.0, cur_pos.1 + 1)
    } else if matches!(get_tile(&map, cur_pos.0 - 1, cur_pos.1 + 1), Tile::Air) {
        (cur_pos.0 - 1, cur_pos.1 + 1)
    } else if matches!(get_tile(&map, cur_pos.0 + 1, cur_pos.1 + 1), Tile::Air) {
        (cur_pos.0 + 1, cur_pos.1 + 1)
    } else {
        cur_pos
    };

    if let Some(y) = floor {
        if next_sand_pos.1 >= y {
            return cur_pos;
        }
    }

    next_sand_pos
}

fn simulate_part1(map: &mut Map) -> usize {
    let map_start_size = map.len();
    let max_y = map.keys().max_by(|(_, y1), (_, y2)| y1.cmp(y2)).unwrap().1;

    let sand_source = (500, 0);
    let mut falling_sand_pos = sand_source.clone();

    loop {
        let next_sand_pos = get_next_sand_pos(&map, falling_sand_pos, None);

        if next_sand_pos == falling_sand_pos {
            map.insert(falling_sand_pos, Tile::Sand);
            falling_sand_pos = sand_source.clone();
        } else if next_sand_pos.1 >= max_y {
            return map.len() - map_start_size;
        } else {
            falling_sand_pos = next_sand_pos;
        }
    }
}

fn simulate_part2(map: &mut Map) -> usize {
    let map_start_size = map.len();
    let max_y = map.keys().max_by(|(_, y1), (_, y2)| y1.cmp(y2)).unwrap().1 + 2;

    let sand_source = (500, 0);
    let mut falling_sand_pos = sand_source.clone();

    loop {
        let next_sand_pos = get_next_sand_pos(&map, falling_sand_pos, Some(max_y));

        if next_sand_pos == falling_sand_pos {
            map.insert(falling_sand_pos, Tile::Sand);

            if next_sand_pos == sand_source {
                return map.len() - map_start_size;
            } else {
                falling_sand_pos = sand_source.clone();
            }
        } else {
            falling_sand_pos = next_sand_pos;
        }
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut map = Map::new();

    for line in reader.lines().map(|line| line.unwrap()) {
        let parts = line
            .split(" -> ")
            .map(|part| {
                part.split(",")
                    .map(|value| value.parse::<i64>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();

        for i in 0..parts.len() - 1 {
            let (from, to) = (&parts[i], &parts[i + 1]);

            let (from_x, to_x) = if from[0] < to[0] {
                (from[0], to[0])
            } else {
                (to[0], from[0])
            };
            
            let (from_y, to_y) = if from[1] < to[1] {
                (from[1], to[1])
            } else {
                (to[1], from[1])
            };

            for x in from_x..=to_x {
                for y in from_y..=to_y {
                    map.insert((x, y), Tile::Rock);
                }
            }
        }
    }

    println!("{}", simulate_part1(&mut map.clone()));
    println!("{}", simulate_part2(&mut map.clone()));

    Ok(())
}
