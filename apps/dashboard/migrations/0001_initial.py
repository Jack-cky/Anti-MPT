from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(max_length=32)),
                ('trading_date', models.DateField()),
                ('price_close', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=18)),
                ('price_long', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('price_short', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('portfolio', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=18)),
                ('market_index', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=18)),
                ('risk_free', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=18)),
                ('created_at', models.DateTimeField(db_index=True)),
            ],
            options={
                'db_table': 'dashboard',
                'ordering': ['agent', 'trading_date'],
                'constraints': [models.UniqueConstraint(fields=('agent', 'trading_date'), name='dashboard_agent_trading_date_uniq')],
            },
        ),
    ]
