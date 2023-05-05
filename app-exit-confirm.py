import flet
from flet import (
    AlertDialog,
    ElevatedButton,
    OutlinedButton,
    Page,
    Text,
    ControlEvent,
    RoundedRectangleBorder,
    ButtonStyle
)


# 在python中并不是所有的语句都会产生作用域，只有当变量在Module(模块)、Class(类)、def （函数）中定义时，才会有作用域。在作用域中的变量，一般只在作用域中才有效。
# 在if-elif -else 、for -else 、while 、try -except try -finallly等关键词的语句块中并不会产生作用域。
# 判断局部变量是否存在只能使用in方法判断locals()，不能使用hasattr因为hasattr只能判断class对象，不能判断dict字典，深坑
# flet的默认退出行为并不会释放申请的资源，需要主动控制生命周期才行

def main(page:Page):
    page.title = "Demo"

    def window_event(e: ControlEvent):
        if e.data == 'close':
            page.dialog = confirm_dialog  # 局部作用域 ~>嵌套作用域 ~>全局作用域 ~>内置作用域
            confirm_dialog.open = True
            page.update()
            

    page.window_prevent_close = True #设置了这个才会有close事件
    page.on_window_event = window_event

    def yes_click(e: ControlEvent):
        page.window_destroy()

    def no_click(e: ControlEvent):
        confirm_dialog.open = False
        page.update()

    confirm_dialog = AlertDialog(
        modal=True,
        title=Text('请确认'),
        content=Text('确认需要退出程序？？？'),
        shape=RoundedRectangleBorder(radius=5),
        actions= [
            ElevatedButton('是的', on_click=yes_click, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5))),
            OutlinedButton('不要', on_click=no_click, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)))
        ],
        actions_alignment='end'
    )

    page.add(Text("这是一个演示如何进行退出时如何进行确认和资源释放的演示"))

flet.app(target=main, view=flet.FLET_APP)