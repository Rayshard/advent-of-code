use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut cur_elf_running_cal = 0;
    let mut largest_cal_count = 0;

    for line in reader.lines() {
        let value = line.unwrap();

        if value.is_empty() {
            cur_elf_running_cal = 0;
        } else {
            cur_elf_running_cal += value.parse::<i32>().unwrap();
            if cur_elf_running_cal > largest_cal_count {
                largest_cal_count = cur_elf_running_cal;
            }
        }
    }

    println!("{}", largest_cal_count);
    Ok(())
}
