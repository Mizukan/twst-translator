# -*- coding: utf-8 -*-
"""第一次设置：把本地译文仓库连到 GitHub 上，并上传第一次。

（由 1-第一次设置.bat 调用；也可以直接 python first_setup.py 跑）
"""
import os
import subprocess
import sys

import gitutil

sys.stdout.reconfigure(errors="replace")     # 万一有打不出来的符号也不崩
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_URL = "https://github.com/Mizukan/twst-translator.git"


def main():
    print("=" * 62)
    print("  第一次设置（只管一次）")
    print("=" * 62)
    print()
    print("这个脚本会把当前文件夹，连到你 GitHub 上的仓库，并上传第一次。")
    print()
    print("先确认两件事：")
    print("  1) 你已经在网页上建好了仓库，名字叫 twst-translator")
    print("     建仓库的地址：https://github.com/new")
    print("  2) 那个仓库选的是 Public（公开）—— 私有的别人下载不到更新")
    print()
    ans = input("都弄好了吗？好了输入 y 再回车：").strip().lower()
    if ans != "y":
        print()
        print("那先去建仓库，建好了再跑一次这个脚本。")
        return 1

    print()
    GIT = gitutil.git_or_explain()
    if not GIT:
        return 1
    print()
    print("正在连接仓库 ...")
    subprocess.run([GIT, "remote", "remove", "origin"], cwd=HERE,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    r = subprocess.run([GIT, "remote", "add", "origin", REPO_URL], cwd=HERE)
    if r.returncode != 0:
        print()
        print("连接失败，把上面的提示截图发我看看。")
        return 1
    subprocess.run([GIT, "remote", "-v"], cwd=HERE)

    print()
    print("现在开始上传。")
    print("如果弹出登录窗口：选 Sign in with your browser，")
    print("浏览器里登录 Mizukan 账号、点授权。这次之后就不用再登了。")
    print()
    r = subprocess.run([GIT, "push", "-u", "origin", "main"], cwd=HERE)
    print()
    print("-" * 62)
    if r.returncode == 0:
        print("成功了！刷新一下你的仓库页面，能看到 version.json 就对了。")
        print("以后出新译文，双击「发布.bat」就行。")
    else:
        print("这次没传上去。把上面的提示截图发我，我看看是怎么回事。")
        print("（最常见的原因是：仓库还没建，或者名字/账号写错了）")
    print("-" * 62)
    return 0 if r.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
