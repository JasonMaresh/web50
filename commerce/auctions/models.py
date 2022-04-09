from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, TextInput, NumberInput, Select, URLInput
from django import forms

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    Categories = [
        ("Electronics", "Electronics"),
        ("Collectables_Art","Collectables & Art"),
        ("Home_Garden","Home & Garden"),
        ("Clothing_Shoes_Accessories","Clothing, Shoes & Accessories"),
        ("Toys_Hobbies","Toys & Hobbies"),
        ("Sporting Goods","Sporting Goods"),
        ("Books_Movies_Music", "Books, Movies & Music"),
        ("Health_Beauty", "Health & Beauty"),
        ("Buisness_Industrial", "Buisness & Industrial"),
        ("Jewelry_Watches","Jewelry & Watches"),
        ("Baby Essentials","Baby Essentials"),
        ("Pet_Supplies", "Pet Supplies"),
        ("Pet", "Pet"),
        ("Other", "Other")
    ]
    category = models.CharField(choices = Categories, max_length=200)
    image_url = models.URLField(max_length = 200)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class NewListingForm(ModelForm):
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin: 10px',
                'placeholder': 'Title'
                }),
           'description': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin: 10px',
                'placeholder': 'Description'
                }),
            'starting_bid': NumberInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin: 10px',
                'placeholder': 'Starting Bid'
                }),
            'category': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin: 10px',
                'placeholder': 'Title'
                }),
            'image_url': URLInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin: 10px',
                'placeholder': 'Image URL'
                })
        }


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bidder")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid on {self.item} for an amount of {self.bid}"

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': NumberInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Bid'
                })
        }

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter comments here ...'
                })
        }

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    active = models.BooleanField(default=False)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watching")

    def __str__(self):
        return f"{self.user} watching {self.item} is {self.active}"

