from django.db import models


# Create your models here.
class Comments(models.Model):
    content = models.TextField()
    url = models.CharField(max_length=256)
    publisher = models.CharField(max_length=64)
    website_authentication = models.TextField(max_length=64)
    number_of_comments = models.IntegerField()
    number_of_shares = models.IntegerField()
    number_of_likes = models.IntegerField()
    source_platform = models.CharField(max_length=64)

    def __str__(self):
        return self.url


# 创建索引表
class CommentIndex(models.Model):
    cmt_keyword = models.CharField(max_length=256)
    cmt_list = models.TextField()

    def __str__(self):
        return self.cmt_keyword


# 创建可视化图片相关信息表
class CommentView(models.Model):
    img_name = models.CharField(max_length=256)
    img_text = models.TextField()

    def __str__(self):
        return self.img_name


# 创建问答知识库
class QAmap(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


# 创建问答数据集索引
class QAIndex(models.Model):
    keyword = models.CharField(max_length=256)
    ids = models.TextField()

    def __str__(self):
        return self.keyword