#import csv
#from multiprocessing import connection

import tkinter
#import sqlite3

###############################################################################

import tkinter as tk 
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors

#########################################################################

# ユーザー情報を登録するDB名
#DB_NAME = "pre"
DB_NAME = "app01"


class Login():

    ############################################################################

    def connect2(self):
        connection = pymysql.connect(host = '127.0.0.1',
                                    user = 'root',
                                    password = '',
                                    db = DB_NAME,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor)
        try:
            # トランザクション開始
            connection.begin()

            with connection.cursor() as cursor:
                cursor = connection.cursor()

                sql1 = "select * from user where (username, password) = ('{}', '{}');".format(self.name_entry.get(), self.pass_entry.get())
                cursor.execute(sql1)
                tmp = cursor.fetchall()

                if len(tmp) != 0:
                    # 表示中のウィジェットを一旦削除
                    for widget in self.widgets:
                        widget.destroy()
                
                    # "ようこそ！"メッセージを表示
                    self.message = tk.Label(
                    self.master,
                    text = "ログインしました。",
                    font = ("",20)
                    )

                    self.message.place(
                    x = self.master.winfo_width() // 2,
                    y = self.master.winfo_height() // 2,
                    anchor = tk.CENTER
                    )

                    # 少しディレイを入れてredisplayを実行
                    self.master.after(1000, app.destroy)

                else:
                    # 表示中のウィジェットを一旦削除
                    for widget in self.widgets:
                        widget.destroy()

                  # "誰？"メッセージを表示
                    self.message = tk.Label(
                        self.master,
                        text = "誰？",
                        font = ("", 30)
                    )
                    self.message.place(
                        x = self.master.winfo_width() // 2,
                        y = self.master.winfo_height() // 2,
                        anchor=tk.CENTER
                    )

                    # 少しディレイを入れてredisplayを実行
                    self.master.after(1000, self.redisplay)

            connection.commit()

        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()



    def __init__(self, master, main):
        # ログインを制御する

        self.master = master

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()
    
    def create_widgets(self):
        # ウィジェットの作成・配置

        # ユーザー名入力用のウィジェット
        self.name_label = tkinter.Label(

            self.master, 
            text = "ユーザー名"

        )

        self.name_label.grid(

            row = 0, 
            column = 0

        )

        self.widgets.append(self.name_label)


        self.name_entry = tkinter.Entry(self.master)
        self.name_entry.grid(

            row = 0, 
            column = 1

        )

        self.widgets.append(self.name_entry)


        # パスワード入力用のウィジェット
        self.pass_label = tkinter.Label(

            self.master, 
            text = "パスワード"

        )

        self.widgets.append(self.pass_label)

        self.pass_entry = tkinter.Entry(

            self.master, 
            show = "*"

        )

        self.pass_entry.grid(

            row = 1, 
            column = 1

        )

        self.widgets.append(self.pass_entry)


        # ログインボタン
        self.login_button = tkinter.Button(

            self.master, 
            text = "ログイン", 
            command = self.connect2
            #command = self.login

        )

        self.login_button.grid(

            row = 2, 
            column = 0, 
            columnspan = 2, 

        )

        self.widgets.append(self.login_button)


        # 登録ボタン
        self.register_button = tkinter.Button(

            self.master, 
            text = "登録", 
            command = self.register
        )

        self.register_button.grid(

            row = 3, 
            column = 0, 
            columnspan = 2, 

        )

        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tkinter.CENTER)



    def login(self):

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        if self.check(username, password):

            # ログインユーザー名を設定
            self.login_name = username


            self.success()
        else:
            self.fail()


    def check(self, username, password):

        username = self.name_entry.get()
        password = self.pass_entry.get()


        self.connection = pymysql.connect(host = '127.0.0.1',
                                    user = 'root',
                                    password = '',
                                    db = DB_NAME,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor)

        try:
            self.connection.begin()

            with self.connection.cursor() as self.cursor:
                check = self.cursor.execute(
                    "SELECT * FROM user WHERE username=? and password=?", 
                    [username, password]
                )

                user_list = check.fetchall()

                if user_list:
                    ret = True
                else:
                    ret = False

                return ret


        except Exception as e:
            print('error:', e)
            self.connection.rollback()
        finally:
            self.connection.close()


    def save(self, username, password):

        username = self.name_entry.get()
        password = self.pass_entry.get()

        self.connection = pymysql.connect(host = '127.0.0.1',
                                    user = 'root',
                                    password = '',
                                    db = DB_NAME,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor)

        try:
            self.connection.begin()

            with self.connection.cursor() as self.cursor:
                # 取得した情報を DB に追記
                save = "INSERT INTO user (username, password) VALUES('{}', '{}')".format(username, password)

                self.cursor.execute(save)




                for widget in self.widgets:
                    widget.destroy()

                self.message = tkinter.Label(
                self.master, 
                text="登録完了", 
                font=("", 30)
                )

                self.message.place(
                    x=self.master.winfo_width() // 2,
                    y=self.master.winfo_height() // 2,
                    anchor=tk.CENTER
                )

                # 少しディレイを入れてredisplayを実行
                self.master.after(1000, self.redisplay)

            self.connection.commit()

        except Exception as e:
            print('error:', e)
            self.connection.rollback()
        finally:
            self.connection.close()

    

    def register(self):
        # 入力された情報を Entry ウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        self.save(username, password)

        # 少しディレイを入れて redisplay を実行
        self.master.after(1000, self.redisplay)

    def fail(self):
        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tkinter.Label(
            self.master, 
            text="誰？", 
            font=("", 30)
        )
        self.message.place(
            x=self.master.winfo_width() // 2, 
            y=self.master.winfo_height() // 2, 
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れて redisplay を実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):

        # "誰？"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()

    
    def success(self):
        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tkinter.Label(
            self.master, 
            text="ようこそ！", 
            font=("", 40)
        )
        self.message.place(
            x = self.master.winfo_width() // 2, 
            y = self.master.winfo_height() // 2, 
            anchor=tkinter.CENTER
        )

        # 少しディレイをいれて redisplay を実行
        self.master.destroy()

    def main_start(self):

        # アプリ本体を起動
        self.main.start(self.login_name)



