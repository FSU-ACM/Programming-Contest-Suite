from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import render, redirect
from hashid_field import Hashid

from checkin import forms
from checkin import tasks
from checkin.utils import checkin_auth
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT
from register.models import Team


@login_required
@user_passes_test(checkin_auth, login_url='/', redirect_field_name=None)
@transaction.atomic
def checkin(request):
	"""
	View to handle contestant check-in. Parses the email, swipe, and walk-in forms for valid check-in input.
	Form precedence (high > low): walk-in, swipe, email
	"""
	
	context = {}

	if request.method == 'POST':
		email_form = forms.EmailCheckinForm(request.POST)
		swipe_form = forms.SwipeCheckinForm(request.POST)
		walkin_form = forms.WalkinForm(request.POST)
		walk_in_team = None
		is_walkin = False

		if email_form.is_valid() and swipe_form.is_valid() and walkin_form.is_valid():
			# Process a walk-in selection, if one is made.
			if walkin_form.cleaned_data['division']:
				# Get team from selected division
				if walkin_form.cleaned_data['division'] == '1':
					walk_in_team = Team.objects.filter(name__contains='Walk-in-U-').filter(num_members=0).first()						
				else:
					walk_in_team = Team.objects.filter(name__contains='Walk-in-L-').filter(num_members=0).first()
				
				# If an empty walk-in is not found, notify user.
				if walk_in_team is None:
					messages.error(request, 'There are no Walk-in teams available.', fail_silently=True)
					return redirect('checkin_result')
				
				is_walkin = True

			# Process email form entry, if it has been made.
			if swipe_form.cleaned_data['fsu_num']:
				if swipe_form.valid_read():
					fsu_number = Hashid(swipe_form.parse())

					try:
						user = User.objects.get(profile__fsu_num=fsu_number)
					except:
						messages.error(
							request, 'Check in failed. FSU number not found. ', fail_silently=True)
						messages.info(request, 'Retry using email check in.', fail_silently=True)
					else:
						# User already checked in
						if user.profile.checked_in and not checkin_auth(user):
							messages.info(request, 'You are already checked in.',
							              fail_silently=True)
						# User exists but no team selection (walk-in/registered) provided
						elif user.profile.team is None and not is_walkin:
							messages.info(
								request, 'You are not a member of a registered team. Join a registered team, or select NO at the registered team prompt.', fail_silently=True)
						# Check in user
						else:
							user.profile.checked_in = True
							# If walk-in contestant, add walk-in team to profile
							if is_walkin == True:
								if user.profile.has_team():
									messages.info(
										request, 'You are a member of a registered team. Walk-in selection ignored.', fail_silently=True)
								else:
									# update user
									user.profile.team = walk_in_team

									#update team
									walk_in_team.num_members += 1
									walk_in_team.save()

							user.save()

							# Email user DOMjudge credentials
							tasks.send_credentials.delay(user.username)
							messages.success(request, str(user.first_name) +
							                 ', you are checked in!', fail_silently=True)
							messages.info(
								request, 'Check your registered email or account dashboard for DOMjudge credentials.', fail_silently=True)
				else:
					messages.error(
						request, 'Invalid card read. Please try again.', fail_silently=True)

			# Process email form entry, if it has been made.
			elif email_form.cleaned_data['email']:
				try:
					user = User.objects.get(email=email_form.cleaned_data['email'])
				except:
					messages.error(
						request, 'Check in failed. Email address not found.', fail_silently=True)
				else:
					# User already checked in
					if user.profile.checked_in and not checkin_auth(user):
						messages.info(request, 'You are already checked in.', fail_silently=True)
					# User exists but no team selection (walk-in/registered) provided
					elif user.profile.team is None and not is_walkin:
						messages.info(request, 'You are not a member of a registered team. Join a registered team, or select NO at the registered team prompt.', fail_silently=True)
					# Check in user
					else:
						user.profile.checked_in = True
						# If walk-in contestant, add walk-in team to profile
						if is_walkin == True:
							if user.profile.has_team():
								messages.info(request, 'You are a member of a registered team. Walk-in selection ignored.', fail_silently=True)
							else:
								# update user
								user.profile.team = walk_in_team

								#update team
								walk_in_team.num_members += 1
								walk_in_team.save()

						user.save()

						# Email user DOMjudge credentials
						tasks.send_credentials.delay(user.username)
						messages.success(request, str(user.first_name) + ', you are checked in!', fail_silently=True)
						messages.info(request, 'Check your registered email or account dashboard for DOMjudge credentials.', fail_silently=True)
			
			else:
				messages.error(request, 'Invalid form submission. Please resubmit your information.', fail_silently=True)

			return redirect('checkin_result')

	else:
		email_form = forms.EmailCheckinForm()
		swipe_form = forms.SwipeCheckinForm()
		walkin_form = forms.WalkinForm()

	context['email_form'] = email_form
	context['swipe_form'] = swipe_form
	context['walkin_form'] = walkin_form
	return render(request, 'checkin/checkin.html', context)


@login_required
@user_passes_test(checkin_auth, login_url='/', redirect_field_name=None)
def checkin_result(request):
	"""
	View to display the result of a check in attempt.
	"""

	return render(request, 'checkin/checkin_result.html')


@login_required
@user_passes_test(checkin_auth, login_url='/', redirect_field_name=None)
@transaction.atomic
def volunteer_checkin(request):
	"""
	View to handle contest volunteer check in.
	"""

	context = {}

	if request.method == 'POST':
		volunteer_form = forms.VolunteerForm(request.POST)

		if volunteer_form.is_valid():
			try:
				user = User.objects.get(username=volunteer_form.cleaned_data['username'])
			except:
				messages.error(request, 'Username not found', fail_silently=True)
			else:
				# Validate user is a volunteer
				if not user.profile.is_volunteer():
					messages.error(request, f"{user.first_name}, you are not registered as a volunteer.", fail_silently=True)
					return redirect('volunteer_checkin')

				contest = cache.get_or_set(
                                    'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
				
				# Contest object must exist to validate volunteerpassword entry
				if contest is None:
					messages.warning(request, 'Unable to verify PIN. Please try again later.', fail_silently=True)
				else:
					# Validate volunteer password entry
					if volunteer_form.cleaned_data['pin'] == contest.volunteer_pin:
						user.profile.checked_in = True
						user.save()

						if user.profile.has_team():
							# Email user DOMjudge credentials
							tasks.send_credentials.delay(user.username)

						messages.success(request, str(user.first_name)+' you have been checked in. Thanks again for volunteering!', fail_silently=True)
						return redirect('volunteer_checkin')
					else:
						messages.error(request, 'Incorrect PIN provided.', fail_silently=True)
	else:
		volunteer_form = forms.VolunteerForm()

	context['volunteer_form'] = volunteer_form
	return render(request, 'checkin/volunteer_checkin.html', context)
