def traduzione(textToTranslate):
    global morseToEnglish
    # traduce da English a Morse
    if morseToEnglish is False:
        parola_0 = textToTranslate # immette una parola in inglese
        parola = parola_0.upper()
        output = ""
        for x in parola:
            if x not in morseDic:
                return "Invalid Input"
            else:
                y = morseDic.get(x)    
                output += y+" "
        testoTradotto = output

    # traduce da Morse a English
    if morseToEnglish is True:
        parola_M = textToTranslate # immette una parola in codice morse
        output = ""
        parole = parola_M.split("   ")
        for parola in parole:
            lettere = parola.split()
            for y in lettere:
                if y not in englishDic:
                    return "Invalid Input"
                else:
                    z = englishDic.get(y)    
                    output += z.lower()
            output += " "
        testoTradotto = output.rstrip()
        
    return testoTradotto


morseDic = {
  " ":" ",
  "'":".----.",
  "(":"-.--.-",
  ")":"-.--.-",
  ",":"--..--",
  "-":"-....-",
  ".":".-.-.-",
  "/":"-..-.",
  "0":"-----",
  "1":".----",
  "2":"..---",
  "3":"...--",
  "4":"....-",
  "5":".....",
  "6":"-....",
  "7":"--...",
  "8":"---..",
  "9":"----.",
  ":":"---...",
  ";":"-.-.-.",
  "?":"..--..",
  "!":"-.-.--",
  "A":".-",
  "B":"-...",
  "C":"-.-.",
  "D":"-..",
  "E":".",
  "F":"..-.",
  "G":"--.",
  "H":"....",
  "I":"..",
  "J":".---",
  "K":"-.-",
  "L":".-..",
  "M":"--",
  "N":"-.",
  "O":"---",
  "P":".--.",
  "Q":"--.-",
  "R":".-.",
  "S":"...",
  "T":"-",
  "U":"..-",
  "V":"...-",
  "W":".--",
  "X":"-..-",
  "Y":"-.--",
  "Z":"--..",
  "_":"..--.-"
}
englishDic = {}  # reverse the dictionary here
for d1 in morseDic:
    d2 = morseDic.get(d1)
    englishDic.update({d2:d1})
domanda = input("Parola di input in codice Morse (M) o in lingua inglese (E) ?")
risposta = domanda.upper()
if risposta == "M":
    morseToEnglish = True
elif risposta == "E":
    morseToEnglish = False
else:
    print("scelta non corretta")
    exit(1)
domanda = input("Immettere il testo da tradurre: ")


print(traduzione(domanda))
