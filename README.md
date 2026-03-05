# Programming Assignment 2 - Greedy Algorithms (Cache Eviction)

## Student
Name: Alexis Morales  
UFID: 20325573

## Files
- src/cache_sim.py : program that simulates FIFO, LRU, and OPTFF
- data/example.in : small example input
- data/example.out : output for example.in
- data/file1.in, data/file2.in, data/file3.in : input files used for Question 1
- data/q2_lru.in, data/q2_lru.out : input and output for Question 2 sequence

## How to run
From the repository root:

python3 src/cache_sim.py data/example.in

To recreate the example output:

python3 src/cache_sim.py data/example.in > data/example.out
python3 src/cache_sim.py data/q2_lru.in > data/q2_lru.out

You can also run:

python3 src/cache_sim.py data/file1.in  
python3 src/cache_sim.py data/file2.in  
python3 src/cache_sim.py data/file3.in  
python3 src/cache_sim.py data/q2_lru.in

## Input format
k m  
r1 r2 r3 ... rm  

k is cache capacity  
m is number of requests  
requests are integer IDs

## Output format
FIFO  : <number_of_misses>  
LRU   : <number_of_misses>  
OPTFF : <number_of_misses>  

## Assumptions
- Input file is formatted as described above.
- Requests are integers separated by spaces or newlines.


# Written Component

## Question 1: Empirical Comparison

    Input File   k   m   FIFO  LRU  OPTFF
    file1.in     3   60  3     3    3
    file2.in     3   60  60    60   22
    file3.in     4   60  51    48   31

Does OPTFF have the fewest misses?
Yes. It was the smallest in file2 and file3, and it tied in file1.

How does FIFO compare to LRU?
They can be the same or different depending on the sequence. In file2 they matched, but in file3 LRU did better than FIFO.

## Question 2: Bad Sequence for LRU (k = 3)

Question:
For k = 3, is there a request sequence for which OPTFF incurs strictly fewer misses than LRU? If so, construct one and report the miss counts. Briefly explain your reasoning.

Answer:
Yes, such a sequence exists.

Sequence (k = 3, m = 12):

    1 2 3 4 1 2 5 1 2 3 4 5

Miss counts on this sequence:

    LRU   : 10
    OPTFF : 7

Brief explanation:

OPTFF knows the full request sequence, so when the cache is full it evicts the item whose next use is farthest in the future or never happens again. LRU only uses past information, so it can evict an item that will be needed soon. On this sequence, that causes LRU to have more misses than OPTFF.

## Question 3: Prove OPTFF is Optimal

Question:
Let OPTFF be Belady’s farthest in future algorithm. Let A be any offline algorithm that knows the full request sequence. Prove that the number of misses of OPTFF is no larger than that of A on any fixed sequence.

Proof:
Fix a cache size k and a request sequence. Consider any offline algorithm A.

Look at any time t when the cache is full and there is a miss. OPTFF evicts the item in the cache whose next request is farthest in the future, or is never requested again.

Suppose A evicts a different item than OPTFF at time t. Let x be the item OPTFF evicts, and let y be the item A evicts. Build a new algorithm A' that is the same as A, except at time t it evicts x instead of y.

Right after time t, A' keeps y while A keeps x. By OPTFF’s choice, x is not needed before y is needed, because x is used no sooner than y in the future. So until the next time y is requested, keeping y cannot make A' get more misses than A. When y is requested, A' will have y and A might not, so A' can only be better.

From that point on, A' can just act like A. This swap never increases the number of misses.

So whenever A disagrees with OPTFF on an eviction, we can swap A’s choice to match OPTFF without increasing misses. Repeating this for every disagreement turns A into OPTFF and never increases misses.

Therefore, OPTFF has no more misses than any offline algorithm A, so OPTFF is optimal.