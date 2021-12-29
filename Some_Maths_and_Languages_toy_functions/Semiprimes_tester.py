"""
This script factors a number in its primes divisors.
Then, it tests if it's a semi-prime number.
The factoring is performed using N.2 different algorithms: a fast one, and a recursive one.
The number to factor and test can be set at the beginning of the script.
After a certain number of digits, the recursive algorithm becomes unapplicable.
"""
import time
import math

number = 10011123157
# number = 1517


def fast_computing(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def recursive_function(n, x, factor_list=[]):
    if n == x:
        f = float(x)
        f2 = math.sqrt(f)
        f3 = math.floor(f2)
    else:
        f = f3 = int(x)
    for i in range(2, f3 + 1):
        if (f % i) == 0:
            n2 = f / i
            factor_list.append(int(i))
            p = 1
            for j in factor_list:
                p *= j
            if p == n:
                return factor_list
            else:
                p2 = recursive_function(n, n2, factor_list)
                p = 1
                for j in p2:
                    p *= j
                    if p == n:
                        return factor_list
    return factor_list


def main():
    start_time = time.time()
    print("USING FAST COMPUTING ...:", end=' ')
    fc = fast_computing(number)
    print(fc, "elapsed time: --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    print("USING RECURSIVE COMPUTING ...:", end=' ')
    rc = recursive_function(n=number, x=number)
    print(rc, "elapsed time: --- %s seconds ---" % (time.time() - start_time))
    isSemiprime = True if len(rc) == 2 else False        
    print('The number is a semi-prime:', isSemiprime)


if __name__ == '__main__':
    main()