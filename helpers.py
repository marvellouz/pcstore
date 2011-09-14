from store.models import *


def init_vars(request):
	login_form=LoginForm()
	categories=Category.objects.all()
	cart=find_cart(request.user)
	if 'flash' in request.session:
		flash=request.session['flash']
	else:
		flash=None
	return locals()#({"categories": categories, "cart": cart, })

def find_cart(user):
	cart=None
	if user.is_authenticated():
		try:
			cart=user.cart
		except Cart.DoesNotExist:
			cart=Cart(customer=user)
			cart.save()
	return cart
