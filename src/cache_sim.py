import sys
from collections import deque


def read_input(path):
    # Read file
    with open(path, "r") as f:
        nums = [int(x) for x in f.read().split()]

    # Get header
    k = nums[0]
    m = nums[1]
    reqs = nums[2:2 + m]
    return k, reqs


def fifo_misses(k, reqs):
    # FIFO cache
    cache = set()
    q = deque()
    misses = 0

    for x in reqs:
        # Check hit
        if x in cache:
            continue

        # Count miss
        misses += 1

        # Evict oldest
        if len(cache) == k:
            old = q.popleft()
            cache.remove(old)

        # Insert item
        cache.add(x)
        q.append(x)

    return misses


def lru_misses(k, reqs):
    # LRU cache
    cache = []
    misses = 0

    for x in reqs:
        # Hit case
        if x in cache:
            cache.remove(x)
            cache.append(x)
            continue

        # Count miss
        misses += 1

        # Evict oldest
        if len(cache) == k:
            cache.pop(0)

        # Insert item
        cache.append(x)

    return misses


def optff_misses(k, reqs):
    # Build positions
    positions = {}
    for i, x in enumerate(reqs):
        if x not in positions:
            positions[x] = []
        positions[x].append(i)

    # Next pointers
    idx_ptr = {}
    for x in positions:
        idx_ptr[x] = 0

    # OPT cache
    cache = []
    misses = 0
    INF = 10**18

    for i, x in enumerate(reqs):
        # Move pointer
        idx_ptr[x] += 1

        # Check hit
        if x in cache:
            continue

        # Count miss
        misses += 1

        # Insert if room
        if len(cache) < k:
            cache.append(x)
            continue

        # Pick victim
        victim = cache[0]
        farthest = -1

        for y in cache:
            # Next use
            p = idx_ptr[y]
            if p >= len(positions[y]):
                nxt = INF
            else:
                nxt = positions[y][p]

            # Choose farthest
            if nxt > farthest:
                farthest = nxt
                victim = y

        # Evict victim
        cache.remove(victim)

        # Insert item
        cache.append(x)

    return misses


def main():
    # Basic args
    if len(sys.argv) != 2:
        print("Usage: python3 src/cache_sim.py <input_file>")
        return

    # Read input
    k, reqs = read_input(sys.argv[1])

    # Run policies
    fifo = fifo_misses(k, reqs)
    lru = lru_misses(k, reqs)
    opt = optff_misses(k, reqs)

    # Print output
    print(f"FIFO  : {fifo}")
    print(f"LRU   : {lru}")
    print(f"OPTFF : {opt}")


if __name__ == "__main__":
    main()