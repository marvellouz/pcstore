# -*- coding: utf-8 -*-
# Copyright (c) 2008, Ryan Witt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the organization nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from re import compile
 
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS = [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
 
class LoginRequiredMiddleware:
    """
Middleware that requires a user to be authenticated to view any page other
than LOGIN_URL. Exemptions to this requirement can optionally be specified
in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
you can copy from your urls.py).
 
Requires authentication middleware and template context processors to be
loaded. You'll get an error if they aren't.
"""
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
requires authentication middleware to be installed. Edit your\
MIDDLEWARE_CLASSES setting to insert\
'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
'django.core.context_processors.auth'."
	if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
	    # changed from if not any...
            if any( m.match(path) for m in EXEMPT_URLS):
                request.session['flash']="За да видите тази страница, трябва да сте се влезли."
                return HttpResponseRedirect(settings.LOGIN_URL)

class FlashMiddleware:
	def process_response(self, request, response):
		if hasattr(request, 'session') and 'flash' in request.session and not isinstance(response, HttpResponseRedirect): del request.session['flash']
		return response
