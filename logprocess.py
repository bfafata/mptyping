with open('log.txt') as log:
    result=[]
    rawstr=str(log.read())

    rawstr.split(" ")
    print(rawstr[0:100])
    for word in rawstr:
        try:
            float(word)
            result.append(word)
        except:
            pass
print(result[0:100])
with open("goodlog.txt","a") as goodlog:
    for item in result:
        goodlog.write(item+"\n")


# C:/Users/wxyan/anaconda3/python.exe 