from django.contrib import admin
from .models import User,Cookie,Liked_Diliked_Video,SubscribedChannel

# Register your models here.
admin.site.register(User)
admin.site.register(Cookie)
admin.site.register(Liked_Diliked_Video)
admin.site.register(SubscribedChannel)

