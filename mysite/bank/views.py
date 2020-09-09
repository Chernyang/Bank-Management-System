from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.db.models import Sum
from .models import *
from .forms import *
from datetime import datetime
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def index(request):
    """主页"""
    return render(request, 'bank/index.html')


def add_customer(request):
    """客户注册"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = AddCustomerForm()
    else:
        # POST提交的数据，对数据进行处理
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "注册成功！"
            form = AddCustomerForm()
        else:
            error_message = "注册失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/add_customer.html', context)


def add_account(request):
    """开设账户"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = AddAccountsForm()
    else:
        # POST提交的数据，对数据进行处理
        form = AddAccountsForm(request.POST)
        if form.is_valid():
            form.save()
            accountid = form.cleaned_data['accountid']
            accounttype = form.cleaned_data['accounttype']
            acc = Accounts.objects.get(accountid=accountid)
            if accounttype == 'saveacc':
                saveacc = Saveacc(accountid=acc)
                saveacc.save()
                form = SaveaccForm()
                context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
                return render(request, 'bank/add_saveacc.html', context)
            else:
                checkacc = Checkacc(accountid=acc)
                checkacc.save()
                form = CheckaccForm()
                context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
                return render(request, 'bank/add_checkacc.html', context)
        else:
            error_message = "注册失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/add_account.html', context)


def add_saveacc(request, accountid):
    """输入存储账户信息"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = SaveaccForm()
    else:
        form = SaveaccForm(request.POST)
        if form.is_valid():
            interestrate = form.cleaned_data['interestrate']
            savetype = form.cleaned_data['savetype']
            Saveacc.objects.filter(accountid=accountid).update(interestrate=interestrate, savetype=savetype)
            success_message = "注册成功！"
            form = AddAccountsForm()
            context = {'form': form, 'error_message': error_message, 'success_message': success_message}
            return render(request, 'bank/add_account.html', context)
        else:
            error_message = "注册失败！"

    context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
    return render(request, 'bank/add_saveacc.html', context)


def add_checkacc(request, accountid):
    """输入支票账户信息"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = CheckaccForm()
    else:
        form = CheckaccForm(request.POST)
        if form.is_valid():
            overdraft = form.cleaned_data['overdraft']
            Checkacc.objects.filter(accountid=accountid).update(overdraft=overdraft)
            success_message = "注册成功！"
            form = AddAccountsForm()
            context = {'form': form, 'error_message': error_message, 'success_message': success_message}
            return render(request, 'bank/add_account.html', context)
        else:
            error_message = "注册失败！"

    context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
    return render(request, 'bank/add_checkacc.html', context)


def add_loan(request):
    """增加贷款"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = AddLoanForm()
    else:
        # POST提交的数据，对数据进行处理
        form = AddLoanForm(request.POST)
        if form.is_valid():
            form.save()
            Payinfo.objects.filter(money__isnull=True).delete()
            success_message = "增加成功！"
            form = AddLoanForm()
        else:
            error_message = "增加失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/add_loan.html', context)


def delete_customer(request):
    """删除客户"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = CustomerIDForm()
    else:
        # POST提交的数据，对数据进行处理
        form = CustomerIDForm(request.POST)
        if form.is_valid():
            cusID = form.cleaned_data['cusid']
            cus = Customer.objects.filter(cusid=cusID)
            if not cus.exists():
                error_message = "删除失败！该客户不存在！"
            elif Accounts.objects.filter(customer__cusid=cusID).exists():
                error_message = "删除失败！该客户存在着关联帐户，不可删除！"
            elif Loan.objects.filter(loanforcus__cusid=cusID).exists():
                error_message = "删除失败！该客户存在着贷款记录，不可删除！"
            else:
                cus.delete()
                success_message = "删除成功！"
                form = CustomerIDForm()
        else:
            error_message = "删除失败！"
        
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/delete_customer.html', context)


