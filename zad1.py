import math
from collections import Counter
import string

"""
is_palindrome(text: str) -> bool - sprawdza, czy dany ciąg znaków jest palindromem
(ignorując wielkość liter i spacje).
2. fibonacci(n: int) -> int - zwraca n-ty element ciągu Fibonacciego (Załóż, że
fibonacci(0) == 0 , fibonacci(1) == 1 .).
3. count_vowels(text: str) -> int - zlicza liczbę samogłosek w podanym ciągu (a, e, i, o, u,
y – wielkość liter bez znaczenia).
4. calculate_discount(price: float, discount: float) -> float - zwraca cenę po uwzględnieniu zniżki
(np. calculate_discount(100, 0.2) → 80).
Jeśli discount jest spoza zakresu 0–1, ma zostać zgłoszony wyjątek
ValueError.
5. flatten_list(nested_list: list) -> list - przyjmuje listę (mogącą zawierać zagnieżdżone
listy) i zwraca ją „spłaszczoną”.
Przykład: [1, [2, 3], [4, [5]]] → [1, 2, 3, 4, 5]
6. word_frequencies(text: str) -> dict - zwraca słownik z częstością występowania słów w
tekście (ignorując wielkość liter i interpunkcję).

Testy jednostkowe 1

7. is_prime(n: int) -> bool - sprawdza, czy liczba jest pierwsza.
Jeśli n < 2, zwraca False.
"""


def is_palindrome(text: str) -> bool:
    normalized = ''.join(c.lower() for c in text if c.isalnum())
    return normalized == normalized[::-1]


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def count_vowels(text: str) -> int:
    vowels = "aeiouyąęóAEIOUYĄĘÓ"
    return sum(c in vowels for c in text)


def calculate_discount(price: float, discount: float) -> float:
    if not (0 <= discount <= 1):
        raise ValueError("discount must be between 0 and 1")
    return price * (1 - discount)


def flatten_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def word_frequencies(text: str):
    translator = str.maketrans('', '', string.punctuation)
    normalized = text.lower().translate(translator)
    words = normalized.split()
    return dict(Counter(words))


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
