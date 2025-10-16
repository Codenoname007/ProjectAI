HƯỚNG DẪN CHẠY DỰ ÁN SNAKE AI (Snake Ai game)
--------------------------------------------------------
1) Tạo môi trường ảo:
   python -m venv venv
2) Kích hoạt (PowerShell):
   .\venv\Scripts\Activate.ps1
   Nếu bị chặn: mở PowerShell (Run as Admin) và chạy:
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
3) Cài thư viện:
   pip install -r requirements.txt
4) Chạy menu chính (Pygame):
   python main.py
5) Chạy benchmark (xuất results.csv và results.png):
   python benchmark.py
