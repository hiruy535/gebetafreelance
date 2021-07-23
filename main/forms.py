from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *


class RegistrationForm(UserCreationForm):
	#email = forms.EmailField(max_length=60, help_text="Required. Add a valid email addess")
	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2')

class AccountAuthonticationForm(forms.ModelForm):

		class Meta:
			model = Account
			fields = ('email', 'password',)

		def clean(self):
			if self.is_valid():
				email = self.cleaned_data['email']
				password = self.cleaned_data['password']
				if not authenticate(email=email, password=password):
					raise forms.ValidationError("Invalig login")

class AddRoomForm(forms.ModelForm):
	roomname = forms.CharField(max_length=60)
	class Meta:
		model = Room
		fields = ('roomname', 'roomsize', 'is_taken', 'roomimage')

class UpdateServiceForm(forms.ModelForm):
	

	class Meta:
		model = Room
		fields = ('roomimage', 'roomname', 'car_price', 'car_description', 'roomimage2', 'roomimage3', 'roomimage4')

	def save(self, commit=True):
		#if self.is_valid():
		update_room = self.instance
		
		if self.is_valid():
			update_room.roomname 		= self.cleaned_data['roomname']
			update_room.car_price 		= self.cleaned_data['car_price']
			update_room.car_description = self.cleaned_data['car_description']
			#print(self.cleaned_data['basic_price_title'])
			#catagoryid 					= self.cleaned_data['catagory']
			#catagory 					= Category.objects.get(categoryname=catagoryid)
			#update_room.catagory 		= catagory
			
				
				
			if self.cleaned_data['roomimage']:
				update_room.roomimage = self.cleaned_data['roomimage']
			if self.cleaned_data['roomimage2']:
				update_room.roomimage2 = self.cleaned_data['roomimage2']
			if self.cleaned_data['roomimage3']:
				update_room.roomimage3 = self.cleaned_data['roomimage3']
			if self.cleaned_data['roomimage4']:
				update_room.roomimage4 = self.cleaned_data['roomimage4']
			if commit:
				update_room.save()
		return update_room

		#else:
			#raise forms.ValidationError("validation error")	

class AddServiceForm(forms.ModelForm):

	class Meta:
		model = Room
		fields = ('roomname', 'car_price', 'car_description', 'roomimage', 'roomimage2', 'roomimage3', 'roomimage4')


class AddPriceBasic(forms.ModelForm):

	class Meta:
		model = Price
		fields = ('price_title', 'price_number', 'price_description', 'price_delivery', 'price_revision')

		



class CompleteUserProfileForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('firstname', 'lastname', 'address', 'phonenumber', 'profile_image')

	def save(self, commit=True):
		user_image = self.instance
		print(self.cleaned_data['profile_image'])
		if self.is_valid():
			user_image.firstname		= self.cleaned_data['firstname']
			user_image.lastname 		= self.cleaned_data['lastname']
			user_image.address 			= self.cleaned_data['address']
			user_image.phonenumber 		= self.cleaned_data['phonenumber']
			
			print(self.cleaned_data['firstname'],self.cleaned_data['phonenumber'])
			if self.cleaned_data['profile_image']:
				user_image.profile_image = self.cleaned_data['profile_image']
			if commit:
				user_image.save()
		
		return user_image
	