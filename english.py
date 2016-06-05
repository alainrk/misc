import json
import random
import time
import sys

ADD = 1
STUDY = 2

def english(mode):
    random.seed(time.time())

    with open('words.json', 'r') as wordsfile:
        jsondata = json.load(wordsfile)
        wordsfile.close()
        words = jsondata['words']

        if mode == STUDY:
            print
            while words:
                choice = random.randint(0,len(words)-1)
                source = ", ".join(words[choice]['en'])
                dest = ", ".join(words[choice]['it'])
                guess = raw_input("Translate ["+source+"]: ")
                print "Translations ["+dest+"]\n"
                del words[choice]

        elif mode == ADD:
            all_engs, all_itas = [],[]

            while True:
                answer = raw_input("\nPress \"w\" to continue adding words, or \"s\" to save and close: ")
                if answer == "w":
                    pass
                elif answer == "s":
                    if all_engs and all_itas:
                        print "ENGS:",all_engs
                        print "ITAS:",all_itas
                        for item in zip(all_engs, all_itas):
                            words.append({'en':item[0], 'it':item[1]})
                        print "Updating dictionary...\nDo not close the program!\n"
                        with open('words.json', 'w+') as wordsfile:
                            wordsfile.write(json.dumps(jsondata))
                            wordsfile.close()
                            break
                        print "\nWriting file ERROR\n"
                    else:
                        print "\nNothing to save!\n"
                else:
                    continue

                engs = raw_input("Write all ENGLISH terms comma-separated [Ex: path, way, road]\n> ").strip(", ")
                itas = raw_input("Write all ITALIAN terms comma-separated [Ex: strada, via, percorso]\n> ").strip(", ")
                engs, itas = filter(lambda x: len(x), engs.split(",")), filter(lambda x: len(x), itas.split(","))

                if engs and itas:
                    print "Adding to dictionary... \n\nENG:", engs, "\nITA:", itas
                    answer = raw_input("\nConfirm [y/n]: ")
                    if answer == "y":
                        all_engs += [engs]
                        all_itas += [itas]
                        print "Adding confirmed!\n"
                        pass
                    else:
                        print "Adding cancelled!\n"
                else:
                    print "\n\nEmpty definition NOT allowed!\n"

        else:
            print "Mode not recognized.\n"
    return


if __name__ == "__main__":
    try:
        mode = sys.argv[1]
    except:
        mode = "Error"

    if mode not in ["--add","--study"]:
        print "\nEnglish Study:\n\n\t--help\t[Get this message]\n\t\n\t--add\t[Add a word]\n\t--study\t[Guess your words]\n"
        sys.exit(0)

    if mode == "--add":
        mode = ADD
    elif mode == "--study":
        mode = STUDY
    else:
        "Unknown option!"
        sys.exit(0)

    english(mode)
