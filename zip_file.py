#coding: utf-8
import re
import os
import zipfile

def zipdir(path):
    for root, dirs, files in os.walk(path):
        # print root, dirs, files
        for file in files:
            abs_path = os.path.join(root, file)

            # 压缩文件
            # zfile = zipfile.ZipFile(abs_path + '.zip', 'w', zipfile.ZIP_DEFLATED)
            # zfile.write(abs_path)
            # zfile.close()

            # 删除压缩文件
            if re.match(r'.+\.zip', file):
                os.remove(abs_path)


if __name__ == '__main__':
    zipdir('/Users/dickr/Downloads/mgcmall/PublicWelfareStar/webgl/models/obj/')
    # zipdir('tmp 2/')
