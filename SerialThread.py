import serial.tools.list_ports
import threading

import global_maneger
import time
import serial
from PyQt5.QtCore import pyqtSignal, QTimer, QObject


class SerialThread(QObject):        # 需要继承QObject才可以使用QTimer
    # 在初始化函数__init__ 之前加入的就是自定义信号的申明,这个声明只能在初始化函数外面
    dataReadoutSignal = pyqtSignal(int) # 输出信号，用于告知调用者，发送和接受情况
    def __init__(self):
        super(SerialThread, self).__init__()  # 分别调用了2个父类的初始化函数
        # 构造时不配置串口，打开时才配置
        self.my_serial = serial.Serial()
        self.com_dict = {}  # 存放串口名-串口号
        self.send_buffer = []
        self.read_buffer = []
        self.alive = False              # 串口工作标志，供多个子线程访问
        self.thread_serial = None         # threading.Thread()
        self.modbus_reg = [0]*21    # 索引+1对应于modbus寄存器地址
        self.modbus_10resend_timer = QTimer(self)       # 重发定时器
        self.modbus_10resend_timer.timeout.connect(self.modbus_10resend_slot)
        self.modbus_10cmd_timeout = 100                 # ms，没收到10cmd的应答则重发
        self.sender_timer = QTimer(self)                # 主站轮询定时器
        self.sender_timer.timeout.connect(self.sender_management_slot)
        self.sender_timer_timeout = 250                 # 主站固定时间轮询一次


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

    # 在主线程中，开启子线程作为串口接收、发送
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
            self.alive = True
            self.thread_serial = threading.Thread(target=self.thread_loop)
            self.thread_serial.setDaemon(True)        # setDaemon(True)，则为守护进程，主线程结束时，守护线程被强制结束
            self.thread_serial.start()
            return True
        else:
            return False
    def thread_loop(self):
        self.sender_timer.start(100)        # 启动轮询定时器，100ms
        while self.alive:
            self.data_num = self.my_serial.inWaiting()
            time.sleep(0.1)                         # 睡眠0.1秒
            try:
                # 串口空闲原理：一段时间内num不增加，说明出现空闲时间，利用空闲时间分割2个数据帧
                if self.data_num > 0 and self.data_num == self.my_serial.inWaiting():
                    self.read_buffer = self.my_serial.read(self.data_num)
                    self.modbus_Receive_Translate(self.read_buffer, self.data_num)
                    self.data_num = 0
                    print('recv' + ' ' + time.strftime("%Y-%m-%d %X") + ' ' + str(self.read_buffer))
                else:
                    self.data_num = self.my_serial.inWaiting()
            except Exception as ex:
                print(ex)

    # 串口停止
    def stop(self):
        self.alive = False
        self.sender_timer.stop()
        self.thread_serial.join() # join方法主要是会阻塞主线程，在子线程结束运行前，主线程会被阻塞等待。
        if self.my_serial.isOpen():
            self.my_serial.close()
    def modbus_send03cmd(self, start_addr=1, num=3):
        send_buf = bytearray(8)#返回一个长度为 8 的初始化数组
        send_buf[0] = 0x01    #地址
        send_buf[1] = 0x03    #功能码
        send_buf[2] = start_addr // 256  # startaddr
        send_buf[3] = start_addr % 256  #
        send_buf[4] = num // 256  # number
        send_buf[5] = num % 256  #
        crc16 = getcrc16(send_buf, 6)
        send_buf[6] = crc16 // 256
        send_buf[7] = crc16 % 256
        num = self.my_serial.write(send_buf)      # 串口写并返回字节数
    def modbus_send10cmd(self, start_addr=1, num=18):
        send_buf = bytearray(8+num*2)  # 返回一个长度为 * 的初始化数组
        send_buf[0] = 0x01  # 地址
        send_buf[1] = 0x10  # 功能码
        send_buf[2] = start_addr // 256     # startaddr
        send_buf[3] = start_addr % 256      # startaddr
        send_buf[4] = num // 256  # number
        send_buf[5] = num % 256  # number
        for i in range(num):
            send_buf[6+i*2] = int(self.modbus_reg[start_addr+i]) // 256
            send_buf[7+i*2] = int(self.modbus_reg[start_addr+i]) % 256
        crc16 = getcrc16(send_buf, 8+num*2-2)
        send_buf[8+num*2-2] = crc16 // 256
        send_buf[8+num*2-1] = crc16 % 256
        num = self.my_serial.write(send_buf)    # 串口写并返回字节数
        self.modbus_10cmd_wait = True           # 等待应答标志位
        self.modbus_10resend_timer.start(self.modbus_10cmd_timeout)
    def modbus_Receive_Translate(self, data, length):
        # 只当执行到modbus_Receive_Translate函数时才会创建，并作为实例变量一直存在
        data_crc = getcrc16(data, length-2)
        if data[0] == 0x01 and data_crc//256 == data[length-2] and data_crc % 256 == data[length-1]:
            if data[1] == 0x03:         # 03 功能码，读
                self.modbus_03cmd_wait = False
                reg_num = data[2]       # 字节数目
                for i in range(0, reg_num//2):  # 0-99只读，把数据填入modbus_reg队列
                    self.modbus_reg[i] = data[3+i*2]*256 + data[4+i*2]
                # 把modbus_reg数组转移到全局变量中
                self.move_modbus_reg_to_global_value()
            elif data[1] == 0x10:
                # 写命令的应答只要CRC通过就行
                global_maneger.set_global_value('send_to_PLC', False)
                self.modbus_10resend_timer.stop()  # 关闭定时器
                self.modbus_10cmd_wait = False

            # 串口接收到数据，发送信号给外部槽函数，功能码作为传递参数
            self.dataReadoutSignal.emit(data[1])
        else:
            print("CRC_ERROR")
    def sender_management_slot(self):
        # 主站轮询函数，被轮询定时器触发
        if self.alive:
            # 如果轮询周期到，但还在等10cmd的应答，说明cmd10应答超时
            if self.modbus_10cmd_wait:
                self.dataReadoutSignal.emit(0)      # 串口应答超时，发送信号给外部槽函数，0作为传递参数
                self.sender_timer.stop()            # 主站轮询定时器关闭
                self.modbus_10resend_timer.stop()   # 应答定时器关闭
                self.modbus_10cmd_wait = False
                print("cmd10应答超时")
                return
            if global_maneger.get_global_value('send_to_PLC'):
                # 把全局变量转移到modbus_reg数组中
                self.move_global_value_to_modbus_reg()
                self.modbus_send10cmd()
            else:
                self.modbus_send03cmd()
            self.sender_timer.start(self.sender_timer_timeout)  # 再次启动轮询定时器，1ms
    def modbus_10resend_slot(self):
        # 10cmd应答超时，数据重发函数，被应答定时器触发
        if self.modbus_10cmd_wait:
            self.modbus_send10cmd()
    def move_global_value_to_modbus_reg(self):
        # read-write寄存器
        self.modbus_reg[1] = global_maneger.get_global_value('status_print')
        self.modbus_reg[2] = global_maneger.get_global_value('status_recheck')
        self.modbus_reg[3] = global_maneger.get_global_value('cmd_mode')
        # only-write寄存器
        self.modbus_reg[11] = global_maneger.get_global_value('x_1')
        self.modbus_reg[12] = global_maneger.get_global_value('y_1')
        self.modbus_reg[13] = global_maneger.get_global_value('print_res_1')
        self.modbus_reg[14] = global_maneger.get_global_value('x_2')
        self.modbus_reg[15] = global_maneger.get_global_value('y_2')
        self.modbus_reg[16] = global_maneger.get_global_value('print_res_2')
        self.modbus_reg[17] = global_maneger.get_global_value('recheck_res_1')
        self.modbus_reg[18] = global_maneger.get_global_value('recheck_res_2')
    def move_modbus_reg_to_global_value(self):
        # read-write寄存器
        global_maneger.set_global_value('status_print', self.modbus_reg[1])
        global_maneger.set_global_value('status_recheck', self.modbus_reg[2])
        global_maneger.set_global_value('cmd_mode', self.modbus_reg[3])
        # only-write寄存器
        global_maneger.set_global_value('x_1', self.modbus_reg[11])
        global_maneger.set_global_value('y_1', self.modbus_reg[12])
        global_maneger.set_global_value('print_res_1', self.modbus_reg[13])
        global_maneger.set_global_value('x_2', self.modbus_reg[14])
        global_maneger.set_global_value('y_2', self.modbus_reg[15])
        global_maneger.set_global_value('print_res_2', self.modbus_reg[16])
        global_maneger.set_global_value('recheck_res_1', self.modbus_reg[17])
        global_maneger.set_global_value('recheck_res_2', self.modbus_reg[18])

aucCRCLo = [
    0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04, 0xCC,
    0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09, 0x08, 0xC8, 0xD8,
    0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC, 0x14,
    0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3, 0x11, 0xD1, 0xD0, 0x10, 0xF0,
    0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C,
    0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A, 0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28,
    0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4,
    0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26, 0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0,
    0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C,
    0xAC, 0xAD, 0x6D, 0xAF, 0x6F, 0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78,
    0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4,
    0x74, 0x75, 0xB5, 0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50,
    0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C,
    0x5C, 0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
    0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C, 0x44,
    0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80, 0x40,
]

aucCRCHi = [
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
]

def getcrc16(frame, length): #传入要校验的数组名及其长度
    CRCHi = 0xff
    CRCLo = 0xff
    for i in range(0, length):
        i_index = CRCHi ^ (frame[i])
        CRCHi = (CRCLo ^ aucCRCHi[i_index])
        CRCLo = aucCRCLo[i_index]
    return CRCHi*256 + CRCLo    #CRC校验返回值 // CRCHI向左移动，就是逆序计算的代表



