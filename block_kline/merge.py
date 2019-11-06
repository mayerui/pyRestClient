#encoding=GBK
import os

if __name__ == '__main__':
    with open("result.csv","w") as f_result:
        filelist = os.listdir("./")
        for filename in filelist:
            if ".csv" in filename: #可选
                with open(filename, "r") as f:
                    lines = f.readlines()
                    f_result.writelines(lines)