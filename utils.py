import pandas as pd


def get_maximum(elems:list) -> list:
    max = elems[0]
    for elem in elems :
        if max[0] >=elem[0]:
            max= elem
    return elem

def filter(elems:list,indices_not:list = []):
    indices_rest = indices_not.copy()
    if len(elems)!=0:
        test = []
        indices_out = elems[0][1:]
        test.append(elems[0])
        for i,elem_i in enumerate(elems[1:]):
            if  len(list(set(elem_i[1:]) & set(indices_rest))) ==0:
                test.append(elem_i)
                indices_out+=elem_i[1:]
                indices_rest += elem_i[1:] # not to use anymore
        if len(list(set(elems[0][1:]) & set(indices_rest))) !=0:
            test.remove(elems[0])
        return test, indices_out

    else: 
        return [],[]

def chunks(text:pd.DataFrame,N_CTX;int)-> list:
    text.reset_index(drop=True,inplace=True)
    tokens = text.n_tokens.to_list()
    out_3 = [[sum([y,x,z]),i,j,k] for i,y in enumerate(tokens) for j,x in enumerate(tokens) for k,z in enumerate(tokens) if i!=j and j!=k and i!=k]
    out_3 = [elem for elem in out_3 if elem[0]<N_CTX]
    out_3,indices = filter(out_3)
    out_2 = [[sum([y,x]),i,j] for i,y in enumerate(tokens) for j,x in enumerate(tokens) for k,z in enumerate(tokens) if i!=j]
    out_2 = [elem for elem in out_2 if elem[0]<N_CTX]
    out_2,indices_2 = filter(out_2,indices)
    out_1 = [[y,i] for i,y in enumerate(tokens)]
    out_1,indices_3 = filter(out_1,indices_2+indices)
    results = [elem[1:] for elem in out_3]+[elem[1:] for elem in out_2] +[elem[1:] for elem in out_1]
    texts = ["\n\n".join(text.loc[elem,'text'].to_list()) for elem in results]
    return texts
