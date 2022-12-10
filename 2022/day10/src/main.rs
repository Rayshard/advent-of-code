use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut register = 1i64;
    let mut cycle = 0;
    let mut total = 0;

    for line in reader.lines().map(|line| line.unwrap()) {
        let parts = line.split_whitespace().collect::<Vec<_>>();
        let values = match &parts[..] {
            ["noop"] => vec![0],
            ["addx", value] => vec![0, value.parse().unwrap()],
            other => panic!("Invalid instruction: {other:?}"),
        };

        for value in values {
            cycle += 1;

            if (cycle - 20) % 40 == 0 {
                total += cycle * register;
            }

            register += value;
        }
    }

    println!("{total}");

    Ok(())
}
