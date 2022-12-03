use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_priority(c: char) -> u32 {
    match c as u32 {
        upper if upper >= 65 && upper <= 90 => upper - 64 + 26,
        lower if lower >= 97 && lower <= 122 => lower - 96,
        value => panic!("Invalid char: {value}"),
    }
}

fn get_part1(lines: &Vec<String>) -> u32 {
    let mut total = 0u32;

    for line in lines {
        let compartment_size = line.len() / 2;
        let (compartment1, compartment2) = (&line[..compartment_size], &line[compartment_size..]);
        let seen = HashSet::<char>::from_iter(compartment1.chars());

        for c in compartment2.chars() {
            if seen.contains(&c) {
                total += get_priority(c);
                break;
            }
        }
    }

    return total;
}

fn get_part2(lines: &Vec<String>) -> u32 {
    let mut total = 0u32;
    let chunks = lines.chunks(3);

    for chunk in chunks {
        let elves: Vec<HashSet<_>> = chunk
            .iter()
            .map(|line| HashSet::<char>::from_iter(line.chars()))
            .collect();

        let common : HashSet<char> = elves[0].intersection(&elves[1]).map(|c| *c).collect();
        let common : HashSet<char> = common.intersection(&elves[2]).map(|c| *c).collect();
        total += common.iter().map(|c| get_priority(*c)).sum::<u32>();
    }

    return total;
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let lines = BufReader::new(file)
        .lines()
        .map(|l| l.expect("Could not parse line"))
        .collect();

    println!("{}", get_part1(&lines));
    println!("{}", get_part2(&lines));

    Ok(())
}
