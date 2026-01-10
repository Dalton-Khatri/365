numbers=[2,2,4,6,3,4,6,1]
uniques = []
for i in numbers:
    if i not in uniques:
        uniques.append(i)
print(uniques)