import random
import string
from pyscript import document, window
from pyodide.ffi import create_proxy

mode_select = document.getElementById("mode-select")
encrypt_section = document.getElementById("encrypt")
decrypt_section = document.getElementById("decrypt")
e_label = document.getElementById("value-e")
n_label = document.getElementById("value-n")
e_input = document.getElementById("input-e")
n_input = document.getElementById("input-n")
msg_input = document.getElementById("input-msg")
ciphertext_label = document.getElementById("value-ciphertext")
ciphertext_input = document.getElementById("input-ciphertext")
msg_label = document.getElementById("value-msg")


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def prime_nums_generator():
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


def gcd(a, b, w):  # euclidean algorithm
    while a != w:
        b, a = a, b % a
    return b


letters = list(string.ascii_uppercase) + list(string.ascii_lowercase) + [" "]
primenum = prime_nums_generator()
primes = []
for _ in range(100):
    primes.append(next(primenum))


def gen_credentials(_=None):
    global e, n, a, d
    p = primes[random.randint(0, len(primes) - 1)]
    q = primes[random.randint(0, len(primes) - 1)]
    n = p * q

    r = (p - 1) * (q - 1)
    for i in range(r - 1):  # because 1 < e < r-1
        if gcd(i, r, 0) == 1:
            if gcd(i, n, 0) == 1:
                e = i  # e is coprime with r and n

    # decryption
    a, d = 0, 0
    while a != 1:  # generates decryption key
        a += e
        a = a % r
        d += 1

    e_label.innerText = e
    n_label.innerText = n
    window.localStorage.setItem("e", e)
    window.localStorage.setItem("n", n)
    window.localStorage.setItem("a", a)
    window.localStorage.setItem("d", d)


def change_mode(e):
    mode = e.target.value
    if mode == "decrypt":
        decrypt_section.style.display = "flex"
        encrypt_section.style.display = "none"
    else:
        decrypt_section.style.display = "none"
        encrypt_section.style.display = "flex"


def encrypt(_):
    try:
        e = int(e_input.value)
        n = int(n_input.value)
    except ValueError:
        ciphertext_label.innerText = "Please enter E and N values."
        return
    msg = msg_input.value

    number_message = []
    for k in range(len(msg)):
        for l in range(len(letters)):
            if msg[k] == letters[l]:
                break
        number_message.append(l)

    ciphertext = []
    for c in range(len(number_message)):
        ciphertext.append((number_message[c] ** e) % n)
    ciphertext_label.innerText = ",".join([str(n) for n in ciphertext])


def decrypt(_):
    try:
        ciphertext = [int(n) for n in ciphertext_input.value.strip().split(",")]
    except ValueError:
        msg_label.innerText = "Invalid ciphertext."
        return

    decoded_message = []
    for h in range(len(ciphertext)):
        decoded_message.append((ciphertext[h] ** d) % n)

    final_message = ""
    for g in range(len(decoded_message)):
        for l in range(len(letters)):
            if decoded_message[g] == l:
                final_message += letters[l]
    msg_label.innerText = final_message
    if len(ciphertext) > 0 and len(final_message) == 0:
        msg_label.innerText = "Ciphertext not encrypted with correct E and N values."


mode_select.addEventListener("change", create_proxy(change_mode))


try:
    e = int(window.localStorage.getItem("e"))
    n = int(window.localStorage.getItem("n"))
    a = int(window.localStorage.getItem("a"))
    d = int(window.localStorage.getItem("d"))
except (ValueError, TypeError):
    gen_credentials()

e_label.innerText = e
n_label.innerText = n
