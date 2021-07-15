def compute_max_lenght_ascending_subset(sequence: list) -> (list, int):
    """
    Given a sequence of integers, this function finds the maximum-length strictly ascending ordered sub-sequence  
    :param sequence: list of integers
    :return: the sub-sequence and its length
    """
    from itertools import combinations
    for n0 in range(len(sequence)):
        n = len(sequence) - n0
        subsequences = list(combinations(sequence, n))
        for subset in subsequences:
            candidate = True
            for x in range(1, len(subset)):
                if subset[x] <= subset[x - 1]:
                    candidate = False
                    break
            if candidate:
                return list(subset), n
    return [], 0


test_list = [1, 22, 9, 33, 21, 50, 41, 60, 80, 90, 90, 100, 103, 108, 105]
extracted_sequence, es_length = compute_max_lenght_ascending_subset(test_list)
print("the max sub-sequence is:", extracted_sequence)
print("and it's composed of %d elements." % es_length)
