# GUI库
import tkinter as tk
from tkinter import scrolledtext
# 音频库
import pyaudio
import wave
import threading

# 语音识别
from aip import AipSpeech

# 硬件
import Hardware

APP_ID = ' '
API_KEY = ' '
SECRET_KEY = ' '
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

onCmd = "打开电灯"
offCmd = "关闭电灯"

# 修改开启指令的函数
def onChanged():
    str = onEntry.get()
    global onCmd
    onCmd = str
    logText.insert('end', ' 开灯指令已修改为：')
    logText.insert('end', str)
    logText.insert('end', '\n')
    logText.insert('end', '\n')

# 修改关闭指令的函数
def offChanged():
    str = offEntry.get()
    global offCmd
    offCmd = str
    logText.insert('end', ' 关灯指令已修改为：')
    logText.insert('end', str)
    logText.insert('end', '\n')
    logText.insert('end', '\n')

# 恢复默认指令的函数
def backToDefault():
    global onCmd
    onCmd = "打开电灯"
    global offCmd
    offCmd = "关闭电灯"
    logText.insert('end', ' 已恢复默认指令，开灯指令为“打开电灯”，关灯指令为“关闭电灯”\n')
    logText.insert('end', '\n')


# 录音
class VoiceRecorder:
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def __recording(self):
        self._running = True
        logText.insert('end', ' 开始接受指令...\n')
        logText.insert('end', '\n')
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)
 
        stream.stop_stream()
        stream.close()
        p.terminate()

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def stopAndSave(self):
        self._running = False
        p = pyaudio.PyAudio()
        wf = wave.open("cmdOfUser.wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        logText.insert('end', ' 已接受指令\n')
        logText.insert('end', '\n')


# 调用百度语音识别API
def VoiceRecognition(file):
    data = open(file, 'rb').read()
    result = client.asr(data, 'wav', 16000, {'dev_pid':1537})
    return result['result'][0]
    

# 创建录音对象
recorder = VoiceRecorder()

# 按下终止录音按钮时停止录音并保存，之后直接读取音频文件进行语音识别并打开电灯
def Off():
    # 停止录音并保存
    recorder.stopAndSave()
    # 读取音频文件进行语音识别，输出日志
    logText.insert('end', ' 你的指令是：')
    cmd = VoiceRecognition(' ') # 文件目录
    logText.insert('end', cmd)
    logText.insert('end', '\n')
    logText.insert('end', '\n')

    # 打开电灯
    response_code, master = Hardware.ConnectRelay('com3')
    if onCmd in cmd:
        Hardware.Switch(master, "on")
        if response_code > 0:
            logText.insert('end', ' 电灯开启成功！\n')
            logText.insert('end', '\n')
        else:
            logText.insert('end', ' 电灯开启失败，请检查串口连接！\n')
            logText.insert('end', '\n')

    if offCmd in cmd:
        Hardware.Switch(master, "off")
        if response_code > 0:
            logText.insert('end', ' 电灯关闭成功！\n')
            logText.insert('end', '\n')
        else:
            logText.insert('end', ' 电灯关闭失败，请检查串口连接！\n')
            logText.insert('end', '\n')


# 窗口基础设置
window = tk.Tk()
window.title('电灯控制系统')
window.geometry('800x800')
window.config(background="#F0F0F0")
window.iconbitmap('C:/Users/Admin/Desktop/人机交互/期末设计/pic/Epoch.ico')
window.resizable(False, False)

# 录音按钮的图片对象
recordButtonImg = tk.PhotoImage(file=' ')
# 终止录音按钮的图片对象
recordOffButtonImg = tk.PhotoImage(file=' ')
# 退出按钮的图片对象
quitButtonImg = tk.PhotoImage(file=' ')
# 恢复默认按钮的图片对象
defaultButtonImg = tk.PhotoImage(file=' ')

# 状态日志标签
logLabel = tk.Label(window, text="状态日志", width=10, height=1, bg="#F0F0F0")
logLabel.place(x=20, y=250)
# 状态日志列表框
logText = tk.scrolledtext.ScrolledText(window, width=100, height=25, bd=0)
logText.place(x=20, y=280)
# 提示标签
tips = "tips: \n点击录音按钮后开始录音\n点击停止录音按钮后停止录音并执行操作\n点击右上角退出按钮即可退出该程序\n默认开灯指令为“打开电灯”，关灯指令为“关闭电灯”\n点击自定义指令按钮可以输入自己想要的指令\n点击恢复默认指令按钮可以恢复默认指令\n"
tipsMessage = tk.Message(window, text=tips, width=400, bd=0)
tipsMessage.place(x=20, y=620)
# 开启自定义标签
onLabel = tk.Label(window, text="开灯指令", width=10, height=2, bg="#F0F0F0")
onLabel.place(x=400, y=50)
# 关闭自定义标签
offLabel = tk.Label(window, text="关灯指令", width=10, height=2, bg="#F0F0F0")
offLabel.place(x=400, y=100)
# 恢复默认按钮描述标签
defaultLabel = tk.Label(window, text="恢复默认指令", width=10, height=2, bg="#F0F0F0")
defaultLabel.place(x=680, y=130)

# 开启自定义输入框
onEntry = tk.Entry(window, width=20)
onEntry.place(x=470, y=60)
# 关闭自定义输出框
offEntry = tk.Entry(window, width=20)
offEntry.place(x=470, y=110)

# 开启指令修改按钮
onChangedButton = tk.Button(window, text="修改", bd=1,command=onChanged)
onChangedButton.place(x=620, y=60)
# 关闭指令修改按钮
offChangedButton = tk.Button(window, text="修改", bd=1, command=offChanged)
offChangedButton.place(x=620, y=110)
# 恢复默认指令按钮
defaultButton = tk.Button(window, image=defaultButtonImg, bd=0, command=backToDefault)
defaultButton.place(x=690, y=70)
# 关闭按钮
quitButton = tk.Button(window, image=quitButtonImg, bd=0, command=window.quit)
quitButton.place(x=760, y=10)
# 录音按钮
recordButton = tk.Button(window, image=recordButtonImg, bd=0, command=recorder.start)
recordButton.place(x=50, y=50)
# 终止录音按钮
recordOffButton = tk.Button(window, image=recordOffButtonImg, bd=0, command=Off)
recordOffButton.place(x=250, y=50)

# 运行
window.mainloop()
