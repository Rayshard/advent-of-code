use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_visible(strip: &[(usize, u32)]) -> Vec<usize> {
    let mut visible: Vec<usize> = vec![(*strip.first().unwrap()).0, (*strip.last().unwrap()).0];

    // forward
    let mut tallest = 0u32;

    for (i_map, height) in strip {
        if height > &tallest {
            tallest = *height;
            visible.push(*i_map);
        }
    }

    // reverse
    tallest = 0u32;

    for (i_map, height) in strip.iter().rev() {
        if height > &tallest {
            tallest = *height;
            visible.push(*i_map);
        }
    }

    return visible;
}

fn get_sceneic_score(
    position: (usize, usize),
    rows: &[&[(usize, u32)]],
    cols: &Vec<Vec<(usize, u32)>>,
) -> u32 {
    let tree_height = &rows[position.0][position.1].1;
    let mut from_left = 0u32;
    let mut from_right = 0u32;
    let mut from_top = 0u32;
    let mut from_bottom = 0u32;

    for (_, h) in rows[position.0][..position.1].iter().rev() {
        from_left += 1;

        if h >= tree_height {
            break;
        }
    }

    for (_, h) in rows[position.0][position.1 + 1..].iter() {
        from_right += 1;

        if h >= tree_height {
            break;
        }
    } 
    
    for (_, h) in cols[position.1][..position.0].iter().rev() {
        from_top += 1;

        if h >= tree_height {
            break;
        }
    }

    for (_, h) in cols[position.1][position.0 + 1..].iter() {
        from_bottom += 1;

        if h >= tree_height {
            break;
        }
    }
    
    return (from_left * from_right * from_top * from_bottom) as u32;
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

    // Construct rows and columns
    let rows = input.chunks(size).collect::<Vec<_>>();
    let cols = (0..size)
        .map(|i| {
            rows.iter()
                .map(|row| *row.get(i).unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    // Part 1
    let mut visible: HashSet<usize> = HashSet::new();

    for row in rows.iter() {
        visible.extend(get_visible(row));
    }

    for col in cols.iter() {
        visible.extend(get_visible(&col));
    }

    println!("{:?}", visible.len());

    // Part 2
    let max_scenic_score = (0..size)
        .flat_map(|i_row| (0..size).map(move |i_col| (i_row, i_col)))
        .map(|pos| get_sceneic_score(pos, &rows, &cols))
        .max()
        .unwrap_or(0);

    println!("{max_scenic_score}");

    Ok(())
}
