# Fairy Bell 第三方组件声明

本文件记录 Fairy Bell 当前发布包中使用的主要第三方组件及其许可证。
这些组件仍然适用各自的许可证；本文件不改变其授权条件。

## Python 与打包

| 组件 | 许可证 | 上游 |
| --- | --- | --- |
| Python | PSF License 2.0 | <https://www.python.org/> |
| Tcl/Tk | Tcl/Tk License（BSD 风格） | <https://www.tcl.tk/> |
| PyInstaller | GPL-2.0-or-later，带允许打包非自由程序的特殊例外 | <https://pyinstaller.org/> |

PyInstaller 的打包器许可证带有特殊例外，不要求使用它打包的程序本身采用 GPL。

## OCR、图像与匹配

| 组件 | 许可证 | 上游 |
| --- | --- | --- |
| RapidOCR | Apache-2.0 | <https://github.com/RapidAI/RapidOCR> |
| ONNX Runtime | MIT | <https://github.com/microsoft/onnxruntime> |
| OpenCV | Apache-2.0 | <https://github.com/opencv/opencv> |
| Pillow | MIT-CMU | <https://python-pillow.org/> |
| NumPy / OpenBLAS | BSD-3-Clause | <https://numpy.org/> |
| RapidFuzz | MIT | <https://github.com/rapidfuzz/RapidFuzz> |
| Shapely | BSD-3-Clause | <https://github.com/shapely/shapely> |
| mss | MIT | <https://github.com/BoboTiG/python-mss> |

RapidOCR 附带的 OCR 模型还可能有单独的模型许可证，发布时应保留
`_internal/rapidocr-*.dist-info/licenses/MODEL_LICENSES.md`。

## 网络与其他运行依赖

| 组件 | 许可证 |
| --- | --- |
| requests | Apache-2.0 |
| urllib3 | MIT |
| certifi | MPL-2.0 |
| charset-normalizer | MIT |
| attrs | MIT |
| tqdm | MPL-2.0 AND MIT |

## 内置字体

| 字体 | 许可证 |
| --- | --- |
| 霞鹜文楷 Lite | SIL Open Font License 1.1，含保留字体名称条款 |
| 霞鹜新晰黑 | IPA Font License 1.0 |

字体并非统一使用 OFL：`LXGWNeoXiHei.ttf` 使用 IPA Font License 1.0。
正式发布包必须在 `fonts` 目录或 `LICENSES` 目录随附对应完整授权文本，
并保留字体名称、版权与保留字体名称要求。

## 说明

本文件是组件清单，不是完整许可证汇编。正式公开分发前，应将上述组件所需的
完整许可证文本和版权声明一并放入发布包。
