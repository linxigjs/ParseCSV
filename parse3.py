
def del_replicate_elems(ll):
    if len(ll) < 2:
        return None
    result = []
    for elem in ll:
        if elem not in result:
            result.append(elem)
    return result

def get_all_keys(files):
    keys = []
    for f in files:
        fileread = open(f, 'r')
        oneline = fileread.readline()
        oneline = oneline.strip(' ')
        oneline = oneline.strip('\n')
        keys.extend(oneline.split(','))
        fileread.close()
    return del_replicate_elems(keys)

def parse_first(firstfile, result, keys):
    with open(firstfile, 'r') as fileread1:
        oneline = fileread1.readline()
        oneline = oneline.strip(' ')
        oneline = oneline.strip('\n')
        keys1 = oneline.split(',')
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
    return result

def parse_one_file(onefile, result, keys):
    with open(onefile, 'r') as fileread:
        oneline = fileread.readline()
        oneline = oneline.strip(' ')
        oneline = oneline.strip('\n')
        keys2 = oneline.split(',')
        while True:
            oneline = fileread.readline()
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
    return result


def parse_others(others, result, keys):
    for f in others:
        result = parse_one_file(f, result, keys)
    return result

def parse_to_one(files):
    ### 解析所有的key
    if(len(files) == 0):
        return None
    keys = get_all_keys(files)
    result = {}
    result = parse_first(files[0], result, keys)
    result = parse_others(files[1:], result, keys)
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
    file3 = "table3.csv"
    context, keys = parse_to_one([file1, file2, file3])
    write_to_csv("result.csv", context, keys)

main()