use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead, BufReader},
};

type Element = (i64, usize);

fn swap_forward(element: Element, elements: &mut Vec<Element>, map: &mut HashMap<Element, usize>) {
    let elem_cur_index = *map.get(&element).unwrap();
    let elem_new_index = (elem_cur_index + 1) % elements.len();
    let elem_to_swap_with = elements.get_mut(elem_new_index).unwrap();

    map.insert(element, elem_new_index);
    map.insert(*elem_to_swap_with, elem_cur_index);

    elements[elem_cur_index] = *elem_to_swap_with;
    elements[elem_new_index] = element;
}

fn swap_backward(element: Element, elements: &mut Vec<Element>, map: &mut HashMap<Element, usize>) {
    let elem_cur_index = *map.get(&element).unwrap();
    let elem_new_index = if elem_cur_index == 0 {
        elements.len() - 1
    } else {
        elem_cur_index - 1
    };
    let elem_to_swap_with = elements.get_mut(elem_new_index).unwrap();

    map.insert(element, elem_new_index);
    map.insert(*elem_to_swap_with, elem_cur_index);

    elements[elem_cur_index] = *elem_to_swap_with;
    elements[elem_new_index] = element;
}

fn calculate(initial_elements: &Vec<i64>, num_times_to_mix: usize) -> i64 {
    let mut updated_elements = initial_elements
        .iter()
        .enumerate()
        .map(|(i, num)| (*num, i))
        .collect::<Vec<_>>();
    let mut current_map = updated_elements
        .iter()
        .map(|(num, i)| ((*num, *i), *i))
        .collect::<HashMap<_, _>>();

    for _ in 1..=num_times_to_mix {
        for (i, num) in initial_elements.iter().enumerate() {
            let count = num % ((initial_elements.len() - 1) as i64);

            if num >= &0 {
                for _ in 1..=count {
                    swap_forward((*num, i), &mut updated_elements, &mut current_map);
                }
            } else {
                for _ in 1..=-count {
                    swap_backward((*num, i), &mut updated_elements, &mut current_map);
                }
            }
        }
    }

    let ((_, _), index_of_zero) = current_map
        .iter()
        .find(|((value, _), _)| value == &0)
        .unwrap();

    let (num1000, _) = updated_elements[(index_of_zero + 1000) % updated_elements.len()];
    let (num2000, _) = updated_elements[(index_of_zero + 2000) % updated_elements.len()];
    let (num3000, _) = updated_elements[(index_of_zero + 3000) % updated_elements.len()];

    num1000 + num2000 + num3000
}

fn main() -> io::Result<()> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    // Part 1
    let initial_elements = reader
        .lines()
        .map(|line| line.unwrap().parse::<i64>().unwrap())
        .collect::<Vec<_>>();

    println!("{}", calculate(&initial_elements, 1));

    //Part 2
    let initial_elements = initial_elements
        .iter()
        .map(|num| num * 811589153)
        .collect::<Vec<_>>();
    
    println!("{}", calculate(&initial_elements, 10));
    
    Ok(())
}
