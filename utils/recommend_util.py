import operator
from math import sqrt


# 基于用户的协同过滤推荐算法实现
# 基于用户的协同过滤推荐算法实现原理：
# 1、根据用户动漫评分信息构建用户动漫评分数据模型；
# 2、根据用户动漫评分数据模型计算用户之间的相似度；
# 3、根据用户之间的相似度得到目标用户的最近邻居KNN；
# 4、预测动漫的评分值并进行推荐。
# 参数：currentUserid，目标用户id，即登录用户id
# 参数：rates，用户评分集合
def doCFBasedUser(currentUserid, rates):
    print("基于用户的协同过滤推荐算法开始")
    # 当前登录用户id，即目标用户id，数据类型转换
    currentUserid = int(currentUserid)
    # 创建一个空字典，保存用户-动漫评分数据模型（字典的键是用户id，值也是字典（键是动漫id，值是评分））
    data_dic = {}
    # 遍历所有评分数据
    if rates is not None and len(rates) > 0:
        for rate in rates:
            userid = int(rate.userid_id)  # 用户id
            itemid = int(rate.animeid_id)  # 动漫id
            rating = float(rate.score)  # 评分值
            # 为 用户-动漫评分数据模型 赋值
            if userid not in data_dic.keys():
                data_dic[userid] = {itemid: rating}
            else:
                data_dic[userid][itemid] = rating
    # 如果 用户-动漫评分数据模型 为空
    if len(data_dic) == 0:
        print("没有评分数据！")
        print("基于用户的协同过滤推荐算法结束")
        return None
    # 判断目标用户是否有评分数据
    if currentUserid not in data_dic.keys():
        print("目标用户没有评分数据！")
        print("基于用户的协同过滤推荐算法结束")
        return None
    # 计算用户相似度（余弦相似度算法）
    print("计算目标用户与其他用户的相似度（余弦相似度算法）：")
    similarity_dic = dict()  # 定义目标用户与其他用户的相似度字典（键是用户id，值是相似度）
    for userid, items in data_dic.items():  # 遍历用户-动漫评分数据模型中的所有用户
        if currentUserid != userid:  # 不计算目标用户与自身的相似度
            # 余弦相似度算法
            temp = 0.0  # 计算分子
            temp2 = 0.0  # 计算分母
            temp3 = 0.0  # 计算分母
            sim = 0.0  # 定义两个用户的相似度
            for itemid, rating in data_dic[currentUserid].items():  # 遍历目标用户的评分动漫
                if itemid in items.keys():  # 只计算有共同评分的动漫
                    temp += rating * items[itemid]  # 评分相乘 之和
                    temp2 += pow(rating, 2)  # 评分相乘 之和
                    temp3 += pow(items[itemid], 2)  # 评分相乘 之和
            if temp2 != 0.0 and temp3 != 0.0:
                sim = temp / (sqrt(temp2) * sqrt(temp3))  # 计算相似度
            # 赋值
            similarity_dic[userid] = sim
            # 打印输出用户相似度
            print("userid:" + str(currentUserid) + "    与userid：" + str(userid) + "    相似度=" + str(sim))
    # 将相似度排序（降序排列），返回list类型，目标用户与其他用户的相似度（按照相似度大小降序排列后的结果，即用户的所有邻居）
    similarity_dic = sorted(similarity_dic.items(), key=operator.itemgetter(1), reverse=True)
    print("目标用户与其他用户的相似度（按照相似度大小降序排列）：")
    print(similarity_dic)
    # 截取前N个用户，作为目标用户的最近邻居knn
    similarity_dic = similarity_dic[:20]
    # 过滤掉相似度为0的最近邻居
    similarity_dic = [(key, value) for key, value in similarity_dic if value > 0]
    print("目标用户的最近邻居：")
    print(similarity_dic)
    similarity_dic = dict(similarity_dic)  # 列表转字典类型
    # 推荐并预测评分
    # 定义待推荐的动漫字典（键是动漫id，值是字典（键是最近邻用户id，评分值））
    # 待推荐的动漫是所有最近邻居评分的动漫，但是目标用户没有评分的动漫
    item_rec_dic = dict()
    # 遍历最近邻居，获取待推荐的动漫
    for userid, similarity in similarity_dic.items():
        # 遍历当前用户的评分动漫
        for itemid, rating in data_dic[userid].items():
            # 过滤掉目标用户已评分的动漫
            if itemid not in data_dic[currentUserid].keys():
                # 将待推荐的动漫加入到字典中
                if itemid not in item_rec_dic.keys():
                    item_rec_dic[itemid] = {userid: rating}
                else:
                    item_rec_dic[itemid][userid] = rating
    print("所有待推荐的动漫（所有最近邻居评分的动漫，但是目标用户没有评分的动漫）：")
    print(item_rec_dic)
    # 定义最终推荐的动漫字典，键是动漫id，值是预测评分
    # 至少有两个最近邻用户同时评分的同一个动漫才可以推荐，即只有一个最近邻推荐的动漫，误差较大，排除
    item_rec_final_dic = dict()
    # 遍历所有待推荐的动漫，计算预测评分
    for itemid, users in item_rec_dic.items():
        if len(users) > 1:
            temp1 = 0  # 分子
            temp2 = 0  # 分母
            for userid, rating in users.items():
                temp1 += similarity_dic[userid] * rating  # 相似度 * 评分 之和
                temp2 += similarity_dic[userid]  # 相似度之和
            if temp2 != 0.0:
                item_rec_final_dic[itemid] = temp1 / temp2  # 预测评分
    print("所有推荐的动漫和预测评分：")
    print(item_rec_final_dic)
    # 降序排序，根据预测评分
    item_rec_final_dic = sorted(item_rec_final_dic.items(), key=operator.itemgetter(1), reverse=True)
    print("最终推荐的动漫和预测评分：")
    # 截取前n个预测评分较高的动漫进行推荐
    item_rec_final_dic = item_rec_final_dic[:10]
    print(item_rec_final_dic)
    print("基于用户的协同过滤推荐算法结束")
    # 返回推荐动漫id列表
    return [itemid for itemid, pref in item_rec_final_dic]
