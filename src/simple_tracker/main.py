import json

import os
#DATA_PATH = "../test_data/Raw-full-untar.json"
#DATA_PATH="./func_test.json"
DATA_PATH="../test_data/Raw-for-normal-tar.json"
MAX_LEV=6
TAR_ID="b7f744d75e01ed158d3dc78264f17559"
OUTPUT_PATH="./data/"
DIRECTION=True
"""
运行前有这几个地方需要检查和配置：
1. 输入位置。TAR_ID
2. 数据位置。DATA_PATH
3. 查找方向。在调用tracer的位置找。
"""

def record_finder(keys: list, values: list) -> list[dict]:
    """ An universal finder for finging records.

    The finder traverse all record in `DATA` and return list of result.
    Args:
        keys: a list of keys in the json. If Fa key comes from a nested json like `annotaions.path`, the value should be a list like ['annotations','path']. ATTENTION: the maxium levels of nested keyword is **2**.
        values: target value that wanna find. The key-value pair should present one by one.
    Returns:
        A dict contains all record that match all input query keywords. 
    Raise:
        AssertionError: key/value are not presented one by one.

    """
    # TODO: 输入改成dict?
    assert (len(keys) == len(values)
            )  # Check if key/value are presented one by one.
    # prev refers the data before filtering by the current keyword and res refers filtered data.
    prev, res = DATA, []

    # For each keyword
    for word_index in range(len(keys)):
        key_word, key_value = keys[word_index], values[word_index]

        # Check if keyword is nested
        if type(key_word) == list:
            for r in prev:
                # Check if the key is existed
                data_keys = r.keys()
                if key_word[0] in data_keys and type(r[key_word[0]]) == dict and key_word[1] in r[key_word[0]].keys():
                    # Check if the value is matched
                    if r[key_word[0]][key_word[1]] == key_value:
                        res.append(r)
        else:
            # For querying with non-nested keyword
            for r in prev:
                # Check if the key is existed
                data_keys = r.keys()
                if key_word in data_keys:
                    # Check if the value is matched
                    if r[key_word] == key_value:
                        res.append(r)

        # iter results and ready for the next filter
        prev, res = res, []
    return prev

def removeduplicate(list1:list[dict]):
    """
    Remove duolicate result of the given list of dicts
    :param list1: 输入一个有重复值的列表
    :return: 返回一个去掉重复的列表
    """
    newlist = []
    for i in list1:  # 先遍历原始字典
        flag = True
        if newlist == []:  # 如果是空的列表就不会有重复，直接往里添加
            pass
        else:
            for j in newlist:
                count = len(i.keys())
                su = 0
                for key in i.keys():
                    if i[key]  == j[key]:
                        su += 1
                if su == count:
                    flag = False
        if flag:
            newlist.append(i)
    return newlist

def tracer(root_artifact: dict, maxlevel: int,direction:bool) -> list[list[dict]]:
    """ To trace UPWARD or DOWNWARD to locate which atrifacts involved.
    There are two main categories of records in spade's audit results: points and edges. Points (entities) are linked to each other by edges, thus building up a complete chain of calls. g The function tries to derive the entity that uses it backwards, achieved by looking up the source of the edge pointing to the entity.
    Args:
        root_artifact:
        record of artifact wanna trace
        maxlevel:
        maxium steps wanna trace
        direction:
        true:Upward, to->from
        false:Downward, from->to
    Returns:
        list of records which have less steps than maxlevel. res[index] means step=index+1
    """
    res = [[root_artifact]]
    artifacts = [root_artifact]
    # Trace recursively
    for _ in range(maxlevel):
        artifacts = recursively_trace(artifacts,direction)
        res.append(artifacts)
    
    return res


def recursively_trace(artifacts: list[dict],direction:bool) -> list[dict]:
    """ Recursive body of tracer.
    Provide one step of trace
    Arg:
        artifacts: list of records wanna find the upper level atrifact
        direction: same as `tracer`:
            true:Upward, to->from
            false:Downward, from->to
    Return:
        list of artigfacts which "use" artifact with given id.
    """
    res = []
    for artifact in artifacts:
        id = artifact['id']
        #print("id is %s"%id)
        # edge records which points to this artifact
        if direction:
            edges = removeduplicate( record_finder(['to'], [id]))
        else:
            edges = removeduplicate( record_finder(['from'], [id]))
        #print(edges)
        if direction:
            for edge in edges:
                to_id = edge['from']
                #print("to:%s"%to_id)
                tmp=record_finder(['id'], [to_id])
                for r in tmp:
                    # memory address has no parent and no use, drop it.
                    if "memory address" not in r['annotations'].keys():
                        res.append(r)
        else:
            for edge in edges:
                from_id = edge['to']
                tmp=record_finder(['id'], [from_id])
                for r in tmp:
                    # memory address has no parent and no use, drop it.
                    if "memory address" not in r['annotations'].keys():
                        res.append(r)         
    return removeduplicate(res)


def display_name(records: list[dict], path: str):
    ''' Display atrifacts' name and other infos and output to files
    Args:
        records: list of records wanna display
        path: path of output files
    '''
    filtered_records = []
    for record in records:
        anno = record["annotations"]
        if record["type"] == "Process":
            tmp = {
                "children pid namespace": anno["children pid namespace"], "pid": anno["pid"], "net ns": anno["net namespace"], "PID ns": anno["pid namespace"], "mnt ns": anno["mount namespace"], "exe path": anno["exe"], "id": record["id"], "type": record["type"]}
            if "command line" in anno.keys():
                tmp['cmd']=anno['command line']
        elif record["type"] == "Artifact":
            if anno["subtype"] == "file":
                tmp = {"path": anno["path"], "subtype": anno["subtype"],
                       "id": record["id"], "type": record["type"]}
            else:
                tmp = {"mem addr": anno["memory address"], "subtype": anno["subtype"],
                       "id": record["id"], "type": record["type"]}
            if "root path" in anno.keys():
                tmp["root path"]=anno["root path"]
        filtered_records.append(tmp)

    print(filtered_records)

    # Create output file
    jsObj = json.dumps(filtered_records)
    fileObject = open(path, 'w')
    fileObject.write(jsObj)
    fileObject.close()


if __name__ == "__main__":
    global DATA

    with open(DATA_PATH, 'r') as f:
        DATA = json.load(f)
    target_lists=[]
    
    
    """
    NOTE: if you need to trace a file, activate this
    """
    """
    target_lists = record_finder(
        [['annotations', 'path'], ['annotations', 'subtype']], [TAR_FILE, TAR_FILE_TYPE])
    print("Get %d records. Ready to trace" % len(target_lists))
    """
    
    
    res = []
    
    # Get target
    target_lists=record_finder(['id'],[TAR_ID])
    print("Get %d records. Ready to trace:" % len(target_lists))
    print(target_lists)
    
    
    #  Trace and display
    for target in target_lists:

        path = OUTPUT_PATH+target['id']+"/"
        if not os.path.exists(path):
            os.makedirs(path)

        res = tracer(target, MAX_LEV,DIRECTION)

        for index, lev in enumerate(res):
            # For each level, display it
            print(str(index)+":\n")
            display_name(lev, path+str(index)+".json")
        print("\n--------------------------------------------------------\n")
        print(res)
