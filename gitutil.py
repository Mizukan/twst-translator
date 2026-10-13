# -*- coding: utf-8 -*-
"""找一个能用的 git。

这台电脑上不一定有独立安装的 Git（有的机器只用 Codex 自带的那份，
它藏在用户目录的 .cache 里，双击 bat 时 PATH 里没有它），
所以这里按「PATH → Codex 自带的 → 常见安装位置」挨个试，返回可用的那个路径。
"""
import glob
import os
import shutil
import subprocess


def _candidates():
    home = os.path.expanduser("~")
    out = []
    p = shutil.which("git")
    if p:
        out.append(p)
    pats = [
        # Codex 自带的（用通配符，版本目录变了也能找到）
        os.path.join(home, ".cache", "codex-runtimes", "*", "dependencies",
                     "native", "git", "cmd", "git.exe"),
        # 正常安装 Git for Windows 会在这几个地方
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        os.path.join(home, "AppData", "Local", "Programs", "Git", "cmd", "git.exe"),
        r"D:\Program\Git\cmd\git.exe",
        r"D:\Programs\Git\cmd\git.exe",
        r"D:\Program Files\Git\cmd\git.exe",
    ]
    for pat in pats:
        out += glob.glob(pat)
    # 去掉重复，保持顺序
    seen, uniq = set(), []
    for c in out:
        k = c.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq


def find_git():
    """返回一个能跑的 git 路径；一个都找不到就返回空字符串"""
    for c in _candidates():
        try:
            r = subprocess.run([c, "--version"], capture_output=True, text=True,
                               timeout=20)
            if r.returncode == 0:
                return c
        except Exception:
            continue
    return ""


def git_or_explain():
    """给脚本用：返回 git 路径；找不到就打印一段人话并返回空"""
    g = find_git()
    if not g:
        print()
        print("!" * 62)
        print("这台电脑上找不到 git，所以没法上传。")
        print("解决办法：装一个 Git for Windows（免费，一路点下一步就行）：")
        print("   https://git-scm.com/download/win")
        print("装完把「发布.bat」（或第一次设置那个）再双击一次就好。")
        print("!" * 62)
    else:
        print("用这个 git：%s" % g)
    return g
