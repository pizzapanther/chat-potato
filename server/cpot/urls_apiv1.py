from django.urls import path

import chat.views


urlpatterns = [
  path('my-details', chat.views.my_details),
  path('my-orgs', chat.views.my_orgs),
]
