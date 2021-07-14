class Solution:

    def run(self, n, m, a, b):
        #
        # Some work here; return type and arguments should be according to the problem's requirements
        #
        from itertools import combinations
        lista = ''
        result = None
        mn = min(n,m)
        for i in range(mn):
            j = mn-i
            c_a = list(combinations(a,j))
            c_b = list(combinations(b,j))
            for x in c_b:
                if (x in c_a):
                    result = x
                    # lista =  ' '.join(result)
                    risultato = [str(y) for y in result]
                    lista = ','.join(risultato)
                    return lista
        
        longest_common_subseq = None
        return lista