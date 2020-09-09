from django.contrib import admin

from .models import Accounts, Bank, Checkacc, Customer, Department, Employee, Loan, Saveacc, AccforCus, Payinfo
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Bank)
admin.site.register(Checkacc)
admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Loan)
admin.site.register(Saveacc)
admin.site.register(AccforCus)
admin.site.register(Payinfo)