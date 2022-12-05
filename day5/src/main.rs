use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn get_top(stacks: &Vec<Vec<char>>) -> String {
    String::from_iter(stacks.into_iter().map(|stack| *stack.last().unwrap()))
}

fn rearrange_part1(stacks: &Vec<Vec<char>>, lines: &Vec<String>) -> Vec<Vec<char>> {
    let mut rearranged = stacks.clone();

    for line in lines {
        let elements = line.split_whitespace().collect::<Vec<_>>();
        let amount = elements[1].parse::<u32>().unwrap();
        let from = elements[3].parse::<usize>().unwrap() - 1;
        let to = elements[5].parse::<usize>().unwrap() - 1;
        
        for _ in 0..amount {
            let item = rearranged[from].pop().unwrap();
            rearranged[to].push(item);
        }
    }

    rearranged
}

fn rearrange_part2(stacks: &Vec<Vec<char>>, lines: &Vec<String>) -> Vec<Vec<char>> {
    let mut rearranged = stacks.clone();

    for line in lines {
        let elements = line.split_whitespace().collect::<Vec<_>>();
        let amount = elements[1].parse::<usize>().unwrap();
        let from = elements[3].parse::<usize>().unwrap() - 1;
        let to = elements[5].parse::<usize>().unwrap() - 1;
        
        let tail_start = rearranged[from].len() - amount;
        let items = rearranged[from].split_off(tail_start);
        rearranged[to].extend(items);
    }

    rearranged
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let mut reader = BufReader::new(file);

    let mut lines: Vec<String> = Vec::new();

    // Construct stacks
    loop {
        let mut line = String::new();
        reader.read_line(&mut line)?;

        // finished reading stacks
        if line.trim_start().starts_with("1") {
            let positions: HashMap<usize, usize> = line
                .chars()
                .enumerate()
                .filter_map(|(i, c)| {
                    if char::is_numeric(c) {
                        Some((i, (c.to_digit(10).unwrap() - 1) as usize))
                    } else {
                        None
                    }
                })
                .collect();

            let mut stacks: Vec<Vec<char>> = vec![Vec::new(); positions.len()];
            lines.reverse();

            for line in lines {
                let chars = line.chars().collect::<Vec<_>>();
                for (i_char, stack) in &positions {
                    let char = chars[*i_char];
                    if !char.is_whitespace() {
                        stacks[*stack].push(char);
                    }
                }
            }

            reader.read_line(&mut line)?; // skip new line after numbers

            let lines = reader.lines().map(|line| line.unwrap()).collect::<Vec<String>>();
            
            println!("{}", get_top(&rearrange_part1(&stacks, &lines)));
            println!("{}", get_top(&rearrange_part2(&stacks, &lines)));
            break;
        } else {
            lines.push(line);
        }
    }

    Ok(())
}
