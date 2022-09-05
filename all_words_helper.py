import os

# inp = open('all_englist_words.txt', 'r')
# out = open('all_4+_letter_words.txt', "w")
# for line in inp:
#     if len(line) >= 5:
#         out.write(line)

# inp.close()
# out.close()

# os.remove('superstrings_removed.txt')
# print('1')

inp = open('all_4+_letter_words.txt', 'r')
# out = open('superstrings_removed.txt', "w")
# print('1')

wordList = []
# endList = []
# print('1')
for line in inp:
    wordList.append(line[:-1])
    # endList.append(line)

wordList.sort()

temp = "1"
i = 0
while True:
    try:
        if wordList[i].startswith(temp):
            print('superstring found')
            print(temp)
            print(wordList[i])
            wordList.pop(i)
        else:
            print('no superstring')
            temp = wordList[i]
            print(temp)
            i += 1
    except:
        break

# print(wordList)
print(len(wordList))

# print(inp)
# # print(wordList)
# print('1')
# print(type(inp))

# inp.close()
# inp = open('all_4+_letter_words.txt', 'r')

# for line in inp:
#     print("test")
#     print(type(line))
# print('1')
# inp.close()
# inp = open('all_4+_letter_words.txt', 'r')
# for line in inp:
#     print(line)
#     for word in wordList:
#         # print(word)
#         if word != line.strip("\n") and line.strip("\n").startswith(word):
#             try:
#                 endList.remove(line)
#             except:
#                 break

# for word in endList:
#     out.write(word)

inp.close()
# out.close()
