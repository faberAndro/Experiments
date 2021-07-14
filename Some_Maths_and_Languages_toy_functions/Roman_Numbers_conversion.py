roman_numbers = [['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
                 ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
                 ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']]
maximum = 10000


def convert_number(n1: int) -> str:
    output = ''
    n2 = str(n1)
    numbers = [int(char) for char in n2]
    m = ''
    if len(n2) == 4:
        for i in range(numbers[0]):
            m += 'M'
        output = m
        l2 = 3
    else:
        l2 = len(n2)
    for i in range(l2):
        if len(n2) == 4:
            roman_digit = roman_numbers[l2 - 1 - i][numbers[i + 1]]
        else:
            roman_digit = roman_numbers[l2 - 1 - i][numbers[i]]
        output += roman_digit
    if n1 == 10000:
        output = "MMMMMMMMMM"
    return output


def main():
    print("THIS PROCEDURE WILL CONVERT A STANDARD ARABIC (DECIMAL) NUMBER TO A ROMAN ONE")
    do_again = 'Y'
    while do_again == 'Y':
        n1 = 0
        int_check = False
        while not int_check:
            n0 = input("Please write a number from 1 to %s: " % str(maximum))
            try:
                n1 = int(n0)
                int_check = False if n1 < 1 or n1 > maximum else True
            except ValueError:
                int_check = False
        print("The correspondent roman number is: %s" % convert_number(n1))
        do_again = input("Would you like to do another conversion? [y/n] ").upper()


if __name__ == '__main__':
    main()
