from invoke import task, Context
import wget
import zipfile
import os
import utils
import time
from typing import List


# 将../python-embed-amd64/Scripts添加至环境变量
os.environ["PATH"] += os.pathsep + \
    os.path.abspath("../python-embed-amd64/Scripts")


@task
def download_python(ctx: Context):
    """
    下载 Embed 版 Python
    """

    print("正在下载Embed版Python...")

    wget.download("https://registry.npmmirror.com/-/binary/python/3.11.9/python-3.11.9-embed-amd64.zip",
                  "../python-embed-amd64.zip")

    print("下载完毕，正在解压缩...")

    with zipfile.ZipFile("../python-embed-amd64.zip", 'r') as zip_ref:
        zip_ref.extractall("../python-embed-amd64")

    os.remove("../python-embed-amd64.zip")

    print("解压缩完毕，正在修改第三方包路径...")

    with open("../python-embed-amd64/python311._pth", "a") as f:
        f.write("\nLib\\site-packages")

    print("修改完毕")


def add_path(path: List[str]):
    tpath = ";".join(map(lambda x: utils.ToAbsolutePath(x), path))
    os.system(rf"set PATH={tpath};%PATH%;{tpath}")


@task
def install_pip(ctx: Context):
    """
    安装 pip
    """

    add_path(["../python-embed-amd64", "../python-embed-amd64/Scripts"])

    time.sleep(1)

    os.system("where python")
    os.system("where pip")

    print("正在下载get-pip.py...")

    if (not utils.IfFileExist("../python-embed-amd64/get-pip.py")):
        wget.download("http://mirrors.aliyun.com/pypi/get-pip.py",
                      "../python-embed-amd64/get-pip.py")

    print("下载完毕，运行get-pip.py...")

    os.chdir("../python-embed-amd64")
    os.system("python.exe ./get-pip.py")

    print("pip安装完毕，正在更新依赖...")

    os.chdir("./Scripts")

    os.system(rf"chdir")

    # 安装依赖
    requirements = " ".join([
        "fastapi",
        '"uvicorn[standard]"',
        "invoke",
        "toml",
        "ffmpy"
    ])

    print("$ pip.exe install " + requirements)
    os.system("pip.exe install " + requirements)

    print("依赖更新完毕")


@task
def download(ctx: Context):
    """
    安装 Python 和 pip
    """
    os.system("chcp 65001")

    if (not utils.IfPathExist("../python-embed-amd64/")):
        download_python(ctx)
    install_pip(ctx)


@task
def build(ctx: Context):
    import bundle
    bundle.main()
