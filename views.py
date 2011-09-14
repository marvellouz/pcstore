# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from pcstore.store.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from helpers import *


def index(request):
	return render_to_response('template.html', locals(), context_instance=RequestContext(request))

def contacts(request):
	return render_to_response('contacts.html', locals(), context_instance=RequestContext(request))

def howto(request):
	return render_to_response('howto.html', locals(), context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html', locals(), context_instance=RequestContext(request))

def products(request, cat):
	try:
		Category.objects.get(id=cat)
	except Category.DoesNotExist:
		request.session['flash']="Категорията не съществува."
		return HttpResponseRedirect('/')
	products_list=Product.objects.filter(category=cat)
	return render_to_response('products.html',  locals(), context_instance=RequestContext(request))

def product_info(request, prod):
	if request.user.is_authenticated():
		try:
			item=request.user.cart.cartitem_set.get(product=prod)
		except CartItem.DoesNotExist:
			item=None

	product=Product.objects.get(id=prod)

	if request.method=='POST':
		form=BuyForm(request.POST)
		if form.is_valid():
			cart=find_cart(request.user)
			cart.add_item(Product.objects.get(id=prod), form.cleaned_data['quantity'])
			cart.save()
			request.session['flash']="Успешно добавихте продукта."
			return HttpResponseRedirect('/show_cart/')
	else:
		form=BuyForm()
	return render_to_response('product_info.html', locals(), context_instance=RequestContext(request))

def register(request):
	if request.method=='POST':
		form=RegisterForm(request.POST)
		if form.is_valid():
			new_user=User.objects.create_user(form.cleaned_data['user_name'], form.cleaned_data['email'], form.cleaned_data['password'])
			new_user.first_name=form.cleaned_data['first_name']
			new_user.last_name=form.cleaned_data['last_name']
			new_user.save()
			new_profile=UserProfile()
			new_profile.user, new_profile.address = new_user, form.cleaned_data['address']
			new_profile.save()
			request.session['flash']=u"Успешна регистрация"
			return render_to_response('template.html', locals(), context_instance=RequestContext(request))
	else:
		form=RegisterForm()
	return render_to_response('registration/register.html', locals(), context_instance=RequestContext(request))


def login_view(request):
	if request.user.is_authenticated():
		request.session['flash']= u'Вече сте се логнали.'
		return render_to_response('template.html', locals(), context_instance=RequestContext(request))
	else:
		if request.method=='POST':
			form=LoginForm(request.POST)
			if form.is_valid():
				username=request.POST['username']
				password=request.POST['password']
				user=authenticate(username=username, password=password)
				if user and user.is_active:
					login(request, user)
					request.session['flash']= u'Здравейте '+ user.first_name +"!"
					return HttpResponseRedirect('/')
				else:
					form=LoginForm()
					request.session['flash']=u'Грешно потребителско име или парола!'
					return render_to_response('registration/login.html', locals(), context_instance=RequestContext(request))
		else:
			form=LoginForm()
	return render_to_response('registration/login.html', locals(), context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return render_to_response('template.html', locals(), context_instance=RequestContext(request))




def show_cart(request):
	return render_to_response('show_cart.html', locals(), context_instance=RequestContext(request))


def remove(request, prod_id):
	if request.method=='POST':
		cart=find_cart(request.user)
		item=CartItem.objects.get(id=prod_id)
		cart.remove_item(item)
	return HttpResponseRedirect('/show_cart/')


def order(request):
	cart=find_cart(request.user)
	if(cart.is_empty()):
		request.session['flash']="Трябва да имате продукти в количката, преди да направите поръчка"
		return HttpResponseRedirect('/')
	form=OrderForm()
	if request.method=='POST':
		form=OrderForm(request.POST)
		if form.is_valid():
			new_order=Order()
			new_order.user=request.user
			new_order.status=OrderStatus.objects.get(name="приета")
			new_order.pay_method=form.cleaned_data['pay_method']
			new_order.address=form.cleaned_data['address']
			new_order.courier=form.cleaned_data['courier']
			new_order.save()
			for item in cart.cartitem_set.all():
				order_item=OrderItem(order=new_order)
				order_item.product=item.product
				order_item.price=item.product.price
				order_item.quantity=item.quantity
				order_item.save()
			cart.delete()
			request.session['flash']="Поръчката ви беше приета успешно."
			return HttpResponseRedirect('/')
	return render_to_response("order.html", locals(), context_instance=RequestContext(request))

def my_orders(request):
	orders=Order.objects.filter(user=request.user)
	return render_to_response("orders.html", locals(), context_instance=RequestContext(request))



