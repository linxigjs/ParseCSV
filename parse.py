
def del_replicate_elems(ll):
    if len(ll) < 2:
        return None
    result = []
    for elem in ll:
        if elem not in result:
            result.append(elem)
    return result

def parse_file(filename):
    linecnt = 0
    result = {}
    keys = []
    with open(filename, 'r') as fileread:
        while True:
            oneline = fileread.readline()
            if not oneline:
                break
                pass
            oneline = oneline.strip(' ')
            oneline = oneline.strip('\n')
            data = oneline.split(',')
            if linecnt == 0:
                keys = data
            else:
                temp = dict(zip(keys, data))
                # print(temp)
                result[temp['id']] = temp
                # print(result)
            linecnt += 1
    return result, keys, linecnt

def merge_dicts(dic1, keys1, lines1, dic2, keys2, lines2):
    keys = del_replicate_elems(keys1 + keys2)
    result = {}
    print(keys)
    for i in range(1, lines1+lines2):
        i = str(i)
        res1 = dic1.get(i)
        res2 = dic2.get(i)
        result[i] = dict.fromkeys(keys)
        if res1 == None and res2 == None:
            result.pop(i)
            break
        else:
            for k in keys:
                elem1 = None
                elem2 = None
                if res1 != None:
                    elem1 = res1.get(k)
                if res2 != None:
                    elem2 = res2.get(k)
                if elem1 != None and elem2 != None and elem1 != elem2:
                    print("Error: id=" + str(i) + ", key=" + k + ", value1=" + elem1 + ", value2=" + elem2)
                    result[i][k] = "ERROR"
                    pass
                elif elem1 == None:
                    result[i][k] = elem2
                else:
                    result[i][k] = elem1
    result = sorted(result.items(), key = lambda item : item[0])
    for k,v in result:
        print("{key} : {value}".format(key = k, value = v))
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
    dic1, keys1, lines1 = parse_file(file1)
    dic2, keys2, lines2 = parse_file(file2)
    merged, keys = merge_dicts(dic1, keys1, lines1, dic2, keys2, lines2)
    write_to_csv("result.csv", merged, keys)

main()