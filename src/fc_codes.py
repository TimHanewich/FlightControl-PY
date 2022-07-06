import math
import json

def input_to_code(seed:int, mean_power:int, backward_forward:int, left_right: int) -> int:

    #convert values
    c_mp = mean_power
    c_bf = backward_forward + 100
    c_lr = left_right + 100

    permutations_mean_power = 101
    permutations_backward_forward = 201
    permutations_left_right = 201

    part1 = c_mp * permutations_backward_forward * permutations_left_right
    part2 = c_bf * permutations_left_right
    part3 = c_lr

    CODE = seed + part1 + part2 + part3
    return CODE

def code_to_input(seed:int, code:int):

    permutations_mean_power = 101
    permutations_backward_forward = 201
    permutations_left_right = 201

    #take out the seed
    base = code - seed

    #find val 3 (left_right)
    rev3 = float(base) / float(permutations_left_right)
    rem3 = rev3 - math.floor(rev3)
    val3_raw = round(rem3 * permutations_left_right)
    val3_adj = val3_raw - 100

    #find val 2 (backward_forward)
    rev2 = float(base) / float(permutations_backward_forward * permutations_left_right)
    rem2 = rev2 - math.floor(rev2)
    val2_raw = math.floor(rem2 * permutations_backward_forward)
    val2_adj = val2_raw - 100

    #find val 1 (mean_power)
    rev1 = float(base) / float(permutations_mean_power * permutations_backward_forward * permutations_left_right)
    rem1 = rev1 - math.floor(rev1)
    val1_raw = math.floor(rem1 * permutations_mean_power)

    return val1_raw, val2_adj, val3_adj