# =======================================================
#               PHẦN 1: BANNER VÀ THIẾT LẬP MÀU
# =======================================================
import os
import sys
import requests
import time
import random
import string
import re 
import json
import uuid
import platform
from datetime import datetime

# Import select chỉ khi nó tồn tại
try:
    import select 
except ImportError:
    select = None

# ANSI COLOR CODES
RED = '\033[91m'        
GREEN = '\033[92m'      
YELLOW = '\033[93m'     
BLUE = '\033[94m'       
MAGENTA = '\033[95m'    
VIOLET_STANDARD = '\033[35m' 
CYAN = '\033[96m'       
BOLD = '\033[1m'
RESET = '\033[0m'

# KHAI BÁO MÀU MỚI:
MAIN_FRAME_COLOR = VIOLET_STANDARD 
MAIN_LABEL_COLOR = MAGENTA         
DETAIL_COLOR = CYAN                

# KHAI BÁO BIẾN TOÀN CỤC:
SAVE_DIRECTORY = os.getcwd() 
LOG_FILE = "tghieu_email.txt"   
GLOBAL_PUBLIC_IP = "Đang lấy IP..."
MAC_ADDRESS_HEX = "Đang lấy ID"
#
def get_public_ip():
    """Lấy địa chỉ IP công cộng của thiết bị qua API"""
    try:
        # Sử dụng API miễn phí chỉ trả về địa chỉ IP dưới dạng văn bản thuần
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Lỗi HTTP {response.status_code}"
    except requests.exceptions.RequestException:
        return "Lỗi Kết nối Internet/API"
        
# --- ĐÃ SỬA: Thêm global và gán giá trị vào biến toàn cục ---
def get_device_unique_id():
    global MAC_ADDRESS_HEX
    mac_address_int = uuid.getnode()
   
    device_uuid = uuid.uuid1()
    
    mac_address_hex = format(mac_address_int, '012x')
    MAC_ADDRESS_HEX = mac_address_hex
# =======================================================
#               PHẦN 2: CẤU HÌNH
# =======================================================
DOMAIN_MAIL = "satato.com.vn" 
API_BASE_URL = "https://maytinhkhanhngan.com/tmail/index.php?fetch_email=" 
NGUONG_NOI_DUNG_TOI_THIETU = 10 

# --- HÀM BANNER CHÍNH (ĐÃ SỬA DÒNG IP) ---
def print_tghieux_banner():
    global GLOBAL_PUBLIC_IP, MAC_ADDRESS_HEX
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"")
    print(f"{YELLOW}  ████████╗ ███████╗ ██╗  ██╗ ███╗ ███████╗ ██╗   ██╗ ██╗  ██╗{RESET}  ")
    print(f"{YELLOW}  ╚══██╔══╝ ██╔════╝ ██║  ██║ ███║ ██╔════╝ ██║   ██║ ╚██╗██╔╝{RESET}  ")
    print(f"{YELLOW}     ██║    ██║ ███╗ ███████║ ███║ █████╗   ██║   ██║  ╚███╔╝ {RESET}  ")
    print(f"{YELLOW}     ██║    ██║ ███╗ ██╔══██║ ███║ ██╔══╝   ██║   ██║  ██╔██╗ {RESET}  ")
    print(f"{YELLOW}     ██║    ╚██████║ ██║  ██║ ███║ ███████╗ ╚██████╔╝ ██╔╝╚██╗{RESET}  ")
    print(f"{YELLOW}     ╚═╝     ╚══════╝ ╚═╝  ╚═╝ ╚═╝ ╚══════╝  ╚═════╝  ╚═╝  ╚═╝{RESET}  ")
    print(f"")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{CYAN}┌{'─'*65}┐{RESET}")
    # ĐÃ SỬA DÒNG IP/MAC
    print(f" {BOLD}[><]{RED}{BOLD} IP:{RESET} {GLOBAL_PUBLIC_IP}")
    print(f" {BOLD}[><]{YELLOW}{BOLD} ID MAC:{RESET} {CYAN}{MAC_ADDRESS_HEX}{RESET}")
    print(f" {BOLD}[><]{YELLOW}{BOLD}{' Fb: tg.nux — Trung Hiếu(nuxw)':<63}{RESET}")
    print(f" {BOLD}[><]{GREEN}{BOLD}{' Zalo: 0338.316.701':<63}{RESET}")
    print(f" {BOLD}[><]{MAIN_FRAME_COLOR}{BOLD} Email được lưu trong {YELLOW}{BOLD}tghieu_email.txt{RESET} ")
    print(f"{CYAN}└{'─'*65}┘{RESET}")
 
