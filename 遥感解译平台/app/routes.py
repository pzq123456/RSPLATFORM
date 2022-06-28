import os
import time
from cv2 import DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG
 # 用以给图片加时间戳 保证不会重名

from requests import post
from app import app,db
from flask import render_template, flash, redirect, url_for, request,jsonify
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm,CommentForm,ChangeDETForm

from flask_login import current_user, login_user,logout_user,login_required

from werkzeug.urls import url_parse # 处理next页面问题

from app.models import User,Post,Follow_Post

from datetime import datetime

from collections import OrderedDict

from hashlib import md5 # 生成MD5哈希值

#from app.tasks import change_det


# 注意：本webapp魔改自小队成员的webgis期末大作业 并非抄袭
# 由于比赛时间临近期末 来不及从头再写 
# 经过激烈的组内讨论与深思熟虑 大家发现小组内某成员的大作业刚好与大赛要求存在重合的功能（帖子管理<->遥感图片管理）
# 还望见谅 原作品为某基于百度地图api的社交网站 支持：注册 发帖 跟帖 关注 历时半个月写完




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()




@app.route('/home', methods=['GET', 'POST'])
@login_required # 限制访问 只有登录后才能访问
def home(): # 本页为左侧iframe
    form = PostForm()
    comment_form = CommentForm() # 实例化用户评论类
    change_form = ChangeDETForm() # 实例化变化检测表单

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user,img_path=form.img_path.data)
        db.session.add(post)
        db.session.commit()
        flash('帖子发表成功!')
        return redirect(url_for('home'))

    elif comment_form.validate_on_submit():
            if (comment_form.post_num.data <=0 or comment_form.post_num.data>Post.query.count()):
                flash("请输入正确的图片编号！")
            else:
                follow_post = Follow_Post(body=comment_form.comment.data,
                landlord=Post.query.get(comment_form.post_num.data),
                username=current_user.username)
                db.session.add(follow_post)
                db.session.commit()
                flash('新建长备注成功!')
                return redirect(url_for('home'))

    elif change_form.validate_on_submit(): # 变化检测表单

            current_posts=current_user.followed_posts().all()
            current_posts_id_list=[]
            for p in current_posts:
                current_posts_id_list.append(p.id)
            #获取所有该用户的图像编号 防止越界

            if (change_form.img_1.data <=0 or change_form.img_1.data <=0 or 
            change_form.img_1.data not in current_posts_id_list  or 
            change_form.img_2.data <=0 or change_form.img_2.data <=0 or 
            change_form.img_2.data not in current_posts_id_list
            or change_form.img_1.data==change_form.img_2.data):
                flash("请输入正确的图片编号！")
            else:
                flash('变化检测开始!约一分钟后请手动刷新！')

                #change_det.apply_async(args=[10, 20]) #调用后台任务
                # 异步编程 在此处启动一个worker 但是不会自动刷新
                # 执行完成后
                
                return redirect(url_for('home'))
    

    posts = current_user.followed_posts().all()
    follow_posts = Follow_Post.query.all()
    return render_template("home.html", title='主 页', form=form,
                           posts=posts,follow_posts=follow_posts,comment_form =comment_form,change_form=change_form )




@app.route('/login',methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated: # 先查询已登录用户表
        return redirect(url_for('home')) # 若用户已登录则直接返回home页面
    form = LoginForm() # 否则实例化表单类
    if form.validate_on_submit(): # 表单提交后开始查询数据库
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
        # 若未找到用户 或者密码错误 则闪现以下错误消息
            flash('用户名无效或密码错误')
            return redirect(url_for('login')) # 重定向至登录页面
        # 否则就登录用户 并缓存用户信息
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # 处理next字段参数 方便用户登录后返回该页面
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='登 录', form=form) # 首先返回表单页面


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_map'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜！您已成功注册！')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>') # 用户主页
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    follow_posts = Follow_Post.query.filter_by(username=username).all()
    return render_template('user.html', user=user, posts=posts,follow_posts=follow_posts)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username) # 构造函数
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user',username=current_user.username))# format.(current_user.username)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# 实现用户关注与取消关注

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore',methods=['GET', 'POST'])
@login_required
def explore(): # 正在测试评论组件
    comment_form = CommentForm() # 实例化用户评论类
    posts = Post.query.order_by(Post.timestamp.desc()).all() # 获取所有用户发帖表 并按时间排序
    if comment_form.validate_on_submit():
        if (comment_form.post_num.data <=0 or comment_form.post_num.data>Post.query.count()):
            flash("请输入正确的帖子编号！")
        else:
            follow_post = Follow_Post(body=comment_form.comment.data,
            landlord=Post.query.get(comment_form.post_num.data),
            username=current_user.username)
            db.session.add(follow_post)
            db.session.commit()
            flash('跟帖成功!')
            return redirect(url_for('explore'))

        
    return render_template('home.html', title='Explore', posts=posts,comment_form=comment_form)