def delete_account(request):
    """销毁账户"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = AccountIDForm()
    else:
        # POST提交的数据，对数据进行处理
        form = AccountIDForm(request.POST)
        if form.is_valid():
            accountID = form.cleaned_data['accountid']
            acc = Accounts.objects.filter(accountid=accountID)
            if not acc.exists():
                error_message = "销毁失败！该账户不存在！"
            else:
                acc.delete()
                success_message = "销毁成功！"
                form = AccountIDForm()
        else:
            error_message = "销毁失败！"
        
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/delete_account.html', context)


def delete_loan(request):
    """删除贷款"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = LoanIDForm()
    else:
        # POST提交的数据，对数据进行处理
        form = LoanIDForm(request.POST)
        if form.is_valid():
            loanID = form.cleaned_data['loanid']
            try:
                loan = Loan.objects.get(loanid=loanID)
            except ObjectDoesNotExist:
                error_message = "删除失败！该贷款不存在！"
            else:
                if loan.state == '1':
                    error_message = "删除失败！该贷款正在发放中！"
                else:
                    loan.delete()
                    success_message = "删除成功！"
                    form = LoanIDForm()
        else:
            error_message = "删除失败！"
        
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/delete_loan.html', context)


def change_customer_id(request):
    """输入要修改的客户的ID"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = CustomerIDForm()
    else:
        # POST提交的数据，对数据进行处理
        form = CustomerIDForm(request.POST)
        if form.is_valid():
            cusID = form.cleaned_data['cusid']
            try:
                cus = Customer.objects.get(cusid=cusID)
            except ObjectDoesNotExist:
                error_message = "修改失败！该客户不存在！"
            else:
                form = ChangeCustomerForm(model_to_dict(cus))
                context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'cusid': cusID}
                return render(request, 'bank/change_customer.html', context)
        else:
            error_message = "修改失败！"

    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/change_customer_id.html', context)


def change_customer(request, cusid):
    """修改客户信息"""
    error_message, success_message = "", ""
    if request.method == 'POST':
        # POST提交的数据，对数据进行处理
        form = ChangeCustomerForm(request.POST)
        if form.is_valid():
            post = request.POST
            cusname = post.get('cusname')
            cusphone = post.get('cusphone')
            address = post.get('address')
            contact_phone = post.get('contact_phone')
            contact_name = post.get('contact_name')
            contact_email = post.get('contact_email')
            relation = post.get('relation')
            loanres = post.get('loanres')
            accres = post.get('accres')
            Customer.objects.filter(cusid=cusid).update(cusname=cusname, cusphone=cusphone,
                address=address, contact_phone=contact_phone, contact_name=contact_name,
                contact_email = contact_email, relation=relation, loanres=loanres, accres=accres)

            success_message = "修改成功！"
        else:
            error_message = "修改失败！"
            context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'cusid': cusid}
            return render(request, 'bank/change_customer.html', context)
    
    form = CustomerIDForm()
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/change_customer_id.html', context)


def change_account_id(request):
    """输入要修改的帐户的ID"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = AccountIDForm()
    else:
        # POST提交的数据，对数据进行处理
        form = AccountIDForm(request.POST)
        if form.is_valid():
            accID = form.cleaned_data['accountid']
            try:
                acc = Accounts.objects.get(accountid=accID)
            except ObjectDoesNotExist:
                error_message = "修改失败！该帐户不存在！"
            else:
                acc_dict = model_to_dict(acc)
                form = ChangeAccountForm(acc_dict)
                context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accID}
                return render(request, 'bank/change_account.html', context)
        else:
            error_message = "修改失败！"
        
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/change_account_id.html', context)


