allowed=[]
with open("allowed.txt") as f:
    allowed = [w.strip() for w in f]
print(allowed)