# 接下来要针对地图开发出一套地址 实现数据的读写 跟帖等操作




@app.route('/',methods=['GET', 'POST'])
def home_map_ori():
    img_path='static/foto_02.jpg'# 初始欢迎图片
    return render_template('home_map.html',img_path=img_path)


@app.route('/<img_id>',methods=['GET', 'POST'])
def home_map(img_id):
    post=Post.query.filter_by(id=img_id).first_or_404()
    img_path=post.img_path
    return render_template('home_map.html',img_path=img_path)# 主页 展示图片 由于未知原因 该路径只能这样写 否则canvas罢工 可能是画布污染问题 暂时搁置









@app.route('/login/mapview')
def login_map():
    return render_template('login_map.html')

@app.route('/user/mapview')
def user_map():
    return render_template('user_map.html')


@app.route('/explore/mapview')
def explore_map():
    return render_template('explore_map.html')

@app.route('/register/mapview')
def register_map():
    return render_template('register_map.html')

@app.route('/edit_profile/mapview')
def edit_profile_map():
    return render_template('edit_profile_map.html')



# 接下来是地图视图引擎的接口 地图与主业务逻辑是相互独立的关系 
    
def post_to_dict(post):
    return OrderedDict(
        user = post.author.username,
        lon = post.lon,
        lat = post.lat,
        content=post.body,
        digest = md5(post.author.username.lower().encode('utf-8')).hexdigest(),
        post_id=post.id # 获取帖子编号

    )

@app.route('/JSON', methods = ['GET', 'POST'])# 返回数据库中所有记录的post数
@login_required # 只有登录才能看到所有的帖子
def get_json():
   return jsonify(list(map(post_to_dict, Post.query.all())))


@app.route('/map', methods = ['GET', 'POST'])# json数据绘制到地图上
def root_map():
    if request.method == 'POST':
      if not request.form['lon'] or not request.form['lat'] or not request.form['content']:
         flash('Please enter all the fields', 'error')
      else:
         post = Post(lon=request.form['lon'], lat=request.form['lat'],body=request.form['content'],author=current_user )
         db.session.add(post)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('root_map'))
    return render_template('root_map.html')





def follow_post_to_dict(follow_post):
    return OrderedDict(
        user = follow_post.username,
        content=follow_post.body,
        digest = md5(follow_post.username.lower().encode('utf-8')).hexdigest(),
    )



@app.route('/FOLLOWPOST/<post_id>', methods = ['GET', 'POST'])# 返回数据库中所有记录的post数
@login_required # 只有登录才能看到所有的帖子
def get_follow_post(post_id):
    follow_post = Follow_Post.query.filter_by(post_id=post_id).order_by(Follow_Post.timestamp.desc()).all()
    return jsonify(list(map(follow_post_to_dict, follow_post)))
    
    

@app.route('/comment', methods = ['GET', 'POST'])# json数据绘制到地图上
def comment_map():
    if request.method == 'POST':
        follow_post = Follow_Post(body=request.form['content'],
        landlord=Post.query.get(request.form['post_id']),
        username=current_user.username)
        db.session.add(follow_post)
        db.session.commit()
        return redirect(url_for('root_map'))









# 以下是遥感解译平台的路径 为了快速构建应用 暂时先不删除已有的代码

@app.route('/image') # 图像展示与前端预处理页面 理想状态是对每一个图像ID参数返回一个包含该图像的页面
def image():
    return render_template('image.html')
# 注意这是测试另一个前端库的文件



#备用 
@app.route('/IMGPATH/<img_id>', methods = ['GET', 'POST'])# 返回数据库中所有记录的post数
@login_required # 只有登录才能看到所有的帖子
def get_img_path(img_id):# 这里的img_path其实是post的id号
    # follow_post = Follow_Post.query.filter_by(post_id=img_id).order_by(Follow_Post.timestamp.desc()).all()
    post=Post.query.filter_by(id=img_id).first_or_404()
    return post.img_path # 返回请求的图片地址







@app.route('/uploads', methods=['GET', 'POST'])
@login_required # 
def upload(): # 处理上传图片的函数
    t = time.time()# 获取UTC时间

    if request.method == 'POST':
        f = request.files.get('file')#先获取上传的图片文件
        filename=f.filename
        fm=filename.split('.')
        filename=fm[0]+str(round(t))+'.'+fm[1]# 加时间戳防止图片名重复
        f.save(os.path.join('app\\static\\userimg',filename ))# 存入对应图片文件夹

        # 以下是写入用户图片列表

        img_path="static/userimg/"+filename 

        post = Post(author=current_user,img_path= img_path)
        db.session.add(post)
        db.session.commit()
    return render_template('dropzone.html')



