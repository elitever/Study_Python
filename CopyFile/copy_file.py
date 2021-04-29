import os
import shutil
import re

file_type = '.png'#指定文件类型
str_cond = '-Dfn_info-'#正则条件
saveRootDirPath = os.path.abspath('.')
old_path = os.path.abspath('.') + "/FileName" #原文件夹路径
image_path = os.path.abspath('.') + "/Image"#新文件夹路径
new_path = os.path.abspath('.') + "/NewFile"#新文件夹路径

#获取指定文件中文件名
def get_filename(filetype):
    name =[]
    final_name_list = []
    source_dir=os.getcwd()#读取当前路径
    for root,dirs,files in os.walk(source_dir):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype,''))
    final_name_list = [item +filetype for item in name]
    return final_name_list

#主函数
def main_function(filetype,str_cond,old_path,new_path):
    final_name_list = get_filename(filetype)
    for imagename in final_name_list:
        newname_pach = old_path + "/" +imagename.replace('.png','')
        shutil.copyfile(os.path.join(image_path, imagename), os.path.join(newname_pach , imagename))
    return 1

if __name__ == "__main__" :

  main_function(file_type,str_cond,old_path,new_path)#主函数

