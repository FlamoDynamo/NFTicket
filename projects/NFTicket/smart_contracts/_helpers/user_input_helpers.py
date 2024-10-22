import getpass

# Hàm nhập Application ID
def get_application_id():
    try:
        app_id = int(input("Nhập Application ID: "))
        return app_id
    except ValueError:
        print("Application ID phải là một số nguyên.")
        return get_application_id()

# Hàm nhập NFT ID
def get_nft_id():
    try:
        nft_id = int(input("Nhập NFT ID: "))
        return nft_id
    except ValueError:
        print("NFT ID phải là một số nguyên.")
        return get_nft_id()

# Hàm nhập thời gian kết thúc (GMT)
def get_end_timestamp():
    try:
        end_time = input("Nhập thời gian kết thúc (GMT - định dạng: YYYY/MM/DD HH:MM:SS): ")
        from datetime import datetime
        dt_obj = datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
        return int(dt_obj.timestamp())  # Trả về Unix timestamp
    except ValueError:
        print("Định dạng thời gian không hợp lệ. Vui lòng thử lại.")
        return get_end_timestamp()

# Hàm nhập số lượng vé
def get_ticket_count():
    try:
        ticket_count = int(input("Nhập số lượng vé: "))
        return ticket_count
    except ValueError:
        print("Số lượng vé phải là một số nguyên.")
        return get_ticket_count()

# Hàm nhập địa chỉ người gửi
def get_sender_address():
    sender_address = input("Nhập địa chỉ người gửi: ")
    return sender_address

# Hàm nhập private key dưới dạng mnemonic
def get_private_key():
    mnemonic_phrase = getpass.getpass("Nhập private key dưới dạng mnemonic: ")
    from algosdk import mnemonic
    try:
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        return private_key
    except Exception:
        print("Private key không hợp lệ. Vui lòng thử lại.")
        return get_private_key()

# Hàm nhập mã vé cho người dùng
def get_ticket_code():
    try:
        ticket_code = int(input("Nhập mã vé (Ticket Code - từ 001 đến 100): "))
        if 1 <= ticket_code <= 100:
            return ticket_code
        else:
            print("Mã vé phải nằm trong khoảng từ 001 đến 100.")
            return get_ticket_code()
    except ValueError:
        print("Mã vé phải là một số nguyên.")
        return get_ticket_code()