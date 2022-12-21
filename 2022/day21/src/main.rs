use std::{
    collections::{HashMap, VecDeque},
    fmt::Display,
    fs::File,
    io::{self, BufRead, BufReader},
    str::FromStr,
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

    pub fn inverse(&self) -> Operation {
        match self {
            Operation::Add => Operation::Sub,
            Operation::Sub => Operation::Add,
            Operation::Mul => Operation::Div,
            Operation::Div => Operation::Mul,
        }
    }
}

impl FromStr for Operation {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "+" => Ok(Operation::Add),
            "-" => Ok(Operation::Sub),
            "*" => Ok(Operation::Mul),
            "/" => Ok(Operation::Div),
            s => Err(format!("Unable to parse operation from: {s}")),
        }
    }
}

impl Display for Operation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Operation::Add => write!(f, "+"),
            Operation::Sub => write!(f, "-"),
            Operation::Mul => write!(f, "*"),
            Operation::Div => write!(f, "/"),
        }
    }
}

#[derive(Debug, Clone)]
enum Expression {
    X,
    I64(i64),
    BinaryOperation(Box<Expression>, Operation, Box<Expression>),
}

impl Expression {
    pub fn reduce(&self) -> Expression {
        match self {
            Expression::BinaryOperation(left, op, right) => {
                match (left.as_ref(), *op, right.as_ref()) {
                    (Expression::X, Operation::Add, Expression::X) => Expression::BinaryOperation(
                        Box::new(Expression::X),
                        Operation::Mul,
                        Box::new(Expression::I64(2)),
                    ),
                    (Expression::X, Operation::Add, Expression::BinaryOperation(_, _, _)) => {
                        todo!()
                    }
                    (Expression::X, Operation::Sub, Expression::X) => Expression::BinaryOperation(
                        Box::new(Expression::X),
                        Operation::Mul,
                        Box::new(Expression::I64(-2)),
                    ),
                    (Expression::X, Operation::Sub, Expression::BinaryOperation(_, _, _)) => {
                        todo!()
                    }
                    (Expression::X, Operation::Mul, Expression::X) => todo!(),
                    (Expression::X, Operation::Mul, Expression::BinaryOperation(_, _, _)) => {
                        todo!()
                    }
                    (Expression::X, Operation::Div, Expression::X) => Expression::I64(1),
                    (Expression::X, Operation::Div, Expression::BinaryOperation(_, _, _)) => {
                        todo!()
                    }
                    (Expression::I64(left), op, Expression::I64(right)) => {
                        Expression::I64(op.perform(*left, *right))
                    }
                    (Expression::I64(left), op, Expression::BinaryOperation(_, _, _)) => {
                        Expression::BinaryOperation(
                            Box::new(Expression::I64(*left)),
                            op,
                            Box::new(right.reduce()),
                        )
                    }
                    (Expression::BinaryOperation(_, _, _), op, Expression::I64(right)) => {
                        Expression::BinaryOperation(
                            Box::new(left.reduce()),
                            op,
                            Box::new(Expression::I64(*right)),
                        )
                    }
                    (Expression::BinaryOperation(_, _, _), Operation::Add, Expression::X) => {
                        todo!()
                    }
                    (
                        Expression::BinaryOperation(_, _, _),
                        Operation::Add,
                        Expression::BinaryOperation(_, _, _),
                    ) => todo!(),
                    (Expression::BinaryOperation(_, _, _), Operation::Sub, Expression::X) => {
                        todo!()
                    }
                    (
                        Expression::BinaryOperation(_, _, _),
                        Operation::Sub,
                        Expression::BinaryOperation(_, _, _),
                    ) => todo!(),
                    (Expression::BinaryOperation(_, _, _), Operation::Mul, Expression::X) => {
                        todo!()
                    }
                    (
                        Expression::BinaryOperation(_, _, _),
                        Operation::Mul,
                        Expression::BinaryOperation(_, _, _),
                    ) => todo!(),
                    (Expression::BinaryOperation(_, _, _), Operation::Div, Expression::X) => {
                        todo!()
                    }

                    (
                        Expression::BinaryOperation(_, _, _),
                        Operation::Div,
                        Expression::BinaryOperation(_, _, _),
                    ) => todo!(),
                    _ => self.clone(),
                }
            }
            _ => self.clone(),
        }
    }
}

impl Display for Expression {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Expression::X => write!(f, "x"),
            Expression::I64(value) => write!(f, "{value}"),
            Expression::BinaryOperation(left, op, right) => write!(f, "({left} {op} {right})"),
        }
    }
}

#[derive(Debug, Clone)]
enum Job {
    Expression(Expression),
    ExpressionOpName(Expression, Operation, String),
    NameOpExpression(String, Operation, Expression),
    NameOpName(String, Operation, String),
}

