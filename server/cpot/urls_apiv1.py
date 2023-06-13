from django.urls import path

import account.views
import chat.views


urlpatterns = [
  path('get-token', account.views.get_perm_token),
  path('my-details', account.views.my_details),
  path('my-orgs', chat.views.my_orgs),
]
