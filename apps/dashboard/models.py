from decimal import Decimal

from django.db import models


class Dashboard(models.Model):
    agent = models.CharField(max_length=32)
    trading_date = models.DateField()
    price_close = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal("0"),
    )
    price_long = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
    )
    price_short = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
    )
    portfolio = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal("0"),
    )
    market_index = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal("0"),
    )
    risk_free = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal("0"),
    )
    created_at = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "dashboard"
        ordering = ["agent", "trading_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["agent", "trading_date"],
                name="dashboard_agent_trading_date_uniq",
            ),
        ]
