import serial.tools.list_ports
import threading
import time
import serial
from PyQt5.QtCore import pyqtSignal

class SerialThread:
    # 在初始化函数__init__ 之前加入的就是自定义信号的申明,这个声明只能在初始化函数外面
    dataReadoutSignal = pyqtSignal(dict) # 输出信号，用于告知调用者，发送和接受情况

    def __init__(self):
        # 构造时不配置串口，打开时才配置

        self.my_serial = serial.Serial()
        self.com_dict = {}  # 存放串口名-串口号
        self.send_buffer = []
        self.send_flag = False
        self.read_buffer = []
        self.read_flag = False
        self.alive = False              # 串口工作标志，供多个子线程访问
        self.waitEnd = None             # 存放threading.Event()创建的event标志
        self.thread_read = None # threading.Thread()
        self.thread_send = None


    # 串口检测
    def scan(self):
        # 检测所有存在的串口，将信息存储在字典中，然后返回字典
        self.com_dict = {}
        # 获取串口列表，调用list把一个字典转换成一个列表，port_list是个2维数组。
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            # 把port_list里的每个对象转换成字典键值对，port[0]是COM0，port[1]是COM1对应的信息
            self.com_dict["%s" % port[0]] = "%s" % port[1]
            # "%s:%d"%("ab",3) => "ab:3"，%s表示格化式一个对象为字符串，%d表示整数。
        return self.com_dict

    # 在主线程中，开启2个子线程作为串口接收、发送
    def start(self, port, baudrate=115200, bytesize=8, stopbits=1, parity='N', timeout=0):

        self.my_serial.port = port       # 串口号
        self.my_serial.baudrate = baudrate   # 波特率
        self.my_serial.bytesize = bytesize   # 数据位
        self.my_serial.stopbits = stopbits   # 停止位
        self.my_serial.parity = parity        # 校验位
        self.my_serial.timeout = timeout     # 超时时间
        try:
            # 开串口
            self.my_serial.open()
        except Exception as ex:
            print(ex)
        if self.my_serial.isOpen():
            # self.waitEnd = threading.Event() # 事件标志位，2个子线程公用一个
            self.alive = True

            self.thread_read = threading.Thread(target=self.reader)
            self.thread_read.setDaemon(True)        # setDaemon(True)，则为守护进程
            self.thread_send = threading.Thread(target=self.sender)
            self.thread_send.setDaemon(True)        # setDaemon(True)，则为守护进程

            self.thread_read.start()
            self.thread_send.start()
            return True
        else:
            return False
    def reader(self):
        while self.alive:

            self.data_num = self.my_serial.inWaiting()
            time.sleep(0.1)                         # 睡眠0.1秒
            try:
                if self.data_num > 0 and self.data_num == self.my_serial.inWaiting():
                    self.read_buffer = self.my_serial.read(self.data_num)
                    print('recv' + ' ' + time.strftime("%Y-%m-%d %X") + ' ' + str(self.read_buffer))
                    self.data_num = 0
                    self.read_flag = True
                    # 将数据返回
                    self.send_buffer = self.read_buffer
                    self.send_flag = True
                else:
                    self.data_num = self.my_serial.inWaiting()
                        
            except Exception as ex:
                print(ex)
       # self.waitEnd.set()
       # self.alive = False
    def sender(self):
        while self.alive:
            if self.send_flag:
                try:
                    self.my_serial.write(self.send_buffer)
                    print('sent' + ' ' + time.strftime("%Y-%m-%d %X"))
                    self.send_buffer = ""
                    self.send_flag = False
                except Exception as ex:
                    print(ex)


        # self.waitEnd.set() # 线程结束
        # self.alive = False

    # 串口停止
    def stop(self):
        self.alive = False
        self.thread_read.join() # join方法主要是会阻塞主线程，在子线程结束运行前，主线程会被阻塞等待。
        self.thread_send.join()
        if self.my_serial.isOpen():
            self.my_serial.close()

    def modbus_read(self):
        mode = self.read_buffer[1]
        if mode == 6:
            pass
        if mode == 3:
            pass
    def modbus_send(self, addr, data, mode):
        self.send_buffer[1] = mode
        if mode == 3:
            pass
        if mode == 6:
            pass




