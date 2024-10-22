import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationNoOpTxn
from dotenv import load_dotenv
from user_input_helpers import get_application_id, get_nft_id, get_end_timestamp, get_ticket_count, get_sender_address, get_private_key

# Tải biến môi trường từ file .env
load_dotenv()

ALGOD_ADDRESS = os.getenv('NODELY_ENDPOINT_URL')
ALGOD_TOKEN = os.getenv('NODELY_API_KEY')

# Khởi tạo client
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def call_create_event():
    try:
        app_id = get_application_id()  # Lấy Application ID từ người dùng
        nft_id = get_nft_id()  # Lấy NFT ID từ người dùng
        end_timestamp = get_end_timestamp()  # Lấy thời gian kết thúc
        ticket_count = get_ticket_count()  # Lấy số lượng vé
        sender_address = get_sender_address()  # Lấy địa chỉ người gửi
        private_key = get_private_key()  # Lấy private key dưới dạng mnemonic

        # Lấy thông số giao dịch
        params = client.suggested_params()

        # Chuẩn bị arguments cho transaction
        app_args = [
            "create_event".encode('utf-8'),
            nft_id.to_bytes(8, 'big'),
            end_timestamp.to_bytes(8, 'big'),
            ticket_count.to_bytes(8, 'big')
        ]

        # Tạo transaction ApplicationNoOpTxn
        txn = ApplicationNoOpTxn(sender_address, params, app_id, app_args)

        # Ký và gửi giao dịch
        signed_txn = txn.sign(private_key)
        txid = client.send_transaction(signed_txn)
        print(f"Giao dịch được gửi với ID: {txid}")
    except Exception as e:
        print(f"Error creating event: {e}")

if __name__ == "__main__":
    call_create_event()