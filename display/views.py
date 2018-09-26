from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

def home_view(request):
	return render(request, 'index.html')


@login_required
def dashboard_view(request):
	return render(request, 'dashboard.html')


@login_required
def settings_view(request):
	user = request.user

	try:
		github_login = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github_login = None

	try:
		twitter_login = user.social_auth.get(provider='twitter')
	except UserSocialAuth.DoesNotExist:
		twitter_login = None

	try:
		facebook_login = user.social_auth.get(provider='facebook')
	except UserSocialAuth.DoesNotExist:
		facebook_login = None

	can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

	return render(request, 'core/settings.html', {
		'github_login': github_login,
		'twitter_login': twitter_login,
		'facebook_login': facebook_login,
		'can_disconnect': can_disconnect
	})
