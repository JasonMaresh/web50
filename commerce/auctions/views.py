from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



from .models import User, Listing, Bid, Comment, Watchlist, BidForm, CommentForm, NewListingForm


@login_required(redirect_field_name="")
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watch = listing.watching.get(user=listing.user)
    watch.active=False
    listing.active=False
    listing.save()
    watch.save()
    return HttpResponseRedirect(reverse("details", args=(listing_id,)))


@login_required(redirect_field_name="")
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            item = Listing.objects.get(pk=listing_id)
            user_comment=Comment(comment=comment, item=item, user=request.user)
            user_comment.save()
            return HttpResponseRedirect(reverse("details", args=(listing_id,)))



def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all(),
        "title": "Active Listings"
    })

def category(request, cat):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(category=cat).all(),
        "title": cat + " Listings"
    })


def category_list(request):
    return render(request, "auctions/categories.html",{
        "listings":Listing.objects.filter(active=True).values('category').distinct().order_by()
    })

def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            item = Listing.objects.get(pk=listing_id)

            if bid >= item.starting_bid and bid >= float(item.price) + 0.01:
                user = request.user
                new_bid = Bid(bid=bid, item=item, user=user)
                new_bid.save()
                item.price = bid
                item.save()
                message = "Your bid was processed sucessfully!"
            else:
                message = "Your bid must be at least the starting bid and greater than any other bids that have been place."
        
            number_of_bids = len(item.bid.all())
            highest_bid = Bid.objects.get(item=item, bid=item.price)
        

            return render(request, "auctions/details.html",{
                "message":message,
                "listing":item,
                "number_of_bids":number_of_bids,
                "bidder": highest_bid.user,
                "watchlist":Watchlist.objects.filter(user=request.user, item=item),
                "comment_form":CommentForm(),
                "bid_form": BidForm(),
                "comments": Comment.objects.filter(item=item)
            })

@login_required(redirect_field_name="")
def view_watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "watchlist":Watchlist.objects.filter(user=request.user, active = True)
        
    })

@login_required(redirect_field_name="")
def watchlist(request, listing_id):
    user = request.user
    item = Listing.objects.get(pk=listing_id)
    watch = Watchlist.objects.get(user=user, item=item)
    if watch.active == True:
        watch.active = False
    else:
        watch.active = True
    watch.save()
    return HttpResponseRedirect(reverse("details", args=(listing_id,)))


def details(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if not request.user.is_authenticated:
        return render(request, "auctions/details.html",{
            "listing":listing,
            "comments": Comment.objects.filter(item=listing)
        })
    number_of_bids = len(listing.bid.all())
    list = Watchlist.objects.filter(user=request.user, item=listing)
    if len(list) == 0:
        watch = Watchlist(user=request.user, item=listing, active=False)
        watch.save()
    watchlist = Watchlist.objects.get(user=request.user, item=listing)
    if not listing.price == 0:
        highest_bid = Bid.objects.filter(item=listing, bid=listing.price).first()
        bidder = highest_bid.user
        return render(request, "auctions/details.html",{
            "listing": listing,
            "number_of_bids": number_of_bids,
            "bidder": bidder,
            "watchlist":watchlist,
            "comment_form":CommentForm(),
            "bid_form": BidForm(),
            "comments": Comment.objects.filter(item=listing)
        })
    return render(request, "auctions/details.html",{
        "listing":listing,
        "watchlist":watchlist,
        "comment_form":CommentForm(),
        "bid_form": BidForm(),
        "comments": Comment.objects.filter(item=listing)
        })

@login_required(redirect_field_name="")
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]
            description = form.cleaned_data["description"]
            user=request.user
            active = True
            price = 0
            listing = Listing(title=title, price = price, category=category, image_url=image_url,description=description, user=user, active=active, starting_bid=starting_bid)
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html",{
        "form": NewListingForm()
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required(redirect_field_name="")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
