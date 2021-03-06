from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from math import modf

# 共通列用抽象クラス
class Payment_Model(models.Model):
    DELETE_CHOICES = (
        (0, '未削除'),
        (1, '削除済'),
    )
    delete_flag = models.IntegerField(choices=DELETE_CHOICES, default=0, null=True)
    create_user = models.CharField(max_length=20, null=True, editable=False)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    update_user = models.CharField(max_length=20, null=True, editable=False)
    update_datetime = models.DateTimeField(auto_now=True, null=True, editable=False)

    class Meta:
        abstract = True

# 企業マスタ
class Company(Payment_Model):
    company_id = models.CharField(primary_key=True, max_length=20)
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name

# 部署マスタ
class Department(Payment_Model):
    vendor_id = models.CharField(primary_key=True, max_length=20)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50, default="", blank=True)
    contact = models.CharField(max_length=50)
    post_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    representative = models.CharField(max_length=20, null=True, blank=True)
    payment_account = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.vendor_id

# 通貨マスタ
class Currency(Payment_Model):
    currency_id = models.IntegerField(primary_key=True)
    currency_name = models.CharField(max_length=20)
    currency_mark = models.CharField(max_length=20)

    def __str__(self):
        return self.currency_name

# 請求ヘッダ
class Bills_Header(Payment_Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50)
    vendor_id = models.ForeignKey(Department, on_delete=models.PROTECT)
    publish_date = models.DateField()
    limit_date = models.DateField()
    TERMS_CHOICES = (
        (0, '振込'),
        (1, '引落'),
    )
    terms = models.IntegerField(choices=TERMS_CHOICES, default=0)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    PAYED_CHOICES = (
        (0, '未払い'),
        (1, '支払済'),
    )
    payed_flag = models.IntegerField(choices=PAYED_CHOICES, default=0)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = [
            "limit_date",
            "publish_date",
        ]

# 請求明細
class Bills_Detail(Payment_Model):
    invoice_id = models.ForeignKey(Bills_Header, on_delete=models.CASCADE, related_name="header")
    invoice_detail_number = models.IntegerField()
    part_number = models.CharField(max_length=50)
    part_name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=20, decimal_places=5)
    quantity = models.IntegerField()
    product = models.DecimalField(max_digits=20, decimal_places=5, default=0, editable=False)

    def __str__(self):
        return self.part_number
    
    def get_unit_price(self):
        if float(self.unit_price).is_integer:
            return str(Decimal(self.unit_price).quantize(Decimal("0"), ROUND_HALF_UP))
        else:
            return str(float(self.unit_price))

    def get_product(self):
        if float(self.product).is_integer:
            return str(Decimal(self.product).quantize(Decimal("0"), ROUND_HALF_UP))
        else:
            return str(float(self.product))

    def save(self, *args, **kwargs):
        self.product = self.unit_price * self.quantity
        super(Payment_Model, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("invoice_id", "invoice_detail_number"))
        ordering = [
            "invoice_detail_number",
        ]
        
        
