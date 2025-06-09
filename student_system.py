import tkinter as tk
from tkinter import messagebox
import mysql.connector

class StudentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("学生选课管理系统")
        self.root.geometry("400x300")
        
        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Cjz02200059+",
            database="undefined" 
        )
        self.cursor = self.db.cursor()
        
        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=50)
        
        tk.Label(self.login_frame, text="账号:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self.login_frame, text="密码:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.login_frame, text="登录", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(self.login_frame, text="注册", command=self.show_register).grid(row=2, column=1, pady=10)
        
        # Register Frame
        self.register_frame = tk.Frame(self.root)
        
        tk.Label(self.register_frame, text="学号:").grid(row=0, column=0)
        self.reg_id_entry = tk.Entry(self.register_frame)
        self.reg_id_entry.grid(row=0, column=1)
        
        tk.Label(self.register_frame, text="姓名:").grid(row=1, column=0)
        self.reg_name_entry = tk.Entry(self.register_frame)
        self.reg_name_entry.grid(row=1, column=1)
        
        tk.Label(self.register_frame, text="密码:").grid(row=2, column=0)
        self.reg_pw_entry = tk.Entry(self.register_frame, show="*")
        self.reg_pw_entry.grid(row=2, column=1)
        
        tk.Label(self.register_frame, text="确认密码:").grid(row=3, column=0)
        self.reg_confirm_entry = tk.Entry(self.register_frame, show="*")
        self.reg_confirm_entry.grid(row=3, column=1)
        
        tk.Button(self.register_frame, text="提交", command=self.register).grid(row=4, column=0, pady=10)
        tk.Button(self.register_frame, text="返回", command=self.show_login).grid(row=4, column=1, pady=10)
    
    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(pady=50)
    
    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(pady=50)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check if admin
        self.cursor.execute("SELECT * FROM 管理员 WHERE 用户名=%s AND 密码=%s", (username, password))
        admin = self.cursor.fetchone()
        if admin:
            messagebox.showinfo("登录成功", "管理员登录成功!")
            return
        
        # Check if student
        self.cursor.execute("SELECT * FROM 学生基本信息表 WHERE 学号=%s AND 密码=%s", (username, password))
        student = self.cursor.fetchone()
        if student:
            messagebox.showinfo("登录成功", f"欢迎, {student[1]}!")
            return
        
        # Check if student
        self.cursor.execute("SELECT * FROM 教师表 WHERE 登陆帐号=%s AND 登陆密码=%s", (username, password))
        teacher = self.cursor.fetchone()
        if teacher:
            messagebox.showinfo("教师登录成功", f"欢迎, {teacher[1]}!")
            return
        
        messagebox.showerror("登录失败", "用户名或密码错误")
    
    def register(self):
        student_id = self.reg_id_entry.get()
        name = self.reg_name_entry.get()
        password = self.reg_pw_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if password != confirm:
            messagebox.showerror("错误", "密码不匹配")
            return
        
        try:
            self.cursor.execute("INSERT INTO 学生基本信息表 (学号, 姓名, 密码) VALUES (%s, %s, %s)", 
                              (student_id, name, password))
            self.db.commit()
            messagebox.showinfo("成功", "注册成功!")
            self.show_login()
        except mysql.connector.Error as err:
            messagebox.showerror("错误", f"注册失败: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentSystem(root)
    root.mainloop()
