import math

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
    return text == text[::-1]


def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def count_vowels(text: str) -> int:
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']

    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

