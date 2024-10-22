import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn, ApplicationNoOpTxn
from dotenv import load_dotenv
from user_input_helpers import get_application_id, get_sender_address, get_private_key

# Tải biến môi trường từ file .env
load_dotenv()

ALGOD_ADDRESS = os.getenv('NODELY_ENDPOINT_URL')
ALGOD_TOKEN = os.getenv('NODELY_API_KEY')

# Khởi tạo client
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def check_opt_in(app_id, sender_address):
    try:
        account_info = client.account_info(sender_address)
        for app in account_info.get('apps-local-state', []):
            if app['id'] == app_id:
                return True
        return False
    except Exception as e:
        print(f"Error checking opt-in status: {e}")
        return False

def perform_opt_in(app_id, sender_address, private_key):
    try:
        params = client.suggested_params()
        txn = ApplicationOptInTxn(sender_address, params, app_id)
        signed_txn = txn.sign(private_key)
        txid = client.send_transaction(signed_txn)
        print(f"Giao dịch opt-in được gửi với ID: {txid}")
        return True
    except Exception as e:
        print(f"Error during opt-in: {e}")
        return False

def call_add_attendant():
    try:
        app_id = get_application_id()
        sender_address = get_sender_address()
        private_key = get_private_key()

        # Kiểm tra người dùng đã opt-in chưa
        if not check_opt_in(app_id, sender_address):
            print(f"Người dùng chưa opt-in vào ứng dụng {app_id}. Thực hiện opt-in...")
            if not perform_opt_in(app_id, sender_address, private_key):
                return

        # Nhập event ID từ người dùng
        event_id = int(input("Nhập event ID: "))

        params = client.suggested_params()
        app_args = [
            "add_attendant".encode('utf-8'),  # Tham số 1
            event_id.to_bytes(8, 'big')       # Tham số 2
        ]

        # Tạo giao dịch NoOp để đăng ký người tham dự
        txn = ApplicationNoOpTxn(sender_address, params, app_id, app_args)
        signed_txn = txn.sign(private_key)
        txid = client.send_transaction(signed_txn)
        print(f"Giao dịch được gửi với ID: {txid}")
    except Exception as e:
        print(f"Error registering attendant: {e}")

if __name__ == "__main__":
    call_add_attendant()