def change_account(request, accountid):
    """修改帐户信息"""
    error_message, success_message = "", ""
    if request.method == 'POST':
        form = ChangeAccountForm(request.POST)
        if form.is_valid():
            # POST提交的数据，对数据进行处理
            post = request.POST
            money = post.get('money')
            settime = post.get('settime').replace('/', '-')
            accounttype = post.get('accounttype')
            customer = post.get('customer')
            bank = post.get('bank')

            Accounts.objects.filter(accountid=accountid).update(money=money, settime=settime,
                accounttype=accounttype, bank=bank)
            
            form = ChangeAccountForm(post)
            cusidList = []  # 此次修改中选中的customer
            if form.is_valid():
                # QuerySet，里面是customer objects
                customer = form.cleaned_data['customer']

                for cus in customer:
                    cusid = (model_to_dict(cus))['cusid']
                    cusidList.append(cusid)
            
            # 中间表
            accforcusList = Accounts.customer.through
            # 中间表的每个object
            for accforcus in accforcusList.objects.filter(accounts=accountid):
                # 每个中间表object的客户ID
                cusid = (model_to_dict(accforcus))['customer']
                if cusid in cusidList:
                    # 如果在此次修改中选中的customer中，则不用考虑之
                    cusidList.remove(cusid)
                else:
                    # 如果不在，则删除之
                    accforcus.delete()
            
            # 对于原中间表中没有的customer，要加入之
            for cusid in cusidList:
                accounts = Accounts.objects.get(accountid=accountid)
                customer = Customer.objects.get(cusid=cusid)
                accforcus = AccforCus(accounts=accounts, customer=customer)
                accforcus.save()
        else:
            error_message = "修改失败！"
            context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
            return render(request, 'bank/change_account.html', context)
    
    form = ChangeAccountForm()
    if accounttype == 'saveacc':
        saveacc = Saveacc.objects.get(accountid=accountid)
        form = SaveaccForm(model_to_dict(saveacc))
        context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
        return render(request, 'bank/change_saveacc.html', context)
    else:
        checkacc = Checkacc.objects.get(accountid=accountid)
        form = CheckaccForm(model_to_dict(checkacc))
        context = {'form': form, 'error_message': error_message, 'success_message': success_message, 'accountid': accountid}
        return render(request, 'bank/change_checkacc.html', context)


def change_saveacc(request, accountid):
    """修改客户信息"""
    error_message, success_message = "", ""
    if request.method == 'POST':
        # POST提交的数据，对数据进行处理
        form = SaveaccForm(request.POST)
        if form.is_valid():
            post = request.POST
            interestrate = post.get('interestrate')
            savetype = post.get('savetype')
            Saveacc.objects.filter(accountid=accountid).update(interestrate=interestrate, savetype=savetype)
            success_message = "修改成功！"
        else:
            error_message = "修改失败！"
            context = {'form': form, 'error_message': error_message, 'success_message': success_message}
            return render(request, 'bank/change_saveacc.html', context)
    
    form = AccountIDForm()
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/change_account_id.html', context)


def change_checkacc(request, accountid):
    """修改客户信息"""
    error_message, success_message = "", ""
    if request.method == 'POST':
        # POST提交的数据，对数据进行处理
        form = CheckaccForm(request.POST)
        if form.is_valid():
            post = request.POST
            overdraft = post.get('overdraft')
            Checkacc.objects.filter(accountid=accountid).update(overdraft=overdraft)
            success_message = "修改成功！"
        else:
            error_message = "修改失败！"
            context = {'form': form, 'error_message': error_message, 'success_message': success_message}
            return render(request, 'bank/change_checkacc.html', context)
    
    form = AccountIDForm()
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/change_account_id.html', context)


