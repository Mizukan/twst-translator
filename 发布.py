# -*- coding: utf-8 -*-
"""发布译文更新包（往这个仓库里塞新译文，推上去，装了翻译器的人就能更新到）

用法：
    python 发布.py --note "活动表更新：新增活动「XXX」（1234 句）"
    python 发布.py --note "..." --data "另一个 data 目录"
    python 发布.py --note "..." --push        # 顺手 git add/commit/push

做的事：
  1. 逐张比对新表和旧表的 sha256 —— 只有变了的才重新打包（没变的沿用旧包，
     客户端就不会白下十几 MB）
  2. 生成 / 更新 version.json（翻译器读它来检查更新、显示更新日志）
  3. 把这次的说明追加到 CHANGELOG.md
  4. 顺手把本机 data\\_version.json 记成最新（省得自己检查自己）
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = r"G:\make ai great again\扭曲仙境翻译器\data"
TABLES = ["tm_main.csv", "tm_event.csv", "tm_card.csv", "tm.csv"]
MANIFEST = "version.json"


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_old():
    p = os.path.join(HERE, MANIFEST)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"files": {}, "changelog": []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DEFAULT_DATA, help="放新 csv 的目录")
    ap.add_argument("--note", action="append", default=[],
                    help="这次改了什么（可以给多条）")
    ap.add_argument("--ver", default="", help="版本号，默认用当前时间")
    ap.add_argument("--push", action="store_true", help="顺便 git 提交并推送")
    a = ap.parse_args()

    if not os.path.isdir(a.data):
        print("找不到目录：%s" % a.data)
        return 2

    now = datetime.datetime.now()
    ver = a.ver.strip() or now.strftime("%Y-%m-%d %H:%M")
    old = load_old()
    old_files = old.get("files") or {}

    files, changed = {}, []
    for name in TABLES:
        src = os.path.join(a.data, name)
        if not os.path.exists(src):
            print("跳过（data 里没有）：%s" % name)
            continue
        digest = sha256(src)
        size = os.path.getsize(src)
        prev = old_files.get(name) or {}
        zp = os.path.splitext(name)[0] + ".zip"
        if prev.get("sha256") == digest and os.path.exists(os.path.join(HERE, zp)):
            files[name] = prev                    # 一字没动：沿用旧的包和版本号
            print("没变：%s（%s）" % (name, prev.get("ver")))
            continue
        tmp = os.path.join(HERE, zp + ".tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            z.write(src, name)
        os.replace(tmp, os.path.join(HERE, zp))
        zsize = os.path.getsize(os.path.join(HERE, zp))
        files[name] = {"ver": ver, "size": size, "sha256": digest,
                       "zip": zp, "zipsize": zsize}
        changed.append(name)
        print("已打包：%s -> %s（%.1f MB -> %.1f MB）"
              % (name, zp, size / 1048576, zsize / 1048576))

    if not files:
        print("一张表都没找到，什么都没做")
        return 1

    # 清单里的更新日志（给翻译器显示）
    log = list(old.get("changelog") or [])
    notes = [n.strip() for n in a.note if n.strip()]
    if not notes:
        notes = ["更新了：" + "、".join(changed)] if changed else ["重新发布"]
    for n in reversed(notes):
        log.insert(0, "%s %s" % (now.strftime("%Y-%m-%d"), n))
    log = log[:40]

    manifest = {"format": 1, "updated": now.strftime("%Y-%m-%d"),
                "ver": ver, "changelog": log, "files": files}
    with open(os.path.join(HERE, MANIFEST), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    # 人看的更新日志
    cl = os.path.join(HERE, "CHANGELOG.md")
    head = "# 更新日志\n\n"
    body = ""
    if os.path.exists(cl):
        txt = open(cl, encoding="utf-8").read()
        body = txt.split("\n", 1)[1].lstrip("\n") if "\n" in txt else ""
    for n in reversed(notes):
        body = "## %s\n- %s\n\n" % (now.strftime("%Y-%m-%d"), n) + body
    with open(cl, "w", encoding="utf-8") as f:
        f.write(head + body)

    # 本机也记成最新，免得自己检查自己
    lv = os.path.join(a.data, "_version.json")
    try:
        old_lv = {}
        if os.path.exists(lv):
            old_lv = json.load(open(lv, encoding="utf-8")).get("files") or {}
        old_lv.update({k: v["ver"] for k, v in files.items()})
        json.dump({"files": old_lv}, open(lv, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    except Exception as e:
        print("（本地 _version.json 没写成：%s）" % e)

    print("\n清单已更新：%s  版本 %s" % (MANIFEST, ver))
    print("变动的表：%s" % ("、".join(changed) if changed else "（没有）"))

    if a.push:
        for cmd in (["git", "add", "-A"],
                    ["git", "commit", "-m", "译文更新 %s：%s"
                     % (ver, notes[0])],
                    ["git", "push"]):
            print(">>", " ".join(cmd))
            r = subprocess.run(cmd, cwd=HERE)
            if r.returncode != 0 and cmd[1] != "commit":
                print("这条命令没成功（%d），你自己看一眼" % r.returncode)
    else:
        print("\n接着执行：")
        print('  cd /d "%s"' % HERE)
        print("  git add -A && git commit -m \"译文更新 %s\" && git push" % ver)
    return 0


if __name__ == "__main__":
    sys.exit(main())
