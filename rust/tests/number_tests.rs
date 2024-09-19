#[cfg(test)]
mod tests {
    use lib::numbers::is_palindromic;

    #[test]
    fn test_is_palindromic_positive() {
        assert!(is_palindromic(0));
        assert!(is_palindromic(121));
        assert!(is_palindromic(12321));
        assert!(is_palindromic(123454321));
        assert!(is_palindromic(1234554321));
    }

    #[test]
    fn test_is_palindromic_negative() {
        assert!(!is_palindromic(123));
        assert!(!is_palindromic(123456));
    }
}