fn calculate(name: &str, jobs: &HashMap<String, Job>) -> Expression {
    let mut unresolved = VecDeque::from([(name.to_string(), jobs.get(name).unwrap().clone())]);
    let mut resolved = HashMap::<String, Expression>::new();

    while !unresolved.is_empty() {
        let (front_name, front_job) = unresolved.pop_front().unwrap();

        match &front_job {
            Job::Expression(value) => {
                resolved.insert(front_name, value.reduce());
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
                            )
                            .reduce(),
                            Expression::I64(right_value) => Expression::BinaryOperation(
                                Box::new(value.clone()),
                                *op,
                                Box::new(Expression::I64(*right_value)),
                            )
                            .reduce(),
                            binop => Expression::BinaryOperation(
                                Box::new(value.clone()),
                                *op,
                                Box::new(binop.clone()),
                            )
                            .reduce(),
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
                            )
                            .reduce(),
                            Expression::I64(left_value) => Expression::BinaryOperation(
                                Box::new(Expression::I64(*left_value)),
                                *op,
                                Box::new(value.clone()),
                            )
                            .reduce(),
                            binop => Expression::BinaryOperation(
                                Box::new(binop.clone()),
                                *op,
                                Box::new(value.clone()),
                            )
                            .reduce(),
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
                        resolved.insert(
                            front_name,
                            Expression::BinaryOperation(
                                Box::new(left_value.clone()),
                                *op,
                                Box::new(right_value.clone()),
                            )
                            .reduce(),
                        );
                    }
                }
            }
        }
    }

    resolved.get(name).unwrap().reduce()
}

fn solve(left: &Expression, right: &Expression) -> Result<i64, String> {
    let (mut result, mut expr_with_x) = match (left.reduce(), right.reduce()) {
        (Expression::I64(value), Expression::BinaryOperation(_, _, _)) => (value, right),
        (Expression::BinaryOperation(_, _, _), Expression::I64(value)) => (value, left),
        _ => todo!(),
    };

    loop {
        let new_expr_with_x: &Expression;

        match expr_with_x {
            Expression::X => return Ok(result),
            Expression::BinaryOperation(left, op, right) => {
                match (left.as_ref(), op, right.as_ref()) {
                    (Expression::BinaryOperation(_, _, _), op, Expression::I64(value)) => {
                        result = op.inverse().perform(result, *value);
                        new_expr_with_x = left.as_ref();
                    },
                    (Expression::I64(value), Operation::Add, Expression::BinaryOperation(_, _, _))  => {
                        result = Operation::Sub.perform(result, *value);
                        new_expr_with_x = right.as_ref();
                    },
                    (Expression::I64(value), Operation::Sub, Expression::BinaryOperation(_, _, _))  => {
                        result = Operation::Sub.perform(-result, -*value);
                        new_expr_with_x = right.as_ref();
                    },
                    (Expression::I64(value), Operation::Mul, Expression::BinaryOperation(_, _, _))  => {
                        result = Operation::Div.perform(result, *value);
                        new_expr_with_x = right.as_ref();
                    },
                    (Expression::X, op, Expression::I64(value)) => {
                        return Ok(op.inverse().perform(result, *value));
                    },
                    _ => todo!("I was too lazy to implement this because the problem was solved without it")
                }
            }
            expr => return Err(format!("No x found in {expr}")),
        }

        expr_with_x = new_expr_with_x;
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut jobs = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let parts = line.split_whitespace().collect::<Vec<_>>();

            let name = parts[0].trim_end_matches(':').to_string();
            let job = match &parts[1..] {
                [value] => Job::Expression(Expression::I64(value.parse().unwrap())),
                [left, op, right] => {
                    Job::NameOpName(left.to_string(), op.parse().unwrap(), right.to_string())
                }
                parts => panic!("Invalid line: {parts:?}"),
            };

            (name, job)
        })
        .collect::<HashMap<_, _>>();

    // Part 1
    if let Expression::I64(result) = calculate("root", &jobs) {
        println!("{result}");
    } else {
        panic!("Problem with part 1!");
    }

    // Part 2
    jobs.insert("humn".to_string(), Job::Expression(Expression::X));

    let (left, right) = match jobs.get("root").unwrap() {
        Job::Expression(expr) => match expr {
            Expression::BinaryOperation(left, _, right) => (left.reduce(), right.reduce()),
            _ => panic!("Job is not a binary expression!"),
        },
        Job::ExpressionOpName(left, _, right) => (left.reduce(), calculate(right, &jobs)),
        Job::NameOpExpression(left, _, right) => (calculate(left, &jobs), right.reduce()),
        Job::NameOpName(left, _, right) => (calculate(left, &jobs), calculate(right, &jobs)),
    };

    println!("{}", solve(&left, &right).unwrap());

    Ok(())
}
