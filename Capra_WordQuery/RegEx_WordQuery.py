
# coding: utf-8

# In[1]:


import re
import string


# In[2]:


def word_without_punctuation(lines):
    new_words = []  # this holds the values of the words without punctuation
    lines = lines.rstrip()  # this will get rid of any whitespace
    words = lines.split()  # this will hold the value of the words given in the parameter

    # this goes through the list of words and makes it lower case
    for word in words:
        new_words.append(word.strip(string.punctuation).lower())

    return new_words


# In[3]:


def stopWords():
    new_stopwords = []
    stoplist = open('stopwords.txt', 'r', encoding='utf8')
    stopwords = stoplist.readlines()
    for word in stopwords:
        new_stopwords.append(word.rstrip())
    stoplist.close()
    return new_stopwords


# In[4]:


def querySearch(indexDic):
    matches = False
    query=input('Please enter a query: ')
    querySplit = query.split()
    print("query= ", query)
    if query=="qquit":
        quit()

    elif len(querySplit) == 1:
        if querySplit[0] in indexDic.keys():
            for title, lNum in indexDic[query].items():
                print(title)
                for ln in lNum:
                    print(" ", ln, part2LineList[ln - 1].replace(query, "**" + query.upper() + "**"))
        else:
            print("- -")

    elif len(querySplit)==2:
        if querySplit[0] in indexDic.keys() and querySplit[1] in indexDic.keys():
            for title,lNum in indexDic[querySplit[0]].items():
                for title2, lNum2 in indexDic[querySplit[1]].items():
                    if title==title2:
                        matches=True
                        print(title)
                        print("   ", querySplit[0])
                        for ln in lNum:
                            print("     ", ln, part2LineList[ln - 1].replace(querySplit[0], "**" + querySplit[0].upper() + "**"))
                        print("   ", querySplit[1])
                        for ln2 in lNum2:
                            print("     ", ln2, part2LineList[ln2 - 1].replace(querySplit[1], "**" + querySplit[1].upper() + "**"))
        if matches==False:
            print("- -")

    elif len(querySplit) >= 3:
        if querySplit[1]=='or':
            if querySplit[0] in indexDic.keys():
                ## print(querySplit[0])
                for title, lNum in indexDic[querySplit[0]].items():
                    print(" ", title, "\n", querySplit[0])
                    for ln in lNum:
                        print("   ", ln, part2LineList[ln - 1].replace(querySplit[0], "**" + querySplit[0].upper() + "**"))

            else:
                print(querySplit[0], "\n", "- -")

            if querySplit[2] in indexDic.keys():
                #print(querySplit[2])
                for title, lNum in indexDic[querySplit[2]].items():
                    print(" ", title, "\n", querySplit[2])
                    for ln in lNum:
                        print("   ", ln, part2LineList[ln - 1].replace(querySplit[2], "**" + querySplit[2].upper() + "**"))
            else:
                print(querySplit[2], "\n", "- -")
        elif querySplit[1]=='and':
            if querySplit[0] in indexDic.keys() and querySplit[2] in indexDic.keys():
                for title, lNum in indexDic[querySplit[0]].items():
                    for title2, lNum2 in indexDic[querySplit[2]].items():
                        if title == title2:
                            matches = True
                            print(title)
                            print("   ", querySplit[0])
                            for ln in lNum:
                                print("     ", ln,part2LineList[ln - 1].replace(querySplit[0], "**" + querySplit[0].upper() + "**"))
                            print("   ", querySplit[2])
                            for ln2 in lNum2:
                                print("     ", ln2, part2LineList[ln2 - 1].replace(querySplit[2],"**" + querySplit[2].upper() + "**"))
            if matches == False:
                print("- -")


        elif querySplit[1]=='near':
            if querySplit[0] in indexDic.keys() and querySplit[2] in indexDic.keys():
                for title, lNum in indexDic[querySplit[0]].items():
                    for title2, lNum2 in indexDic[querySplit[2]].items():
                        if title == title2:
                            for ln in lNum:
                                for ln2 in lNum2:
                                    difference = 0
                                    difference = abs(ln - ln2)
                                    if difference<=1 and difference>=0:
                                        matches=True
                                        print(title)
                                        print("   ", querySplit[0])
                                        print("     ", ln, part2LineList[ln - 1].replace(querySplit[0],"**" + querySplit[0].upper() + "**"))
                                        print("   ", querySplit[2])
                                        print("     ", ln2, part2LineList[ln2 - 1].replace(querySplit[2],"**" + querySplit[2].upper() + "**"))


            if matches==False:
                print("- -")

        else:

            counter=0
            for words in querySplit:
                if words in indexDic.keys():
                    # match will be True if all the query words are in the dictionary
                    # counter counts how many words are in the query
                    matches=True
                    counter+=1
                else:
                    # if it is false the loop will break and the "if" statement below will not execute
                    matches=False
                    break

            if matches==True:
                titles=[]
                # for loop iterates through every word query
                for i in range(counter):
                    # for loop iterates through every title associated with query
                    for title in indexDic[querySplit[i]].keys():
                        # holds all the titles associated with the word query
                        titles.append(title)
                for x in titles:
                    # if the current title in the list appears the same amount of how many query words
                    # then every query word shares that title
                    if titles.count(x)==counter:
                        print("\n",x)
                        for i in range(counter):
                            print("  ", querySplit[i])
                            for lineNums in indexDic[querySplit[i]][x]:
                                integerLine=int(lineNums)
                                print("     ", integerLine,part2LineList[integerLine - 1].replace(querySplit[i], "**" + querySplit[i].upper() + "**"))
                        break
            else:
                print("- -")

    querySearch(indexDic)


# In[ ]:


if __name__ == '__main__':
    indexDic={}
    stopWordList= stopWords()
    grimmText = open('grimms.txt', 'r')
    lineNum=0
    part2LineList=[]
    for line in grimmText:
        lineNum += 1
        lines=line.strip()
        part2LineList.append(lines)

        matchTitle = re.search(r'^[A-Z\-\[ ]+-?[A-Z]$', line)
        if lineNum<401 or lineNum>9593:

            continue
        else:
            if matchTitle:
                cur_title=line.strip()

            else:
                newlineList = word_without_punctuation(line)
                for word in newlineList:
                    if word not in stopWordList:
                        indexDic.setdefault(word,{}).setdefault(cur_title,[]).append(lineNum)


    querySearch(indexDic)

