#-*- coding:utf-8 –*-

#列表去重
def list_unique(List):
    new_list=[]
    for id in List:
        if id not in new_list:
            new_list.append(id)
    return new_list


#创建矩阵，number为矩阵一维个数，number为填充数字
def create_matrix(number,amount):
    matrix = []
    for i in xrange(0,number):
        tmp = []
        for j in xrange(0,number):
            tmp.append(amount)
        matrix.append(tmp)
    return matrix


#查找包含该元素的所有位置
def find_index(List,node):
    return [i for i,j in enumerate(List) if j==node]


#获取模块度
def get_modularity(node_list,node_club,club_list,node_matrix):
    uni = list_unique(club_list)



    #更新社团位置
    for node in uni:
        idices=find_index(club_list,node)
        for i in idices:
            node_club[i]=uni.index(node)

    Q=0
    m=sum([sum(node) for node in node_matrix])/2# 网络的边的数目

    k=len(list_unique(node_club))# 社团数目 输出满足条件的个数

    e=create_matrix(k,0)#构造0矩阵

    for i in xrange(k):
        idx=find_index(node_club,i)
        labelsi=idx

        for j in xrange(k):
            idx=find_index(node_club,j)
            labelsj=idx

            for ii in labelsi:
                for jj in labelsj:
                    e[i][j]=e[i][j]+node_matrix[ii][jj]#e[i][j]代表i社团与j社团之间有多少连接


    e=[[float(j)/(2*m) for j in i] for i in e]


    a = []

    for i in xrange(k):
        ai=sum(e[i])
        a.append(ai)
        Q = Q + e[i][i]-ai**2

    return Q,e,a,node_club

if __name__ == '__main__':

    print "2"