from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length,NumberRange
# 注意：本webapp魔改自小队成员的webgis期末大作业 并非抄袭
# 由于比赛时间临近期末 来不及从头再写 
# 经过激烈的组内讨论与深思熟虑 大家发现小组内某成员的大作业刚好与大赛要求存在重合的功能（帖子管理<->遥感图片管理）
# 还望见谅 原作品为某基于百度地图api的社交网站 支持：注册 发帖 跟帖 关注 历时半个月写完


#调用WTF库 创建登录表单
class LoginForm(FlaskForm): # 用户登录表单
    username = StringField('用 户 名：', validators=[DataRequired()])#DataRequired()验证内容是否为空
    password = PasswordField('密 码：', validators=[DataRequired()])
    remember_me = BooleanField('记 住 我')
    submit = SubmitField('登 录')


class RegistrationForm(FlaskForm): # 用户注册表单
    username = StringField('用 户 名：', validators=[DataRequired()])
    email = StringField('邮 箱：', validators=[DataRequired(), Email()])
    password = PasswordField('密 码：', validators=[DataRequired()])
    password2 = PasswordField('确 认 密 码：'
                                    , validators=[DataRequired()
                                                    , EqualTo('password')])
    submit = SubmitField('注 册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('已存在该用户名！请换一个！')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱地址已被注册！请换一个！')


class EditProfileForm(FlaskForm): # 用户编辑资料表单
    username = StringField('用 户 名：', validators=[DataRequired()])
    about_me = TextAreaField('个 性 签 名：', validators=[Length(min=0, max=140)])
    submit = SubmitField('提 交')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已存在，请换一个。')

class PostForm(FlaskForm): # 用户发帖表单
    post = TextAreaField('帖 子 内 容：', validators=[
        DataRequired(), Length(min=1, max=800)])
    img_path=TextAreaField('图片相对路径：', validators=[
        DataRequired(), Length(min=1, max=800)])
    
    submit = SubmitField('发布')



# 跟帖表单需要跟在某一个具体的帖子后面
class CommentForm(FlaskForm): # 用户跟帖表单
    post_num=IntegerField('图片系统编号：',validators=[
        DataRequired()])
    comment = TextAreaField('长备注：', validators=[
        DataRequired(), Length(min=5, max=140)])
    submit = SubmitField('添加长备注')


class ChangeDETForm(FlaskForm): # 变化检测提交图表
    img_1=IntegerField('前时像：',validators=[
        DataRequired()])
    img_2=IntegerField('后时像：', validators=[
        DataRequired()])
    submit = SubmitField('开始变化检测')# 用户挑选自己已经上传的图像编号然后提交