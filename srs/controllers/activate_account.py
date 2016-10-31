from django.shortcuts import redirect

from app.models import User_ConfirmationHash


def activate_account_cont(request, hash):
    uch = User_ConfirmationHash.objects.filter(type='create-account', hash=hash).get()
    if uch is not None:
        uch.user.active = True
        uch.user.save()
        uch.delete()
        request.session['activated-account'] = True
    return redirect('sign_in')