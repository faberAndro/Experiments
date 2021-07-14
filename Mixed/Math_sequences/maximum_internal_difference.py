import numpy as np
import random as ra
import time
import matplotlib.pyplot as plt 


def tdiff():
    global t
    diff = time.time() - t
    t = time.time()
    print(diff)
    

def goodSegment(lower, badNumbers, upper):
    bad_list = sorted(badNumbers)
    for i, n in enumerate(bad_list):
        # if i % 5000:
        #     print(i, '/', len(bad_list), end='  ')
        if n<lower or n>upper:
            badNumbers.remove(n)
    badNumbers.sort()
    diff_lower = badNumbers[0] - lower
    diff_n = []
    for n in range(1, len(badNumbers)):
        diff_n.append(badNumbers[n] - badNumbers[n-1] - 1)
    diff_upper = upper - badNumbers[-1]
    all_diffs = [diff_lower] + diff_n + [diff_upper]
    return max(all_diffs)


def fab(lower, badNumbers, upper):
    global t
    # print('starting fab ...')
    t = time.time()
    badNumbers.sort()
    # left_trim = set(np.arange(badNumbers[0], lower))
    # tdiff()
    # right_trim = set(np.arange(upper + 1, badNumbers[-1] + 1))
    # tdiff()
    # purgedSet = set(badNumbers) - left_trim - right_trim
    # tdiff()
    purgedSet = np.array(badNumbers)
    badNumbersArray = purgedSet[np.logical_and(purgedSet >= lower, purgedSet <= upper)]
    # badNumbersArray = np.asarray(sorted(purgedSet))
    if badNumbersArray.size > 0:
        diffs = (badNumbersArray - np.roll(badNumbersArray, 1) - 1)[1:]
        left = badNumbersArray[0] - lower
        right = upper - badNumbersArray[-1]
        all_diffs = np.concatenate(([left], diffs, [right]))
        return max(all_diffs)
    else:
        return upper - lower + 1


if __name__ == '__main__':
    """
    goodSegement e fab fanno la stessa cosa, ma fab dovrebbe farla in modo più efficiente.
    entrambe estraggono il segmento interno di numeri a distanza maggiore, considerati e inclusi gli estremi upper e lower.
    praticamente è come se avessimo una lista di numeri consecutivi da min a max, estremi inclusi. Poi eliminiamo dalla lista i numeri "bad" (in b).
    Ora calcoliamo la lunghezza di tutti i sottoinsiemi di numeri consecutivi, e ne estraiamo la massima.
     
    """
    t = time.time()
    with_numpy = True
    with_standard = True
    massimo = 100000000
    xa, y1, y2 = [], [], []
    passo = 10000
    for x in range(1, 15):
        xa.append(passo + x*passo)
        b = ra.sample(range(1, massimo), passo + x*passo)
        l0 = ra.randint(1, massimo)
        u0 = ra.randint(1, massimo)
        lo = min(l0, u0)
        u = max(l0, u0)
        # lo, b, u = 20, [50], 60
        # print(l0, b, u)

        if with_numpy:
            t1_0 = time.time()
            m1 =fab(lo, b, u)
            t1_1 = time.time()
            y1.append(t1_1 - t1_0)
            print('fab:', m1, 'dt:', t1_1 - t1_0)

        if with_standard:
            t2_0 = time.time()
            m2 =goodSegment(lo, b, u)
            t2_1 = time.time()
            y2.append(t2_1 - t2_0)
            print('goodSegment', m2, 'dt:', t2_1 - t2_0)

        print(x)

    plt.figure()
    if with_numpy:
        plt.plot(xa, y1, label='fab')
    if with_standard:
        plt.plot(xa, y2, label='goodSegment')
    plt.legend(loc="upper left")
    plt.show()
