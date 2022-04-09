from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.details, name="details"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("category_list", views.category_list, name="category_list"),
    path("category/<str:cat>", views.category, name="category"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction")
]
