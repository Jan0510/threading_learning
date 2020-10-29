import serial.tools.list_ports
import threading, time
import serial

# Python中的threading.Event()操控多线程的过程有：
# - 定义事件：man_talk_event = threading.Event()
# - 创建线程，传入对应事件：t1 = threading.Thread(target=man, args=(man_talk_event,), name='man')
# - 查看对应事件的标志：man_talk_event.is_set()返回Ture或False
# - 阻塞对应事件线程：man_talk_event.wait() 如果event.isSet()==False将阻塞进程
# - 继续对应事件线程：man_talk_event.set() 设置event的状态Ture，将所有阻塞池的线程激活，进入就绪状态。等待操作系统调度
# - 结束对应事件线程：man_talk_event.clear() 设置event的状态为False
# - 注意创建线程的时候，如果之前设置成t1.setDaemon(True)，则创建的是守护线程
class SerialThread:
    # 在初始化函数__init__ 之前加入的就是自定义信号的申明,这个声明只能在初始化函数外面
    dataReadoutSignal = pyqtSignal(str) # 输出信号，用于告知调用者，发送和接受情况

    def __init__(self):
        # 构造时不配置串口，打开时才配置
        self.my_serial = serial.Serial()
        self.com_dict = {}  # 存放串口名-串口号

        self.my_serial.port = None       # 串口号
        self.my_serial.baudrate = None   # 波特率
        self.my_serial.bytesize = None   # 数据位
        self.my_serial.stopbits = None   # 停止位
        self.my_serial.parity = None        # 校验位
        self.my_serial.timeout = None     # 超时时间

        self.alive = False              # 串口工作标志，供多个子线程访问
        self.waitEnd = None             # 存放threading.Event()创建的event标志
        fname = time.strftime("%Y%m%d")  # blog名称为当前时间
        self.rfname = 'r' + fname  # 接收blog名称
        self.sfname = 's' + fname  # 发送blog名称
        self.thread_read = None # threading.Thread()
        self.thread_send = None
    # 等待self.waitEnd.set()
    def waiting(self):
        
        if self.waitEnd:            # 
            self.waitEnd.wait()     # event.wait(timeout=None)：调用该方法的线程会被阻塞，如果设置了timeout参数，超时后，线程会停止阻塞继续执行；

    # 在主线程中，开启2个子线程作为串口接收、发送
    def start(self, port, baudrate, bytesize, stopbits, parity, timeout=0):
        self.my_serial.port = port       # 串口号
        self.my_serial.baudrate = baudrate   # 波特率
        self.my_serial.bytesize = bytesize   # 数据位
        self.my_serial.stopbits = stopbits   # 停止位
        self.my_serial.parity = parity        # 校验位
        self.my_serial.timeout = timeout     # 超时时间
        try:
            # 开串口
            # self.rfile = open(self.rfname, 'w')
            # self.sfile = open(self.sfname, 'w')
            self.my_serial.open()
        except Exception as ex:
            print(ex)
        if self.my_serial.isOpen():
            # self.waitEnd = threading.Event() # 事件标志位，2个子线程公用一个
            self.alive = True

            self.thread_read = threading.Thread(target=self.reader)
            # self.thread_read.setDaemon(True)        # setDaemon(True)，则为守护进程

            self.thread_send = threading.Thread(target=self.sender)
            # self.thread_send.setDaemon(True)        # setDaemon(True)，则为守护进程

            self.thread_read.start()
            self.thread_send.start()
            return True
        else:
            return False
    def reader(self):
        while self.alive:
            sleep(0.1) # 睡眠0.1秒
            try:
                if self.data_num > 0 and self.data_num == self.my_serial.inWaiting():
                    data = ''
                    self.data_num = 0
                    data = self.my_serial.read(self.data_num)
                    print('recv' + ' ' + time.strftime("%Y-%m-%d %X") + ' ' + data.strip())
                    print(time.strftime("%Y-%m-%d %X:") + data.strip(), file=self.rfile)
                    # if len(data) == 1 and ord(data[len(data) - 1]) == 113:  # 收到字母q，程序退出
                    #    break
                else:
                    self.data_num = self.my_serial.inWaiting()

                        
            except Exception as ex:
                print(ex)

       # self.waitEnd.set()
       # self.alive = False
    def sender(self, msg = None):
        while self.alive:
            try:
                snddata = input("input data:\n") 
                self.my_serial.write(snddata)
                print('sent' + ' ' + time.strftime("%Y-%m-%d %X"))
                print(snddata, file=self.sfile) # 备份到文件
            except Exception as ex:
                print(ex)

        # self.waitEnd.set() # 线程结束
        # self.alive = False

    # 串口停止
    def stop(self):
        self.alive = False
        # self.thread_read.join() # join方法主要是会阻塞主线程，在子线程结束运行前，主线程会被阻塞等待。
        # self.thread_send.join()
        if self.my_serial.isOpen():
            self.my_serial.close()
        # self.rfile.close()
        # self.sfile.close()
    def modbus_handle(self, str, mode):
        pass

if __name__ == '__main__':

    ser = SerThread()
    try:
        if ser.start():         # 返回true则成功
            ser.waiting()       # 阻塞等待‘q’字符
            ser.stop()          # 释放打开的资源
        else:
            pass
    except Exception as ex:
        print(ex)

    if ser.alive:
        ser.stop()

    print('End OK .')
    del ser
# 使用线程工作
class SerialThread(QtCore.QThread):
    # 输出信号
    dataReadoutSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SerialThread, self).__init__(parent)
        self.m_serialPort = serial.Serial()
        self.receive_buffer = None
        self.receive_buffer_lock = None
        self.send_buffer = None
        self.send_buffer_lock = None
        self.Com_Dict = {}  # 存放串口
    # 串口检测，返回检测到的串口个数
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        port_list = list(serial.tools.list_ports.comports())  # 获取串口列表
        # 调用list()把一个字典转换成一个列表，port_list是个2维数组
        for port in port_list:
            # 1个port包含2个数据,port[0]port[1], port[0]是串口名，port[1]是串口号
            self.Com_Dict["%s" % port[0]] = "%s" % port[1] # key是串口名，value是串口号
            #"%s:%d"%("ab",3) => "ab:3"，%s表示格化式一个对象为字符，%d表示整数。
        return len(self.Com_Dict)

    # 串口信息
    def port_imf(self):
        pass
    # 打开串口
    def port_open(self,portName, baudrate, parity, bytesize, stopbits, timeout):
        self.m_serialPort.port = portName       # 串口号
        self.m_serialPort.baudrate = baudrate   # 波特率
        self.m_serialPort.bytesize = bytesize   # 数据位
        self.m_serialPort.stopbits = stopbits   # 停止位
        self.m_serialPort.parity = parity       # 校验位
        self.m_serialPort.timeout = timeout     # 超时时间
        try:    # 被监控的程序段
            self.m_serialPort.open()
        except: # 若发送异常则执行的程序段
            return "串口不能打开"
        pass

    # 关闭串口
    def port_close(self):
        try:
            self.m_serialPort.close()
        except:
            return "串口不能关闭"
        pass

    # 串口发送
    def data_send(self):
        pass

    # 串口接收
    def data_receive(self):
        pass

    # QThread线程主函数
    def run(self):
        while True:
            time.sleep(2)


