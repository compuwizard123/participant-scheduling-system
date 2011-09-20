def run():
    from django.contrib.sites.models import Site
    from django.conf import settings

    Site.objects.all().delete()

    site = Site()
    site.id = settings.SITE_ID
    site.domain = 'hci.cs.' + settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()

    from django.contrib.auth.models import User

    user = User.objects.create_user('groppcw', 'groppcw@rose-hulman.edu')
    user.first_name = 'Chris'
    user.last_name = 'Gropp'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('risdenkj', 'risdenkj@rose-hulman.edu')
    user.first_name = 'Kevin'
    user.last_name = 'Risden'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('jawaidss', 'jawaidss@rose-hulman.edu')
    user.first_name = 'Samad'
    user.last_name = 'Jawaid'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('cahilltr', 'cahilltr@rose-hulman.edu')
    user.first_name = 'Trey'
    user.last_name = 'Cahill'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()