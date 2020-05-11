from django.db import models

# 企業マスタ
class Companies(models.Model):
    company_id = models.CharField(primary_key=True, max_length=20)
    company_name = models.CharField(max_length=50)

# 部署マスタ
class Departments(models.Model):
    vendor_id = models.CharField(primary_key=True, max_length=20)
    company_id = models.ForeignKey(Companies, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=50)
    post_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    representative = models.CharField(max_length=20, null=True)
    payment_account = models.CharField(max_length=100)

# 通貨マスタ
class Currencies(models.Model):
    currency_id = models.IntegerField(primary_key=True)
    currency_name = models.CharField(max_length=20)
    currency_mark = models.CharField(max_length=20)

# 請求ヘッダ
class BillsHeader(models.Model):
    invoice_id = models.CharField(primary_key=True, max_length=20)
    invoice_number = models.CharField(max_length=50)
    vendor_id = models.ForeignKey(Departments, on_delete=models.PROTECT)
    publish_date = models.DateField(auto_now_add=True)
    limit = models.DateField(auto_now_add=True)
    terms = models.IntegerField(default=0)
    currency_id = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    payed_flag = models.IntegerField(default=0)


# 請求明細
class BillsDetail(models.Model):
    invoice_id = models.CharField(max_length=20)
    invoice_detail_number = models.IntegerField()
    part_number = models.CharField(max_length=50)
    part_name = models.CharField(max_length=50)
    unit_price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        unique_together = (("invoice_id", "invoice_detail_number"))
