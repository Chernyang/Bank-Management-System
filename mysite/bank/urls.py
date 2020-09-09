from django.urls import path

from . import views

# 如果Django匹配网址（第一个参数），如果匹配成功则调用views里的函数，由这个函数返回一个html文件
# 如果Django使用bank:xxxx，则转到对应网址，然后调用views里的相应函数

app_name = 'bank'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('add_account', views.add_account, name='add_account'),
    path('add_saveacc/<int:accountid>', views.add_saveacc, name='add_saveacc'),
    path('add_checkacc/<int:accountid>', views.add_checkacc, name='add_checkacc'),
    path('add_loan', views.add_loan, name='add_loan'),
    path('delete_customer', views.delete_customer, name='delete_customer'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('delete_loan', views.delete_loan, name='delete_loan'),
    path('change_customer_id', views.change_customer_id, name='change_customer_id'),
    path('change_customer/<int:cusid>', views.change_customer, name='change_customer'),
    path('change_account_id', views.change_account_id, name='change_account_id'),
    path('change_account/<int:accountid>', views.change_account, name='change_account'),
    path('change_saveacc/<int:accountid>', views.change_saveacc, name='change_saveacc'),
    path('change_checkacc/<int:accountid>', views.change_checkacc, name='change_checkacc'),
    path('issue_loan', views.issue_loan, name='issue_loan'),
    path('customer_query', views.customer_query, name='customer_query'),
    path('account_query', views.account_query, name='account_query'),
    path('loan_query', views.loan_query, name='loan_query'),
    path('save_money_statistics', views.save_money_statistics, name='save_money_statistics'),
    path('save_users_statistics', views.save_users_statistics, name='save_users_statistics'),
    path('loan_money_statistics', views.loan_money_statistics, name='loan_money_statistics'),
    path('loan_users_statistics', views.loan_users_statistics, name='loan_users_statistics')
]