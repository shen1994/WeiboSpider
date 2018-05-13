# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:50:29 2018

@author: shen1994
"""

import os
import pymongo

user_id = ["1420174783", "1246792191", "1559383255"]

is_delete = True
data_path = "weibo"

if __name__ == "__main__":

    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["weibo"]

    post_coll = db["posts"]
    response_coll = db["responses"]
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    for id_num in user_id:
        
        if not os.path.exists(data_path + os.sep + id_num):
            os.makedirs(data_path + os.sep + id_num)
        
        user_id_path = data_path + os.sep + id_num
        
        to_posts = post_coll.find({"ID": id_num})
        
        for i in range(to_posts.count()):

            one_post = to_posts.next()		            
            
            if len(one_post) < 7: # 防止数据库存在空值
                continue
        
            one_one_post = one_post["post"]    
            one_comment = one_post["comment"]
            one_like = one_post["like"]
            one_transfer = one_post["transfer"]    
            one_time = one_post["time"] 
            one_id = one_post["_id"]
            
            if is_delete:
                post_coll.delete_one({"_id": one_id})
            
            to_responses = response_coll.find({"ID": one_id, "ID_ID": id_num})
            
            with open(user_id_path + os.sep + one_id + ".txt", "w") as infile:
                
                infile.truncate()
                infile.writelines("P0")
                infile.writelines(" +++$+++ ")
                infile.writelines(one_one_post.encode("utf-8"))
                infile.writelines(" +++$+++ ")
                infile.writelines(one_time.encode("utf-8"))
                infile.writelines(" +++$+++ ")
                infile.writelines(str(one_comment).encode("utf-8"))
                infile.writelines(" +++$+++ ")
                infile.writelines(str(one_like).encode("utf-8"))
                infile.writelines(" +++$+++ ")
                infile.writelines(str(one_transfer).encode("utf-8"))
                infile.writelines("\n")

                for j in range(to_responses.count()):
                        
                    one_response = to_responses.next()
                        
                    if len(one_response) < 6:
                        continue
                            
                    one_one_response = one_response["response"]
                    one_time = one_response["time"]
                    one_like = one_response["like"]
                            
                    if is_delete:
                        response_coll.delete_one({"_id": one_response["_id"]})
       
                    infile.writelines("R" + str(j + 1))
                    infile.writelines(" +++$+++ ")
                    infile.writelines(one_one_response.encode("utf-8"))
                    infile.writelines(" +++$+++ ")
                    infile.writelines(one_time.encode("utf-8"))
                    infile.writelines(" +++$+++ ")
                    infile.writelines(str(one_like).encode("utf-8"))
                    infile.writelines("\n")

            print id_num + "--->" + one_id + "--->" + str(i) + "--->" + "OK"
        
        # 删除信息缺失的项
        if is_delete:
            post_coll.delete_many({"ID": id_num})
            response_coll.delete_many({"ID_ID": id_num})
            
        print id_num + "--->" + "OK"