def issue_loan(request):
    """发放贷款"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        form = PayinfoForm()
    else:
        form = PayinfoForm(request.POST)
        if form.is_valid():
            # loan为贷款表中的此贷款
            loan = form.cleaned_data['loan']

            cusList = loan.loanforcus.all()    # 与此贷款关联的客户
            # 此次发行贷款的客户
            payCus = form.cleaned_data['customer']
            if not payCus in cusList:
                # 如果此次发行贷款的客户不是与此贷款关联的客户
                error_message = "不可向与此贷款无关的客户付款！"

            if error_message == "":
                # 此次要发放的金额
                money = form.cleaned_data['money']
                sumMoney = loan.money   # 贷款总金额
                # 已发放金额
                everIssueMoney = Payinfo.objects.filter(loan=loan.loanid).aggregate(money=Sum('money'))
                if everIssueMoney['money'] is None:
                    everIssueMoney['money'] = 0
                if money + everIssueMoney['money'] < sumMoney:
                    loan.state = 1
                    loan.save()
                    form.save()
                    success_message = "发放成功!"
                elif money + everIssueMoney['money'] == sumMoney:
                    loan.state = 2
                    loan.save()
                    form.save()
                    success_message = "发放成功!"
                else:
                    error_message = "发行失败，超出贷款金额！"
            
            form = PayinfoForm()
            context = {'form': form, 'error_message': error_message, 'success_message': success_message}
            return render(request, 'bank/issue_loan.html', context)
        else:
            error_message = "修改失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/issue_loan.html', context)


def customer_query(request):
    """客户查询"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        form = CustomerQuery()
    else:
        form = CustomerQuery(request.POST)
        if form.is_valid():
            cusid = form.cleaned_data['cusid']
            cusname = form.cleaned_data['cusname']
            cusphone = form.cleaned_data['cusphone']
            address = form.cleaned_data['address']
            contact_name = form.cleaned_data['contact_name']
            accountid = form.cleaned_data['accountid']
            loanres_name = form.cleaned_data['loanres_name']
            accres_name = form.cleaned_data['accres_name']
            cusList = Customer.objects.all()
            if cusid != '':
                cusList = cusList.filter(cusid=cusid)
            if cusname != '':
                cusList = cusList.filter(cusname=cusname)
            if cusphone != '':
                cusList = cusList.filter(cusphone=cusphone)
            if address != '':
                cusList = cusList.filter(address=address)
            if contact_name != '':
                cusList = cusList.filter(contact_name=contact_name)
            if loanres_name != '':
                cusList = cusList.filter(loanres__empname=loanres_name)
            if accres_name != '':
                cusList = cusList.filter(accres__empname=accres_name)
            if accountid != '':
                cusidList = []
                for cus in cusList:
                    if cus.account.filter(accountid=accountid).exists():
                        cusidList.append(cus.cusid)
                cusList = cusList.filter(cusid__in=cusidList)
            if cusList.exists():
                cusList = sorted(cusList, key=lambda x: int(x.cusid))
                context = {'cusList': cusList}
                return render(request, 'bank/customer_table.html', context)
            else:
                error_message = "数据库中无此客户信息！"
        else:
            error_message = "查询失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/customer_query.html', context)


