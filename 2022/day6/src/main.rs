use std::{collections::HashSet, fs, io};

fn num_read_b4_all_distinct(input: &Vec<char>, size: usize) -> usize {
    for i in 0..(input.len() - (size - 1)) {
        let set: HashSet<&char> = HashSet::from_iter(&input[i..i + size]);
        if set.len() == size {
            return i + size;
        }
    }

    input.len()
}

fn main() -> io::Result<()> {
    let input = fs::read_to_string("input.txt")?.chars().collect::<Vec<_>>();

    let start_of_packet = num_read_b4_all_distinct(&input, 4);
    let start_of_message = num_read_b4_all_distinct(&input, 14);
    println!("{}", start_of_packet);
    println!("{}", start_of_message);
    Ok(())
}
