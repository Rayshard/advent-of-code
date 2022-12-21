use std::{
    collections::{HashMap, VecDeque},
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone)]
enum Operation {
    Add,
    Sub,
    Mul,
    Div,
}

impl Operation {
    pub fn perform(&self, left: i64, right: i64) -> i64 {
        match self {
            Operation::Add => left + right,
            Operation::Sub => left - right,
            Operation::Mul => left * right,
            Operation::Div => left / right,
        }
    }
}

#[derive(Debug, Clone)]
enum Job {
    Value(i64),
    ValueOpName(i64, Operation, String),
    NameOpValue(String, Operation, i64),
    NameOpName(String, Operation, String),
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut untouched = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let parts = line.split_whitespace().collect::<Vec<_>>();

            let name = parts[0].trim_end_matches(':').to_string();
            let job = match &parts[1..] {
                [value] => Job::Value(value.parse().unwrap()),
                [left, "+", right] => {
                    Job::NameOpName(left.to_string(), Operation::Add, right.to_string())
                }
                [left, "-", right] => {
                    Job::NameOpName(left.to_string(), Operation::Sub, right.to_string())
                }
                [left, "*", right] => {
                    Job::NameOpName(left.to_string(), Operation::Mul, right.to_string())
                }
                [left, "/", right] => {
                    Job::NameOpName(left.to_string(), Operation::Div, right.to_string())
                }
                parts => panic!("Invalid line: {parts:?}"),
            };

            (name, job)
        })
        .collect::<HashMap<_, _>>();

    let mut unresolved = VecDeque::from([untouched.remove_entry("root").unwrap()]);
    let mut resolved = HashMap::<String, i64>::new();

    while !unresolved.is_empty() {
        let (front_name, front_job) = unresolved.pop_front().unwrap();

        match &front_job {
            Job::Value(value) => {
                resolved.insert(front_name, *value);
            }
            Job::ValueOpName(value, op, name) => {
                if let Some(right) = resolved.get(name) {
                    resolved.insert(front_name, op.perform(*value, *right));
                } else {
                    unresolved.push_front((front_name, front_job.clone()));
                    unresolved.push_front(untouched.remove_entry(name).unwrap());
                }
            }
            Job::NameOpValue(name, op, value) => {
                if let Some(left) = resolved.get(name) {
                    resolved.insert(front_name, op.perform(*left, *value));
                } else {
                    unresolved.push_front((front_name, front_job.clone()));
                    unresolved.push_front(untouched.remove_entry(name).unwrap());
                }
            }
            Job::NameOpName(left_name, op, right_name) => {
                match (resolved.get(left_name), resolved.get(right_name)) {
                    (None, None) => {
                        unresolved.push_front((front_name, front_job.clone()));
                        unresolved.push_front(untouched.remove_entry(left_name).unwrap());
                        unresolved.push_front(untouched.remove_entry(right_name).unwrap());
                    }
                    (None, Some(value)) => {
                        unresolved.push_front((front_name, Job::NameOpValue(left_name, op, value)));
                        unresolved.push_front(untouched.remove_entry(left_name).unwrap());
                    },
                    (Some(_), None) => todo!(),
                    (Some(_), Some(_)) => todo!(),
                }
            }
        }
    }

    Ok(())
}
