import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect,url_for, jsonify

from app import celery
from app import app

from app import db
from app.models import User,Post,Follow_Post

from aipro import predict_classification,predict_building_change,predict_extract # 调用ai算法
from flask_login import current_user


# 本文件是异步算法接口加路径 测试完毕

# flask异步算法调用接口区：

# 测试页面
@app.route('/123', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
# 测试页面 end

# 测试算法
@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/classification/<img_id>', methods=['GET', 'POST']) # 地物分类任务接口
def classification(img_id):
    args=[]
    args=img_path_parse(img_id,"cla")
    task = classification.apply_async(args=args) # 带参数
    return jsonify({}), 202, {'Location': url_for('classificationstatus',
                                                  task_id=task.id)}


@app.route('/extract/<img_id>', methods=['GET', 'POST']) # 地物检测任务接口
def extract(img_id):
    args=[]
    args=img_path_parse(img_id,"ext")
    task = extract.apply_async(args=args) # 带参数
    return jsonify({}), 202, {'Location': url_for('extractstatus',
                                                  task_id=task.id)}


#@app.route('/change/<img_id>', methods=['GET', 'POST']) # 变化检测任务接口
#def extract(img_id):
 #   args=[]
  #  args=img_path_parse(img_id,"ext")
   # task = extract.apply_async(args=args) # 带参数
    #return jsonify({}), 202, {'Location': url_for('extractstatus',
     #                                             task_id=task.id)}


# ======end============ #



# flask异步算法调用状态查询接口区


@app.route('/status/<task_id>')
def taskstatus(task_id):

    task = long_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }

    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)



@app.route('/classificationstatus/<task_id>')
def classificationstatus(task_id):
    response=status_check(task_id)
    return jsonify(response)


@app.route('/extractstatus/<task_id>')
def extractstatus(task_id):
    response=status_check(task_id)
    return jsonify(response)

# ======end============ #



# 异步算法函数封装区域：

@celery.task(bind=True)
def long_task(self):

    """Background task that runs a long function with progress reports."""
    '''后台长时间运行代码 附带代码状态报告'''

    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''

    total = random.randint(10, 50)

    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}






@celery.task(bind=True) # 地物检测接口
def extract(self,img_id,img_path,save_path_0,save_path_1):
    
    # 安慰剂 空循环 让ai算法看起来没有卡死
    message = '正在执行地物检测算法，请稍等……'
    for i in range(5):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': 100,
                                'status': message})
        time.sleep(1)
    
    message = '核验结果是否存在，请稍等……'
    self.update_state(state='PROGRESS',
                          meta={'current': 20, 'total': 100,
                                'status': message})
    time.sleep(2)
    
    if not os.path.exists(save_path_1): # 不存在才会生成

        run= predict_extract.Predict_extract(img_path,save_path_1)
        run.Predict()
        if not os.path.exists(save_path_1): # 不存在才会生成
            run.Save() # 存储图片之前再检查一次 防止用户并发存储多次
            # ai算法装填完毕
            message = '载入并启动模型，请稍等……'
            # 当ai算法调用完成时 设定状态为85%
            self.update_state(state='PROGRESS',
                                meta={'current': 85, 'total': 100,
                                        'status': message})
            return {'current': 100, 'total': 100, 'status': img_id+'号图片地物检测算法执行完成！',
                'result': save_path_0} # 最后返回结果
        else :
            message = '并发存储，请不要多次点击该按钮……'
            # 当ai算法调用完成时 设定状态为85%
            self.update_state(state='PROGRESS',
                                meta={'current': 85, 'total': 100,
                                        'status': message})
            return {'current': 100, 'total': 100, 'status': '算法执行失败，请勿多次连续点击！'}
               # 'result': save_path_0} # 最后返回结果
    else:
        message = '已存在该结果，请稍等……'
        self.update_state(state='PROGRESS',
                          meta={'current': 20, 'total': 100,
                                'status': message})
        time.sleep(2)
        return {'current': 100, 'total': 100, 'status': '已存在该结果，仔细查一查之前的结果吧！'}
               # 'result': save_path_0} # 最后返回结果


@celery.task(bind=True) # 地物分类接口
def classification(self,img_id,img_path,save_path_0,save_path_1):
    
    # 安慰剂 空循环 让ai算法看起来没有卡死
    message = '正在执行地物分类算法，请稍等……'
    for i in range(5):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': 100,
                                'status': message})
        time.sleep(1)
    

    message = '核验结果是否存在，请稍等……'
    self.update_state(state='PROGRESS',
                          meta={'current': 20, 'total': 100,
                                'status': message})
    time.sleep(2)
    
    if not os.path.exists(save_path_1): # 不存在才会生成
        run = predict_classification.Predict_classification(img_path,save_path_1)
        run.Predict()
        if not os.path.exists(save_path_1): # 不存在才会生成
            run.Save() # 存储图片之前再检查一次 防止用户并发存储多次
            # ai算法装填完毕
            message = '载入并启动模型，请稍等……'
            # 当ai算法调用完成时 设定状态为85%
            self.update_state(state='PROGRESS',
                                meta={'current': 85, 'total': 100,
                                        'status': message})
            return {'current': 100, 'total': 100, 'status': img_id+'号图片地物分类算法执行完成！',
                'result': save_path_0} # 只有这里会返回图片路径
        else :
            message = '并发存储，请不要多次点击该按钮……'
            # 当ai算法调用完成时 设定状态为85%
            self.update_state(state='PROGRESS',
                                meta={'current': 85, 'total': 100,
                                        'status': message})
            return {'current': 100, 'total': 100, 'status': '算法执行失败，请勿多次连续点击！'}
                #'result': save_path_0} # 最后返回结果
    else:
        message = '已存在该结果，请稍等……'
        self.update_state(state='PROGRESS',
                          meta={'current': 20, 'total': 100,
                                'status': message})
        time.sleep(2)
        return {'current': 100, 'total': 100, 'status': '已存在该结果，仔细查一查之前的结果吧！'}
                #'result': save_path_0} # 最后返回结果


# ======end============ #



# 封装函数D
def img_path_parse(img_id,task_name):

    post=Post.query.filter_by(id=img_id).first_or_404()
    img_path=post.img_path

    fm0=img_path.split('.')
    fm3=""
    fm3=fm0[0]
    fm1=fm3.split('/') # 提取图片名
    filename=fm1[2]+task_name+'.png' # 重写图片名 加上后缀cla表示地物分类的结果

    img_path="./app/"+img_path# 相对于ai算法的路径
    # 遥感影像

    save_path_0 = "static/resultimg/"+filename # 相对于flask的相对路径

    save_path_1 = "./app/"+"static/resultimg/"+filename # 相对于ai算法的
    return [img_id,img_path,save_path_0,save_path_1]

def status_check(task_id):

    task = classification.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }

    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            # 放在此处存储
            post = Post(author=current_user,img_path=task.info['result'],body=task.info['status'])
            db.session.add(post)
            db.session.commit()

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return response