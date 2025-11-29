# 🔐 PyCuTe Obfuscator v3.0 

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-lightgrey.svg)]()

**Advanced Python Code Protection & Obfuscation**  
*Make Your Code Unbreakable*

**Bảo vệ & Làm rối Mã nguồn Python Nâng cao**  
*Làm cho Mã của Bạn trở nên Bất khả xâm phạm*

---

**PyCuTe Obfuscator** is a state-of-the-art Python code protection tool designed to secure your intellectual property against reverse engineering, tampering, and unauthorized usage. With its multi-layered obfuscation engine and advanced protection mechanisms, PyCuTe ensures your code remains safe and secure in any environment.

*PyCuTe Obfuscator là công cụ bảo vệ mã nguồn Python hiện đại được thiết kế để bảo vệ tài sản trí tuệ của bạn chống lại việc dịch ngược, giả mạo và sử dụng trái phép. Với công cụ làm rối đa lớp và các cơ chế bảo vệ tiên tiến, PyCuTe đảm bảo mã của bạn luôn an toàn trong mọi môi trường.*

---

## 📑 Table of Contents / Mục lục

- [✨ Key Features / Tính năng Chính](#-key-features--tính-năng-chính)
- [🚀 Installation / Cài đặt](#-installation--cài-đặt)
- [💻 Usage / Sử dụng](#-usage--sử-dụng)
- [🧪 QA Studio / Công cụ Kiểm thử](#-qa-studio--công-cụ-kiểm-thử)
- [⚙️ Configuration / Cấu hình](#️-configuration--profiles--cấu-hình--hồ-sơ)
- [📂 Project Structure / Cấu trúc Dự án](#-project-structure--cấu-trúc-dự-án)
- [⚠️ Disclaimer / Tuyên bố miễn trừ trách nhiệm](#-disclaimer--tuyên-bố-miễn-trừ-trách-nhiệm)

---

## ✨ Key Features / Tính năng Chính

### 🛡️ Core Obfuscation / Làm rối Cốt lõi
**PyCuTe employs a variety of techniques to make your code unreadable while maintaining its original functionality:**
*PyCuTe sử dụng nhiều kỹ thuật khác nhau để làm cho mã của bạn không thể đọc được trong khi vẫn giữ nguyên chức năng ban đầu:*

- **Control Flow Flattening**: Transforms linear code into complex, non-linear structures using custom exception-based dispatchers.
  - *Làm phẳng Luồng Điều khiển: Biến đổi mã tuyến tính thành các cấu trúc phức tạp, phi tuyến tính bằng cách sử dụng các bộ điều phối dựa trên ngoại lệ tùy chỉnh.*
- **String Encryption**: Encrypts all string literals with dynamic XOR encoding and runtime decoding.
  - *Mã hóa Chuỗi: Mã hóa tất cả các chuỗi ký tự bằng mã hóa XOR động và giải mã khi chạy.*
- **Integer Obfuscation**: Replaces integer constants with complex arithmetic expressions.
  - *Làm rối Số nguyên: Thay thế các hằng số nguyên bằng các biểu thức số học phức tạp.*
- **Name Mangling**: Renames variables, functions, and classes to meaningless Unicode characters (e.g., `蹶馪脜`).
  - *Làm mang tên: Đổi tên các biến, hàm và lớp thành các ký tự Unicode vô nghĩa.*
- **Dead Code Injection**: Inserts junk code and fake instructions to confuse decompilers.
  - *Chèn Mã chết: Chèn mã rác và các lệnh giả để gây nhầm lẫn cho các trình dịch ngược.*

### 🔒 Advanced Protection / Bảo vệ Nâng cao
**Beyond simple obfuscation, PyCuTe adds active protection measures:**
*Ngoài việc làm rối đơn giản, PyCuTe còn bổ sung các biện pháp bảo vệ chủ động:*

- **Anti-Debugging**: Detects and blocks debuggers (GDB, PDB, etc.).
  - *Chống Gỡ lỗi: Phát hiện và chặn các trình gỡ lỗi.*
- **Anti-Tamper**: Verifies code integrity at runtime to prevent modification.
  - *Chống Giả mạo: Xác minh tính toàn vẹn của mã khi chạy để ngăn chặn sửa đổi.*
- **Anti-VM/Sandbox**: Identifies virtual environments to prevent analysis.
  - *Chống VM/Sandbox: Nhận diện môi trường ảo để ngăn chặn việc phân tích.*
- **Anti-Decompile**: Targets tools like `uncompyle6`, `pycdc`.
  - *Chống Dịch ngược: Nhắm mục tiêu vào các công cụ như `uncompyle6`, `pycdc`.*

---

## 🚀 Installation / Cài đặt

### Prerequisites / Yêu cầu tiên quyết
- Python **3.9+**
- `pip` (Python Package Installer)

### Quick Install / Cài đặt Nhanh
1. **Clone the repository / Sao chép kho lưu trữ:**
   ```bash
   git clone https://github.com/hoangtuvungcao/OBF_PyCuTe.git
   cd OBF_PyCuTe
   ```
2. **Run the automated installation script:**
*Chạy tập lệnh cài đặt tự động:*

```bash
python install.py
```
*This script will check your environment and automatically install all required dependencies.*
*Tập lệnh này sẽ kiểm tra môi trường của bạn và tự động cài đặt tất cả các gói phụ thuộc cần thiết.*

### Manual Install / Cài đặt Thủ công

1. **Clone the repository / Sao chép kho lưu trữ:**
   ```bash
   git clone https://github.com/hoangtuvungcao/OBF_PyCuTe.git
   cd OBF_PyCuTe
   ```

2. **Install dependencies / Cài đặt các gói phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage / Sử dụng

### Interactive Mode / Chế độ Tương tác
**Simply run the main script and follow the prompts:**
*Chỉ cần chạy tập lệnh chính và làm theo hướng dẫn:*

```bash
python main.py
```
*You will be asked to enter the input file path, select options, and confirm the obfuscation.*
*Bạn sẽ được yêu cầu nhập đường dẫn tệp đầu vào, chọn các tùy chọn và xác nhận quá trình làm rối.*

### Command Line Interface / Giao diện Dòng lệnh
**For automated workflows and advanced users:**
*Dành cho quy trình làm việc tự động và người dùng nâng cao:*

```bash
python main.py -f <input_file> -o <output_file> [options]
```

**Options / Tùy chọn:**
- `-f, --file`: Input file path / *Đường dẫn tập tin đầu vào*
- `-o, --output`: Output file path / *Đường dẫn tập tin đầu ra*
- `-p, --profile`: Obfuscation profile (`minimal`, `balanced`, `maximum`, `production`) / *Hồ sơ làm rối*
- `--batch`: Process directory (batch mode) / *Xử lý thư mục (chế độ hàng loạt)*
- `--recursive`: Recursive search in batch mode / *Tìm kiếm đệ quy trong chế độ hàng loạt*
- `--list-profiles`: List available profiles / *Liệt kê các hồ sơ có sẵn*
- `-v, --verbose`: Enable verbose output / *Bật chế độ hiển thị chi tiết*
- `--help`: Show help message / *Hiển thị thông báo trợ giúp*

**Examples / Ví dụ:**

1. **Obfuscate a single file with maximum protection:**
   *Làm rối một tệp đơn với bảo vệ tối đa:*
   ```bash
   python main.py -f my_script.py -o protected_script.py -p maximum
   ```

2. **Batch process a directory:**
   *Xử lý hàng loạt một thư mục:*
   ```bash
   python main.py --batch ./my_project --recursive
   ```

---

## 🧪 QA Studio / Công cụ Kiểm thử

**PyCuTe includes a powerful Quality Assurance tool (`test.py`) to verify your obfuscated code.**
*PyCuTe bao gồm một công cụ Đảm bảo Chất lượng mạnh mẽ (`test.py`) để xác minh mã đã làm rối của bạn.*

Run the QA Studio GUI:
```bash
python test.py
```

**Features / Tính năng:**
- **Syntax Check**: Verifies that the obfuscated code is valid Python syntax.
  - *Kiểm tra Cú pháp: Xác minh rằng mã đã làm rối là cú pháp Python hợp lệ.*
- **Benchmark**: Compares execution speed and output between source and obfuscated code.
  - *Đánh giá Hiệu năng: So sánh tốc độ thực thi và đầu ra giữa mã nguồn và mã đã làm rối.*
- **Output Verification**: Ensures the logic remains identical by comparing stdout/stderr.
  - *Xác minh Đầu ra: Đảm bảo logic vẫn giống hệt nhau bằng cách so sánh stdout/stderr.*
- **Encoding Fixer**: Automatically repairs encoding issues (e.g., invalid characters, BOMs).
  - *Sửa lỗi Mã hóa: Tự động sửa các vấn đề về mã hóa (ví dụ: ký tự không hợp lệ, BOM).*

---

## ⚙️ Configuration & Profiles / Cấu hình & Hồ sơ

**You can customize obfuscation levels using profiles defined in `utils/profiles.py` or via CLI arguments.**
*Bạn có thể tùy chỉnh mức độ làm rối bằng cách sử dụng các hồ sơ được định nghĩa trong `utils/profiles.py` hoặc thông qua các tham số dòng lệnh.*

| Profile | Description (Mô tả) | Use Case (Trường hợp sử dụng) |
|---------|---------------------|-------------------------------|
| **Minimal** | Light obfuscation, high performance. (*Làm rối nhẹ, hiệu suất cao*) | Development / Testing (*Phát triển / Kiểm thử*) |
| **Balanced** | Good trade-off between security and speed. (*Cân bằng tốt giữa bảo mật và tốc độ*) | Distribution (*Phân phối*) |
| **Maximum** | Heavy obfuscation, multiple layers. (*Làm rối nặng, nhiều lớp*) | High Security (*Bảo mật cao*) |
| **Production** | Optimized for release, includes anti-tamper. (*Tối ưu cho phát hành, bao gồm chống giả mạo*) | Final Release (*Phát hành cuối*) |

---

## 📂 Project Structure / Cấu trúc Dự án

Here is a detailed breakdown of the project files and their functions:
*Dưới đây là chi tiết về các tệp dự án và chức năng của chúng:*

```
Source-Pymeomeo-main/
├── core/                   # Core Logic
│   ├── obfuscator.py       # Main obfuscation engine (Công cụ làm rối chính)
│   ├── ast_transformer.py  # AST manipulation logic (Logic thao tác AST)
│   ├── string_encoder.py   # String encryption logic (Logic mã hóa chuỗi)
│   └── ...
├── protection/             # Protection Modules
│   ├── anti_debug.py       # Anti-debugging code generation (Tạo mã chống gỡ lỗi)
│   ├── anti_tamper.py      # Integrity checking (Kiểm tra tính toàn vẹn)
│   ├── anti_decompile.py   # Anti-decompilation tricks (Thủ thuật chống dịch ngược)
│   └── ...
├── techniques/             # Obfuscation Techniques
│   ├── control_flow.py     # Control flow flattening (Làm phẳng luồng điều khiển)
│   ├── name_mangling.py    # Variable renaming (Đổi tên biến)
│   └── ...
├── ui/                     # User Interface
│   ├── cli.py              # Command line interface handler (Xử lý giao diện dòng lệnh)
│   └── progress.py         # Progress bar display (Hiển thị thanh tiến trình)
├── utils/                  # Utilities
│   ├── config.py           # Configuration management (Quản lý cấu hình)
│   ├── logger.py           # Logging system (Hệ thống ghi nhật ký)
│   ├── random_gen.py       # Random data generator (Tạo dữ liệu ngẫu nhiên)
│   └── profiles.py         # Obfuscation profiles (Các hồ sơ làm rối)
├── logs/                   # Log files directory (Thư mục tập tin nhật ký)
├── main.py                 # Main entry point script (Tập lệnh điểm nhập chính)
├── install.py              # Automated installer script (Tập lệnh cài đặt tự động)
├── requirements.txt        # Python dependencies list (Danh sách các gói phụ thuộc)
├── test.py                 # QA Studio GUI application (Ứng dụng GUI kiểm thử)
└── README.md               # This documentation file (Tập tin tài liệu này)
```

---

## ⚠️ Disclaimer / Tuyên bố miễn trừ trách nhiệm

**This tool is for educational and security research purposes only.**
*Công cụ này chỉ dành cho mục đích giáo dục và nghiên cứu bảo mật.*

- **The authors are not responsible for any misuse of this software.**
  *Các tác giả không chịu trách nhiệm về bất kỳ việc sử dụng sai phần mềm này.*
- **Do not use this tool to protect malicious software.**
  *Không sử dụng công cụ này để bảo vệ phần mềm độc hại.*
- **Always backup your source code before obfuscation.**
  *Luôn sao lưu mã nguồn của bạn trước khi làm rối.*

---

*Powered by PyCuTe Team*
