# 扭曲仙境 翻译器 · 译文更新源

这个仓库只干一件事：给「扭曲仙境剧情翻译器」提供**译文表更新**。
翻译器启动时会（或点界面上的「译文更新」时）来读 `version.json`，比对本地版本，
只下载**变化的那几张表**。

## 里面有什么

| 文件 | 说明 |
| --- | --- |
| `version.json` | 清单：每张表的版本、大小、sha256、更新日志（翻译器读的就是它） |
| `tm_main.zip` / `tm_event.zip` / `tm_card.zip`  | 译文包，一张表一个 |
| `CHANGELOG.md` | 给人看的更新日志 |
| `publish.py` / `first_setup.py` | 发布脚本 / 第一次设置脚本（分别由同名 bat 调用） |

## 怎么发一版新译文

1. 把新的 csv 放进翻译器的 `data\` 目录（就是平时解包、翻译、替换那套）
2. **双击 `发布.bat`**，按提示写一句「这次更新了什么」，最后输入 `y` 上传。

   > 不熟悉命令行就照 `怎么发布.md` 一步步来（那份是写给零基础看的）。
   > 想用命令行也行，等价于：

```bat
cd /d "G:\make ai great again\twst-translator-data"
python publish.py --note "活动表更新：新增活动「XXX」（1234 句）"
```

   脚本会逐张比对 sha256：**只有变了的才重新打包**，没变的沿用旧包和旧版本号，
   所以客户端不会白下十几 MB。清单和 `CHANGELOG.md` 会一起更新，
   顺便把本机 `data\_version.json` 记成最新。
3. 推上去（`发布.bat` 最后问你要不要上传，选 y 就替你做了）：

```bat
git add -A && git commit -m "译文更新" && git push
```

   （或者给脚本加 `--push`，让它顺手做完）

推上去之后，装了翻译器的人下次打开、或者点「译文更新」，就能看到新内容。

## 翻译器那边怎么对接

翻译器 `config.json` 里的 `update_repo` 填的就是这个仓库（`用户名/仓库名`）。
默认会依次尝试几面镜像：`raw.githubusercontent.com`、`cdn.jsdelivr.net`、
`raw.gitmirror.com`、`ghproxy.net`，哪面通就用哪面。
