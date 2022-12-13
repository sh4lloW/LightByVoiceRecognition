# 基于声控的电灯控制系统

使用方式为：

1. 以管理员身份运行上位机控制器，选择端口，连接模块

2. 命令行运行LightGUI脚本
```cmd
python LightGUI.py
```

项目目录树如下：
```
LightByVoiceRecognition
│  │  C2S03_Utility_Release.exe # 上位机控制器
│  │  cmdOfUser.wav             # 保存录音的音频文件
│  │  Hardware.py               # 连接硬件的脚本
│  │  LightGUI.py               # GUI和其他函数的脚本
│  │
│  ├─pic                        # GUI中的图片
│  │      Epoch.ico
│  │      logout.png
│  │      undo.png
│  │      voice-off.png
│  │      voice.png
│  │
│  └─__pycache__                # 缓存
│          Hardware.cpython-38.pyc
```
