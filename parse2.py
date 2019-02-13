
def del_replicate_elems(ll):
    if len(ll) < 2:
        return None
    result = []
    for elem in ll:
        if elem not in result:
            result.append(elem)
    return result

def parse_to_one(filename1, filename2):
    ### 解析所有的key
    fileread1 = open(filename1, 'r')
    oneline = fileread1.readline()
    oneline = oneline.strip(' ')
    oneline = oneline.strip('\n')
    keys1 = oneline.split(',')

    fileread2 = open(filename2, 'r')
    oneline = fileread2.readline()
    oneline = oneline.strip(' ')
    oneline = oneline.strip('\n')
    keys2 = oneline.split(',')

    keys = del_replicate_elems(keys1 + keys2)
    result = {}

    ### 解析file1
    while True:
        oneline = fileread1.readline()
        if not oneline:
            break
        oneline = oneline.strip(' ')
        oneline = oneline.strip('\n')
        value1 = oneline.split(',')
        temp = dict(zip(keys1, value1))
        i = value1[keys1.index('id')]
        result[i] = dict.fromkeys(keys)
        for k in keys:
            result[i][k] = temp.get(k)
    fileread1.close()

    ### 解析file2
    while True:
        oneline = fileread2.readline()
        if not oneline:
            break
        oneline = oneline.strip(' ')
        oneline = oneline.strip('\n')
        value2 = oneline.split(',')
        temp = dict(zip(keys2, value2))
        i = value2[keys2.index('id')]
        sliced = result.get(i)
        if sliced == None:
            result[i] = dict.fromkeys(keys)
            for k in keys:
                result[i][k] = temp.get(k)
        else:
            for k in keys:
                if result[i][k] == None:
                    result[i][k] = temp.get(k)
                elif result[i][k] != temp.get(k) and temp.get(k) != None:
                    print("Error: id=" + str(i) + ", key=" + k + ", value1=" + result[i][k] + ", value2=" + temp.get(k))
                    result[i][k] = "ERROR"
    fileread2.close()

    result = sorted(result.items(), key=lambda item: item[0])
    for k, v in result:
        print("{key} : {value}".format(key=k, value=v))

    return result, keys

def write_to_csv(filename, context, keys):
    with open(filename, 'w') as filewrite:
        onerecord = ""
        for e in keys:
            onerecord += (e + ',')
        onerecord = onerecord[:-1]
        filewrite.write(onerecord)
        filewrite.write('\n')
        for key, data in context:
            onerecord = ""
            for k in keys:
                if data.get(k) != None:
                    onerecord += (data.get(k) + ",")
                else:
                    onerecord += ','
            onerecord = onerecord[:-1]
            filewrite.write(onerecord)
            filewrite.write('\n')

def main():
    file1 = "table1.csv"
    file2 = "table2.csv"
    context, keys = parse_to_one(file1, file2)
    write_to_csv("result.csv", context, keys)

main()