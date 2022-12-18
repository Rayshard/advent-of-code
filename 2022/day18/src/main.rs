use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

type Position = (i64, i64, i64);

fn get_adjacent((x, y, z): Position) -> Vec<Position> {
    vec![
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]
}

fn get_exterior_surface_area(cubes: &HashSet<Position>) -> usize {
    let (mut min_x, mut min_y, mut min_z) = cubes.iter().next().unwrap();
    let (mut max_x, mut max_y, mut max_z) = cubes.iter().next().unwrap();

    for (x, y, z) in cubes {
        if x < &min_x {
            min_x = *x;
        }
        if y < &min_y {
            min_y = *y;
        }
        if z < &min_z {
            min_z = *z;
        }
        if x > &max_x {
            max_x = *x;
        }
        if y > &max_y {
            max_y = *y;
        }
        if z > &max_z {
            max_z = *z;
        }
    }

    min_x -= 1;
    min_y -= 1;
    min_z -= 1;
    max_x += 1;
    max_y += 1;
    max_z += 1;

    let mut exterior_surface_area = 0;
    let mut visited_air_blocks = HashSet::<Position>::new();
    let mut air_blocks_to_visit = HashSet::<Position>::new();
    air_blocks_to_visit.insert((min_x, min_y, min_z));

    while !air_blocks_to_visit.is_empty() {
        let current = *air_blocks_to_visit.iter().next().unwrap();
        air_blocks_to_visit.remove(&current);

        visited_air_blocks.insert(current);

        for pos in get_adjacent(current) {
            if visited_air_blocks.contains(&pos) {
                continue;
            } else if cubes.contains(&pos) {
                exterior_surface_area += 1;
            } else {
                let (adj_x, adj_y, adj_z) = pos;

                // check if prospect air block is outside of enclosing cube
                if adj_x < min_x
                    || adj_y < min_y
                    || adj_z < min_z
                    || adj_x > max_x
                    || adj_y > max_y
                    || adj_z > max_z
                {
                    continue;
                }

                air_blocks_to_visit.insert(pos);
            }
        }
    }

    exterior_surface_area
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut cubes = HashSet::<Position>::new();
    let mut surface_area = 0;

    for line in reader.lines().map(|line| line.unwrap()) {
        let coords = line
            .split(',')
            .map(|coord| coord.parse::<i64>().unwrap())
            .collect::<Vec<_>>();
        let coords = (coords[0], coords[1], coords[2]);

        cubes.insert(coords);

        for pos in get_adjacent(coords) {
            if cubes.contains(&pos) {
                surface_area -= 1;
            } else {
                surface_area += 1;
            }
        }
    }

    println!("{surface_area}");
    println!("{}", get_exterior_surface_area(&cubes));

    Ok(())
}
