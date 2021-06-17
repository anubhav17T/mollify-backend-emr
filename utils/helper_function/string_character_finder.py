import random
import string


def get_part_of_string(input_string: str, character):
    if character == "space":
        partitioned_string = input_string.partition(" ")
        return partitioned_string[0]
    else:
        partitioned_string = input_string.partition("{}".format(character))
        return partitioned_string[0]


def specific_string(length: int):
    sample_string = 'mentalhealth'  # define the specific string
    result = ''.join((random.choice(sample_string)) for x in range(length))
    return result
