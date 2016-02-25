# backup
备份文件到硬盘和百度云


将文件或目录备份到硬盘和百度云，备份到硬盘时需要存在对应目录。如需添加其它备份方法，添加存在对应接口的类即可


Baidu接口使用说明：

初始化用户名和密码，目前为明文，没有加密
baidu = Baidu({'username': 'baidu_yun_test@sina.com', 'password': 'test123456'})

登陆Baidu账号，目前没有考虑验证码的情况，在通常情况下可以正常登陆
baidu.login()

获得配额信息
baidu.quota()

查看目录下文件
baidu.show('/')

创建目录，若有相同目录则在名称后加上'(1)'的后缀，以此类推
baidu.mkdir('/cc')

删除文件或目录，目录前的'/'一定要带上
baidu.delete('/cc')

检查目录或文件是否存在
baidu.check_path('/abc')

上传文件，第一个参数为文件列表，需使用绝对路径，第二个参数为目标路径
baidu.upload(['F:/a.txt'], '/backup')

获取文件或目录的元信息，第一个参数为文件列表，第二个参数为1且不为目录时包含下载链接
baidu.get_metas(['/abc'], 1)

获取下载链接，参数为文件列表
baidu.get_link(['/abc'])

下载文件，第一个参数为文件列表，第二个参数为目标路径，需使用绝对路径
baidu.download(['/abc'], 'F:/')

以上参数为文件列表的，若仅有一个文件，则可直接使用文件名替代之