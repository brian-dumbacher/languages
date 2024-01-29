
import io
import re

def isTableStart(line):
    return re.search(r"<table", line)

def isTableEnd(line):
    return re.search(r"</table>", line)

def getTableId(line):
    m = re.search(r"id=\"([a-zA-Z0-9]+)\"", line)
    return m.group(1)

def isTrTh(line):
    return re.search(r"<tr><th>", line)

def isTrTd(line):
    return re.search(r"<tr><td>", line)

def getPos(tableId):
    if re.search(r"Nouns", tableId):
        return "NOUN"
    elif re.search(r"Pronouns", tableId):
        return "PRON"
    elif re.search(r"Adjectives", tableId):
        return "ADJ"
    elif re.search(r"Verbs", tableId):
        return "VERB"
    elif re.search(r"Adverbs", tableId):
        return "ADV"
    elif re.search(r"Prepositions", tableId):
        return "PREP"
    elif re.search(r"Conjunctions", tableId):
        return "CONJ"
    elif re.search(r"Interjections", tableId):
        return "INTERJ"
    return ""

def getNounDeclension(tableId):
    if re.search(r"First", tableId):
        return "1"
    elif re.search(r"Second", tableId):
        return "2"
    elif re.search(r"Third", tableId):
        return "3"
    elif re.search(r"Fourth", tableId):
        return "4"
    elif re.search(r"Fifth", tableId):
        return "5"
    return ""

def getAdjDeclension(tableId):
    if re.search(r"FirstSecond", tableId):
        return "12"
    elif re.search(r"Third", tableId):
        return "3"
    return ""

def getGender(tableId):
    if re.search(r"Feminine", tableId):
        return "F"
    elif re.search(r"Masculine", tableId):
        return "M"
    elif re.search(r"Neuter", tableId):
        return "N"
    return ""

def getNounBase(noun, declension, gender):
    if declension == "":
        return noun
    elif declension == "1":
        if noun[-1] == "a":
            return noun[:-1]
        elif noun[-2:] == "ae":
            return noun[:-2]
    elif declension == "2":
        if gender == "M":
            if noun[-2:] == "us":
                return noun[:-2]
            elif noun[-1] == "i":
                return noun[:-1]
        elif gender == "N":
            if noun[-2:] == "um":
                return noun[:-2]
            elif noun[-1] == "a":
                return noun[:-1]
    elif declension == "4":
        if gender in ["F", "M"]:
            return noun[:-2]
        elif gender == "N":
            if noun[-1] == "u":
                return noun[:-1]
            elif noun[-2:] == "ua":
                return noun[:-2]
    return noun

def getAdjBase(adj, declension):
    if declension == "":
        return adj
    elif declension == "12":
        if adj[-2:] == "us":
            return adj[:-2]
        elif adj[-1] == "i":
            return adj[:-1]
    return adj

def getAdjFeminine(adj, base):
    if adj[-2:] == "us":
        return base + "a"
    elif adj[-1] == "i":
        return base + "ae"
    return base + "a"

def getAdjNeuter(adj, base):
    if adj[-2:] == "us":
        return base + "um"
    elif adj[-1] == "i":
        return base + "a"
    return base + "um"

def getConjugation(tableId):
    if re.search(r"First", tableId):
        return "1"
    elif re.search(r"Second", tableId):
        return "2"
    elif re.search(r"Third", tableId):
        return "3"
    elif re.search(r"ThirdIO", tableId):
        return "3io"
    elif re.search(r"Fourth", tableId):
        return "4"
    return ""

def removeSpecialChars(text):
    text = re.sub(r"&#x0100;", "A", text)
    text = re.sub(r"&#x0101;", "a", text)
    text = re.sub(r"&#x0112;", "E", text)
    text = re.sub(r"&#x0113;", "e", text)
    text = re.sub(r"&#x012A;", "I", text)
    text = re.sub(r"&#x012B;", "i", text)
    text = re.sub(r"&#x014C;", "O", text)
    text = re.sub(r"&#x014D;", "o", text)
    text = re.sub(r"&#x016A;", "U", text)
    text = re.sub(r"&#x016B;", "u", text)
    text = re.sub(r"&ndash;",  "-", text)
    return text

def cleanTh(text):
    text = removeSpecialChars(text)
    text = re.sub(r"<br>", " ", text)
    return text

def cleanTd(text):
    text = removeSpecialChars(text)
    text = re.sub(r"<br>", "; ", text)
    return text

