import unittest
import app

class TestPrime(unittest.TestCase):
    def test_is_prime(self):
        primes = [2, 3, 5, 47, 211, 1117, 7741, 7879, 494933, 63480017]
        for prime in primes:
            self.assertTrue(app.is_prime_sync(prime), prime)

    def test_is_not_prime(self):
        nonprimes = [-1, 0, 1, 8, 16, 69, 77, 5823, 6629, 7721, 459655]
        for nonprime in nonprimes:
            self.assertFalse(app.is_prime_sync(nonprime), nonprime)


if __name__ == "__main__":
    unittest.main()
