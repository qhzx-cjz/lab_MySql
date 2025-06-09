import tkinter as tk
from tkinter import messagebox
import mysql.connector
import yaml

class StudentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("学生选课管理系统")
        self.root.geometry("400x350")

        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            db_config = config['database']

        # Database connection
        self.db = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
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

        # 身份选择
        self.role_var = tk.StringVar(value="student")
        tk.Label(self.register_frame, text="身份:").grid(row=0, column=0)
        self.role_menu = tk.OptionMenu(self.register_frame, self.role_var, "student", "teacher", command=self.switch_role)
        self.role_menu.grid(row=0, column=1)

        # 学生字段
        self.student_fields = {}
        tk.Label(self.register_frame, text="学号:").grid(row=1, column=0)
        self.student_fields['学号'] = tk.Entry(self.register_frame)
        self.student_fields['学号'].grid(row=1, column=1)

        tk.Label(self.register_frame, text="姓名:").grid(row=2, column=0)
        self.student_fields['姓名'] = tk.Entry(self.register_frame)
        self.student_fields['姓名'].grid(row=2, column=1)

        tk.Label(self.register_frame, text="密码:").grid(row=3, column=0)
        self.student_fields['密码'] = tk.Entry(self.register_frame, show="*")
        self.student_fields['密码'].grid(row=3, column=1)

        tk.Label(self.register_frame, text="确认密码:").grid(row=4, column=0)
        self.student_fields['确认密码'] = tk.Entry(self.register_frame, show="*")
        self.student_fields['确认密码'].grid(row=4, column=1)

        # 教师字段（默认隐藏）
        self.teacher_fields = {}
        tk.Label(self.register_frame, text="学号/登录帐号:").grid(row=1, column=0)
        self.teacher_fields['学号/登陆帐号'] = tk.Entry(self.register_frame)
        self.teacher_fields['学号/登陆帐号'].grid(row=1, column=1)

        tk.Label(self.register_frame, text="姓名:").grid(row=2, column=0)
        self.teacher_fields['教师'] = tk.Entry(self.register_frame)
        self.teacher_fields['教师'].grid(row=2, column=1)

        tk.Label(self.register_frame, text="密码:").grid(row=3, column=0)
        self.teacher_fields['登陆密码'] = tk.Entry(self.register_frame, show="*")
        self.teacher_fields['登陆密码'].grid(row=3, column=1)

        tk.Label(self.register_frame, text="确认密码:").grid(row=4, column=0)
        self.teacher_fields['确认密码'] = tk.Entry(self.register_frame, show="*")
        self.teacher_fields['确认密码'].grid(row=4, column=1)

        tk.Label(self.register_frame, text="院系:").grid(row=5, column=0)
        self.teacher_fields['院系'] = tk.Entry(self.register_frame)
        self.teacher_fields['院系'].grid(row=5, column=1)

        tk.Label(self.register_frame, text="性别:").grid(row=6, column=0)
        self.teacher_fields['性别'] = tk.Entry(self.register_frame)
        self.teacher_fields['性别'].grid(row=6, column=1)

        tk.Label(self.register_frame, text="年龄:").grid(row=7, column=0)
        self.teacher_fields['年龄'] = tk.Entry(self.register_frame)
        self.teacher_fields['年龄'].grid(row=7, column=1)

        tk.Label(self.register_frame, text="职称:").grid(row=8, column=0)
        self.teacher_fields['职称'] = tk.Entry(self.register_frame)
        self.teacher_fields['职称'].grid(row=8, column=1)

        # 提交和返回按钮
        tk.Button(self.register_frame, text="提交", command=self.register).grid(row=9, column=0, pady=10)
        tk.Button(self.register_frame, text="返回", command=self.show_login).grid(row=9, column=1, pady=10)

        # 默认显示学生字段
        self.current_fields = self.student_fields
        self.hide_teacher_fields()

    def switch_role(self, role):
        if role == "student":
            self.hide_teacher_fields()
            self.show_student_fields()
            self.current_fields = self.student_fields
        else:
            self.hide_student_fields()
            self.show_teacher_fields()
            self.current_fields = self.teacher_fields

    def hide_student_fields(self):
        for widget in self.student_fields.values():
            widget.grid_remove()

    def show_student_fields(self):
        for widget in self.student_fields.values():
            widget.grid()

    def hide_teacher_fields(self):
        for widget in self.teacher_fields.values():
            widget.grid_remove()

    def show_teacher_fields(self):
        for widget in self.teacher_fields.values():
            widget.grid()

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(pady=10)

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

        # Check if teacher
        self.cursor.execute("SELECT * FROM 教师表 WHERE 登陆帐号=%s AND 登陆密码=%s", (username, password))
        teacher = self.cursor.fetchone()
        if teacher:
            messagebox.showinfo("教师登录成功", f"欢迎, {teacher[1]}!")
            return

        messagebox.showerror("登录失败", "用户名或密码错误")

    def register(self):
        role = self.role_var.get()
        if role == "student":
            student_id = self.student_fields['学号'].get()
            name = self.student_fields['姓名'].get()
            password = self.student_fields['密码'].get()
            confirm = self.student_fields['确认密码'].get()

            if password != confirm:
                messagebox.showerror("错误", "密码不匹配")
                return

            try:
                self.cursor.execute("INSERT INTO 学生基本信息表 (学号, 姓名, 密码) VALUES (%s, %s, %s)",
                                    (student_id, name, password))
                self.db.commit()
                messagebox.showinfo("成功", "学生注册成功!")
                self.show_login()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"注册失败: {err}")

        elif role == "teacher":
            account = self.teacher_fields['登陆帐号'].get()
            name = self.teacher_fields['教师'].get()
            password = self.teacher_fields['登陆密码'].get()
            confirm = self.teacher_fields['确认密码'].get()
            college = self.teacher_fields['院系'].get()
            gender = self.teacher_fields['性别'].get()
            age = self.teacher_fields['年龄'].get()
            title = self.teacher_fields['职称'].get()

            if password != confirm:
                messagebox.showerror("错误", "密码不匹配")
                return

            try:
                self.cursor.execute(
                    "INSERT INTO 教师表 (登陆帐号, 教师, 登陆密码, 院系, 性别, 年龄, 职称) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (account, name, password, college, gender, age, title)
                )
                self.db.commit()
                messagebox.showinfo("成功", "教师注册成功!")
                self.show_login()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"注册失败: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentSystem(root)
    root.mainloop()