use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_visible(strip: &[(usize, u32)]) -> Vec<usize> {
    let mut visible: Vec<usize> = Vec::new();
    let mut tallest = 0;
    
    // forward
    for (i, height) in strip {
        if tallest == 0 || height > &tallest {
            visible.push(*i);
            tallest = *height;
        }
    }

    tallest = 0;

    // reverse
    for (i, height) in strip.iter().rev() {
        if tallest == 0 || height > &tallest {
            visible.push(*i);
            tallest = *height;
        }
    }

    return visible;
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let input = reader
        .lines()
        .flat_map(|line| line.unwrap().chars().collect::<Vec<_>>())
        .map(|c| c.to_digit(10).unwrap())
        .enumerate()
        .collect::<Vec<_>>();

    // I'm making the terrible assumption that the input is a square
    let size = (input.len() as f64).sqrt() as usize;

    let rows = input.chunks(size).collect::<Vec<_>>();
    let cols = (0..size)
        .map(|i| {
            rows.iter()
                .map(|row| *row.get(i).unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    // Contains the indices that were seen
    let mut visible: HashSet<usize> = HashSet::new();

    for row in rows {
        visible.extend(get_visible(row));
    }

    for col in cols {
        visible.extend(get_visible(&col));
    }

    let num_visible = visible.len();
    println!("{num_visible:?}");

    Ok(())
}