class MainAppli():

    def __init__(self, master):
        self.master = master

        # ログインは完了していないのでウィジェットは作成しない

    def start(self, login_name):

        # ログインユーザー名を表示する
        self.message = tkinter.Label(
            self.master, 
            font=("", 10), 
            text=login_name + "でログイン中"
        )
        self.message.pack()


app = tkinter.Tk()


# メインウィンドウのサイズ設定
app.geometry("300x200")

#アプリ本体のインスタンス生成
main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
login = Login(app, main)



        # 必要に応じてウィジェット作成やイベントの設定なども行う
###############################################################################


WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class YicDiary:
    def __init__(self, root):
        root.title('予定管理アプリ')
        root.geometry('520x280')
        root.resizable(0, 0)
        root.grid_columnconfigure((0, 1), weight=1)
        self.sub_win = None

        self.year  = da.date.today().year
        self.mon = da.date.today().month
        self.today = da.date.today().day

        self.title = None
        # 左側のカレンダー部分
        leftFrame = tk.Frame(root)
        leftFrame.grid(row=0, column=0)
        self.leftBuild(leftFrame)

    # 右側の予定管理部分
        rightFrame = tk.Frame(root)
        rightFrame.grid(row=0, column=1)
        self.rightBuild(rightFrame)


#-----------------------------------------------------------------
# アプリの左側の領域を作成する
#
# leftFrame: 左側のフレーム
    def leftBuild(self, leftFrame):
        self.viewLabel = tk.Label(leftFrame, font=('', 10))
        beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
        nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

        self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
        beforButton.grid(row=0, column=0, pady=10, padx=10)
        nextButton.grid(row=0, column=2, pady=10, padx=10)

        self.calendar = tk.Frame(leftFrame)
        self.calendar.grid(row=1, column=0, columnspan=3)
        self.disp(0)


#-----------------------------------------------------------------
# アプリの右側の領域を作成する
#
# rightFrame: 右側のフレーム
    def rightBuild(self, rightFrame):
        r1_frame = tk.Frame(rightFrame)
        r1_frame.grid(row=0, column=0, pady=10)
        r2_frame = tk.Frame(rightFrame)
        r2_frame.grid(row=5, column=0, pady=10)

        temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
        self.title = tk.Label(r1_frame, text=temp, font=('', 12))
        self.title.grid(row=0, column=0, padx=20)

        self.title2 = tk.Label(r2_frame, text=temp, font=('', 10))
        self.title2.grid(row=0, column=0, padx=10)

        button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
        button.grid(row=0, column=1)

        self.r2_frame = tk.Frame(rightFrame)
        self.r2_frame.grid(row=1, column=0)

        self.schedule()


