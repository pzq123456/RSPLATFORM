# RSPLATFORM
这是2022年软件杯 A4（遥感解译）赛道参赛作品，我们是来自山东科技大学的 RSIDAS+97012744 队。
1、项目结构介绍：
/遥感解译平台
│  .flaskenv
│  .gitignore
│  app.db
│  config.py
│  map_community.py
│  requirements.txt
│
├─aipro
│  │  predict_building_change.py
│  │  predict_classification.py
│  │  predict_extract.py
│  │  predict_object_detection.py
│  │  __init__.py
│  │
│  ├─inference_model_building （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）
│  │      .success
│  │      model.pdiparams
│  │      model.pdiparams.info
│  │      model.pdmodel
│  │      model.yml
│  │      pipeline.yml
│  │
│  ├─inference_model_classification （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）
│  │      .success
│  │      model.pdiparams
│  │      model.pdiparams.info
│  │      model.pdmodel
│  │      model.yml
│  │      pipeline.yml
│  │
│  ├─inference_model_extract （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）
│  │      .success
│  │      model.pdiparams
│  │      model.pdiparams.info
│  │      model.pdmodel
│  │      model.yml
│  │      pipeline.yml
│  │
│  ├─inference_model_object_detection （注意：由于模型文件过大 github上传失败 请于百度网盘自提 请复制于该目录下 否则算法无法运行）
│        .success
│        model.pdiparams
│        model.pdiparams.info
│        model.pdmodel
│        model.yml
│        pipeline.yml
│  
│
├─app（这里是软件的主体部分）
│  │  errors.py
│  │  forms.py
│  │  models.py
│  │  routes.py
│  │  tasks.py
│  │  __init__.py
│  │
│  ├─static
│  │  │  canvs.js
│  │  │  foto_02.jpg
│  │  │  map.js
│  │  │  marvinj-1.0.js
│  │  │  nanobar.min.js
│  │  │
│  │  ├─resultimg/略
│  │  │      
│  │  │
│  │  └─userimg/略
|  |
│  │
│  ├─templates
│  │      404.html
│  │      500.html
│  │      base.html
│  │      dropzone.html
│  │      edit_profile.html
│  │      edit_profile_map.html
│  │      explore_map.html
│  │      home.html
│  │      home_map.html
│  │      image.html
│  │      index.html
│  │      login.html
│  │      login_map.html
│  │      map_card1.html
│  │      register.html
│  │      register_map.html
│  │      root_map.html
│  │      user.html
│  │      user_map.html
│  │      _comment.html
│  │      _comment_post.html
│  │      _funbut.html
│  │      _imgpan.html
│         _post.html
│  
│  
│
├─migrations
│  │  alembic.ini
│  │  env.py
│  │  README
│  │  script.py.mako
│  │
│  ├─versions
│  │  │  006207ba3dce_followers.py
│  │  │  0e128da4c8de_new_fields_in_user_model.py
│  │  │  3cb61ba66270_follpost_img_path.py
│  │  │  b33fcf4ecff9_posts_table.py
│  │  │  c50aabbd817e_新增字段.py
│  │  │  d45e0cc5224d_.py
│  │  │
│  │  └─__pycache__
│  │          006207ba3dce_followers.cpython-38.pyc
│  │          006207ba3dce_followers.cpython-39.pyc
│  │          0e128da4c8de_new_fields_in_user_model.cpython-38.pyc
│  │          0e128da4c8de_new_fields_in_user_model.cpython-39.pyc
│  │          3cb61ba66270_follpost_img_path.cpython-38.pyc
│  │          b33fcf4ecff9_posts_table.cpython-38.pyc
│  │          b33fcf4ecff9_posts_table.cpython-39.pyc
│  │          c50aabbd817e_新增字段.cpython-38.pyc
│  │          c50aabbd817e_新增字段.cpython-39.pyc
│  │          d45e0cc5224d_.cpython-38.pyc
│  │          d45e0cc5224d_.cpython-39.pyc
│  │
2、项目具体运行步骤
part_1非异步部分的运行步骤：
  1、请先安装requirements.txt :pip install -r requirements(python版本3.8.5)
     *请于百度网盘（链接：https://pan.baidu.com/s/1O5LEXmQrb3tHwgd23xvXzA 
      提取码：h9qv）自提ai解译算法的模型文件，并放置于aipro文件夹内。（注意缺失该文件会导致app无法成功启动！）
  2、上传的项目包含有数据库文件（app.db）但是数据库中写入的图片路径均已失效（图片体积过大没有上传），您可以先删除该数据库文件（即删除app.db）
  然后执行"(venv) $ flask db upgrade"命令即可生成新的空白数据库。（请确保您的计算机已经安装SQLite）
  3、项目启动，如果您使用的是VScode（推荐使用），请选择打开文件夹，请直接打开“遥感解译平台”主文件夹（不要打开app文件夹，否则flask命令将无法生效），
  直接点击运行，选择flask，选择默认app名称即可开始运行非异步模块，此时您已经可以进入系统页面，可以注册登录上传图片，注意此时点击功能按钮将会导致进度条卡死。
  *如果您使用的是非VScode，请在“遥感解译平台”主文件夹处打开终端（windows--powershell、cmd、Unix--bash）首先设置flask参数，然后执行falsk的run命令。
  （详见flask的官方文档）
 part_2异步部分运行步骤：本项目实现了异步并发操作（falsk原生不支持异步操作）。本项目借助celery库及Redis服务器实现异步项目，因而需要配置异步服务。
  1、首先请安装Redis服务器，详细教程见Redis.org。（推荐Unix系统使用，Redis原生不支持Windows，但是可以使用WSL2子系统运行Unix安装上Redis）
  2、在app外部预先启动Redis服务器。
  3、在终端中输入命令"celery -A app.celery worker --loglevel=info -P eventlet -c 10"启动celery服务。（同样是“遥感解译平台”大文件夹）
 现在您已经成功启动项目了。如果启动失败，请在github上与我联系。如果觉得还不错欢迎给该项目点赞。
  



