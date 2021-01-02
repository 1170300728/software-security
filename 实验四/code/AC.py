def get_input_list():
    input_list = []
    while True:
        input_string = input("输入模式字符串（输入空串将结束输入）：")
        if input_string == "":
            break
        else:
            input_list.append(input_string)
    return input_list

def pretreat(input_list):
    length = max(map(len, input_list))
    next_list = [[0] + [-1 for i in range(255)], ["" for j in range(256)]]
    base_list = [-1 for i in range(256)]
    check_list = [-1 for i in range(256)]
    count = 1
    level_list_all = []
    for j in range(length):
        level_list = []
        for i in input_list:
            if len(i) > j:
                if i[j] not in level_list:
                    level_list.append(i[j])
                    if j != 0:
                        check_list[count] = level_list_all[j-1].index(i[j-1]) + sum(map(len, level_list_all[0:j-1])) + 1
                    else:
                        check_list[count] = 0
                    count += 1
        first_ptr = next_list[0].index(-1)
        temp_num = max(next_list[0]) + 1
        temp_base = min(map(ord,level_list))
        flag = True
        while flag:
            for l in level_list:
                if first_ptr + ord(l) - temp_base > len(next_list[0]):
                    next_list[0] += [-1 for i in range(256)]
                    next_list[1] += ["" for i in range(256)]
                if next_list[0][first_ptr + ord(l) - temp_base] != -1:
                    first_ptr += 1
                    flag = True
                    break
                else:
                    flag = False
        for l in level_list:
            next_list[0][first_ptr + ord(l) - temp_base] = temp_num
            next_list[1][first_ptr + ord(l) - temp_base] = l
            temp_num += 1
        # print(level_list)
        level_list_all.append(level_list)
    ind1 = next_list[0].index(1)
    ind2 = next_list[0].index(0)
    base_list[0] = ind1 -ord(next_list[1][ind1]) - ind2
    # print(next_list)
    # print(check_list)
    for i in range(len(check_list)):
        if check_list[i] != -1 and base_list[check_list[i]] == -1:
            ind1 = next_list[0].index(i)
            ind2 = next_list[0].index(check_list[i])
            base_list[check_list[i]] = ind1 -ord(next_list[1][ind1]) - ind2
    failure_list = [0] + [-1 for i in range(255)]
    # print(base_list)
    for i in range(max(next_list[0])):
        if check_list[i+1] == 0:
            failure_list[i+1] = 0
        elif check_list[i+1] != -1:
            temp_state = failure_list[check_list[i+1]]
            failure_list[i+1] = get_next_state(temp_state, next_list[1][next_list[0].index(i+1)], next_list, base_list, check_list)
    # print(failure_list)
    output_list = ["" for i in range(256)]
    for i in input_list:
        state = 0
        for j in i:
            state = get_next_state(state, j, next_list, base_list, check_list)
        output_list[state] = i
    # print(output_list)
    return next_list, base_list, check_list, failure_list, output_list

def get_next_state(state_now, input_chr, next_list, base_list, check_list):
    next_state = next_list[0][next_list[0].index(state_now) + base_list[state_now] + ord(input_chr)]
    if check_list[next_state] == state_now:
        return next_state
    else:
        return 0

def parse_input(input_string, next_list, base_list, check_list, failure_list, output_list):
    state = 0
    output = [[],[]]
    length = len(input_string)
    count = 0
    while True:
        if count >= length:
            while True:
                state = failure_list[state]
                if state == 0:
                    break
                elif output_list[state] != "":
                    temp_str = output_list[state]
                    if temp_str in output[0]:
                        output[1][output[0].index(temp_str)] += 1
                    else:
                        output[0].append(temp_str)
                        output[1].append(1)
                    print(state)
            break
        c = input_string[count]
        next_state = get_next_state(state, c, next_list, base_list, check_list)
        if state == 0:
            count += 1
        elif next_state == 0:
            next_state = failure_list[state]
        else:
            count += 1
        if output_list[next_state] != "":
            temp_str = output_list[next_state]
            if temp_str in output[0]:
                output[1][output[0].index(temp_str)] += 1
            else:
                output[0].append(temp_str)
                output[1].append(1)
        state = next_state
        print(state)
    return output

if __name__ == "__main__":
    while True:
        input_list = get_input_list()
        if input_list == []:
            print("\n请至少输入一个字符串！")
        else:
            break
    next_list, base_list, check_list, failure_list, output_list = pretreat(input_list)
    print(next_list)
    print(base_list)
    print(check_list)
    print(failure_list)
    print(output_list)
    count_next = next_list[0].count(-1)
    print(1 - count_next / len(next_list[0]))
    while True:
        input_string = input("输入目标字符串（输入空串将结束程序）：")
        if input_string == "":
            break
        else:
            output = parse_input(input_string, next_list, base_list, check_list, failure_list, output_list)
            print(output)
            for i in range(len(output[0])):
                print(output[0][i] + "出现了" + str(output[1][i]) + "次")

    