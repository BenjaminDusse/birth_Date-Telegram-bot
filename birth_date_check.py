


import django
import sys
import os

# ---------  Setup django  //  --------------
path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import datetime
from accounts.models import Profile
from datetime import timedelta
from django.utils import timezone
# ---------  //  Setup django  --------------

datetime_now = timezone.now()
now_day, now_month = datetime_now.day, datetime_now.month

# datetime_tomorrow = datetime_now + timedelta(days=1)
# tomorrow_day, tomorrow_month = datetime_tomorrow.day, datetime_tomorrow.month

birth_day_today = Profile.objects.filter(dob__day=now_day, dob__month=now_month)
print(birth_day_today)
# birth_day_tomorrow = Profile.objects.filter(dob__day=tomorrow_day, dob__month=tomorrow_month)
