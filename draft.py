from collections import defaultdict

nums = [1,2,2,2,3,3,3]
k = 2


bucket = [[] for i in range(len(nums) + 1)]
counter = defaultdict(int)

for n in nums:
    counter[n] += 1

for k, v in counter.items():
    bucket[v].append(k)
print(bucket)

res = []

for i in range(len(bucket)-1, 0, -1):
    for n in bucket[i]:
        res.append(n)
        print(res, len(res))
        if len(res) == k:
            print(f"THIS IS IT! : {res}\n\n")