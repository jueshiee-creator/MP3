def caidan(root):
    menu = Menu(root)
    submenu1=Menu(menu,tearoff=0)
    submenu1.add_command(label='关于作者', command=author)
    submenu1.add_command(label='版本信息', command=introduce)
    menu.add_cascade(menu=submenu1,label='查看')

    submenu2=Menu(menu,tearoff=0)
    submenu2.add_command(label='复制')                
    submenu2.add_command(label='粘粘')
    menu.add_cascade(menu=submenu2,label='编辑')

    submenu3=Menu(menu,tearoff=0)
    # submenu3.add_command(label='使用手册')
    submenu3_1=Menu(menu,tearoff=0)
    submenu3_1.add_command(label='操作目的')
    submenu3_1.add_command(label='操作方法')
    submenu3.add_cascade(menu=submenu3_1, label='使用手册')

    submenu3.add_separator()                        # 下拉菜单中加分隔线
    submenu3.add_command(label='附加功能',command=bomb)
    menu.add_cascade(menu=submenu3,label='帮助')
    
    root.config(menu=menu)