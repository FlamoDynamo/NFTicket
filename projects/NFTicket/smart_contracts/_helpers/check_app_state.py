import os
from algosdk.v2client import algod
from dotenv import load_dotenv
from algosdk import encoding
import time
import base64
from user_input_helpers import get_sender_address

# Tải biến môi trường từ file .env
load_dotenv()

ALGOD_ADDRESS = os.getenv('NODELY_ENDPOINT_URL')
ALGOD_TOKEN = os.getenv('NODELY_API_KEY')
APP_ID = 724754669  # Thay bằng Application ID của bạn

# Khởi tạo client
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def unix_to_datetime(unix_time):
    """Chuyển đổi Unix timestamp thành định dạng YYYY/MM/DD HH:MM:SS (GMT+7)"""
    adjusted_time = unix_time + 7 * 3600  # Cộng thêm 7 giờ (25200 giây) để điều chỉnh về GMT+7
    return time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(adjusted_time))

def decode_state(state):
    """Giải mã Global hoặc Local State của ứng dụng"""
    decoded = {}
    for item in state:
        key = base64.b64decode(item['key']).decode('utf-8')
        value = item['value']
        
        if value['type'] == 1:  # string
            decoded_value = base64.b64decode(value['bytes']).decode('utf-8')
        else:  # uint
            decoded_value = value['uint']
            
        decoded[key] = decoded_value
    return decoded

def format_sender_address(address):
    """Ẩn phần giữa của địa chỉ, chỉ chừa lại 8 ký tự đầu và 8 ký tự cuối"""
    return f"{address[:8]}****{address[-8:]}"

def check_app_state():
    try:
        app_id = APP_ID  # Sử dụng APP_ID được định nghĩa sẵn
        sender_address = get_sender_address()

        # Lấy Global State
        app_state = client.application_info(app_id)['params']['global-state']
        global_state = decode_state(app_state)
        print("Global State của Smart Contract:")

        # In các giá trị trong Global State
        for key, value in global_state.items():
            print(f"{key}: {value}")

        # Lấy Local State của người gửi
        account_info = client.account_application_info(sender_address, app_id)
        if 'app-local-state' in account_info and 'key-value' in account_info['app-local-state']:
            local_state = account_info['app-local-state']['key-value']
            local_state_decoded = decode_state(local_state)
            
            # In mã vé với định dạng ẩn phần giữa của địa chỉ người gửi
            ticket_code_key = f"ticket_code_1"  # Có thể thay đổi nếu có nhiều sự kiện
            ticket_code = local_state_decoded.get(ticket_code_key)
            
            if ticket_code:
                # Định dạng ẩn phần giữa của địa chỉ người gửi
                sender_address_formatted = f"{sender_address[:8]}****{sender_address[-8:]}"
                print(f"Mã vé của người gửi {sender_address_formatted}: {ticket_code}")
            else:
                print(f"Người gửi {sender_address} chưa có mã vé.")
        else:
            print(f"Người gửi {sender_address} chưa có mã vé.")

        # In ID của sự kiện mới nhất và thời gian kết thúc
        event_count = global_state.get('event_count', 0)
        print(f"ID của sự kiện mới nhất (event_count): {event_count}")
        if event_count > 0:
            end_timestamp = global_state.get(f'event_end_{event_count}', 0)
            if end_timestamp > 0:
                end_time = unix_to_datetime(end_timestamp)
                print(f"Thời gian kết thúc của sự kiện {event_count}: {end_time}")
            else:
                print(f"Không tìm thấy thời gian kết thúc cho sự kiện {event_count}")
    except Exception as e:
        print(f"Error checking app state: {e}")

if __name__ == "__main__":
    check_app_state()