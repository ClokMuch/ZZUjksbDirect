# ZZUjksbDirect 的错误邮件发送方法集
#
# By Clok Much
import smtplib
from email.mime.text import MIMEText


def report_mail(title="jksb 错误或异常反馈信息",
                details=[],
                config=["somebody@site.site", "here_is_no_password_or_auth_code"],
                receiver="who_will_be_notified@site.site",
                public_mail_config="a_dict_contain_mail_send_config"):
    # 配置邮件内容
    mail_message = MIMEText(str(details), 'plain', 'utf-8')
    mail_message['Subject'] = title
    mail_message['From'] = config[0]
    mail_message['To'] = receiver
    # 尝试发送邮件
    try:
        mail_host = "Zero"
        mail_port = "0"
        this_host = "Zero"
        for each_host in public_mail_config["symbol"]:
            if each_host in config[0]:
                mail_host = public_mail_config[each_host]["host"]
                mail_port = public_mail_config[each_host]["port"]
                this_host = each_host
                break
        if mail_host == "Zero":
            print('发送结果的邮箱设置异常，请在 mail_public_config.json 中检查邮箱的域名配置，以及发信SMTP服务器配置.')
            raise smtplib.SMTPException
        if this_host == "Zero":
            print('发送结果的邮箱设置异常，请确保 mail_public_config.json 中包含您的邮箱配置.')
            raise smtplib.SMTPException
        if "encryption" in public_mail_config[this_host].keys():
            smtp_obj = smtplib.SMTP(mail_host, mail_port)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.ehlo()
            smtp_obj.login(config[0], config[1])
            smtp_obj.sendmail(config[0], receiver, mail_message.as_string())
            smtp_obj.quit()
            print('邮件发送完毕，注意不要泄露邮件内容.')
        else:
            smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
            smtp_obj.login(config[0], config[1])
            smtp_obj.sendmail(config[0], receiver, mail_message.as_string())
            smtp_obj.quit()
            print('邮件发送完毕，注意不要泄露邮件内容.')
    except smtplib.SMTPException:
        print('发送结果的邮箱设置可能异常，请检查邮箱和密码配置，以及发信SMTP服务器配置.')
        raise smtplib.SMTPException
