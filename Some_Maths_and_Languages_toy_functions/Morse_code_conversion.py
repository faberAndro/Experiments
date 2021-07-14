morseDic = {
  " ": " ",
  "'": ".----.",
  "(": "-.--.-",
  ")": "-.--.-",
  ",": "--..--",
  "-": "-....-",
  ".": ".-.-.-",
  "/": "-..-.",
  "0": "-----",
  "1": ".----",
  "2": "..---",
  "3": "...--",
  "4": "....-",
  "5": ".....",
  "6": "-....",
  "7": "--...",
  "8": "---..",
  "9": "----.",
  ":": "---...",
  ";": "-.-.-.",
  "?": "..--..",
  "!": "-.-.--",
  "A": ".-",
  "B": "-...",
  "C": "-.-.",
  "D": "-..",
  "E": ".",
  "F": "..-.",
  "G": "--.",
  "H": "....",
  "I": "..",
  "J": ".---",
  "K": "-.-",
  "L": ".-..",
  "M": "--",
  "N": "-.",
  "O": "---",
  "P": ".--.",
  "Q": "--.-",
  "R": ".-.",
  "S": "...",
  "T": "-",
  "U": "..-",
  "V": "...-",
  "W": ".--",
  "X": "-..-",
  "Y": "-.--",
  "Z": "--..",
  "_": "..--.-"
}   # define an English to Morse dict
englishDic = {}     # revert the dictionary
for d1 in morseDic:
    d2 = morseDic.get(d1)
    englishDic.update({d2: d1})


def translate_from_English_to_Morse(text_to_be_translated: str) -> str:
    # translate from English to Morse
    word_0 = text_to_be_translated    # input an english word
    word = word_0.upper()
    output = ""
    for x in word:
        if x not in morseDic:
            return "Invalid Input"
        else:
            y = morseDic.get(x)
            output += y + " "
    return output


def translate_from_Morse_to_English(text_to_be_translated: str) -> str:
    # translate from Morse to English
    word_M = text_to_be_translated   # input a Morse sequence
    output = ""
    words = word_M.split("   ")
    for word in words:
        letters = word.split()
        for y in letters:
            if y not in englishDic:
                return "Invalid Input"
            else:
                z = englishDic.get(y)
                output += z.lower()
        output += " "
    translated_text = output.rstrip()
    return translated_text


def main():
    do_again = 'Y'
    while do_again == 'Y':
        answer = ''
        while answer not in ['M', 'E']:
            answer = input("Choose type of input word: Morse (M) or English (E)?  ").upper()
        if answer == "M":
            print("NOTE: to start a new word, please input N.3 spaces")
            question = input("Please input the text to translate: ")
            translation = translate_from_Morse_to_English(question)
        else:
            question = input("Please input the text to translate: ")
            translation = translate_from_English_to_Morse(question)
        print(translation)
        do_again = input("Would you like to translate something else [y/n]? ").upper()
    print('Program terminated. Good Bye')


if __name__ == '__main__':
    main()
