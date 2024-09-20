use core::panic;
use std::env;
use std::time::Instant;

use lib::numbers::is_palindromic;

fn get_answer(number_of_digits: u32) -> Result<u64, &'static str> {
    let lower_bound = 10_u64.pow(number_of_digits - 1);
    let upper_bound = 10 * lower_bound;
    let mut largest_palindrome: u64 = 0;
    for i in (lower_bound..upper_bound).rev() {
        if i * upper_bound < largest_palindrome {
            return Ok(largest_palindrome);
        }
        for j in (i..upper_bound).rev() {
            let multiple = i * j;
            if largest_palindrome > multiple {
                break;
            }
            if is_palindromic(multiple) {
                largest_palindrome = multiple;
            }
        }
    }
    return Err("No palindrome found");
}

fn proxy(case_key: &str, number_of_digits: u32) {
    let start = Instant::now();
    let answer = get_answer(number_of_digits);
    let duration = start.elapsed();
    println!("Time {} {}", case_key, duration.as_nanos());
    println!(
        "Answer {} {}",
        case_key,
        answer.unwrap_or_else(|err| panic!("error: {}", err))
    );
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let case_key = &args[1];
    let number_of_digits: u32 = args[2].parse().expect("Not a number!");
    proxy(case_key, number_of_digits);
}
