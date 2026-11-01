# ESP32-C6 表情屏

## 功能

几何表情绘制、动画与 SPI 显示驱动实验。

## 技术栈

MicroPython、SPI、ST7789。依赖版本以现有清单和上游兼容要求为准，早期代码可能需要历史版本。

## 目录

main.py 主程序与驱动；smile_geometry.py 几何；smile_animation.py 动画；esp32c6_st7789_smiley.py 独立实验。

## 启动

在本仓库目录执行；Python 示例需先激活自行创建的虚拟环境。

```sh
# 将 main.py、smile_geometry.py、smile_animation.py 上传到运行 MicroPython 的板卡
# 依据代码核对 SPI 接线，再复位运行 main.py
```

## 公开范围与许可

仅包含脱敏文本源码，不含原 Git 历史、私人绝对路径、凭据、用户数据库/聊天日志、未经逐张审阅的原始图片或二进制媒体。未发布资源不在许可证授权范围内。详见 [LICENSE](LICENSE) 与 [ATTRIBUTION.md](ATTRIBUTION.md)。

维护者有权授权的自有实现代码采用 MIT。第三方依赖、参考实现、团队内容、角色设定与未发布素材不由此重新许可；请同时遵守 ATTRIBUTION.md 所列来源边界。

## 验证与限制

未接硬件验证；屏幕型号、引脚、电源与固件需自行确认。不含固件备份、图片和 3D 模型。

本次执行静态语法/JSON 检查和独立密钥扫描；结果记录在 `VALIDATION.md`。静态通过不代表界面、依赖安装、硬件或端到端运行成功。缺失资源须使用自行创建或获得授权的替代品，不能从原个人素材库自动恢复。
