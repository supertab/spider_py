import pickle

def classf_hs(datapth):
    with open(datapth, 'rb') as f:
        data = pickle.load(f)

    hs_data = list(set(zip(*data)))
    # get item then init classfiy dictionary
    item = set(data[0])
    classf ={} 
    for i in item:
        classf.setdefault(i,[])

    for each_hs in hs_data:
        classf[each_hs[0]].append(each_hs)

    return classf

datapth = 'hs_info_5000.pkl'
dictHourse = classf_hs(datapth)
data_out = 'hs_info_5000.dict.pkl'
with open(data_out, 'wb') as f:
    pickle.dump(dictHourse, f)
