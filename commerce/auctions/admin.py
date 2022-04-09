from django.contrib import admin

from .models import User, Listing, Bid, Comment, Watchlist
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "price", "id", "user", "image_url", "starting_bid", "active", "date_time")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid", "item", "user", "id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "comment", "id", "user", "date_time")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "email", "first_name", "last_name")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "active", "id")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)