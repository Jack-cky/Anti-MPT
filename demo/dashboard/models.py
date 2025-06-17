from django.db import models


class Dashboard(models.Model):
    trading_date = models.TextField(primary_key=True)
    price_close = models.FloatField()
    price_long = models.FloatField(null=True)
    price_short = models.FloatField(null=True)
    portfolio = models.FloatField()
    market_index = models.FloatField()
    risk_free = models.FloatField()
    created_at = models.TextField()
    
    class Meta:
        db_table = "dashboard"
        managed = False
