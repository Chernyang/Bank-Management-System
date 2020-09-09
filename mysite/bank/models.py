# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class Bank(models.Model):
    bankname = models.CharField(primary_key=True, max_length=20)
    city = models.CharField(max_length=20)
    money = models.FloatField()

    class Meta:
        managed = True
        db_table = 'bank'


class Department(models.Model):
    departid = models.CharField(db_column='departID', primary_key=True, max_length=4)  # Field name made lowercase.
    departname = models.CharField(max_length=20)
    departtype = models.CharField(max_length=15, blank=True, null=True)
    manager = models.ForeignKey('Employee', models.DO_NOTHING, blank=True, null=True)
    bank = models.ForeignKey(Bank, models.CASCADE, db_column='bank')

    class Meta:
        managed = True
        db_table = 'department'


class Employee(models.Model):
    TYPE_CHOICES = [
        ('manager', '部门经理'),  # manager
        ('staff', '普通员工'),
    ]
    empid = models.CharField(db_column='empID', primary_key=True, max_length=18)  # Field name made lowercase.
    empname = models.CharField(max_length=20)
    empphone = models.CharField(max_length=11, blank=True, null=True)
    empaddr = models.CharField(max_length=50, blank=True, null=True)
    emptype = models.CharField(max_length=10, blank=True, null=True, choices=TYPE_CHOICES)
    empstart = models.DateField()
    depart = models.ForeignKey(Department, models.CASCADE, db_column='depart')

    class Meta:
        managed = True
        db_table = 'employee'


class Customer(models.Model):
    cusid = models.CharField(db_column='cusID', primary_key=True, max_length=18)  # Field name made lowercase.
    cusname = models.CharField(max_length=10)
    cusphone = models.CharField(max_length=11)
    address = models.CharField(max_length=50, blank=True, null=True)
    contact_name = models.CharField(max_length=10)
    contact_phone = models.CharField(max_length=11)
    contact_email = models.CharField(db_column='contact_Email', max_length=20, blank=True, null=True)  # Field name made lowercase.
    relation = models.CharField(max_length=20)
    loanres = models.ForeignKey('Employee', models.DO_NOTHING, db_column='loanres', related_name='loanres', blank=True, null=True)
    accres = models.ForeignKey('Employee', models.DO_NOTHING, db_column='accres', related_name='accres', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'


class Accounts(models.Model):
    TYPE_CHOICES = [
        ('saveacc', '储蓄账户'),
        ('checkacc', '支票账户'),
    ]
    accountid = models.CharField(db_column='accountID', primary_key=True, max_length=6)  # Field name made lowercase.
    money = models.FloatField()
    settime = models.DateTimeField()
    accounttype = models.CharField(max_length=10, choices=TYPE_CHOICES)
    customer = models.ManyToManyField(Customer, through='AccforCus', related_name='account')
    bank = models.ForeignKey(Bank, models.CASCADE, db_column='bank')

    class Meta:
        managed = True
        db_table = 'accounts'


class Saveacc(models.Model):
    accountid = models.OneToOneField(Accounts, models.CASCADE, db_column='accountID', primary_key=True)  # Field name made lowercase.
    interestrate = models.FloatField(blank=True, null=True)
    savetype = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'saveacc'


class Checkacc(models.Model):
    accountid = models.OneToOneField(Accounts, models.CASCADE, db_column='accountID', primary_key=True)  # Field name made lowercase.
    overdraft = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'checkacc'


class Loan(models.Model):
    loanid = models.CharField(db_column='loanID', primary_key=True, max_length=4)  # Field name made lowercase.
    money = models.FloatField(blank=True, null=True)
    bank = models.ForeignKey(Bank, models.CASCADE, db_column='bank')
    settime = models.DateTimeField()
    state = models.CharField(max_length=1, blank=True, null=True, default='0')  # 0：未发放；1：已发放；2：全部发放
    loanforcus = models.ManyToManyField(Customer, related_name='loanforcus')
    pay_info = models.ManyToManyField(Customer, through='Payinfo', related_name='pay_info')

    class Meta:
        managed = True
        db_table = 'loan'


class AccforCus(models.Model):
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    visit = models.DateTimeField(blank=True, null=True)
    class Meta:
        unique_together = ('accounts', 'customer')


class Payinfo(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    money = models.FloatField(blank=True, null=True)
    paytime = models.DateTimeField(blank=True, null=True)
    class Meta:
        unique_together = ('loan', 'customer', 'money', 'paytime')