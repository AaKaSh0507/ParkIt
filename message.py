import numpy as np
one_a = [1,0,0,0,1,0,0,0]
right_one_a = []
left_one_a = []

for i in range(int(len(one_a)/2)):
            left_one_a.append(int(one_a[i]))

        # print(left_one_a)
first_empty_slot_left = left_one_a.index(0)
        # print(first_empty_slot_left)

for i in range(int(len(one_a)/2), len(one_a)):
            right_one_a.append(int(one_a[i]))

first_empty_slot_right = right_one_a.index(0)
print(right_one_a)
print(first_empty_slot_right)

if(first_empty_slot_left > first_empty_slot_right):
            right_one_a[first_empty_slot_right] = 1
            slot = first_empty_slot_right+len(left_one_a)-1

if(first_empty_slot_left <= first_empty_slot_right):
            left_one_a[first_empty_slot_left] = 1
            slot = first_empty_slot_left

one_a = np.concatenate([left_one_a, right_one_a])
print(f"one a :{one_a}")
