use std::{
    cmp::Ordering,
    fs::File,
    io::{self, BufRead, BufReader},
};

use nom::{
    branch::alt,
    character::complete::{char, one_of},
    combinator::recognize,
    multi::{many1, separated_list0},
    sequence::delimited,
    IResult,
};

#[derive(Debug, Clone)]
enum PacketElement {
    Integer(u64),
    List(Vec<PacketElement>),
}

fn parse_integer_element(input: &str) -> IResult<&str, PacketElement> {
    let (input, value) = recognize(many1(one_of("0123456789")))(input)?;

    Ok((input, PacketElement::Integer(value.parse().unwrap())))
}

fn parse_list_element(input: &str) -> IResult<&str, PacketElement> {
    let (input, value) = delimited(
        char('['),
        separated_list0(char(','), alt((parse_integer_element, parse_list_element))),
        char(']'),
    )(input)?;

    Ok((
        input,
        PacketElement::List(value.iter().map(|elem| elem.clone()).collect()),
    ))
}

fn compare(packet1: &PacketElement, packet2: &PacketElement) -> Ordering {
    match (packet1, packet2) {
        (PacketElement::Integer(value1), PacketElement::Integer(value2)) => value1.cmp(value2),
        (PacketElement::Integer(_), PacketElement::List(_)) => {
            compare(&PacketElement::List(vec![packet1.clone()]), packet2)
        }
        (PacketElement::List(_), PacketElement::Integer(_)) => {
            compare(packet1, &PacketElement::List(vec![packet2.clone()]))
        }
        (PacketElement::List(list1), PacketElement::List(list2)) => {
            let len_comparison = list1.len().cmp(&list2.len());
            let min_list_len = std::cmp::min(list1.len(), list2.len());

            for i in 0..min_list_len {
                match compare(list1.get(i).unwrap(), list2.get(i).unwrap()) {
                    Ordering::Equal => continue,
                    order => return order,
                }
            }

            len_comparison
        }
    }
}

impl PartialEq for PacketElement {
    fn eq(&self, other: &Self) -> bool {
        compare(self, other) == Ordering::Equal
    }
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);
    let packets = reader
        .lines()
        .filter_map(|line| {
            let line = line.unwrap();
            if line.is_empty() {
                None
            } else {
                Some(parse_list_element(&line).unwrap().1)
            }
        })
        .collect::<Vec<_>>();

    // Part 1
    let num_right_order: usize = packets
        .chunks(2)
        .enumerate()
        .map(|(i, pair)| {
            if compare(&pair[0], &pair[1]) == Ordering::Less {
                i + 1
            } else {
                0
            }
        })
        .sum();

    println!("{num_right_order}");

    // Part 2
    let (divider1, divider2) = (
        parse_list_element("[[2]]").unwrap().1,
        parse_list_element("[[6]]").unwrap().1,
    );

    let mut copy = packets.clone();
    copy.push(divider1.clone());
    copy.push(divider2.clone());
    copy.sort_by(compare);

    let mut decoder_key = 0;

    for (i, elem) in copy.iter().enumerate() {
        if elem == &divider1 {
            decoder_key = i + 1;
        } else if elem == &divider2 {
            decoder_key *= i + 1;
            break;
        }
    }
    
    println!("{decoder_key}");

    Ok(())
}
