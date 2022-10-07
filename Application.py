# jksbDirect
#
# By Clok Much

# Python 自带库
import sys
import json
from time import sleep

# Python 非自带的/第三方库
from requests_toolbelt import SSLAdapter
import requests
import urllib3

# 自行设计的方法集
import error_mail_report
import captcha_process

# 整个运行周期都要保留或用到的变量
users_delay = 38    # 运行延迟，如果出现登入步骤的验证码可尝试增加此值
# 虚假地载入静态配置
with open("config.json", "rb") as file_object:
    # 载入默认表单
    initial_config = json.load(file_object)
    file_object.close()
with open("mail_public_config.json", "rb") as file_object:
    # 载入邮箱配置列表
    initial_mail_config = json.load(file_object)
    file_object.close()
with open("description.json", "rb") as file_object:
    initial_description = json.load(file_object)
    file_object.close()
header = {"Origin": "https://jksb.v.zzu.edu.cn",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/97.0.4692.71 Safari/537.36",
          "Host": "jksb.v.zzu.edu.cn"
          }

# 开始时接收传入的 Secrets
mail_id = sys.argv[1]
mail_pd = sys.argv[2]
processing_pool = sys.argv[3]
# 禁用不安全链接的警告
urllib3.disable_warnings()
adapter = SSLAdapter('TLSv1')


# mail_id = "x6sfHZ6h4X53hCU6q435thqryqkcqe9x969n@outlook.com"
# mail_pd = "IA6ZM6E5VnkJqIMpq6aCD2I6RnUgeUx"
# processing_pool = "3206500736，v+n@wInuoH@jtdGx，0025，蒙德.蒙德城.第二街道@蒙德.蒙德城，黄大聪明，super_intelligent_yellow@mondstadt.city"
# 以中文逗号（，）分隔，每个用户以中文感叹号（！）分割，因此子项目不得包含中文逗号和中文感叹号


# 始终去除 processing_pool 开头和末尾的中文感叹号
# 不对仅把中文感叹号填入 processing_pool 的情况处理
while processing_pool[0] == "！":
    processing_pool = processing_pool[1:]
while processing_pool[-1] == "！":
    processing_pool = processing_pool[:-2]
user_pool = processing_pool.split("！")
print("当前用户数量为 " + str(len(user_pool)))


