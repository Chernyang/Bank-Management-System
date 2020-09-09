from django.forms import *
from .models import Customer, Accounts, Loan, Saveacc, Checkacc, Payinfo
from datetime import datetime, date

class AddCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['cusid', 'cusname', 'cusphone', 'address', 'contact_name', 'contact_phone',
                    'contact_email', 'relation', 'loanres', 'accres']


class AddAccountsForm(ModelForm):
    class Meta:
        model = Accounts
        fields = ['accountid', 'money', 'settime', 'accounttype', 'customer', 'bank']
    
    def clean_money(self):
        money = self.cleaned_data.get('money')
        if money >= 0:
            return money
        else:
            raise ValidationError(u"账户金额不能小于0！", code='money invalid')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['settime'].initial = datetime.now()


class AddLoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['loanid', 'money', 'settime', 'bank', 'loanforcus']
    
    def clean_money(self):
        money = self.cleaned_data.get('money')
        if money > 0:
            return money
        else:
            raise ValidationError(u"贷款金额必须大于0！", code='money invalid')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['settime'].initial = datetime.now()


class CustomerIDForm(Form):
    cusid = CharField(max_length=18)


class AccountIDForm(Form):
    accountid = CharField(max_length=6)


class LoanIDForm(Form):
    loanid = CharField(max_length=4)


class ChangeCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['cusname', 'cusphone', 'address', 'contact_name', 'contact_phone',
                    'contact_email', 'relation', 'loanres', 'accres']


class ChangeAccountForm(ModelForm):
    class Meta:
        model = Accounts
        fields = ['money', 'settime', 'accounttype', 'customer', 'bank']
    
    def clean_money(self):
        money = self.cleaned_data.get('money')
        if money >= 0:
            return money
        else:
            raise ValidationError(u"账户金额不能小于0！", code='money invalid')


class SaveaccForm(ModelForm):
    class Meta:
        model = Saveacc
        fields = ['interestrate', 'savetype']
    
    def clean_interestrate(self):
        interestrate = self.cleaned_data.get('interestrate')
        if interestrate >= 0:
            return interestrate
        else:
            raise ValidationError(u"利率不能小于0！", code='interestrate invalid')


class CheckaccForm(ModelForm):
    class Meta:
        model = Checkacc
        fields = ['overdraft']
    
    def clean_overdraft(self):
        overdraft = self.cleaned_data.get('overdraft')
        if overdraft >= 0:
            return overdraft
        else:
            raise ValidationError(u"透支额不能小于0！", code='overdraft invalid')


class PayinfoForm(ModelForm):
    class Meta:
        model = Payinfo
        fields = ['loan', 'customer', 'money', 'paytime']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paytime'].initial = datetime.now()
    
    def clean_money(self):
        money = self.cleaned_data.get('money')
        if money > 0:
            return money
        else:
            raise ValidationError(u"发行金额必须大于0！", code='money invalid')


class CustomerQuery(Form):
    cusid = CharField(max_length=18, required=False)
    cusname = CharField(max_length=10, required=False)
    cusphone = CharField(max_length=11, required=False)
    address = CharField(max_length=50, required=False)
    contact_name = CharField(max_length=10, required=False)
    accountid = CharField(max_length=6, required=False)
    loanres_name = CharField(max_length=20, required=False, label='loanres name')
    accres_name = CharField(max_length=20, required=False, label='accres name')


class AccountQuery(Form):
    MONEY_RANGE_CHOICES = [
        ('empty', '---------'),
        ('lt', "少于"),
        ('lte', "不多于"),
        ('eq', "等于"),
        ('gte', "不少于"),
        ('gt', "多于")
    ]
    TIME_RANGE_CHOICES = [
        ('empty', '---------'),
        ('lt', "早于"),
        ('lte', "不晚于"),
        ('eq', "等于"),
        ('gte', "不早于"),
        ('gt', "晚于")
    ]
    TYPE_CHOICES = [
        ('empty', '---------'),
        ('saveacc', '储蓄账户'),
        ('checkacc', '支票账户'),
    ]
    accountid = CharField(max_length=6, required=False)
    money_range = ChoiceField(choices=MONEY_RANGE_CHOICES, required=False, widget=Select)
    money = FloatField(required=False)
    settime_range = ChoiceField(choices=TIME_RANGE_CHOICES, required=False, widget=Select,)
    settime = DateTimeField(required=False)
    accounttype = ChoiceField(choices=TYPE_CHOICES, required=False, widget=Select)
    customer_name = CharField(max_length=10, required=False)
    bank_name = CharField(max_length=20, required=False)


class LoanQuery(Form):
    MONEY_RANGE_CHOICES = [
        ('empty', '---------'),
        ('lt', "少于"),
        ('lte', "不多于"),
        ('eq', "等于"),
        ('gte', "不少于"),
        ('gt', "多于")
    ]
    STATE_CHOICES = [
        ('empty', '---------'),
        ('0', "未发放"),
        ('1', "发放中"),
        ('2', "已全部发放")
    ]
    loanid = CharField(max_length=4, required=False)
    money_range = ChoiceField(choices=MONEY_RANGE_CHOICES, required=False, widget=Select)
    money = FloatField(required=False)
    bank_name = CharField(max_length=20, required=False)
    state = ChoiceField(choices=STATE_CHOICES, required=False, widget=Select)  # 0：未发放；1：已发放；2：全部发放
    customer_name = CharField(max_length=10, required=False)