# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import admin

from django import forms


class Category (models.Model):
	name=models.CharField(max_length=30)

	def __unicode__ (self):
		return self.name


class Producer (models.Model):
	name=models.CharField(max_length=30)
	website=models.URLField()

	def __unicode__ (self):
		return self.name


class Product (models.Model):
	name=models.CharField(max_length=30)
	description=models.CharField(max_length=100)
	price=models.FloatField()
	img=models.ImageField(upload_to='/tmp', blank=True)
	category=models.ForeignKey(Category)
	producers=models.ManyToManyField(Producer)
	
	def __unicode__ (self):
		return '%s %s %f' % (self.name, self.description, self.price)


class UserProfile(models.Model):
	user=models.OneToOneField(User)
	address=models.CharField(max_length=300)
	telephone=models.CharField(max_length=12)

  
class Cart(models.Model):
	customer=models.OneToOneField(User)

	def add_item(self, product, quantity):
		try:
			item=self.cartitem_set.get(product=product)
			item.quantity+=quantity
			item.save()
		except CartItem.DoesNotExist:
			new_item=CartItem(cart=self, product=product, quantity=quantity)
			new_item.save()
	
	def remove_item(self, item):
		if(not isinstance(item, CartItem) or not item in self.cartitem_set.all()):
			raise ValueError
		item.delete()

	def is_empty(self):
		return not bool(self.cartitem_set.all())
	def total(self):
		return sum([item.price() for item in self.cartitem_set.all()])
	

class CartItem(models.Model):
	cart=models.ForeignKey(Cart)
	product=models.ForeignKey(Product)
	quantity=models.PositiveIntegerField(default=1)
	
	def __unicode__(self):
		return self.product.name

	def price(self):
		return self.product.price*self.quantity



class Courier(models.Model):
	name=models.CharField(max_length=300)

	def __unicode__(self):
		return self.name


class PayMethod(models.Model):
	name=models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name

class OrderStatus(models.Model):
	name=models.CharField(max_length=300)
	
	def __unicode__(self):
		return self.name



class Order(models.Model):
	user=models.ForeignKey(User)
	address=models.CharField(max_length=300)
	status=models.ForeignKey(OrderStatus)
	courier=models.ForeignKey(Courier)
	pay_method=models.ForeignKey(PayMethod)
	date=models.DateTimeField(auto_now_add=True, blank=True, null=True)
	
	def total(self):
		return sum([item.item_price() for item in self.orderitem_set.all()])

class OrderItem(models.Model):
	order=models.ForeignKey(Order)
	product=models.ForeignKey(Product)
	price=models.FloatField()
	quantity=models.PositiveIntegerField(default=1)

	def item_price(self):
		return self.price*self.quantity


class OrderForm(forms.Form):
	courier=forms.ModelChoiceField(queryset=Courier.objects.all() , empty_label="---")
	address=forms.CharField(max_length=300)
	pay_method=forms.ModelChoiceField(queryset=PayMethod.objects.all(), empty_label="---")

class BuyForm(forms.Form):
	quantity=forms.IntegerField()

	def clean_quantity(self):
		quantity=self.cleaned_data['quantity']
		if quantity<=0:
			raise forms.ValidationError(u"Въведете валидна стойност.")
		return quantity


class RegisterForm(forms.Form):
	first_name=forms.CharField(max_length=20)
	last_name=forms.CharField(max_length=20)
	user_name=forms.CharField(max_length=20, required=True)
	password=forms.CharField(max_length=20, required=True)
#	password_confirmation=forms.CharField(max_length=20, required=True)
	address=forms.CharField(max_length=300, required=True)
	email=forms.EmailField(max_length=30, required=True)

	def clean_user_name(self):
		user_name=self.cleaned_data['user_name']
		try:
			User.objects.get(username=user_name)
		except User.DoesNotExist:
			return user_name
		raise forms.ValidationError(u"Потребителското име е заето")

class LoginForm(forms.Form):
	username=forms.CharField(max_length=20, required=True)
	password=forms.CharField(max_length=20, required=True)
