# RSPLATFORM
这是2022年软件杯 A4（遥感解译）赛道参赛作品，我们是来自山东科技大学的 RSIDAS+97012744 队。<br>
注意：如果您也是参赛人员，并看到本库，请勿抄袭，谢谢合作。<br>
1、项目结构介绍：<br>
/遥感解译平台<br>
│  .flaskenv<br>
│  .gitignore<br>
│  app.db<br>
│  config.py<br>
│  map_community.py<br>
│  requirements.txt<br>
│<br>
├─aipro（ai算法整合包 将队友写的ai算法集成为python包便于使用）<br>
│  │  predict_building_change.py<br>
│  │  predict_classification.py<br>
│  │  predict_extract.py<br>
│  │  predict_object_detection.py<br>
│  │  __init__.py<br>
│  │<br>
│  ├─inference_model_building （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）<br>
│  │      .success<br>
│  │      model.pdiparams<br>
│  │      model.pdiparams.info<br>
│  │      model.pdmodel<br>
│  │      model.yml<br>
│  │      pipeline.yml<br>
│  │<br>
│  ├─inference_model_classification （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）<br>
│  │<br>
│  ├─inference_model_extract （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）<br>
│  │<br>
│  ├─inference_model_object_detection （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）<br>
│  <br>
│<br>
├─app（这里是软件的主体部分）<br>
│  │  errors.py<br>
│  │  forms.py<br>
│  │  models.py<br>
│  │  routes.py<br>
│  │  tasks.py<br>
│  │  __init__.py<br>
│  │<br>
│  ├─static（主要是js文件及图片文件）<br>
│  │  │  canvs.js<br>
│  │  │  foto_02.jpg（欢迎图片）<br>
│  │  │  map.js<br>
│  │  │  marvinj-1.0.js<br>
│  │  │  nanobar.min.js<br>
│  │  │<br>
│  │  ├─resultimg/略<br>
│  │  │      <br>
│  │  │<br>
│  │  └─userimg/略<br>
│  │<br>
│  ├─templates(略 主要是html文件)<br>
│  <br>
│  <br>
│<br>
├─migrations(数据库迁移文件 支持修改数据库字段 详见migration库文档)<br>
│  ├─versions（数据库迁移版本文件 略）<br>


2、项目具体运行步骤<br>
# part_1 非异步部分的运行步骤：<br>
  1、请先安装requirements.txt :pip install -r requirements(python版本3.8.5)<br>
     *请于百度网盘（链接："https://pan.baidu.com/s/1O5LEXmQrb3tHwgd23xvXzA "<br>
      提取码：h9qv）自提ai解译算法的模型文件，并放置于aipro文件夹内。（注意缺失该文件会导致app无法成功启动！）<br>
  2、上传的项目包含有数据库文件（app.db）但是数据库中写入的图片路径均已失效（图片体积过大没有上传），您可以先删除该数据库文件（即删除app.db）<br>
      然后执行"(venv) $ flask db upgrade"命令即可生成新的空白数据库。（请确保您的计算机已经安装SQLite）<br>
      或者启动项目后在python交互式终端中键入：<br>
      "from app import db" 回车生效<br>
      "db.create_all()" 回车生效<br>
  3、项目启动，如果您使用的是VScode（推荐使用），请选择打开文件夹，请直接打开“遥感解译平台”主文件夹（不要打开app文件夹，否则flask命令将无法生效），<br>
      直接点击运行，选择flask，选择默认app名称即可开始运行非异步模块，此时您已经可以进入系统页面，可以注册登录上传图片，注意此时点击功能按钮将会导致进度条卡死。<br>
      *如果您使用的是非VScode，请在“遥感解译平台”主文件夹处打开终端（windows--powershell、cmd、Unix--bash）首先设置flask参数，然后执行falsk的run命令。<br>
  （详见flask的官方文档）<br>
 # part_2 异步部分运行步骤：
 注意：本项目实现了异步并发操作（falsk原生不支持异步操作）。本项目借助celery库及Redis服务器实现异步项目，因而需要配置异步服务。<br>
  1、首先请安装Redis服务器，详细教程见"https://Redis.org "。（推荐Unix系统使用，Redis原生不支持Windows，但是可以使用WSL2子系统运行Unix安装上Redis）<br>
  2、在app外部预先启动Redis服务器。<br>
  3、在终端中输入命令"celery -A app.celery worker --loglevel=info -P eventlet -c 10"启动celery服务。（同样是“遥感解译平台”大文件夹）<br>
 现在您已经成功启动项目了。<br>
 如果启动失败，请在github上与我联系。如果觉得还不错欢迎给该项目点赞。<br>
  



