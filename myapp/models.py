from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, help_text='邮箱')
    nick_name = models.CharField(max_length=50, blank=True, null=True, help_text='昵称')
    description = models.TextField(blank=True, null=True, help_text='描述')
    avatar = models.URLField(max_length=255, blank=True, null=True, help_text='头像URL')
    
    class Meta:
        db_table = 'user'  # 指定数据库表名
        verbose_name = '用户'
        verbose_name_plural = '用户'
        
    def __str__(self):
        return self.username

class Account(models.Model):
    # 账户类型选项
    ACCOUNT_TYPE_CHOICES = [
        ('CASH', '现金'),
        ('BANK', '银行卡'),
        ('ALIPAY', '支付宝'),
        ('WECHAT', '微信'),
        ('HOUSING_FUND', '公积金'),
    ]

    account_id = models.AutoField(primary_key=True, verbose_name='账户ID')
    account_type = models.CharField(
        max_length=20, 
        choices=ACCOUNT_TYPE_CHOICES, 
        verbose_name='账户类型'
    )
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00, 
        verbose_name='账户余额'
    )
    account_name = models.CharField(
        max_length=100, 
        verbose_name='账户名称'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'account'
        verbose_name = '账户'
        verbose_name_plural = '账户'

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()})"
