# 验证码简单对比像素点式跨越法
#
# By Clok Much

import json

from PIL import Image
import ddddocr


def give_me_a_captcha_result(image_name, sub_images_with_desc="./captcha_single/"):
    # 裁剪并比较子图片库中符合图片的，返回4位数字 str 型
    captcha_result_output = []
    captcha_original = Image.open(image_name)
    captcha_original_1 = captcha_original.crop((22 * 0, 0, 22 * 1, 24)).crop((4, 4, 20, 20)).histogram()
    captcha_original_2 = captcha_original.crop((22 * 1, 0, 22 * 2, 24)).crop((4, 4, 20, 20)).histogram()
    captcha_original_3 = captcha_original.crop((22 * 2, 0, 22 * 3, 24)).crop((4, 4, 20, 20)).histogram()
    captcha_original_4 = captcha_original.crop((22 * 3, 0, 22 * 4, 24)).crop((4, 4, 20, 20)).histogram()
    captcha_original_crop_pool = [captcha_original_1, captcha_original_2, captcha_original_3, captcha_original_4]
    with open(sub_images_with_desc + "captcha_desc.json", 'rb') as file_object:
        captcha_desc = json.load(file_object)
        file_object.close()
    for each_original in captcha_original_crop_pool:
        for key, value in captcha_desc.items():
            tmp_image = Image.open(sub_images_with_desc + value[0]).crop((4, 4, 20, 20)).histogram()
            un_comp = []
            for i in range(0, len(tmp_image)):
                if tmp_image[i] == each_original[i]:
                    continue
                else:
                    un_comp.append(i)
            if len(un_comp) <= 2:
                captcha_result_output.append(value[1])
                break
            # print(un_comp)
    captcha_result_output = ''.join(captcha_result_output)
    return captcha_result_output


# print(give_me_a_captcha_result("cbs.bmp"))

def bypass_login_captcha(image_name):
    # 申请后端创建指定验证码，并调用 ddddocr 识别验证码，识别来自文件
    captcha_ocr = ddddocr.DdddOcr(show_ad=False)
    with open("zzjgetimg.gif", "rb") as login_tmp:
        login_bypass_img = login_tmp.read()
    captcha_result = captcha_ocr.classification(login_bypass_img)
    print("login captcha detected.")
    return captcha_result


# print(bypass_login_captcha("zzjgetimg.gif"))

