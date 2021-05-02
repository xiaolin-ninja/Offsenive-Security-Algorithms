import gmpy2
import argparse
from math import gcd

parser = argparse.ArgumentParser(description='RSA Common modulus attack')
required_named = parser.add_argument_group('required named arguments')
required_named.add_argument('-n', '--modulus', help='Common modulus', type=int, required=True)
required_named.add_argument('-e1', '--key1', help='First public key', type=int, required=True)
required_named.add_argument('-e2', '--key2', help='Second public key', type=int, required=True)
required_named.add_argument('-c1', '--ciphertext1', help='First ciphertext', type=int, required=True)
required_named.add_argument('-c2', '--ciphertext2', help='Second ciphertext', type=int, required=True)


def common_modulus_attack(c1, c2, e1, e2, n):
    if gcd(e1, e2) != 1:
        raise ValueError("Common modulus attack requires gcd(e1,e2) = 1.")
        
    a = gmpy2.invert(e1, e2)
    b = float(1 - (a * e1)) / e2

    i = gmpy2.invert(c2, n)
    m1 = pow(c1, a, n)
    m2 = pow(i, int(-b), n)
    return ( m1 * m2 ) % n

def main():
    args = parser.parse_args()
    print('Starting attack...')

    try:
        result = hex(common_modulus_attack(args.ciphertext1, args.ciphertext2, args.key1, args.key2, args.modulus))[2:]
        print('Success!')
        print(bytes.fromhex(result).decode("ASCII"))
    except Exception as e:
        print('Attack failed!')
        print(e)


if __name__ == '__main__':
    main()
