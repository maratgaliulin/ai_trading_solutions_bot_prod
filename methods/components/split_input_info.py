def split_input_info(input_str:str) -> list|None:
    list1 = input_str.split(' ')
    list2 = input_str.split(',')
    list3 = input_str.split(", ")

    if(len(list1) == 3):
        return list1
    elif(len(list2) == 3):
        return list2
    elif(len(list3) == 3):
        return list3
    else:
        return None