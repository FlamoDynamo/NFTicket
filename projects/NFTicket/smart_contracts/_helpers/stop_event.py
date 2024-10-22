import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationNoOpTxn
from dotenv import load_dotenv
from user_input_helpers import get_application_id, get_sender_address, get_private_key

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình Algod client
ALGOD_ADDRESS = os.getenv('NODELY_ENDPOINT_URL')
ALGOD_TOKEN = os.getenv('NODELY_API_KEY')

# Khởi tạo client
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def call_stop_event():
    try:
        app_id = get_application_id()

        # Nhập event ID từ người dùng và kiểm tra hợp lệ
        try:
            event_id = int(input("Nhập event ID: "))  # Yêu cầu nhập event ID từ người dùng
            if event_id < 0:
                raise ValueError("event ID phải là số nguyên dương.")
        except ValueError as e:
            print(f"Lỗi: {e}")
            return

        sender_address = get_sender_address()
        private_key = get_private_key()

        # Lấy thông số giao dịch từ client
        params = client.suggested_params()

        # Thiết lập app_args với đúng 2 tham số
        app_args = [
            "stop_event".encode('utf-8'),
            event_id.to_bytes(8, 'big')  # Chuyển event ID thành dạng byte (8 bytes)
        ]

        # Tạo giao dịch ApplicationNoOp
        txn = ApplicationNoOpTxn(sender_address, params, app_id, app_args)

        # Ký giao dịch
        signed_txn = txn.sign(private_key)

        # Gửi giao dịch
        txid = client.send_transaction(signed_txn)
        print(f"Giao dịch được gửi với ID: {txid}")

        # Chờ xác nhận giao dịch (tùy chọn)
        wait_for_confirmation(client, txid)
        print(f"Sự kiện {event_id} đã được dừng thành công.")

    except Exception as e:
        print(f"Error stopping event: {e}")

def wait_for_confirmation(client, txid):
    """Chờ xác nhận giao dịch trên Algorand blockchain"""
    last_round = client.status().get('last-round')
    while True:
        try:
            tx_info = client.pending_transaction_info(txid)
            if tx_info.get('confirmed-round', 0) > 0:
                print(f"Giao dịch đã được xác nhận ở round {tx_info.get('confirmed-round')}")
                return tx_info
            print(f"Đang chờ xác nhận... Vòng hiện tại: {client.status().get('last-round')}")
            client.status_after_block(last_round + 1)
        except Exception as e:
            print(f"Error waiting for confirmation: {e}")
            return

if __name__ == "__main__":
    call_stop_event()