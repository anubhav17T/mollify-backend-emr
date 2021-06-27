def find_unique_element(specialisation_array: list,languages_array) -> bool:
    """:return Boolean whether the array is unique or not """
    flag = len(set(specialisation_array)) == len(specialisation_array) and len(set(languages_array)) == len(languages_array)
    if flag:
        print("true")
        return True
    else:
        return False


