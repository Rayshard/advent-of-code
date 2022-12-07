use std::{collections::HashSet, fs, io};

fn get_part1(input: &Vec<char>) -> usize {
    for i in 0..(input.len() - 3) {
        let set: HashSet<&char> = HashSet::from_iter(&input[i..i + 4]);
        if set.len() == 4 {
            return i + 4;
        }
    }

    input.len()
}

fn main() -> io::Result<()> {
    let input = fs::read_to_string("input.txt")?.chars().collect::<Vec<_>>();


    println!("{}", get_part1(&input));
    Ok(())
}
