from typing import Generator, Literal

from helper import write_to_file, tokens_to_str, to_tokens, overline

One = Literal["1"]
Zero = Literal["0"]


# -------------------------------------------------------
def find_next_bitstring(s: str) -> str | None:
    """
    :param s: the current bitstring
    :return: the next bitstring contain exactly m ones

    For example,
    ----------------------
    Input:
    n = 8, m = 3
    s = 0 0 1 0 1 1 0 0
    ----------------------
    Output: 0 0 1 1 0 0 0 1
    ----------------------

    => Algorithm:
    |---------------------
    s = 0 0 1 0 1 1 0 0
    i = 0 1 2 3 4 5 6 7 (index of each character in s)
    ---
    -> step 1: find rightmost '01' index in s
       + i = 3
    -> step 2: swap '01' into '10'
       + swap '01' into '10', s[i] <- -> s[i+1]
       + prefix: s[:i] = '001'
       + mid: s[i:i+2] = '10'
       + suffix: s[i+2:] = '100'
    -> step 3: find min of suffix (100) to make the next string
       + count the number of 1 in the suffix
       + shift these 1s into the right of suffix
       + push the rest of 0s in front of the these 1s to achieve the smallest next substring
    """
    i = s.rfind("01")
    if i == -1:
        return None
    prefix = s[:i]
    suffix = s[i + 2 :]
    ones_in_suffix = suffix.count("1")
    zeros_in_suffix = len(suffix) - ones_in_suffix
    return prefix + "10" + "0" * zeros_in_suffix + "1" * ones_in_suffix


def generate_all_bitstring(length: int, num_of_ones: int) -> Generator[str, None, None]:
    if not (0 <= num_of_ones <= length):
        return
    current_bitstring = "0" * (length - num_of_ones) + "1" * num_of_ones
    while current_bitstring is not None:
        yield current_bitstring
        current_bitstring = find_next_bitstring(current_bitstring)


def generate_complements(s: str, char: One | Zero) -> Generator[str, None, None]:
    current_bitstring = to_tokens(s)
    one_positions = [
        index for index, character in enumerate(current_bitstring) if character == char
    ]
    num_of_ones = len(one_positions)
    if num_of_ones == 0:
        yield s
        return

    def gen_possible_config(index):
        if index >= num_of_ones:
            yield tokens_to_str(current_bitstring)
            return

        current_position = one_positions[index]

        # choose 1
        current_bitstring[current_position] = char
        yield from gen_possible_config(index + 1)

        # choose ̅1
        current_bitstring[current_position] = overline(char)
        yield from gen_possible_config(index + 1)

        current_bitstring[current_position] = char

    yield from gen_possible_config(0)


def generate_all_variants(n: int, m: int) -> Generator[str, None, None]:
    for bitstring in generate_all_bitstring(n, m):
        for one_variant in generate_complements(bitstring, "1"):
            for zero_variant in generate_complements(one_variant, "0"):
                yield zero_variant


if __name__ == "__main__":
    write_to_file(data=generate_all_variants(n=5, m=3), filename="smn_5_3")
