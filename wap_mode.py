import network

import time

import socket

import ssd1306

from machine import I2C, Pin




#Burada ekranımızı tanımlıyoruz.

i2c = I2C(0, sda=Pin(20), scl=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


#Burası Wireless Access Point'e bağlandığımızda tarayıcımızda  http://192.168.4.1 adresine gittiğimizde göreceğimiz html sayfasıdır.
#Burası siz kendiniz istediğiniz gibi yapılandırabilirsiniz.
def web_page():

    html = """<html>

                <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>

                <body><h1>Welcome to Pico WAP Services</h1></body>

              </html>

           """

    return html

# Ağı göremiyorsanız, gücü kapatıp açmanız gerekebilir.
# Gücü 10 saniyeliğine kesin ve tekrar verin.

def ap_mode(ssid, password):

    """

        Bu Kablosuz Giriş Noktası(Wireless Access Point(WAP)), modunu

        etkinleştirmeye yönelik bir işlevdir.

        İki adet parametre alır.
        
        ssid[str]: İnternet noktanızın adı.
        password[str]: İnternet noktanızın şifresi


    """

    # Sadece internet bağlantımızı yapıyoruz

    ap = network.WLAN(network.AP_IF)

    ap.config(essid=ssid, password=password)

    ap.active(True)

    

    while ap.active() == False:

        pass

    global ip

    ip = ap.ifconfig()[0]

    

    display.text("WAP Mode ON",20,0)

    display.text("IP:"+ip,0,8)

    

    display.show()

    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Soket nesnesi oluşturma

    s.bind(('', 80))

    s.listen(5)

    

    while True:

        conn, addr = s.accept()

        conn_from = str(addr)

        display.fill(0)

        display.text("WAP Mode ON",20,0)

        display.text("IP:"+ip,0,8)

        display.text('CF:'+conn_from,0,16)

        request = conn.recv(1024)

        request_content = str(request)

        display.text("Request Content",0,24)

        display.text(request_content,0,32)

        display.show()

        response = web_page()

        conn.send(response)

        conn.close()

ap_mode('ElattePi WAP 192.168.4.1','PASSWORD')        