# 对分割后用户列表中的每个用户进行处理
now_user = 0    # 标记处理用户的序号
for pop_user in user_pool:
    error_collect_pool = {}  # 用于收集错误信息，尽可能实现用户间信息不交叉
    now_user += 1
    now_form = initial_config.copy()
    error_collect_pool['initialization'] = "succeed for user " + str(now_user)
    this_user = pop_user.split("，")
    # ["3206500736", "v+n@wInuoH@jtdGx", "0025", "蒙德.蒙德城.第二街道@蒙德.蒙德城@188.005789and145.557746", "黄大聪明", "super_intelligent_yellow@mondstadt.city"]
    # 单个用户信息检查
    if len(this_user) < 6:
        print("用户" + str(now_user) + "池配置有误，此用户信息条目数量少于6，需要填写的条目数至少为6，可能是将分割的中文逗号输入为英文逗号，此用户将被跳过.")
        continue
    if len(this_user[2]) != 4:
        print("用户" + str(now_user) + "城市码描述有误，正确的长度应该是4，当前长度为" + str(len(this_user[2])) + '，此用户将被跳过.')
        continue
    now_form["myvs_13a"] = this_user[2][:2]
    now_form["myvs_13b"] = this_user[2]
    if "@" in this_user[3]:
        # 若存在需要修正位置的配置，则解析并准备提交
        tmp = this_user[3].split("@")
        if len(tmp) == 3:
            now_form["myvs_13c"] = tmp[0]
            now_form["memo22"] = tmp[1]
            tmp2 = tmp.split("and")
            now_form["jingdu"] = tmp2[0]
            now_form["weidu"] = tmp2[1]
        elif len(tmp) == 2:
            now_form["myvs_13c"] = tmp[0]
            now_form["memo22"] = tmp[1]
        else:
            error_collect_pool['location_config'] = "the num of @ is not 2 or 3"
            print("位置配置中 @ 符号使用异常，用户" + str(now_user) + "将被跳过.")
    else:
        now_form["myvs_13c"] = this_user[3]

    # 解析条目长度为 7 时的情况（情况包含状态描述或疫苗接种情况任一）
    if len(this_user) == 7:
        if len(this_user[6] == 1):
            now_form['myvs_26'] = this_user[6]
        else:
            for tmp in initial_description["symbols"]:
                if tmp in this_user[6].lower():
                    now_form[initial_description[tmp][0]] = initial_description[tmp][1]
    # 解析条目长度为 8 时的情况（按顺序包含疫苗接种及状态描述）
    if len(this_user) == 8:
        now_form['myvs_26'] = this_user[6]
        for tmp in initial_description["symbols"]:
            if tmp in this_user[7].lower():
                now_form[initial_description[tmp][0]] = initial_description[tmp][1]

    sleep(users_delay)   # 每个用户之间延时，以提高成功率

    # 准备请求数据
    session = requests.session()
    session.keep_alive = False
    # 第一步 获取 token
    error_collect_pool["step_1_calc"] = 0   # 设定第一步的计数器
    header["Referer"] = ":https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0"
    while error_collect_pool["step_1_calc"] < 4:
        error_collect_pool["step_1_calc"] += 1
        try:
            # 接收回应数据
            response = session.post("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login",
                                    data={"uid": this_user[0],
                                          "upw": this_user[1],
                                          "smbtn": "进入健康状况上报平台",
                                          "hh28": "722"},
                                    headers=header,
                                    verify=False)
            if type(response) == requests.models.Response:  # 表示判断回应有效
                response.encoding = "utf-8"
                error_collect_pool["step_1_response"] = response.text.replace(this_user[4], "喵喵喵")
                if "验证码" in error_collect_pool["step_1_response"]:
                    error_collect_pool["login_captcha_detected"] = "login captcha detected, trying to bypass."
                    print('用户' + str(now_user) + "运行时，需要登入验证码，准备尝试识别，建议您在 Action 中合理配置运行时间.")
                    error_collect_pool["login_captcha_calc"] = 0    # 登入验证码计数器
                    # error_collect_pool["login_captcha_result_pool"] = []
                    while error_collect_pool["login_captcha_calc"] <= 3:
                        with open("login_captcha_tmp.bmp", "wb") as login_captcha_tmp_file:
                            login_captcha_byte = session.get(
                                "https://jksb.v.zzu.edu.cn/vls6sss/zzjlogin3d.dll/zzjgetimg?ids=1111",
                                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                       "Chrome/97.0.4692.71 Safari/537.36"},
                                verify=False).content
                            login_captcha_tmp_file.write(login_captcha_byte)
                            login_captcha_tmp_file.close()
                        login_captcha_result = captcha_process.bypass_login_captcha(image_name="login_captcha_tmp.bmp")
                        # error_collect_pool["login_captcha_result_pool"].append(login_captcha_result)
                        if len(login_captcha_result) != 4:
                            print("login captcha bypass failed: wrong length")
                            now_form["ver6"] = login_captcha_result
                            break
                        else:
                            error_collect_pool["login_captcha_state"] = "login captcha bypassed"
                            print("login captcha bypass succeed")
                        if error_collect_pool["login_captcha_calc"] <= 3:
                            error_collect_pool["step_1_calc"] += 1
                            print('用户' + str(now_user) + "突破登入验证码中" + str(error_collect_pool["step_1_calc"]) +
                                  "次失败，将重试本次循环.")
                            continue
                        else:
                            print('用户' + str(now_user) + "突破登入验证码中" + str(error_collect_pool["step_1_calc"])
                                  + "次失败，次数达到预期，终止整体打卡进程，报告失败情况.")
                            error_mail_report.report_mail(title="jksb login verification code",
                                                          details=error_collect_pool,
                                                          config=[mail_id, mail_pd],
                                                          receiver=this_user[5],
                                                          public_mail_config=initial_mail_config)
                            exit(1)
                error_collect_pool["mixed_token"] = response.text[response.text.rfind('ptopid'):
                                                                  response.text.rfind('"}}\r\n</script>')].replace(this_user[4], "喵喵喵")
                if "hidden" in error_collect_pool["mixed_token"]:
                    error_collect_pool["mixed_token"] = error_collect_pool["mixed_token"] +\
                                                        "#####contain unrecognized info, which suggest it's not a right token."
                    print("用户 " + str(now_user) + " token 中含有不应出现的字符，将重新开始本部分循环.")
                    continue
                elif not error_collect_pool["mixed_token"]:
                    print("用户 " + str(now_user) + " token 解析后为空，将重新开始本部分循环.")
                    continue
                else:
                    error_collect_pool["token_ptopid"] = error_collect_pool["mixed_token"][7:
                                                                                           error_collect_pool["mixed_token"].rfind('&sid=')]
                    error_collect_pool["token_sid"] = error_collect_pool["mixed_token"][error_collect_pool["mixed_token"].rfind('&sid=') + 5:]
                    error_collect_pool["step_1_succeed"] = "token_seems_like_be_gained."
                    now_form['ptopid'] = error_collect_pool["token_ptopid"]
                    now_form['sid'] = error_collect_pool["token_sid"]
                    break
            else:
                if error_collect_pool["step_1_calc"] <= 3:
                    print('用户' + str(now_user) + "获取 token 中" + str(error_collect_pool["step_1_calc"])
                          + "次失败，没有response，可能学校服务器故障，或者学号或密码有误，将重试.")
                    continue
                else:
                    print('用户' + str(now_user) + "获取 token 中" + str(error_collect_pool["step_1_calc"]) +
                          "次失败，没有response，可能学校服务器故障，或者学号或密码有误，次数达到预期，终止本用户打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb no response at first",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
        except requests.exceptions.SSLError as tmp:
            error_collect_pool["step_1_SSLError_details"] = str(tmp)
            if error_collect_pool["step_1_calc"] <= 3:
                error_collect_pool["step_1_calc"] += 1
                print('用户' + str(now_user) + "获取 token 中" + str(error_collect_pool["step_1_calc"]) +
                      "次失败，服务器提示SSLError，可能与连接问题有关，将重试本次循环.")
                continue
            else:
                print('用户' + str(now_user) + "获取 token 中" + str(error_collect_pool["step_1_calc"])
                      + "次失败，服务器提示SSLError，次数达到预期，终止本用户打卡，报告失败情况.")
                error_mail_report.report_mail(title="jksb SSLError at first",
                                              details=error_collect_pool,
                                              config=[mail_id, mail_pd],
                                              receiver=this_user[5],
                                              public_mail_config=initial_mail_config)
                break
    # 判断第一步情况，若没有成功则跳过本用户循环进入下一个用户
    try:
        tmp = error_collect_pool["step_1_succeed"]
    except KeyError:
        print("用户" + str(now_user) + "第一步没有成功，本用户循环终止.")
        continue

    # 第二步 提交填报人
    header["Referer"] = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb'
    error_collect_pool["step_2_calc"] = 0  # 设定第二步的计数器
    try:
        del(response)   # 清除上一步 response 避免影响后续判断
    except NameError:
        print(str(now_user) + "第一步没有response，没有回收成功.")
    while error_collect_pool["step_2_calc"] < 4:
        error_collect_pool["step_2_calc"] += 1
        try:
            # 获取 fun18 的值
            tmp = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?ptopid=' + error_collect_pool["token_ptopid"] + \
                  '&sid=' + error_collect_pool["token_sid"] + \
                  '&fun2='
            response = session.get(tmp, headers=header, verify=False)
            if type(response) == requests.models.Response:
                response.encoding = "utf-8"
                error_collect_pool["step_2_fun18_value"] = response.text[response.text.rfind('input type="hidden" name="fun18" value="') +
                                                                         40:response.text.rfind('" /><input type="hidden" name="sid"')].replace(this_user[4], "喵喵喵")
            try:
                del(response)  # 清除上一步 response 避免影响后续判断
            except NameError:
                print(str(now_user) + "获取 fun18 没有response，没有回收成功.")
            response_2 = session.post('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb',
                                    headers=header,
                                    data={'ptopid': error_collect_pool["token_ptopid"],
                                          'sid': error_collect_pool["token_sid"],
                                          'fun18': error_collect_pool["step_2_fun18_value"],
                                          'day6': 'b', 'did': '1', 'men6': 'a'},
                                    verify=False)
            if type(response_2) == requests.models.Response:
                response_2.encoding = "utf-8"
                error_collect_pool["step_2_output"] = response_2.text.replace(this_user[4], "喵喵喵")
                if "监测指标" in error_collect_pool["step_2_output"]:
                    error_collect_pool["step_2_succeed"] = "step_2: a from seemed to be gained."
                    # 获取 fun118 值
                    error_collect_pool["step_2_fun118_value"] = error_collect_pool["step_2_output"][error_collect_pool["step_2_output"].rfind('input type="hidden" name="fun118" value="') + 40:
                                                                                                    error_collect_pool["step_2_output"].rfind('" /><input type="hidden" name="fun3"')]
                    now_form["fun118"] = error_collect_pool["step_2_fun118_value"]
                    # 识别验证码并存入表单待提交（如果需要验证码）
                    if "myvs_94c" in error_collect_pool["step_2_output"]:
                        print("captcha found.")
                        error_collect_pool["step_2_captcha_get_img_calc"] = 0   # 获取验证码计数器
                        while error_collect_pool["step_2_captcha_get_img_calc"] < 4:
                            error_collect_pool["step_2_captcha_get_img_calc"] += 0
                            try:
                                with open("captcha_tmp.bmp", 'wb') as captcha_tmp_file:
                                    captcha_byte = session.get("https://jksb.v.zzu.edu.cn/vls6sss/zzjlogin3d.dll/getonemencode?p2p="
                                                               + error_collect_pool["token_ptopid"],
                                                               headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                                      "Chrome/97.0.4692.71 Safari/537.36"},
                                                               verify=False).content
                                    captcha_tmp_file.write(captcha_byte)
                                    captcha_tmp_file.close()
                                error_collect_pool["step_2_captcha_get_succeed"] = "captcha got"
                                break
                            except requests.exceptions.SSLError as tmp:
                                error_collect_pool["step_2_get_captcha_img_ssl_detailed"] = str(tmp)
                                continue
                        try:
                            tmp = error_collect_pool["step_2_captcha_get_succeed"]
                        except KeyError:
                            print("用户" + str(now_user) + "获取验证码图片失败，本用户循环终止.")
                            print(str(now_user) + "captcha_image_get_failed_due_to_SSL_error")
                            error_mail_report.report_mail(title="jksb SSLError at get captcha image",
                                                          details=error_collect_pool,
                                                          config=[mail_id, mail_pd],
                                                          receiver=this_user[5],
                                                          public_mail_config=initial_mail_config)
                            break
                        captcha_tmp = captcha_process.give_me_a_captcha_result("captcha_tmp.bmp")
                        error_collect_pool["step_2_captcha_code_or_result"] = captcha_tmp
                        now_form["myvs_94c"] = captcha_tmp
                    else:
                        error_collect_pool["step_2_captcha_get_succeed"] = "no captcha found in the form."
                        print("no captcha now.")
                        del now_form["myvs_94c"]
                    break
                elif "无权" in error_collect_pool["step_2_output"]:
                    print('用户' + str(now_user) + "提交填报人失败，可能是学号或密码有误，"
                                                   "或是间隔过短致需要验证码，终止用户" +
                          str(now_user) + "打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb step 2 failed due to no authority",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
                else:
                    print('用户' + str(now_user) + "提交填报人失败，返回内容在 else ，终止此用户打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb step 2 failed due to unknown error",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
            else:
                if error_collect_pool["step_2_calc"] <= 3:
                    print('用户' + str(now_user) + "提交填报人" + str(error_collect_pool["step_2_calc"])
                          + "次失败，没有response，可能学校服务器故障，或者学号或密码有误，将重试.")
                    continue
                else:
                    print('用户' + str(now_user) + "获取 token 中" + str(error_collect_pool["step_2_calc"]) +
                          "次失败，没有response，可能学校服务器故障，或者学号或密码有误，次数达到预期，终止本用户打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb no response at second",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
        except requests.exceptions.SSLError as tmp:
            if error_collect_pool["step_2_calc"] <= 3:
                print('用户' + str(now_user) + "提交填报人失败，服务器提示SSLError，可能与连接问题有关.")
                continue
            else:
                print('用户' + str(now_user) + "提交填报人失败，服务器提示SSLError，次数达到预期，终止用户"
                      + str(now_user) + "本次打卡，报告失败情况.")
                error_mail_report.report_mail(title="jksb SSLError at second",
                                              details=error_collect_pool,
                                              config=[mail_id, mail_pd],
                                              receiver=this_user[5],
                                              public_mail_config=initial_mail_config)
                break

    # 判断第二步情况，若没有成功则跳过本用户循环进入下一个用户
    try:
        tmp = error_collect_pool["step_2_captcha_get_succeed"]  # 验证码获取是关键
    except KeyError:
        print("用户" + str(now_user) + "第二步没有成功，本用户循环终止.")
        continue

    # 第三步 提交表格并分析结果
    try:
        del response_2  # 清除上一步 response 避免影响后续判断
    except NameError:
        print(str(now_user) + "第二步没有response，没有回收成功.")
    error_collect_pool["step_3_calc"] = 0  # 设定第三步的计数器
    while error_collect_pool["step_3_calc"] < 4:
        error_collect_pool["step_3_calc"] += 1
        try:
            response = session.post('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb', headers=header,
                                    data=now_form,
                                    verify=False)
            if type(response) == requests.models.Response:
                response.encoding = "utf-8"
                error_collect_pool["step_3_output"] = response.text.replace(this_user[4], "喵喵喵")
                if ("感谢你今日上报" in error_collect_pool["step_3_output"]) or ("感谢您今日上报" in error_collect_pool["step_3_output"]):
                    error_collect_pool["step_3_succeed"] = "seems like all jksb succeed"
                    print("用户" + str(now_user) + "进程成功完成.")
                    break
                elif "四个大写" in error_collect_pool["step_3_output"]:
                    print('用户' + str(now_user) + "提交表格中提示验证码异常，可能识别有误，可能验证码有更新，终止用户打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb testify the fail of captcha bypass",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
                elif "重新登录" in error_collect_pool["step_3_output"]:
                    print('用户' + str(
                        now_user) + "提交表格中提示重新登录，可能运行周期内有异地登录或 token 回收，终止用户本次打卡，报告失败情况.")
                    error_mail_report.report_mail(title="jksb testify the fail of re-login request",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
                else:
                    print('用户' + str(now_user) +
                          "提交表格未通过审判，可能打卡平台增加了新内容，或是今日打卡结果已被审核而不能再修改，"
                          "请检查返回邮件信息（第三步回应内容不包含成功提示）.")
                    error_mail_report.report_mail(title="jksb testify the fail of submit final form due to unknown error",
                                                  details=error_collect_pool,
                                                  config=[mail_id, mail_pd],
                                                  receiver=this_user[5],
                                                  public_mail_config=initial_mail_config)
                    break
            else:
                if error_collect_pool["step_3_calc"] <= 3:
                    print('用户' + str(now_user) + "提交表格没有response，可能学校服务器故障，将重试.")
                    continue
                else:
                    print('用户' + str(now_user) + "提交表格没有response，可能学校服务器故障，次数达到预期，终止本用户打卡，报告失败情况.")
                    error_mail_report.report_mail(
                        title="jksb no response at the final phase",
                        details=error_collect_pool,
                        config=[mail_id, mail_pd],
                        receiver=this_user[5],
                        public_mail_config=initial_mail_config)
                    break
        except requests.exceptions.SSLError as tmp:
            if error_collect_pool["step_3_calc"] <= 3:
                error_collect_pool["step_3_ssl_error_detail"] = str(tmp)
                print('用户' + str(now_user) + "提交表格，服务器提示SSLError，可能与连接问题有关，将重试.")
                continue
            else:
                print('用户' + str(now_user) + "提交表格，服务器提示SSLError，次数达到预期，终止本用户打卡，报告失败情况.")
                error_mail_report.report_mail(title="jksb SSLError at the final phase",
                                              details=error_collect_pool,
                                              config=[mail_id, mail_pd],
                                              receiver=this_user[5],
                                              public_mail_config=initial_mail_config)
                break
    # 清除 session 以玄学提高成功率
    try:
        del session
    except NameError:
        print('用户' + str(now_user) + "不存在但被请求回收/消除，但回收/消除请求已被忽略.")

    # 总会发送邮件便于调试
    # error_mail_report.report_mail(title="jksb: send a mail for details for progress",
    #                               details=error_collect_pool,
    #                               config=[mail_id, mail_pd],
    #                               receiver=this_user[5],
    #                               public_mail_config=initial_mail_config)
