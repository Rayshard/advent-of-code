use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_visible(strip: &[(usize, u32)]) -> Vec<usize> {
    let mut visible: Vec<usize> = vec![(*strip.first().unwrap()).0, (*strip.last().unwrap()).0];

    for (i_strip, (i_map, height)) in strip.iter().enumerate() {
        let heights = strip.iter().map(|(_, h)| *h).collect::<Vec<_>>();
        let before_max = heights[..i_strip].iter().max().unwrap_or(&0);
        let after_max = heights[i_strip + 1..].iter().max().unwrap_or(&0);

        if before_max < height || after_max < height {
            visible.push(*i_map);
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

    let x = get_visible(&[(0, 6), (1, 7), (2, 5), (3, 3), (4, 5)]);
    let h: HashSet<&usize> = HashSet::from_iter(x.iter());
    println!("{:?}", h);

    Ok(())
}
