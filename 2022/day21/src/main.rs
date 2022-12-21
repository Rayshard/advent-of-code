use std::{
    collections::{HashMap, VecDeque},
    fs::File,
    io::{self, BufRead, BufReader},
};

#[derive(Debug, Clone, Copy)]
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
enum Expression {
    X,
    I64(i64),
    BinaryOperation(Box<Expression>, Operation, Box<Expression>),
}

#[derive(Debug, Clone)]
enum Job {
    Expression(Expression),
    ExpressionOpName(Expression, Operation, String),
    NameOpExpression(String, Operation, Expression),
    NameOpName(String, Operation, String),
}

fn calculate(jobs: &HashMap<String, Job>) -> Expression {
    let mut unresolved = VecDeque::from([("root".to_string(), jobs.get("root").unwrap().clone())]);
    let mut resolved = HashMap::<String, Expression>::new();

    while !unresolved.is_empty() {
        let (front_name, front_job) = unresolved.pop_front().unwrap();

        match &front_job {
            Job::Expression(value) => {
                resolved.insert(front_name, value.clone());
            }
            Job::ExpressionOpName(value, op, name) => {
                if let Some(right) = resolved.get(name) {
                    resolved.insert(
                        front_name,
                        match right {
                            Expression::X => Expression::BinaryOperation(
                                Box::new(value.clone()),
                                *op,
                                Box::new(Expression::X),
                            ),
                            Expression::I64(right_value) => {
                                Expression::BinaryOperation(Box::new(value.clone()), *op, Box::new(Expression::I64(*right_value)))
                            }
                            binop => Expression::BinaryOperation(
                                Box::new(value.clone()),
                                *op,
                                Box::new(binop.clone()),
                            ),
                        },
                    );
                } else {
                    unresolved.push_front((front_name, front_job.clone()));
                    unresolved.push_front((name.to_string(), jobs.get(name).unwrap().clone()));
                }
            }
            Job::NameOpExpression(name, op, value) => {
                if let Some(left) = resolved.get(name) {
                    resolved.insert(
                        front_name,
                        match left {
                            Expression::X => Expression::BinaryOperation(
                                Box::new(Expression::X),
                                *op,
                                Box::new(value.clone()),
                            ),
                            Expression::I64(left_value) => {
                                Expression::BinaryOperation(Box::new(Expression::I64(*left_value)), *op, Box::new(value.clone()))
                            }
                            binop => Expression::BinaryOperation(
                                Box::new(binop.clone()),
                                *op,
                                Box::new(value.clone()),
                            ),
                        },
                    );
                } else {
                    unresolved.push_front((front_name, front_job.clone()));
                    unresolved.push_front((name.to_string(), jobs.get(name).unwrap().clone()));
                }
            }
            Job::NameOpName(left_name, op, right_name) => {
                match (resolved.get(left_name), resolved.get(right_name)) {
                    (None, None) => {
                        unresolved.push_front((front_name, front_job.clone()));
                        unresolved.push_front((
                            left_name.to_string(),
                            jobs.get(left_name).unwrap().clone(),
                        ));
                        unresolved.push_front((
                            right_name.to_string(),
                            jobs.get(right_name).unwrap().clone(),
                        ));
                    }
                    (None, Some(value)) => {
                        unresolved.push_front((
                            front_name,
                            Job::NameOpExpression(left_name.to_string(), *op, value.clone()),
                        ));
                        unresolved.push_front((
                            left_name.to_string(),
                            jobs.get(left_name).unwrap().clone(),
                        ));
                    }
                    (Some(value), None) => {
                        unresolved.push_front((
                            front_name,
                            Job::ExpressionOpName(value.clone(), *op, right_name.to_string()),
                        ));
                        unresolved.push_front((
                            right_name.to_string(),
                            jobs.get(right_name).unwrap().clone(),
                        ));
                    }
                    (Some(left_value), Some(right_value)) => {
                        resolved.insert(front_name, Expression::BinaryOperation(Box::new(left_value.clone()), *op, Box::new(right_value.clone())));
                    }
                }
            }
        }
    }

    resolved.get("root").unwrap().clone()
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let jobs = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let parts = line.split_whitespace().collect::<Vec<_>>();

            let name = parts[0].trim_end_matches(':').to_string();
            let job = match &parts[1..] {
                [value] => Job::Expression(Expression::I64(value.parse().unwrap())),
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

    println!("{:#?}", calculate(&jobs));

    Ok(())
}
