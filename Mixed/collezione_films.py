'''
Mr. K. I. has a very big movie collection. He has organized his collection in a big stack. Whenever he wants to watch one of the movies, he locates the movie in this stack and removes it carefully, ensuring that the stack doesn't fall over. After he finishes watching the movie, he places it at the top. Since the stack of movies is so big, he needs to keep track of the position of each movie. It is sufficient to know for each movie how many movies are placed above it, since, with this information, its position in the stack can be calculated. Each movie is identified by a number printed on the movie box. Your task is to implement a program which will keep track of the position of each movie. In particular, each time Mr. K. I. removes a movie box from the stack, your program should print the number of movies that were placed above it before it was removed. After the movie is watched it is placed at the top of the stack.

INPUT int n ^^ the number of movies Mr. K. I. has in the stack

int m ^^ the number of movies Mr. K. I. wants to watch

int[] movies ^^ an array with m integers a1 . . . am (1 <= ai <= n) representing the identification numbers of movies that Mr. K. I. wants to watch For simplicity, we assume assume that the initial stack contains the movies with identification numbers 1, 2, . . . , n in increasing order, where the movie box with label 1 is the top-most box.

OUTPUT string movies_array ^^ array with m integers separated by comma, where the i-th integer gives the number of movie boxes above the box with label ai, immediately before this box is removed from the stack.

Note: After each find, the movie box is placed at the top of the stack.

CONSTRAINTS 1 <= n, m <= 100 000

EXAMPLE 1 Input 3 3 [3,1,1]

Output "2,1,0"

EXAMPLE 2 Input 5 3 [4,4,5]

Output "3,0,4"

'''

def run(n, m, movies):
    #
    # Some work here; return type and arguments should be according to the problem's requirements
    #
    movies_track = []
    s = []
    stack = [x for x in range(1,n+1)]
    print(stack)
    for i in movies:
        p = stack.index(i)
        movies_track.append(str(p))
        s = [i] + stack[0:p] + stack[p+1:n]
        stack = s
        print(i,s)
    
    movies_array = ",".join(movies_track);
    return movies_array;

print(run(3,3,[3,1,1]))