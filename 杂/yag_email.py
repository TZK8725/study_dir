import yagmail

def send_email(subject='text',content=None):
    yag=yagmail.SMTP(user='tzk872579163@live.com',password='LZS...1230',port=587,host='smtp.office365.com',smtp_ssl=False)

    

    yag.send(to='tzk872579163@live.com',subject=subject,contents=content)

yag=yagmail.raw()