#-----------------------------------------------------------------
# アプリの右側の領域に予定を表示する
#

    def schedule(self):

        self.title2['text'] = '{}'.format(self.dbmemo())

        # ウィジェットを廃棄
        #for widget in self.r2_frame.winfo_children():
        #    widget.destroy()
    
        # データベースに予定の問い合わせを行う
        lbl = tkinter.Label()
        lbl.place(x = 30, y = 70)

    def dbmemo(self):

        memo = ''

        connection = pymysql.connect(host='127.0.0.1',
                                   user='root',
                                   password= '',
                                   db= DB_NAME,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

        try:
            # トランザクション関数
            connection.begin()

            with connection.cursor() as cursor:
                cursor = connection.cursor()


                sql = "select memo from schedule where days = '{}-{}-{}'".format(self.year, self.mon, self.today)

                print(sql)


                # SQLの実行
                cursor.execute(sql)

                memos = cursor.fetchall()
                for i, text in enumerate(memos):
                    print(text["memo"])
                    memo = memo + '\n' + text["memo"]




            connection.commit()

        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()  

        return memo

    #pass

#'''
#-----------------------------------------------------------------
# カレンダーを表示する
#
# argv: -1 = 前月
#        0 = 今月（起動時のみ）
#        1 = 次月
    def disp(self, argv):
        self.mon = self.mon + argv
        if self.mon < 1:
            self.mon, self.year = 12, self.year - 1
        elif self.mon > 12:
            self.mon, self.year = 1, self.year + 1

        self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

        cal = ca.Calendar(firstweekday=6)
        cal = cal.monthdayscalendar(self.year, self.mon)

        # ウィジットを廃棄
        for widget in self.calendar.winfo_children():
            widget.destroy()

        # 見出し行
        r = 0
        for i, x in enumerate(WEEK):
            label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
            label_day.grid(row=r, column=i, pady=1)

        # カレンダー本体
        r = 1
        for week in cal:
            for i, day in enumerate(week):
                if day == 0: day = ' ' 
                label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
                if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
                    label_day['relief'] = 'solid'
                label_day.bind('<Button-1>', self.click)
                label_day.grid(row=r, column=i, padx=2, pady=1)
            r = r + 1

        # 画面右側の表示を変更
        if self.title is not None:
            self.today = 1
            self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
#'''

    #-----------------------------------------------------------------
    # 予定を追加したときに呼び出されるメソッド
    #
    def add(self):
        if self.sub_win == None or not self.sub_win.winfo_exists():
            self.sub_win = tk.Toplevel()
            self.sub_win.geometry("300x300")
            self.sub_win.resizable(0, 0)

            # ラベル
            sb1_frame = tk.Frame(self.sub_win)
            sb1_frame.grid(row=0, column=0)
            temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
            title = tk.Label(sb1_frame, text=temp, font=('', 12))
            title.grid(row=0, column=0)

            # 予定種別（コンボボックス）
            sb2_frame = tk.Frame(self.sub_win)
            sb2_frame.grid(row=1, column=0)
            label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
            label_1.grid(row=0, column=0, sticky=tk.W)
            #combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
            self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
            #combo.current(0)
            self.combo.current(0)
            #combo.grid(row=0, column=1)
            self.combo.grid(row=0, column=1)



            # テキストエリア（垂直スクロール付）
            sb3_frame = tk.Frame(self.sub_win)
            sb3_frame.grid(row=2, column=0)
            #text = tk.Text(sb3_frame, width=40, height=15)
            self.text = tk.Text(sb3_frame, width=40, height=15)
            #text.grid(row=0, column=0)
            self.text.grid(row=0, column=0)
            #scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=text.yview)
            scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
            scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
            #text["yscrollcommand"] = scroll_v.set
            self.text["yscrollcommand"] = scroll_v.set

            # 保存ボタン
            sb4_frame = tk.Frame(self.sub_win)
            sb4_frame.grid(row=3, column=0, sticky=tk.NE)
            button = tk.Button(sb4_frame, text='保存', command = lambda:self.done())
            button.pack(padx=10, pady=10)
        elif self.sub_win != None and self.sub_win.winfo_exists():
            self.sub_win.lift()



    def done(self):

    # 日付
        days = '{}-{}-{}'.format(self.year, self.mon, self.today)
        print(days)

        # 種別
        kinds = self.combo.get()
        print(kinds)

        # 別表にしている人は、外部キーとして呼び出す値を得る
        # getKey()メソッド（または関数）は自作する
        #foreignKey = getKey(kinds)

        # 予定詳細
        memo = self.text.get("1.0", "end")
        memo = memo.replace('\n',' ')
        print(memo) 

        # データベースに新規予定を挿入する
        connection = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password= '',
                                    db= DB_NAME,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            # トランザクション関数
            connection.begin()

            with connection.cursor() as cursor:
                cursor = connection.cursor()


                sql = "select kindsID from kind where kinds = '{}'".format(kinds)

                print(sql)


                # SQLの実行
                cursor.execute(sql)

                rows = cursor.fetchall()
                for i, row in enumerate(rows):
                    print(row["kindsID"])

                kindsID = row["kindsID"]

                sql = "insert into schedule (days, kindsID, memo) values('{}', {}, '{}')".format(days, kindsID, memo)

                print(sql)

                # SQLの実行
                cursor.execute(sql)

                results = cursor.fetchall()
                for i, row in enumerate(results):
                    print(i, row)
            
                sql = "select * from schedule"

                print(sql)

                # SQLの実行
                cursor.execute(sql)

                results = cursor.fetchall()
                for i, row in enumerate(results):
                    print(i, row)
            
            connection.commit()

        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()

        self.schedule()

        #pass

        self.sub_win.destroy()


    #-----------------------------------------------------------------
    # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
    #
    # event: 左クリックイベント <Button-1>
    def click(self, event):
        day = event.widget['text']
        if day != ' ':
            self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
            self.today = day


def Main():
    app.mainloop()
    root = tk.Tk()
    YicDiary(root)
    root.mainloop()

if __name__ == '__main__':
  Main()



###############################################################################

#app = tk.Tk()


# メインウィンドウのサイズ設定
#app.geometry("300*200")

#アプリ本体のインスタンス生成
#main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
#login = Login(app, main)


#app.mainloop()
