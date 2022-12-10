use std::{
    fmt,
    fs::File,
    io::{self, BufRead, BufReader},
};

#[allow(dead_code)]
struct CRT {
    width: usize,
    height: usize,
    pixels: Vec<bool>,
}

impl CRT {
    pub fn new(width: usize, height: usize) -> CRT {
        CRT {
            width,
            height,
            pixels: vec![false; width * height],
        }
    }

    pub fn set_pixel(&mut self, index: usize, value: bool) {
        self.pixels[index] = value;
    }
}

impl fmt::Display for CRT {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let lines = self.pixels.chunks(self.width).map(|line| {
            line.iter()
                .map(|b| if *b { '#' } else { ' ' })
                .collect::<String>()
        });

        for line in lines {
            writeln!(f, "{line}")?;
        }

        Ok(())
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut register = 1i64;
    let mut cycle = 0;
    let mut total = 0;
    let mut crt = CRT::new(40, 6);

    for line in reader.lines().map(|line| line.unwrap()) {
        let parts = line.split_whitespace().collect::<Vec<_>>();
        let values = match &parts[..] {
            ["noop"] => vec![0],
            ["addx", value] => vec![0, value.parse().unwrap()],
            other => panic!("Invalid instruction: {other:?}"),
        };

        for value in values {
            cycle += 1;

            // for part 1
            if (cycle - 20) % 40 == 0 {
                total += cycle * register;
            }

            // for part 2
            let cycle_minus_1 = cycle - 1;
            let sprite = (register - 1, register + 1);
            crt.set_pixel(
                cycle_minus_1 as usize,
                cycle_minus_1 % crt.width as i64 >= sprite.0 && cycle_minus_1 % crt.width as i64 <= sprite.1,
            );

            register += value;
        }
    }

    println!("{total}");
    println!("{crt}");

    Ok(())
}
