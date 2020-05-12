def divide(arr, depth, m):
    if len(complements) <= depth:
        complements.append(2 ** (depth + 2) + 1)
    complement = complements[depth]
    for i in range(2):
        if complement - arr[i] <= m:
            arr[i] = [arr[i], complement - arr[i]]
            divide(arr[i], depth + 1, m)

m = int(raw_input())

arr = [1, 2]
complements = []

divide(arr, 0, m)
print(arr)