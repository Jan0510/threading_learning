from datetime import datetime
from queue import Queue

import serial.tools.list_ports
import threading

import global_maneger
import time
import serial
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
# # 开机时
# P_A1 = 101  # R?=0x523f
# C_A1 = 109  # RD=0x5244
# # 打印时
# P_B1 = 110  # LS=0x4c53
# C_B1 = 111  # LF=0x4c46
# C_B2 = 112
# C_B3 = 113
# C_B4 = 114
# C_B5 = 115
# # 下料前检查
# P_C1 = 100
# C_C1 = 99
# C_C2 = 102
# C_C3 = 103
# # 下料完成
# P_D1 = 104
# P_D2 = 105
# P_D3 = 106  # 5045
# C_D1 = 107  # 5047
# 开机时
P_A1 = 160  # R?=0x523f
C_A1 = 161  # RD=0x5244
# 打印时
P_B1 = 159  # LS=0x4c53
C_B1 = 163
C_B2 = 164
C_B3 = 165
C_B4 = 166
C_B5 = 162  # LF=0x4c46
# 下料前检查
P_C1 = 158
C_C1 = 169
C_C2 = 170
C_C3 = 168  # 0x4446
# 下料完成
P_D1 = 157
P_D2 = 156
P_D3 = 155  # 0x5045
C_D1 = 167  # 0x5047
class SerialThread(QObject):        # 需要继承QObject才可以使用QTimer
    # 在初始化函数__init__ 之前加入的就是自定义信号的申明,这个声明只能在初始化函数外面
    dataReadoutSignal = pyqtSignal(int) # 输出信号，用于告知连接状态
    def __init__(self):
        super(SerialThread, self).__init__()  # 分别调用了2个父类的初始化函数
        # 构造时不配置串口，打开时才配置
        self.my_serial = serial.Serial()
        self.scan_portbuffer_timer = QTimer()  # 串口缓冲区扫描定时器
        self.scan_portbuffer_timer.setSingleShot(False)  # singleShot=False
        self.scan_portbuffer_timer.timeout.connect(self.scan_portbuffer_slot)
        self.com_dict = {}  # 存放串口名-串口号
        self.prepare_buffer = Queue()
        self.send_buffer = []
        self.read_buffer = []
        self.data_num = 0
        self.alive = False              # 串口工作标志，供多个子线程访问
        self.modbus_resend_timer = QTimer()  # 重发定时器
        self.modbus_resend_timer.timeout.connect(self.modbus_resend_slot)
        self.if_alive_timer = QTimer()  # 检查连接是否存活
        self.if_alive_timer.setSingleShot(False)  # singleShot=False
        self.if_alive_timer.timeout.connect(self.connection_break_slot)
        self.poll_timer = QTimer()  # 主站轮询定时器
        self.poll_timer.setSingleShot(False)  # singleShot=False
        self.poll_timer.timeout.connect(self.sender_poll_slot)
        self.modbus_10cmd_wait = False
        self.modbus_06cmd_wait = False
        self.modbus_03cmd_wait = False
        self.if_connected = False
        # 只负责串口接收和发送,daemon=True，则为守护进程，主线程结束时，守护线程被强制结束
        self.serial_receiever_thread = threading.Thread(target=self.serial_receiever_thread_loop, daemon=True)

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
    def start(self, port, baudrate=9600, bytesize=8, stopbits=1, parity='N', timeout=0):
        self.cnt_03_send = 0
        self.cnt_03_receieve = 0
        self.modbus_reg = [0]*200            # 索引+1对应于modbus寄存器地址
        self.modbus_reg_last_value = [0]*200 # 保存旧值，用于计算上升沿
        self.my_serial.port = port       # 串口号
        self.my_serial.baudrate = baudrate   # 波特率
        self.my_serial.bytesize = bytesize   # 数据位
        self.my_serial.stopbits = stopbits   # 停止位
        self.my_serial.parity = parity        # 校验位
        self.my_serial.timeout = timeout     # 超时时间
        try:
            # 开串口
            self.modbus_10cmd_wait = False
            self.modbus_06cmd_wait = False
            self.modbus_03cmd_wait = False
            self.if_connected = False
            if not self.my_serial.isOpen():
                self.alive = True
                self.my_serial.open()
                # scanbuffer的触发标志
                self.scan_portbuffer_timer.start(10)
                self.scan_scan_portbuffer_timeout = False
                # 开poll定时器
                self.poll_timer.start(100)  # 启动发送轮询定时器
                # 开if_alive定时器
                self.if_alive_timer.start(3000)
                # 开resend定时器
                # 开子线程
                if not self.serial_receiever_thread.is_alive():
                    self.serial_receiever_thread = self.serial_receiever_thread = threading.Thread(target=self.serial_receiever_thread_loop,
                                                                    daemon=True)
                    self.serial_receiever_thread.start()
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
    # 串口接收子线程，循环查询接收缓冲区
    def serial_receiever_thread_loop(self):
        while self.alive:
            if self.scan_scan_portbuffer_timeout:
                self.scan_scan_portbuffer_timeout = False
                self.data_num = self.my_serial.inWaiting()
                # time.sleep(0.02)                         # 间隔0.01秒检查一次接收缓冲区
                try:
                    # 串口空闲原理：一段时间内num不增加，说明出现空闲时间，利用空闲时间分割2个数据帧
                    if self.data_num > 0 and self.data_num == self.my_serial.inWaiting():
                        self.read_buffer = self.my_serial.read(self.data_num)
                        self.modbus_Receive_Translate(self.read_buffer, self.data_num)
                        print("串口接收" + str(self.data_num) + "个字节")
                        l = [hex(int(i)) for i in self.read_buffer]
                        print(" ".join(l))
                        self.data_num = 0
                    else:
                        self.data_num = self.my_serial.inWaiting()
                except Exception as ex:
                    print(ex)
    def scan_portbuffer_slot(self):
        self.scan_scan_portbuffer_timeout = True
    # 串口停止
    def stop(self):
        try:
            self.alive = False
            self.modbus_03cmd_wait = False
            self.modbus_06cmd_wait = False
            self.modbus_10cmd_wait = False
            self.if_connected = False
            self.if_alive_timer.stop()
            self.modbus_resend_timer.stop()
            self.poll_timer.stop()
            self.scan_portbuffer_timer.stop()
            self.serial_receiever_thread.join() # join方法主要是会阻塞主线程，在子线程结束运行前，主线程会被阻塞等待。
            # 如果不加join等待子线程关闭，那么会出现错误：ClearCommError failed (OSError(9, '句柄无效。', None, 6))
            # 该引起该错误的原因是，主线程突然关闭串口，但是子线程正在使用串口，就会报错。
            if self.my_serial.isOpen():
                self.my_serial.close()
            return True
        except Exception as ex:
            print(ex)
            return False
    def modbus_Receive_Translate(self, data, length, start_addr = 150):
        # 只当执行到modbus_Receive_Translate函数时才会创建，并作为实例变量一直存在
        data_crc = data[length-2]*256+data[length-1]
        if data[0] == 0x01 and data_crc == getcrc16(data, length-2):
            if data[1] == 0x03:         # 03 功能码，读
                self.modbus_03cmd_wait = False
                reg_num = data[2]       # 字节数目
                for i in range(0, reg_num//2):  # 把数据填入modbus_reg队列
                    self.modbus_reg[start_addr+i] = data[3+i*2]*256 + data[4+i*2]
                # 把modbus_reg数组转移到全局变量中
                self.move_modbus_reg_to_global_value()
                self.cnt_03_receieve += 1
                # print("cnt_03_send = " + str(self.cnt_03_send))
                # print("cnt_03_receieve = " + str(self.cnt_03_receieve))
            elif data[1] == 0x06:
                # 写命令的应答只要CRC通过就行
                self.modbus_resend_timer.stop()  # 关闭定时器
                self.modbus_06cmd_wait = False
                print("收到06")
            elif data[1] == 0x10:
                # 写命令的应答只要CRC通过就行
                self.modbus_resend_timer.stop()  # 关闭定时器
                self.modbus_10cmd_wait = False
                print("收到10")
            # 串口接收到数据，发送信号给外部槽函数，功能码作为传递参数
            self.dataReadoutSignal.emit(data[1])
            self.if_connected = True
        else:
            print("CRC_ERROR")
    def modbus_send03cmd(self, start_addr=150, num=30):
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
        self.modbus_03cmd_wait = True  # 等待应答标志位
    def modbus_06cmd_format(self, start_addr, reg_value):
        send_buf = bytearray(8)  # 返回一个长度为 8 的初始化数组
        send_buf[0] = 0x01  # 地址
        send_buf[1] = 0x06  # 功能码
        send_buf[2] = start_addr // 256  # startaddr
        send_buf[3] = start_addr % 256  # startaddr
        send_buf[4] = reg_value // 256  #
        send_buf[5] = reg_value % 256  #
        crc16 = getcrc16(send_buf, 6)
        send_buf[6] = crc16 // 256
        send_buf[7] = crc16 % 256
        return send_buf
    def modbus_10cmd_format(self, num, start_addr, reg_value):
        send_buf = bytearray(8+num*2)  # 返回一个长度为 * 的初始化数组
        send_buf[0] = 0x01  # 地址
        send_buf[1] = 0x10  # 功能码
        send_buf[2] = start_addr // 256     # startaddr
        send_buf[3] = start_addr % 256      # startaddr
        send_buf[4] = num // 256  # number
        send_buf[5] = num % 256  # number
        for i in range(num):
            send_buf[6+i*2] = int(reg_value[i]) // 256
            send_buf[7+i*2] = int(reg_value[i]) % 256
        crc16 = getcrc16(send_buf, 8+num*2-2)
        send_buf[8+num*2-2] = crc16 // 256
        send_buf[8+num*2-1] = crc16 % 256
        return send_buf
    def sender_poll_slot(self):
        # 主站轮询函数，被轮询定时器触发
        try:
            if self.alive:
                if self.modbus_06cmd_wait or self.modbus_10cmd_wait:
                    # if self.modbus_03cmd_wait:
                    #     print("在等待03回复，不发送数据")
                    if self.modbus_06cmd_wait:
                        print("在等待06回复，不发送数据")
                    if self.modbus_10cmd_wait:
                        print("在等待10回复，不发送数据")
                    return  # 若还在等待回复，则不发送。返回的数据帧可能会撞车。
                # 检查是否有需要发送的数据放在缓冲区
                if not self.prepare_buffer.empty():
                    self.send_buffer = self.prepare_buffer.get()        # get后队列的第一组数据就消失了
                    if self.send_buffer[1] == 0x06:
                        num = self.my_serial.write(self.send_buffer)  # 串口写并返回字节数
                        self.modbus_resend_timer.start(200)
                        self.modbus_06cmd_wait = True  # 等待应答标志位
                        print("发送06报文")
                    elif self.send_buffer[1] == 0x10:
                        num = self.my_serial.write(self.send_buffer)  # 串口写并返回字节数
                        self.modbus_resend_timer.start(200)
                        self.modbus_10cmd_wait = True  # 等待应答标志位
                        print("发送10报文")
                    else:
                        print("发送功能码异常")
                        return
                else:
                    self.cnt_03_send += 1
                    self.modbus_send03cmd()
                    # print("发送03报文")
                # sender_threading = threading.Thread(target=self.modbus_send03cmd, daemon=True)
                # sender_threading.start()
        except Exception as ex:
            print(ex)
    def modbus_resend_slot(self):
        # 应答超时，数据重发函数，需要重发的内容还存在send_buffer
        if self.modbus_06cmd_wait == True:
            num = self.my_serial.write(self.send_buffer)  # 串口写并返回字节数
            print("重发06")
            self.modbus_resend_timer.start(200)
        elif self.modbus_10cmd_wait == True:
            num = self.my_serial.write(self.send_buffer)  # 串口写并返回字节数
            print("重发10")
            self.modbus_resend_timer.start(200)
    def move_modbus_reg_to_global_value(self):
        # 1 开机阶段
        if self.modbus_reg[P_A1] == 0x523f:
            if self.modbus_reg_last_value[P_A1] != self.modbus_reg[P_A1]:
                print('收到R?上升沿')
                if global_maneger.get_global_value('Computer_ready'):
                    # 2个子线程步骤号初始化+变量初始化+队列缓冲区初始化
                    global_maneger.set_global_value('P_print_cmd', 0)
                    global_maneger.set_global_value('P_recheck_cmd', 0)
                    global_maneger.set_global_value('queue_SN_1', Queue())
                    global_maneger.set_global_value('queue_SN_2', Queue())
                    global_maneger.set_global_value('P_print_first_flag', True)
                    print('发送RD')
                    self.serial_api_sender_stage(1, C_A1, 0x5244)
                else:
                    print('没有ready，不发送')
                    # 在没有ready时，为了保留上升沿所以写0，下次读到时依旧会被判断成上升沿
                    self.modbus_reg[P_A1] = 0
        # 2 打印-检查阶段
        if self.modbus_reg[P_B1] == 0x4c53:
            if self.modbus_reg_last_value[P_B1] != self.modbus_reg[P_B1]:
                print('收到LS上升沿')
                global_maneger.set_global_value('P_print_cmd', 1)
                # if global_maneger.get_global_value('P_print_first_flag'):
                #     global_maneger.set_global_value('P_print_first_flag', False)
                #     global_maneger.set_global_value('P_print_cmd', 50)
                # else:
                #     global_maneger.set_global_value('P_print_cmd', 1)
        # 3 下料-检查阶段
        if self.modbus_reg[P_C1] == 0x4453:
            if self.modbus_reg_last_value[P_C1] != self.modbus_reg[P_C1]:
                print('收到DS上升沿')
                global_maneger.set_global_value('P_recheck_cmd', 1)
        # 4 下料-完成阶段
        if self.modbus_reg[P_D3] == 0x5045:
            if self.modbus_reg_last_value[P_D3] != self.modbus_reg[P_D3]:
                print('收到PE上升沿')
                global_maneger.set_global_value('P_recheck_cmd', 30)
                global_maneger.set_global_value('product_1', self.modbus_reg[P_D1])
                global_maneger.set_global_value('product_2', self.modbus_reg[P_D2])
        for i in range(len(self.modbus_reg)):
            self.modbus_reg_last_value[i] = self.modbus_reg[i]
    def connection_break_slot(self):
        if not self.if_connected:
            print("检查串口连接超时，已断开")
            self.stop()
            self.dataReadoutSignal.emit(0xff)
        else:
            self.if_connected = False
    # 供外部函数调用，将数据打包进发送缓冲队列
    def serial_api_sender_stage(self, reg_num, addr, value):
        self.modbus_03cmd_wait = False
        if reg_num == 1:
            buff = self.modbus_06cmd_format(addr, value)
        else:
            buff = self.modbus_10cmd_format(reg_num, addr, value)
        self.prepare_buffer.put(buff)
auchCRCLo = [
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
    0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80, 0x40
]

auchCRCHi = [
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
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40
]

def getcrc16(frame, length): #传入要校验的数组名及其长度
    uchCRCHi = 0xff
    uchCRCLo = 0xff

    for i in range(0, length):
        uIndex = uchCRCHi ^ frame[i]
        uchCRCHi = uchCRCLo ^ auchCRCHi[uIndex]
        uchCRCLo = auchCRCLo[uIndex]
    return uchCRCHi*256 + uchCRCLo    #CRC校验返回值 // CRCHI向左移动，就是逆序计算的代表

if __name__ == '__main__':
    try:
        ywd = datetime.now().isocalendar()  # (2020, 45, 7)tuple(年，周，日)
        print(ywd)
        print(time.time())
    except Exception as ex:
        print(ex)