def main():
    tuples_noun = []
    tuples_adj = []
    tuples_verb = []
    tuples_other = []

    inTable = False
    tableId = ""
    ths = []
    tds = []

    wordIndex = -1
    baseIndex = -1
    stemTypeIndex = -1
    adjFeminineIndex = -1
    adjNeuterIndex = -1
    conjugationIndex = -1
    fpsaPresentIndex = -1
    fpsaPerfectIndex = -1
    pppIndex = -1
    definitionIndex = -1
    noteIndex = -1

    posTemp = ""
    wordTemp = ""
    baseTemp = ""
    stemTypeTemp = ""
    declensionTemp = ""
    genderTemp = ""
    adjFeminineTemp = ""
    adjNeuterTemp = ""
    conjugationTemp = ""
    fpsaPresentTemp = ""
    fpsaPerfectTemp = ""
    pppTemp = ""
    definitionTemp = ""
    noteTemp = ""

    f = io.open("latin.html", "r")
    for line in f:
        if isTableStart(line):
            inTable = True
            tableId = getTableId(line)
            posTemp = getPos(tableId)
            if posTemp == "NOUN":
                declensionTemp = getNounDeclension(tableId)
                genderTemp = getGender(tableId)
            elif posTemp == "VERB":
                conjugationTemp = getConjugation(tableId)
            elif posTemp == "ADJ":
                declensionTemp = getAdjDeclension(tableId)
        elif isTableEnd(line):
            inTable = False
            tableId = ""
            ths = []
            tds = []

            wordIndex = -1
            baseIndex = -1
            stemTypeIndex = -1
            adjFeminineIndex = -1
            adjNeuterIndex = -1
            conjugationIndex = -1
            fpsaPresentIndex = -1
            fpsaPerfectIndex = -1
            pppIndex = -1
            definitionIndex = -1
            noteIndex = -1

            posTemp = ""
            wordTemp = ""
            baseTemp = ""
            stemTypeTemp = ""
            declensionTemp = ""
            genderTemp = ""
            adjFeminineTemp = ""
            adjNeuterTemp = ""
            conjugationTemp = ""
            fpsaPresentTemp = ""
            fpsaPerfectTemp = ""
            pppTemp = ""
            definitionTemp = ""
            noteTemp = ""

        if inTable:
            if posTemp == "NOUN":
                if isTrTh(line):
                    ths = re.findall(r"<th>([a-zA-Z0-9!();,' -]*)</th>", cleanTh(line))
                    for i in range(len(ths)):
                        if ths[i] == "Noun":
                            wordIndex = i
                        elif ths[i] == "Base":
                            baseIndex = i
                        elif ths[i] == "Stem Type":
                            stemTypeIndex = i
                        elif ths[i] == "Definition":
                            definitionIndex = i
                        elif ths[i] == "Note":
                            noteIndex = i
                elif isTrTd(line):
                    tds = re.findall(r"<td>([a-zA-Z0-9!();,' -]*)</td>", cleanTd(line))
                    wordTemp = tds[wordIndex]
                    definitionTemp = tds[definitionIndex]
                    noteTemp = tds[noteIndex]
                    if baseIndex >= 0:
                        baseTemp = tds[baseIndex][:-1]
                    else:
                        baseTemp = getNounBase(wordTemp, declensionTemp, genderTemp)
                    if stemTypeIndex >= 0:
                        stemTypeTemp = tds[stemTypeIndex]
                    tuples_noun.append((posTemp, wordTemp, baseTemp, stemTypeTemp, declensionTemp, genderTemp, definitionTemp))
            elif posTemp == "VERB":
                if isTrTh(line):
                    ths = re.findall(r"<th>([a-zA-Z0-9!();,'? -]*)</th>", cleanTh(line))
                    for i in range(len(ths)):
                        if ths[i] == "Active Present Infinitive":
                            wordIndex = i
                        elif ths[i] == "First Person Singular Active Present":
                            fpsaPresentIndex = i
                        elif ths[i] == "First Person Singular Active Perfect":
                            fpsaPerfectIndex = i
                        elif ths[i] == "Perfect Passive Participle":
                            pppIndex = i
                        elif ths[i] == "Definition":
                            definitionIndex = i
                        elif ths[i] == "Note":
                            noteIndex = i
                elif isTrTd(line):
                    tds = re.findall(r"<td>([a-zA-Z0-9!();,'? -]*)</td>", cleanTd(line))
                    wordTemp = tds[wordIndex]
                    fpsaPresentTemp = tds[fpsaPresentIndex]
                    fpsaPerfectTemp = tds[fpsaPerfectIndex]
                    pppTemp = tds[pppIndex]
                    definitionTemp = tds[definitionIndex]
                    noteTemp = tds[noteIndex]
                    tuples_verb.append((posTemp, wordTemp, fpsaPresentTemp, fpsaPerfectTemp, pppTemp, conjugationTemp, definitionTemp))
            elif posTemp == "ADJ":
                if isTrTh(line):
                    ths = re.findall(r"<th>([a-zA-Z0-9!();,'? -]*)</th>", cleanTh(line))
                    for i in range(len(ths)):
                        if ths[i] in ["Adjective", "Nominative Singular Masculine"]:
                            wordIndex = i
                        elif ths[i] == "Base":
                            baseIndex = i
                        elif ths[i] == "Nominative Singular Feminine":
                            adjFeminineIndex = i
                        elif ths[i] == "Nominative Singular Neuter":
                            adjNeuterIndex = i
                        elif ths[i] == "Definition":
                            definitionIndex = i
                        elif ths[i] == "Note":
                            noteIndex = i
                elif isTrTd(line):
                    tds = re.findall(r"<td>([a-zA-Z0-9!();,'? -]*)</td>", cleanTd(line))
                    wordTemp = tds[wordIndex]
                    definitionTemp = tds[definitionIndex]
                    noteTemp = tds[noteIndex]
                    if baseIndex >= 0:
                        baseTemp = tds[baseIndex][:-1]
                    else:
                        baseTemp = getAdjBase(wordTemp, declensionTemp)
                    if adjFeminineIndex >= 0:
                        adjFeminineTemp = tds[adjFeminineIndex]
                    else:
                        adjFeminineTemp = getAdjFeminine(wordTemp, baseTemp)
                    if adjNeuterIndex >= 0:
                        adjNeuterTemp = tds[adjNeuterIndex]
                    else:
                        adjNeuterTemp = getAdjNeuter(wordTemp, baseTemp)
                    tuples_adj.append((posTemp, wordTemp, adjFeminineTemp, adjNeuterTemp, declensionTemp, definitionTemp))
            elif posTemp in ["PRON", "ADV", "PREP", "CONJ", "INTERJ"]:
                if isTrTh(line):
                    ths = re.findall(r"<th>([a-zA-Z0-9!();,'? -]*)</th>", cleanTh(line))
                    for i in range(len(ths)):
                        if ths[i] in ["Pronoun", "Adverb", "Preposition", "Conjunction", "Interjection"]:
                            wordIndex = i
                        elif ths[i] == "Definition":
                            definitionIndex = i
                        elif ths[i] == "Note":
                            noteIndex = i
                elif isTrTd(line):
                    tds = re.findall(r"<td>([a-zA-Z0-9!();,'? -]*)</td>", cleanTd(line))
                    wordTemp = tds[wordIndex]
                    definitionTemp = tds[definitionIndex]
                    noteTemp = tds[noteIndex]
                    tuples_other.append((posTemp, wordTemp, definitionTemp))

    f.close()

    tuples_noun.sort(key = lambda x: x[1].lower())
    tuples_verb.sort(key = lambda x: x[1].lower())
    tuples_adj.sort(key = lambda x: x[1].lower())
    tuples_other.sort(key = lambda x: x[1].lower())

    f = io.open("latin_dict_nouns.txt", "w")
    f.write("|".join(["pos", "word", "base", "stemType", "declension", "gender", "definition"]) + "\n")
    for i in range(len(tuples_noun)):
        f.write("|".join([tuples_noun[i][0], tuples_noun[i][1], tuples_noun[i][2], tuples_noun[i][3], tuples_noun[i][4], tuples_noun[i][5], tuples_noun[i][6]]) + "\n")
    f.close()

    f = io.open("latin_dict_verbs.txt", "w")
    f.write("|".join(["pos", "word", "fpsaPresent", "fpsaPerfect", "ppp", "conjugation", "definition"]) + "\n")
    for i in range(len(tuples_verb)):
        f.write("|".join([tuples_verb[i][0], tuples_verb[i][1], tuples_verb[i][2], tuples_verb[i][3], tuples_verb[i][4], tuples_verb[i][5], tuples_verb[i][6]]) + "\n")
    f.close()

    f = io.open("latin_dict_adjs.txt", "w")
    f.write("|".join(["pos", "word", "adjFeminine", "adjNeuter", "declension", "definition"]) + "\n")
    for i in range(len(tuples_adj)):
        f.write("|".join([tuples_adj[i][0], tuples_adj[i][1], tuples_adj[i][2], tuples_adj[i][3], tuples_adj[i][4], tuples_adj[i][5]]) + "\n")
    f.close()

    f = io.open("latin_dict_other.txt", "w")
    f.write("|".join(["pos", "word", "definition"]) + "\n")
    for i in range(len(tuples_other)):
        f.write("|".join([tuples_other[i][0], tuples_other[i][1], tuples_other[i][2]]) + "\n")
    f.close()

    return

if __name__ == "__main__":
    main()
