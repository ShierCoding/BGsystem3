from files import target_files
import zipfile
import os
import utils
import hashlib
import json


# 压缩
def compress():
    with zipfile.ZipFile(utils.ToAbsolutePath("BGsystem3.zip"), "w") as zipf:
        for file in target_files:
            if os.path.isfile(file):
                zipf.write(file, utils.ToParentPath(utils.JoinPath(file)))
            elif os.path.isdir(file):
                print("正在压缩:", file)
                for root, dirs, files in os.walk(file):
                    # print(root, dirs, files)
                    root = os.path.normpath(root)
                    for f in files:
                        zipf.write(utils.JoinPath(root, f),
                                   utils.ToParentPath(utils.JoinPath(root, f)))
            else:
                print(f"文件 {file} 未找到")


version = json.load(open(utils.ToAbsolutePath("../package.json")))["version"]


def main():

    for file in os.listdir("./"):
        if file.startswith("BGsystem3-") and file.endswith(".zip"):
            os.remove(utils.ToAbsolutePath(file))

    compress()

    with open(utils.ToAbsolutePath("BGsystem3.zip"), "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()[:6]

    file_name = f"BGsystem3-{version}-{hash}.zip"

    print(file_name)
    os.rename(utils.ToAbsolutePath("BGsystem3.zip"),
              utils.ToAbsolutePath(file_name))


if __name__ == "__main__":
    main()
