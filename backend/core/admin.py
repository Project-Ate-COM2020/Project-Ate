from django.contrib import admin
from .models import ForecastInput, BundlePosting, Seller, Consumer, Reservation, IssueReport, ForecastOutput

# Register your models here.
admin.site.register(ForecastInput)
admin.site.register(BundlePosting)
admin.site.register(Seller)
admin.site.register(Consumer)
admin.site.register(Reservation)
admin.site.register(IssueReport)
admin.site.register(ForecastOutput)