import requests
import global_maneger
def web_login():

    url = "https://epms.eastech.com/api/login/"
    payload = {'emp_no': "ate",
               'password': "Windows123.."}
    files = []
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=1)

        if response.text.find("token") > 0:
            webapi_token = 'BEABER' + response.json()["token"]
            global_maneger.set_global_value("token", webapi_token)
            return True, response.text
        else:
            return False, response.text
    except Exception as ex:
        print(ex)
        return False, ex
# 上传工单和SN号
def web_post(SN):
    work_order = global_maneger.get_global_value('work_order')
    url = "https://epms.eastech.com/api/sn_detail/"
    payload = {'work_order': str(work_order),
               'sn': str(SN)}
    files = []
    webapi_token = global_maneger.get_global_value("token")
    headers = {'Authorization': webapi_token}
    try:
        # print(url)
        # print(headers)
        # print(payload)
        response = requests.request("POST", url, headers=headers, json=payload, files=files, timeout=1)
        if response.text.find("OK") > 0:
            return True, response.text
        else:
            return False, response.text
    except Exception as ex:
        print(ex)
        return False, ''
# 获取规则、SN范围
def web_get():
    work_order = global_maneger.get_global_value('work_order')
    url = "https://epms.eastech.com/api/sn_detail/" + str(work_order) + '/'
    payload = {}
    files = []
    webapi_token = global_maneger.get_global_value("token")
    headers = {'Authorization': webapi_token}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, files=files, timeout=5)
        if response.text.find("detail") > 0:
            # print(response.text)
            return False, response.text
        else:
            global_maneger.set_global_value("SERIAL_NUMBER", response.json()["SERIAL_NUMBER"])  # 最大SN
            global_maneger.set_global_value("FUNCTION_NAME", response.json()["FUNCTION_NAME"])  # 规则，对应着本地模板
            global_maneger.set_global_value("TARGET_QTY", response.json()["TARGET_QTY"])        # 目标生产量
            global_maneger.set_global_value("SN_QTY", response.json()["SN_QTY"])                # 当前生产量
            global_maneger.set_global_value("PARAME_VALUE", response.json()["PARAME_VALUE"])                # SN模板

            return True, response.text
    except Exception as ex:
        print(ex)
        return False, ''

'''
get的返回值
{
    "SERIAL_NUMBER": null,
    "FUNCTION_NAME": "FSBB100360B03",
    "TARGET_QTY": 1000,
    "SN_QTY": 0,
    "PARAME_VALUE": "EASTECH FSBB10036-0B03 YYWWKSSSSS"
}
'''