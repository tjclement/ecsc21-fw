import binascii, random, os
from pkcs1 import keys, rsaes_pkcs1_v15


def _miller_rabin_is_prime(n, k):
    # Source: https://gist.github.com/Ayrx/5884790
    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = int(random.random() * (n - 1))
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _egcd(a, b):
    """
    From https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
    return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = (b // a, b % a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def _modinv(a, m):
    g, x, y = _egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


# Generated on PC (79284753922901710415148579064982737711, 326684018224851925040338467521754423887)
def gen_p_q(bitsize=128):
    p = 0
    while p == 0 or not _miller_rabin_is_prime(p, 40):
        p = int(binascii.hexlify(os.urandom(bitsize // 8)), 16)
    q = 0
    while q == 0 or not _miller_rabin_is_prime(q, 40):
        q = int(binascii.hexlify(os.urandom(bitsize // 8)), 16)

    return p, q


def _gen_keys_from_p_q(bitsize=128, p=None, q=None):
    if p is None or q is None:
        p, q = gen_p_q(bitsize)
    n = p * q
    phin = (p - 1) * (q - 1)
    e = 0
    # If e is prime, we're sure that gcd(e, phin) == 1
    while e == 0 or e >= phin or not _miller_rabin_is_prime(e, 40):
        e = int(binascii.hexlify(os.urandom(bitsize // 8)), 16)
    d = _modinv(e, n)

    return (n, e), (n, d)


def gen_keys(bitsize=128):
    public, private = keys.generate_key_pair(bitsize)
    n, e, d = public.n, public.e, private.d
    return (n, e), (n, d)


def encrypt(n, e, byte_string):
    public_key = keys.RsaPublicKey(n, e)
    return rsaes_pkcs1_v15.encrypt(public_key, byte_string)


def decrypt(n, d, bin_data):
    private_key = keys.RsaPrivateKey(n, d)
    return rsaes_pkcs1_v15.decrypt(private_key, bin_data)
