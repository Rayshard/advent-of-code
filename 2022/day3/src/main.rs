use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);
    let mut total = 0u32;

    for line in reader.lines() {
        let text = line?;
        let compartment_size = text.len() / 2;
        let (compartment1, compartment2) = (&text[..compartment_size], &text[compartment_size..]);
        let seen = HashSet::<char>::from_iter(compartment1.chars());

        for c in compartment2.chars() {
            if seen.contains(&c) {
                total += match c as u32 {
                    upper if upper >= 65 && upper <= 90  => upper - 64 + 26,
                    lower if lower >= 97 && lower <= 122  => lower - 96,
                    value => panic!("Invalid char: {value}")
                };

                break;
            }
        }
    }

    println!("{total}");

    Ok(())
}
