use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut totals = vec![0];

    for line in reader.lines() {
        let value = line.unwrap();

        if value.is_empty() {
            totals.push(0);
        }
        else {
            *totals.last_mut().unwrap() += value.parse::<i32>().unwrap();
        }
    }

    totals.sort();

    let largest_cal_count =  totals.last().unwrap();
    println!("{}", largest_cal_count);

    let top_3_cal_sum: i32 = totals[(totals.len() - 3)..].iter().sum();
    println!("{}", top_3_cal_sum);
    
    Ok(())
}