def account_query(request):
    """账户查询"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        form = AccountQuery()
    else:
        form = AccountQuery(request.POST)
        if form.is_valid():
            accountid = form.cleaned_data['accountid']
            money_range = form.cleaned_data['money_range']
            money = form.cleaned_data['money']
            settime_range = form.cleaned_data['settime_range']
            settime = form.cleaned_data['settime']
            accounttype = form.cleaned_data['accounttype']
            customer_name = form.cleaned_data['customer_name']
            bank_name = form.cleaned_data['bank_name']
            accList = Accounts.objects.all()
            if accountid != '':
                accList = accList.filter(accountid=accountid)
            if money_range != '' and money != None:
                if money_range == 'lt':
                    accList = accList.filter(money__lt=money)
                elif money_range == 'lte':
                    accList = accList.filter(money__lte=money)
                elif money_range == 'eq':
                    accList = accList.filter(money=money)
                elif money_range == 'gte':
                    accList = accList.filter(money__gte=money)
                elif money_range == 'gt':
                    accList = accList.filter(money__gt=money)
            if settime_range != '' and settime != None:
                if settime_range == 'lt':
                    accList = accList.filter(settime__lt=settime)
                elif settime_range == 'lte':
                    accList = accList.filter(settime__lte=settime)
                elif settime_range == 'eq':
                    accList = accList.filter(settime=settime)
                elif settime_range == 'gte':
                    accList = accList.filter(settime__gte=settime)
                elif settime_range == 'gt':
                    accList = accList.filter(settime__gt=settime)
            if accounttype != '' and accounttype != 'empty':
                accList = accList.filter(accounttype=accounttype)
            if customer_name != '':
                accidList = []
                for acc in accList:
                    if acc.customer.filter(cusname=customer_name).exists():
                        accidList.append(acc.accountid)
                accList = accList.filter(accountid__in=accidList)
            if bank_name != '':
                accList = accList.filter(bank__bankname=bank_name)
            if accList.exists():
                accList = sorted(accList, key=lambda x: int(x.accountid))
                context = {'accList': accList}
                return render(request, 'bank/account_table.html', context)
            else:
                error_message = "数据库中无此帐户信息！"
        else:
            error_message = "查询失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/account_query.html', context)


def loan_query(request):
    """贷款查询"""
    error_message, success_message = "", ""
    if request.method != 'POST':
        form = LoanQuery()
    else:
        form = LoanQuery(request.POST)
        if form.is_valid():
            loanid = form.cleaned_data['loanid']
            money_range = form.cleaned_data['money_range']
            money = form.cleaned_data['money']
            bank_name = form.cleaned_data['bank_name']
            state = form.cleaned_data['state']
            customer_name = form.cleaned_data['customer_name']
            loanList = Loan.objects.all()
            if loanid != '':
                loanList = loanList.filter(loanid=loanid)
            if money_range != '' and money != None:
                if money_range == 'lt':
                    loanList = loanList.filter(money__lt=money)
                elif money_range == 'lte':
                    loanList = loanList.filter(money__lte=money)
                elif money_range == 'eq':
                    loanList = loanList.filter(money=money)
                elif money_range == 'gte':
                    loanList = loanList.filter(money__gte=money)
                elif money_range == 'gt':
                    loanList = loanList.filter(money__gt=money)
            if customer_name != '':
                loanidList = []
                for loan in loanList:
                    if loan.loanforcus.filter(cusname=customer_name).exists():
                        loanidList.append(loan.loanid)
                loanList = loanList.filter(loanid__in=loanidList)
            if state != '' and state != 'empty':
                loanList = loanList.filter(state=state)
            if bank_name != '':
                loanList = loanList.filter(bank__bankname=bank_name)
            if loanList.exists():
                loanList = sorted(loanList, key=lambda x: int(x.loanid))
                context = {'loanList': loanList}
                return render(request, 'bank/loan_table.html', context)
            else:
                error_message = "数据库中无此贷款信息！"
        else:
            error_message = "查询失败！"
    
    context = {'form': form, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'bank/loan_query.html', context)


def save_money_statistics(request):
    """储蓄业务总金额统计"""
    """假设此银行系统从2010年开始运行，统计2010-2019年的用户数据"""
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
    class Money:
        def __init__(self, time, beijing, shanghai, shenzhen):
            self.time = time
            self.beijing = beijing
            self.shanghai = shanghai
            self.shenzhen = shenzhen

    # 月、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13):
            timeList.append(str(year) + '.' + str(month))
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=BeijingBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            BeijingList.append(money['money__sum'])
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=ShanghaiBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShanghaiList.append(money['money__sum'])
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=ShenzhenBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShenzhenList.append(money['money__sum'])

    monthList = []
    for i in range(len(timeList)):
        monthMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        monthList.append(monthMoney)

    context = {}
    context['month_list'] = monthList

    # 月、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    ax.set_xlabel('month', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_month_money.png', dpi=600)

    # 季、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13, 3):
            season = ""
            if month == 1:
                season = "春"
            elif month == 4:
                season = "夏"
            elif month == 7:
                season = "秋"
            else:
                season = "冬"
            timeList.append(str(year) + season)
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=BeijingBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            BeijingList.append(money['money__sum'])
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShanghaiBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShanghaiList.append(money['money__sum'])
            money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShenzhenBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShenzhenList.append(money['money__sum'])
    
    seasonList = []
    for i in range(len(timeList)):
        seasonMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        seasonList.append(seasonMoney)

    context['season_list'] = seasonList

    # 季、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.set_xlabel('season', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_season_money.png', dpi=600)

    # 年、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        timeList.append(year)
        BeijingBank = Bank.objects.get(bankname='Beijing Bank')
        ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
        ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
        money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=BeijingBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        BeijingList.append(money['money__sum'])
        money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=ShanghaiBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        ShanghaiList.append(money['money__sum'])
        money = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=ShenzhenBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        ShenzhenList.append(money['money__sum'])
    
    yearList = []
    for i in range(len(timeList)):
        yearMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        yearList.append(yearMoney)

    context['year_list'] = yearList

    # 年、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.set_xlabel('year', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_year_money.png', dpi=600)

    return render(request, 'bank/save_money_statistics.html', context)


def save_users_statistics(request):
    """储蓄业务用户数统计"""
    """假设此银行系统从2010年开始运行，统计2010-2019年的用户数据"""
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
    class Users:
        def __init__(self, time, beijing, shanghai, shenzhen):
            self.time = time
            self.beijing = beijing
            self.shanghai = shanghai
            self.shenzhen = shenzhen

    # 月、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13):
            timeList.append(str(year) + '.' + str(month))
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=BeijingBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            BeijingList.append(len(set(userList)))
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=ShanghaiBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            ShanghaiList.append(len(set(userList)))
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month=month, bank=ShenzhenBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            ShenzhenList.append(len(set(userList)))

    monthList = []
    for i in range(len(timeList)):
        monthUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        monthList.append(monthUsers)

    context = {}
    context['month_list'] = monthList

    # 月、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    ax.set_xlabel('month', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_month_users.png', dpi=600)

    # 季、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13, 3):
            season = ""
            if month == 1:
                season = "春"
            elif month == 4:
                season = "夏"
            elif month == 7:
                season = "秋"
            else:
                season = "冬"
            timeList.append(str(year) + season)
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=BeijingBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            BeijingList.append(len(set(userList)))
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShanghaiBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            ShanghaiList.append(len(set(userList)))
            accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShenzhenBank)
            userList = []
            for acc in accList:
                for cus in acc.customer.all():
                    userList.append(cus.cusid)
            ShenzhenList.append(len(set(userList)))
    
    seasonList = []
    for i in range(len(timeList)):
        seasonUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        seasonList.append(seasonUsers)

    context['season_list'] = seasonList

    # 季、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.set_xlabel('season', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_season_users.png', dpi=600)

    # 年、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        timeList.append(year)
        BeijingBank = Bank.objects.get(bankname='Beijing Bank')
        ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
        ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
        accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=BeijingBank)
        userList = []
        for acc in accList:
            for cus in acc.customer.all():
                userList.append(cus.cusid)
        BeijingList.append(len(set(userList)))
        accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=ShanghaiBank)
        userList = []
        for acc in accList:
            for cus in acc.customer.all():
                userList.append(cus.cusid)
        ShanghaiList.append(len(set(userList)))
        accList = Accounts.objects.filter(accounttype='saveacc', settime__year=year, bank=ShenzhenBank)
        userList = []
        for acc in accList:
            for cus in acc.customer.all():
                userList.append(cus.cusid)
        ShenzhenList.append(len(set(userList)))
    
    yearList = []
    for i in range(len(timeList)):
        yearUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        yearList.append(yearUsers)

    context['year_list'] = yearList

    # 年、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.set_xlabel('year', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/save_year_users.png', dpi=600)

    return render(request, 'bank/save_users_statistics.html', context)


def loan_money_statistics(request):
    """贷款业务总金额统计"""
    """假设此银行系统从2010年开始运行，统计2010-2019年的用户数据"""
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
    class Money:
        def __init__(self, time, beijing, shanghai, shenzhen):
            self.time = time
            self.beijing = beijing
            self.shanghai = shanghai
            self.shenzhen = shenzhen

    # 月、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13):
            timeList.append(str(year) + '.' + str(month))
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            money = Loan.objects.filter(settime__year=year, settime__month=month, bank=BeijingBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            BeijingList.append(money['money__sum'])
            money = Loan.objects.filter(settime__year=year, settime__month=month, bank=ShanghaiBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShanghaiList.append(money['money__sum'])
            money = Loan.objects.filter(settime__year=year, settime__month=month, bank=ShenzhenBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShenzhenList.append(money['money__sum'])

    monthList = []
    for i in range(len(timeList)):
        monthMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        monthList.append(monthMoney)

    context = {}
    context['month_list'] = monthList

    # 月、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    ax.set_xlabel('month', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_month_moeny.png', dpi=600)

    # 季、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13, 3):
            season = ""
            if month == 1:
                season = "春"
            elif month == 4:
                season = "夏"
            elif month == 7:
                season = "秋"
            else:
                season = "冬"
            timeList.append(str(year) + season)
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            money = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=BeijingBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            BeijingList.append(money['money__sum'])
            money = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShanghaiBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShanghaiList.append(money['money__sum'])
            money = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShenzhenBank).aggregate(Sum('money'))
            if money['money__sum'] is None:
                money['money__sum'] = 0
            ShenzhenList.append(money['money__sum'])
    
    seasonList = []
    for i in range(len(timeList)):
        seasonMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        seasonList.append(seasonMoney)

    context['season_list'] = seasonList

    # 季、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.set_xlabel('season', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_season_money.png', dpi=600)

    # 年、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        timeList.append(year)
        BeijingBank = Bank.objects.get(bankname='Beijing Bank')
        ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
        ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
        money = Loan.objects.filter(settime__year=year, bank=BeijingBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        BeijingList.append(money['money__sum'])
        money = Loan.objects.filter(settime__year=year, bank=ShanghaiBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        ShanghaiList.append(money['money__sum'])
        money = Loan.objects.filter(settime__year=year, bank=ShenzhenBank).aggregate(Sum('money'))
        if money['money__sum'] is None:
            money['money__sum'] = 0
        ShenzhenList.append(money['money__sum'])
    
    yearList = []
    for i in range(len(timeList)):
        yearMoney = Money(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        yearList.append(yearMoney)

    context['year_list'] = yearList

    # 年、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.set_xlabel('year', fontsize=12)
    ax.set_ylabel('money', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_year_money.png', dpi=600)

    return render(request, 'bank/loan_money_statistics.html', context)


def loan_users_statistics(request):
    """储蓄业务用户数统计"""
    """假设此银行系统从2010年开始运行，统计2010-2019年的用户数据"""
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
    class Users:
        def __init__(self, time, beijing, shanghai, shenzhen):
            self.time = time
            self.beijing = beijing
            self.shanghai = shanghai
            self.shenzhen = shenzhen

    # 月、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13):
            timeList.append(str(year) + '.' + str(month))
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            loanList = Loan.objects.filter(settime__year=year, settime__month=month, bank=BeijingBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            BeijingList.append(len(set(userList)))
            loanList = Loan.objects.filter(settime__year=year, settime__month=month, bank=ShanghaiBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            ShanghaiList.append(len(set(userList)))
            loanList = Loan.objects.filter(settime__year=year, settime__month=month, bank=ShenzhenBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            ShenzhenList.append(len(set(userList)))

    monthList = []
    for i in range(len(timeList)):
        monthUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        monthList.append(monthUsers)

    context = {}
    context['month_list'] = monthList

    # 月、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    ax.set_xlabel('month', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_month_users.png', dpi=600)

    # 季、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        for month in range(1, 13, 3):
            season = ""
            if month == 1:
                season = "春"
            elif month == 4:
                season = "夏"
            elif month == 7:
                season = "秋"
            else:
                season = "冬"
            timeList.append(str(year) + season)
            BeijingBank = Bank.objects.get(bankname='Beijing Bank')
            ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
            ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
            loanList = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=BeijingBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            BeijingList.append(len(set(userList)))
            loanList = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShanghaiBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            ShanghaiList.append(len(set(userList)))
            loanList = Loan.objects.filter(settime__year=year, settime__month__in=[month, month + 1, month + 2], bank=ShenzhenBank)
            userList = []
            for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
            ShenzhenList.append(len(set(userList)))
    
    seasonList = []
    for i in range(len(timeList)):
        seasonUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        seasonList.append(seasonUsers)

    context['season_list'] = seasonList

    # 季、曲线图
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.set_xlabel('season', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_season_users.png', dpi=600)

    # 年、表格
    timeList, BeijingList, ShanghaiList, ShenzhenList = [], [], [], []
    for year in range(2010, 2020):
        timeList.append(year)
        BeijingBank = Bank.objects.get(bankname='Beijing Bank')
        ShanghaiBank = Bank.objects.get(bankname='Shanghai Bank')
        ShenzhenBank = Bank.objects.get(bankname='Shenzhen Bank')
        loanList = Loan.objects.filter(settime__year=year, bank=BeijingBank)
        userList = []
        for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
        BeijingList.append(len(set(userList)))
        loanList = Loan.objects.filter(settime__year=year, bank=ShanghaiBank)
        userList = []
        for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
        ShanghaiList.append(len(set(userList)))
        loanList = Loan.objects.filter(settime__year=year, bank=ShenzhenBank)
        userList = []
        for loan in loanList:
                for cus in loan.loanforcus.all():
                    userList.append(cus.cusid)
        ShenzhenList.append(len(set(userList)))
    
    yearList = []
    for i in range(len(timeList)):
        yearUsers = Users(timeList[i], BeijingList[i], ShanghaiList[i], ShenzhenList[i])
        yearList.append(yearUsers)

    context['year_list'] = yearList

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, top=0.9)

    ax.plot(timeList, BeijingList, label='Beijing Bank')
    ax.plot(timeList, ShanghaiList, label='Shanghai Bank')
    ax.plot(timeList, ShenzhenList, label='Shenzhen Bank')

    ax.set_xlabel('year', fontsize=12)
    ax.set_ylabel('user number', fontsize=12)
    ax.legend()

    ax.tick_params(axis='x', rotation=45)

    plt.savefig('./static/pic/loan_year_users.png', dpi=600)

    return render(request, 'bank/loan_users_statistics.html', context)

# for i in range(1, 1001):
#     saveacc = Saveacc()
#     saveacc.accountid = Accounts.objects.get(accountid=i)
#     saveacc.interestrate = 0.03
#     saveacc.savetype = 'r'
#     saveacc.save()
 
# for i in range(1, 1001):
#     cus = Customer()
#     cus.cusid = i
#     cus.cusname = random.choice(['q', 'w', 'r', 't', 'y', 'z', 'x', 'c']) + random.choice(['a', 'e', 'i', 'o']) + random.choice(['s', 'd', 'f', 'g', 'h', 'j', 'k', 'l']) + random.choice(['a', 'e', 'i', 'o']) + random.choice(['b', 'n', 'm', 'p', 'k'])
#     cus.cusphone = '1739838' + str(1000 + i)
#     cus.address = random.choice(['Beijing', 'Shanghai', 'Shenzhen'])
#     cus.contact_name = random.choice(['q', 'w', 'r', 't', 'y', 'z', 'x', 'c']) + random.choice(['a', 'e', 'i', 'o']) + random.choice(['s', 'd', 'f', 'g', 'h', 'j', 'k', 'l']) + random.choice(['a', 'e', 'i', 'o']) + random.choice(['b', 'n', 'm', 'p', 'k'])
#     cus.contact_phone = '1739838' + str(2000 + i)
#     cus.contact_email = cus.contact_name + '@one.piece.com'
#     cus.relation = random.choice(['father', 'mother', 'grandfater', 'grandmother', 'uncle', 'aunt'])
#     cus.loanres = Employee.objects.get(empid=random.choice(['1', '2', '3', '4', '5', '6']))
#     cus.accres = Employee.objects.get(empid=random.choice(['1', '2', '3', '4', '5', '6']))
#     cus.save()

# for i in range(1, 1001):
#     acc = Accounts()
#     acc.accountid = i
#     acc.money = random.randint(1, 10) * 1000
#     acc.settime = datetime(random.randint(2010, 2019), random.randint(1, 12), random.randint(1, 28), random.randint(1, 12), random.randint(0, 59), random.randint(0, 59))
#     acc.accounttype = 'saveacc'
#     r = random.randint(0, 8)
#     if r <= 3:
#         acc.bank = Bank.objects.get(bankname='Beijing Bank')
#     elif r <= 6:
#         acc.bank = Bank.objects.get(bankname='Shanghai Bank')
#     elif r <= 8:
#         acc.bank = Bank.objects.get(bankname='Shenzhen Bank')
#     acc.save()
#     acc.customer.set(Customer.objects.filter(cusid=random.randint(1, 1000)))
#     acc.save()

# for i in range(1, 1001):
#     loan = Loan()
#     loan.loanid = i
#     loan.money = random.randint(1, 10) * 1000
#     r = random.randint(0, 8)
#     if r <= 3:
#         loan.bank = Bank.objects.get(bankname='Beijing Bank')
#     elif r <= 6:
#         loan.bank = Bank.objects.get(bankname='Shanghai Bank')
#     elif r <= 8:
#         loan.bank = Bank.objects.get(bankname='Shenzhen Bank')
#     loan.settime = datetime(random.randint(2010, 2019), random.randint(1, 12), random.randint(1, 28), random.randint(1, 12), random.randint(0, 59), random.randint(0, 59))
#     loan.state = random.choice(['1', '2'])
#     loan.save()
#     loan.loanforcus.set(Customer.objects.filter(cusid=random.randint(1, 1000)))
#     loan.save()