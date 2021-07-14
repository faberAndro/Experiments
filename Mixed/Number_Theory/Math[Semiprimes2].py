import time

def main(n):
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

if __name__ == '__main__':
    start_time = time.time()
    print(main(100000121335352))
    print("--- %s seconds ---" % (time.time() - start_time))
