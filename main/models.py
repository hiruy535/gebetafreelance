from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import reverse
from django.db.models import Q

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have a username")

		user = self.model(
				email= self.normalize_email(email),
				username = username,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
				email = self.normalize_email(email),
				password = password,
				username = username,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
		email						= models.EmailField(verbose_name="email", max_length=60, unique=True)
		username					= models.CharField(max_length=30, unique=True)
		firstname					= models.CharField(max_length=30, unique=False, null=True)
		lastname					= models.CharField(max_length=30, unique=False, null=True)
		address						= models.CharField(max_length=50, unique=False, null=True)
		phonenumber					= models.CharField(max_length=20, unique=False, null=True)
		date_joined					= models.DateTimeField(verbose_name="date joined", auto_now_add=True)
		last_login					= models.DateTimeField(verbose_name="last login", auto_now=True)
		is_admin					= models.BooleanField(default=False)
		is_active					= models.BooleanField(default=True)
		is_staff					= models.BooleanField(default=False)
		is_superuser				= models.BooleanField(default=False)
		profile_image				= models.ImageField(null=False)


		USERNAME_FIELD = 'email'
		REQUIRED_FIELDS = ['username', ]

		objects = MyAccountManager()

		def __str__(self):
			return self.email
		def has_perm(self, perm, obj=None):
			return self.is_admin
		def has_module_perms(self, app_label):
			return True
		def getusername(self):
			return self.username

		@property
		def imageURL(self):
			try:
				url = self.profile_image.url
			except:
				url = ''
			return url

class Category(models.Model):
	categoryname					= models.CharField(max_length=100)
	categoryimage					= models.ImageField(null=False)

	def __str__(self):
			return self.categoryname


	@property
	def imageURL(self):
		try:
			url = self.categoryimage.url
		except:
			url = ''
		return url



class Price(models.Model):
	price_title					= models.CharField(max_length=30, blank=True, unique=False, null=True)
	price_number				= models.CharField(max_length=20, blank=True, unique=False, null=True)
	price_delivery				= models.CharField(max_length=30, blank=True, unique=False, null=True)
	price_description			= models.TextField(max_length=1000, blank=True, unique=False, null=True)
	price_revision				= models.CharField(max_length=20, blank=True, unique=False, null=True)

class PriceBasic(models.Model):
	price					 	= models.ForeignKey(Price, blank=True, on_delete=models.CASCADE, null=True )
	
class PriceStandard(models.Model):
	price 						= models.ForeignKey(Price, blank=True, on_delete=models.CASCADE, null=True )
	
class PricePremium(models.Model):
	price						= models.ForeignKey(Price, blank=True, on_delete=models.CASCADE, null=True )
	
			

class Room(models.Model):
		roomname					= models.CharField(max_length=300, unique=False)
		roomsize					= models.CharField(max_length=30, null=True)
		car_model					= models.CharField(max_length=30, unique=False, null=True)
		car_location				= models.CharField(max_length=30, unique=False, null=True)
		car_price					= models.CharField(max_length=10, unique=False)
		pricebasic					= models.ForeignKey(PriceBasic, blank=True, on_delete=models.CASCADE, null=True )
		pricepremium				= models.ForeignKey(PricePremium, blank=True, on_delete=models.CASCADE, null=True )
		pricestandard				= models.ForeignKey(PriceStandard, blank=True, on_delete=models.CASCADE, null=True )
		total_rate					= models.IntegerField(null=True)
		car_description				= models.TextField(max_length=500, unique=False)
		is_taken					= models.BooleanField(default=False)
		roomimage					= models.ImageField(null=True, blank=True)
		roomimage1					= models.ImageField(null=True, blank=True)
		roomimage2					= models.ImageField(null=True, blank=True)
		roomimage3					= models.ImageField(null=True, blank=True)
		roomimage4					= models.ImageField(null=True, blank=True)
		room_user                 	= models.ForeignKey(Account, blank=True, on_delete=models.CASCADE, null=True )
		catagory                 	= models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True )
		slug						= models.SlugField(null=True)

		def __str__(self):
			return self.roomname
		def get_absolute_url(self):
			return reverse("main:roombooking",kwargs={
				'slug' : self.slug
			})

		@property
		def imageURL(self):
			try:
				url = self.roomimage.url
			except:
				url = ''
			return url
class RateManager(models.Manager):

	def get_or_new(self, user, other_username): # get_or_create
		username = user.username
		qlookup1 = Q(user__username=username) & Q(room__roomname=other_username)
		return qlookup1

	def set_total(self, item):
		total = 0
		num_items = 0
		items = self.filter(room=item)
		for i in items:
			num_items += 1
			total = total + int('0' + i.rate_amount)
		if num_items == 0:
			num_items = 1
		total = total/num_items
		total = round(total,1)
		print(total)
		for i in items:
			i.room.total_rate = total
			i.room.save()
			print(i.room.total_rate)

		return items



class Rate(models.Model):
	user							= models.ForeignKey(Account, blank=True, on_delete=models.CASCADE, null=True )
	room							= models.ForeignKey(Room, blank=True, on_delete=models.CASCADE, null=True)
	rate_amount						= models.CharField(max_length=10, null=True)

	objects      					= RateManager()
	def __str__(self):
		return self.room.roomname


class BookRoom(models.Model):
        account                 = models.ForeignKey(Account, blank=True, on_delete=models.SET_NULL, null=True )
        room                    = models.ForeignKey(Room, blank=True, on_delete=models.SET_NULL, null=True)
        date_booked             = models.DateTimeField(auto_now_add=True)
        complete                = models.BooleanField(default=False, null=True)
        transaction_id          = models.CharField(max_length=200, null=False, blank=False)


        def __str__(self):
            return self.account.username + " booked "+ self.room.roomname
class Comment(models.Model):
	user							= models.ForeignKey(Account, blank=True, on_delete=models.CASCADE, null=True )
	room							= models.ForeignKey(Room, blank=True, on_delete=models.CASCADE, null=True)
	comment 						= models.TextField(max_length=10000, null=True)
	timestamp   					= models.DateTimeField(auto_now_add=True)
