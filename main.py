import requests
import time
import random
import string
import hashlib
from urllib.parse import quote

def generate_device_id():
    """生成16位随机设备ID"""
    return ''.join(random.choices(string.hexdigits.lower(), k=16))

def generate_signature(device_id, cur_time):
    """生成请求签名"""
    sign_str = f"zD9[bM4~sF4~uY2){device_id}{cur_time}"
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

def get_random_phone_info():
    """获取随机手机信息"""
    manufacturers = ['Samsung', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo',
                    'Apple', 'OnePlus', 'Realme', 'Sony', 'Google']
    models = ['Galaxy S21', 'Mate 40', 'Mi 11', 'Reno 5', 'X60',
              'iPhone 12', '8T', 'X7', 'Xperia 1 II', 'Pixel 5']
    return random.choice(manufacturers), random.choice(models)

def get_random_user_agent():
    """随机返回安卓或苹果浏览器的User-Agent"""
    android_agents = [
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-A315G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/90.0.4430.210 Mobile Safari/537.36",
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/116.0 Firefox/116.0"
    ]
   
    ios_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/116.0.5845.177 Mobile/15E148 Safari/604.1"
    ]
   
    return random.choice(android_agents + ios_agents)

def main():

    invite_code = "129543361"
   
    # 生成动态参数
    cur_time = str(int(time.time() * 1000))
    device_id = generate_device_id()
    mob_mfr, mobmodel = get_random_phone_info()
    signature = generate_signature(device_id, cur_time)
   
    # 随机获取浏览器User-Agent
    user_agent = get_random_user_agent()
   
    # 准备请求数据
    data_str = f"invited_by={quote(invite_code)}&ua={quote(user_agent)}&is_install=0"
   
    # 请求头
    headers = {
        "log-header": "I am the log request header.",
        "app_id": "chouyushipin",
        "channel_code": "cysp_sp02",
        "cur_time": cur_time,
        "device_id": device_id,
        "mob_mfr": mob_mfr,
        "mobmodel": mobmodel,
        "package_name": "com.hjmore.taihe",
        "sign": signature,
        "sys_platform": "2",
        "sysrelease": "11",
        "token": "",
        "version": "40000",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "u.yyxdmn.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.0"
    }
   
    try:
        response = requests.post(
            "https://u.gslock.com/api/public/init",
            headers=headers,
            data=data_str,
            timeout=10
        )
        
        print("\n" + "=" * 40)
        
        if response.status_code == 200:
            # 解析JSON响应
            try:
                response_data = response.json()
               
                # 检查业务逻辑是否成功
                if invite_code:  # 用户输入了邀请码
                    # 根据实际接口返回字段判断邀请是否成功
                    # 这里假设成功时返回"success"或"ok"
                    if response_data.get("msg", "").lower() in ["success", "ok"]:
                        print("✅ 邀请成功！")
                    else:
                        print("❌ 邀请失败（业务逻辑）")
                        print(f"失败原因: {response_data.get('msg', '未知错误')}")
                else:  # 用户未输入邀请码
                    print("ℹ️ 设备初始化成功（未使用邀请码）")
            except:
                # 无法解析JSON时使用简单判断
                if invite_code:
                    print("✅ 邀请成功（状态码200）")
                else:
                    print("ℹ️ 设备初始化成功（状态码200）")
        else:
            print(f"❌ 请求失败！状态码: {response.status_code}")
            print(f"失败原因: {response.text}")
        
        print("=" * 40)
        
    except requests.exceptions.RequestException as e:
        print("\n" + "=" * 40)
        print(f"❌ 网络请求失败: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        print("=" * 40)
    except Exception as e:
        print("\n" + "=" * 40)
        print(f"❌ 程序异常: {str(e)}")
        print("=" * 40)

if __name__ == "__main__":
    main()