use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn are_contained(a: (u32, u32), b: (u32, u32)) -> bool {
    a.0 >= b.0 && a.1 <= b.1 || b.0 >= a.0 && b.1 <= a.1
}

fn overlaps(a: (u32, u32), b: (u32, u32)) -> bool {
    a.0 >= b.0 && a.0 <= b.1
        || b.0 >= a.0 && b.0 <= a.1
        || a.1 >= b.0 && a.1 <= b.1
        || b.1 >= a.0 && b.1 <= a.1
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut part1_total = 0u32;
    let mut part2_total = 0u32;

    for line in reader.lines() {
        let ranges = &line
            .unwrap()
            .split(",")
            .map(|x| {
                x.split("-")
                    .map(|y| y.parse::<u32>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>()[..];

        if let [elf1, elf2] = ranges {
            if let ([min1, max1], [min2, max2]) = (&elf1[..], &elf2[..]) {
                part1_total += are_contained((*min1, *max1), (*min2, *max2)) as u32;
                part2_total += overlaps((*min1, *max1), (*min2, *max2)) as u32;
            }
        }
    }

    println!("{part1_total}");
    println!("{part2_total}");

    Ok(())
}