def tao_ten_email_ngau_nhien(min_length=5, max_length=6):
    characters = string.ascii_lowercase + string.digits
    length = random.randint(min_length, max_length)
    random_name = ''.join(random.choice(characters) for i in range(length))
    return random_name

def format_mail_for_display(mail_object):
    subject = mail_object.get("subject", "[Không có tiêu đề]")
    try:
        subject = subject.encode('latin1').decode('utf8')
    except:
        pass 
    return subject.strip()

# --- HÀM GHI LOG (ĐÃ THÊM MẬT KHẨU) ---
def log_email_to_file(email, subjects_received, status="HOÀN THÀNH"):
    global SAVE_DIRECTORY
    log_file_path = os.path.join(SAVE_DIRECTORY, LOG_FILE)
    
    # KHAI BÁO MẬT KHẨU CỐ ĐỊNH 
    mat_khau_co_dinh = "shoptghieux09" 
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            # Ghi TK và MK cố định vào file log
            f.write(f"{now} | TK:{email} MK:{mat_khau_co_dinh}\n") 
            f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"\n{RED}LỖI GHI LOG: Không thể ghi vào {log_file_path}. Lỗi: {e}{RESET}", file=sys.stderr)

def print_summary_block(email, subjects_received, scan_count):
    """In ra khối tóm tắt của email vừa hoàn thành."""
    subject_count = len(subjects_received)
    
    print(f"\n{BLUE}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f" {BOLD}[><]{GREEN}{BOLD} TÓM TẮT QUÉT HOÀN THÀNH:{RESET} {CYAN}{email}{RESET}")
    print(f" {BOLD}[><]{BLUE}{BOLD}   Lần quét tối đa:{RESET} {CYAN}{scan_count}{RESET}")
    print(f" {BOLD}[><]{BLUE}{BOLD}   Tổng thư đã nhận:{RESET} {CYAN}{subject_count}{RESET}")
    if subject_count > 0:
         print(f" {BOLD}[><]{BLUE}{BOLD}   Thư cuối cùng:{RESET} {YELLOW}{format_mail_for_display(subjects_received[-1])[:50]}...{RESET}")
    else:
         print(f" {BOLD}[><]{BLUE}{BOLD}   Ghi chú:{RESET} {YELLOW}Không nhận được thư nào.{RESET}")
    print(f"{BLUE}╚═══════════════════════════════════════════════════════════════════╝{RESET}")


# --- HÀM QUÉT MAIL CHÍNH (ĐÃ XÓA LỆNH TẠO FILE SUBJECTS) ---
def scan_noi_dung_mail_ao(email_can_kiem_tra):
    
    email_encoded = requests.utils.quote(email_can_kiem_tra)
    api_url = API_BASE_URL + email_encoded
    
    danh_sach_thu_da_nhan = [] 
    noi_dung_mail_hien_tai = f"Đang chờ thư..."
    scan_count = 0 
    
    def in_khoi_quet(status_line, subject_count):
        """Dọn màn hình và in lại toàn bộ khối quét."""
        # Dọn màn hình trước khi in để đảm bảo không còn dòng thừa (Phương pháp Clear)
        os.system('clear' if os.name == 'posix' else 'cls') 
        
        # In lại Banner
        print_tghieux_banner()
        
        # Bắt đầu khối quét chính
        print(f"\n{CYAN}┌{'─'*65}┐{RESET}")  
        print(f" {BOLD}[><]{MAIN_LABEL_COLOR}{BOLD} 📧 Email đang theo dõi:{RESET} {DETAIL_COLOR}{email_can_kiem_tra}{RESET}") 
        print(f" {BOLD}[><]{MAIN_LABEL_COLOR}{BOLD} 🔍 Lần quét thư:{RESET} {DETAIL_COLOR}{scan_count}{RESET} {BOLD}(1 giây/lần){RESET}") 
        print(f" {BOLD}[><]{MAIN_LABEL_COLOR}{BOLD} 📩 {subject_count} thư đã nhận:{RESET}") 
        
        # Dòng Trạng thái/Subject cuối cùng
        if subject_count > 0 and not status_line.startswith((f"{RED}LỖI", f"{GREEN}Đã nhận Subject mới!")):
             subject_content = format_mail_for_display(danh_sach_thu_da_nhan[-1])
             output_line = f" {BOLD}[><] ✓ {GREEN}{BOLD}#{subject_count}:{RESET} {YELLOW}{BOLD}{subject_content}"
             print(f"{output_line:<65}│{RESET}") 
        else:
             print(f" {status_line:<63}{RESET}")
        
        print(f" {BOLD}[><]{MAIN_LABEL_COLOR}{BOLD}{YELLOW}Ctrl+C để thoát tool.{RESET}") 
        print(f"{CYAN}└{'─'*65}┘{RESET}") 
        print(f"{YELLOW}{BOLD}>>> Nhấn ENTER để chuyển mail:{RESET} ", end="", flush=True)

    # In khối quét lần đầu
    in_khoi_quet(noi_dung_mail_hien_tai, len(danh_sach_thu_da_nhan))
    
    while True:
        try:
            # --- KIỂM TRA PHÍM ENTER (KHÔNG CHẶN) ---
            if select and sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                user_input = sys.stdin.readline().strip()
                if user_input == '': # ENTER được nhấn
                    subjects_list = [format_mail_for_display(mail) for mail in danh_sach_thu_da_nhan]
                    log_email_to_file(email_can_kiem_tra, subjects_list, status="DỪNG QUÉT BỞI ENTER")
                    
                    # In lại khối quét cuối cùng 
                    in_khoi_quet(noi_dung_mail_hien_tai, len(danh_sach_thu_da_nhan)) 
                    
                    # In tóm tắt email vừa quét xong ngay phía dưới
                    print_summary_block(email_can_kiem_tra, danh_sach_thu_da_nhan, scan_count)
                    
                    return True # Quay lại main_loop

            scan_count += 1
                
            # 3. Gọi API (Quét 1s/lần)
            response = requests.get(api_url, timeout=10)
            last_status = noi_dung_mail_hien_tai

            # --- LOGIC QUÉT MAIL (ĐÃ LOẠI BỎ LỆNH TẠO FILE SUBJECTS) ---
            if response.status_code == 200:
                content = response.text.strip()
                try:
                    all_mails_from_api = json.loads(content)
                    if not isinstance(all_mails_from_api, list):
                        raise ValueError("API không trả về danh sách email.")
                        
                    new_mail_count = 0
                    for mail in all_mails_from_api:
                        is_new = True
                        for existing_mail in danh_sach_thu_da_nhan:
                            if (existing_mail.get('subject') == mail.get('subject') and 
                                existing_mail.get('from') == mail.get('from') and 
                                existing_mail.get('timestamp') == mail.get('timestamp')):
                                is_new = False
                                break
                        if is_new:
                            danh_sach_thu_da_nhan.append(mail) 
                            new_mail_count += 1
                            
                    if new_mail_count > 0:
                        # FIXED: Loại bỏ lệnh gọi save_subjects_to_file và thay bằng cập nhật trạng thái
                        subjects_list = [format_mail_for_display(mail) for mail in danh_sach_thu_da_nhan]
                        subject_count_current = len(danh_sach_thu_da_nhan)
                        noi_dung_mail_hien_tai = f"{GREEN}Đã nhận Subject mới!{RESET} {MAGENTA}{BOLD}(+{new_mail_count} Subjects. Tổng: {subject_count_current}){RESET}"
                        
                    elif len(danh_sach_thu_da_nhan) > 0:
                        noi_dung_mail_hien_tai = f"Đã nhận {len(danh_sach_thu_da_nhan)} thư. Đang chờ thêm..."
                    else:
                        noi_dung_mail_hien_tai = f"Đang chờ thư..."
                        
                except (json.JSONDecodeError, ValueError):
                    if "No email found" in content:
                        noi_dung_mail_hien_tai = f"Đang chờ thư..."
                    # FIXED: Sửa lỗi typo NGUONG_NOI_DUNG_TOI_THIEU -> NGUONG_NOI_DUNG_TOI_THIETU
                    elif len(content) > NGUONG_NOI_DUNG_TOI_THIETU:
                        noi_dung_mail_hien_tai = f"{RED}Lỗi API: Không phải JSON/Rỗng ({content[:30]}...){RESET}"
                
            else:
                noi_dung_mail_hien_tai = f"{RED}Lỗi HTTP {response.status_code}. Đang chờ...{RESET}"
            # END OF LOGIC QUÉT MAIL

            # 2. CẬP NHẬT GIAO DIỆN BẰNG CÁCH XÓA VÀ IN LẠI
            in_khoi_quet(noi_dung_mail_hien_tai, len(danh_sach_thu_da_nhan))

            time.sleep(1)

        except requests.exceptions.RequestException:
            noi_dung_mail_hien_tai = f"{RED}Lỗi kết nối API. Đang chờ...{RESET}"
            
            in_khoi_quet(noi_dung_mail_hien_tai, len(danh_sach_thu_da_nhan)) 
            time.sleep(1)
            
        except KeyboardInterrupt:
            subjects_list = [format_mail_for_display(mail) for mail in danh_sach_thu_da_nhan]
            log_email_to_file(email_can_kiem_tra, subjects_list, status="THOÁT BỞI CTRL+C")
            
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n{RED}Đã ngắt quá trình quét. Thoát chương trình.{RESET}\n")
            sys.exit(0)
            
    return False 

# --- HÀM CHÍNH (ĐÃ SỬA LỖI GIẬT MÀN HÌNH VÀ GỌI ID MAC) ---
def main_loop():
    global SAVE_DIRECTORY, GLOBAL_PUBLIC_IP 
    
    # 1. LẤY IP LẦN ĐẦU (ĐÃ FIX LỖI GIẬT MÀN HÌNH)
    
    # A. Xóa màn hình và in banner với trạng thái chờ
    os.system('clear' if os.name == 'posix' else 'cls')
    GLOBAL_PUBLIC_IP = f"{YELLOW}Đang lấy IP...{RESET}" # Trạng thái chờ
    print_tghieux_banner()
    
    # B. Bắt đầu lấy IP/MAC (Phần gây trễ)
    fetched_ip = get_public_ip()
    GLOBAL_PUBLIC_IP = fetched_ip # Cập nhật biến global với IP đã lấy
    
    # FIXED: Thêm lệnh gọi để lấy và gán ID MAC vào biến toàn cục
    get_device_unique_id() 
    
    # C. Xóa màn hình lần nữa và in banner với IP/MAC cuối cùng (để xóa trạng thái chờ)
    os.system('clear' if os.name == 'posix' else 'cls')
    print_tghieux_banner()
    
    # --- XỬ LÝ ĐƯỜNG DẪN LƯU ---
    current_path = os.getcwd()
    
    print(f"\n{MAIN_LABEL_COLOR}{BOLD}>>> Thư mục lưu mặc định:{RESET} {CYAN}{current_path}{RESET}")
    
    save_path = input(f"{YELLOW}{BOLD}>>> Nhấn ENTER để lưu file:{RESET} ").strip()
    
    if save_path:
        # SỬA ĐỔI ĐỂ XỬ LÝ ĐƯỜNG DẪN EMULATED NHẬP SAI
        if save_path.lower() in ["0/storage/emulated", "0/storage/emulated/0", "/storage/emulated", "/storage/emulated/0"]:
             print(f"{RED}CẢNH BÁO: Đường dẫn không hợp lệ. Đã đổi sang /sdcard/Download để lưu vào bộ nhớ trong.{RESET}")
             save_path = "/sdcard/Download"
        
        try:
            # Lấy đường dẫn tuyệt đối để tránh lỗi
            absolute_path = os.path.abspath(save_path)
            os.makedirs(absolute_path, exist_ok=True)
            SAVE_DIRECTORY = absolute_path
            print(f"{GREEN}Đã đặt thư mục lưu mới:{RESET} {SAVE_DIRECTORY}\n")
        except Exception as e:
            print(f"{RED}LỖI: Không thể tạo/truy cập thư mục {save_path}. Dùng thư mục mặc định.{RESET}")
            print(f"Lỗi chi tiết: {e}")
            SAVE_DIRECTORY = current_path
    else:
        print(f"{GREEN}Dùng thư mục lưu mặc định: {RESET}{SAVE_DIRECTORY}\n")
        
    # 2. CHỜ ENTER BAN ĐẦU
    print(f"{YELLOW}{BOLD}>>> Nhấn ENTER để tạo email ngẫu nhiên và BẮT ĐẦU QUÉT:{RESET} ")
    try:
        input() 
    except KeyboardInterrupt:
        sys.exit(0)

    while True:
        # 1. Tạo email mới cho lần quét này
        ten_ngau_nhien = tao_ten_email_ngau_nhien()
        email_ngau_nhien = f"{ten_ngau_nhien}@{DOMAIN_MAIL}"
        
        # 2. Bắt đầu quét mail
        if scan_noi_dung_mail_ao(email_ngau_nhien):
            # Nếu scan_noi_dung_mail_ao trả về True (do Enter)
            
            # 3. Yêu cầu nhấn Enter lần nữa để bắt đầu quét mail mới (tạo hiệu ứng "nối tiếp")
            print(f"\n>>> Email:{YELLOW}{BOLD} {email_ngau_nhien}{RESET} đã dừng. Nhấn ENTER để bắt đầu quét mail tiếp theo{RESET} ")
            try:
                 input() 
            except KeyboardInterrupt:
                 sys.exit(0)
                 
            # Sau khi nhấn Enter lần 2, vòng lặp tiếp tục, scan_noi_dung_mail_ao sẽ được gọi, 
            # nó sẽ tự động clear screen và hiển thị khối quét mới.
            continue
        else:
            break 

if __name__ == "__main__":
    try:
        main_loop() 
    except KeyboardInterrupt:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n\n{RED}Mày bấm out tool rồi con chó, cút đi XD{RESET}")
        sys.exit(0)
