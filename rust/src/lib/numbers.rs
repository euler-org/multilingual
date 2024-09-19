pub fn is_palindromic(n: u64) -> bool {
    let n_str = n.to_string();
    let reversed_n_str: String = n_str.chars().rev().collect();
    n_str == reversed_n_str
}
