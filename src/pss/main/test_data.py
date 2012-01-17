def run():
    from django.contrib.sites.models import Site
    from django.conf import settings

    Site.objects.all().delete()

    site = Site()
    site.id = settings.SITE_ID
    site.domain = 'pss.csse.rose-hulman.edu' # 'hci.' + settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()

    from django.contrib.auth.models import User

    user = User.objects.create_user('cahilltr', 'cahilltr@rose-hulman.edu')
    user.first_name = 'Trey'
    user.last_name = 'Cahill'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('greenwka', 'greenwka@rose-hulman.edu')
    user.first_name = 'Katherine'
    user.last_name = 'Greenwald'
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

    user = User.objects.create_user('risdenkj', 'risdenkj@rose-hulman.edu')
    user.first_name = 'Kevin'
    user.last_name = 'Risden'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('chenowet', 'chenowet@rose-hulman.edu')
    user.first_name = 'Stephen'
    user.last_name = 'Chenoweth'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('loaj', 'loaj@rose-hulman.edu')
    user.first_name = 'Alexander'
    user.last_name = 'Lo'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('mayhewsw', 'mayhewsw@rose-hulman.edu')
    user.first_name = 'Stephen'
    user.last_name = 'Mayhew'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    user = User.objects.create_user('aterrell', 'aterrell@cs.wisc.edu')
    user.first_name = 'Allie'
    user.last_name = 'Terrell'
    user.is_staff = True
    user.is_superuser = True
    user.set_password('temp123')
    user.save()

    from pss.main.models import Appointment, Building, Experiment, ExperimentDate, ExperimentDateTimeRange, Participant, Qualification, Researcher, Room, Slot

    building1 = Building.objects.create(name='Foo')
    building2 = Building.objects.create(name='Bar')
    building3 = Building.objects.create(name='Baz')

    room1 = Room.objects.create(building=building1, name='100')
    room2 = Room.objects.create(building=building1, name='101')
    room3 = Room.objects.create(building=building1, name='102')
    room4 = Room.objects.create(building=building2, name='200')
    room5 = Room.objects.create(building=building2, name='201')
    room6 = Room.objects.create(building=building2, name='202')
    room7 = Room.objects.create(building=building3, name='300a')
    room8 = Room.objects.create(building=building3, name='301b')
    room9 = Room.objects.create(building=building3, name='302c')

    qualification1 = Qualification.objects.create(name='Bacon ipsum dolor sit amet', description='Meatloaf shankle t-bone pork chop boudin. Hamburger venison jerky ball tip sirloin ham.')
    qualification2 = Qualification.objects.create(name='Fatback meatloaf prosciutto', description='Ham cow rump ribeye bacon, capicola meatball bresaola fatback brisket pancetta spare.')
    qualification3 = Qualification.objects.create(name='Prosciutto chuck tongue short', description='Venison beef ribs salami, ground round prosciutto shoulder brisket spare ribs.')

    researcher1 = Researcher.objects.create(user=User.objects.get(username='aterrell'), phone_number='(123) 123-1230')
    researcher2 = Researcher.objects.create(user=User.objects.get(username='cahilltr'), phone_number='(123) 123-1231')
    researcher3 = Researcher.objects.create(user=User.objects.get(username='greenwka'), phone_number='(123) 123-1232')
    researcher4 = Researcher.objects.create(user=User.objects.get(username='jawaidss'), phone_number='(123) 123-1233')
    researcher5 = Researcher.objects.create(user=User.objects.get(username='risdenkj'), phone_number='(123) 123-1234')
    researcher6 = Researcher.objects.create(user=User.objects.get(username='chenowet'), phone_number='(123) 123-1235')

    experiment1 = Experiment.objects.create(name='Short loin hamburger ground round frankfurter', description='Turducken hamburger tail brisket beef ribs', room=room8, length=50, number_of_participants_needed=2)
    experiment2 = Experiment.objects.create(name='Prosciutto meatball biltong spare ribs, tenderloin swine ham hock andouille filet mignon', description='Bresaola short ribs turkey chuck pork tail salami, capicola biltong', room=room1, length=30)
    experiment3 = Experiment.objects.create(name='Boudin biltong shankle pork, prosciutto ground round chuck t-bone shoulder tri-tip turducken', description='Ground round t-bone andouille pork belly, beef venison ham chicken', room=room6, length=50)
    experiment4 = Experiment.objects.create(name='Tenderloin swine ham hock andouille filet mignon, prosciutto meatball biltong spare ribs', description='Prosciutto strip steak pastrami drumstick, capicola fatback shoulder pancetta filet mignon sirloin brisket t-bone tail tongue', room=room6, length=55)
    experiment5 = Experiment.objects.create(name='Frankfurter sausage chuck, shoulder shank tongue prosciutto pork ball tip ham sirloin filet mignon', description='Pork loin jowl beef ribs t-bone pig shoulder, venison jerky bacon tongue', room=room7, length=15)
    experiment6 = Experiment.objects.create(name='Fatback chuck tail flank pastrami tongue leberkase, andouille sirloin frankfurter tri-tip', description='Short loin hamburger ground round frankfurter', room=room5, length=40)
    experiment7 = Experiment.objects.create(name='Flank shoulder tri-tip shankle biltong', description='Shankle tongue cow strip steak, short ribs beef tenderloin ball tip leberkase filet mignon', room=room7, length=40)
    experiment8 = Experiment.objects.create(name='Pork loin jowl capicola, ham hock ground round turkey drumstick', description='Boudin biltong shankle pork, prosciutto ground round chuck t-bone shoulder tri-tip turducken frankfurter', room=room1, length=15)
    experiment9 = Experiment.objects.create(name='Tri-tip frankfurter ham beef ribs short loin leberkase, jerky meatloaf brisket drumstick ball tip', description='Fatback chuck tail flank pastrami tongue leberkase, andouille sirloin frankfurter tri-tip', room=room7, length=20, number_of_participants_needed=4)

    experiment1.researchers.add(researcher5)
    experiment1.researchers.add(researcher1)
    experiment1.researchers.add(researcher2)
    experiment1.researchers.add(researcher4)
    experiment1.researchers.add(researcher3)
    experiment1.qualifications.add(qualification3)
    experiment1.qualifications.add(qualification2)
    experiment1.qualifications.add(qualification1)
    experiment2.researchers.add(researcher5)
    experiment2.researchers.add(researcher2)
    experiment2.researchers.add(researcher3)
    experiment2.researchers.add(researcher4)
    experiment2.researchers.add(researcher1)
    experiment2.qualifications.add(qualification3)
    experiment2.qualifications.add(qualification2)
    experiment3.researchers.add(researcher4)
    experiment3.qualifications.add(qualification2)
    experiment3.qualifications.add(qualification1)
    experiment3.qualifications.add(qualification3)
    experiment4.researchers.add(researcher2)
    experiment4.researchers.add(researcher1)
    experiment4.researchers.add(researcher5)
    experiment4.researchers.add(researcher4)
    experiment4.qualifications.add(qualification1)
    experiment5.researchers.add(researcher3)
    experiment5.researchers.add(researcher2)
    experiment5.researchers.add(researcher5)
    experiment5.qualifications.add(qualification2)
    experiment5.qualifications.add(qualification3)
    experiment6.researchers.add(researcher4)
    experiment6.researchers.add(researcher2)
    experiment6.researchers.add(researcher1)
    experiment6.researchers.add(researcher3)
    experiment6.qualifications.add(qualification1)
    experiment6.qualifications.add(qualification2)
    experiment7.researchers.add(researcher4)
    experiment7.researchers.add(researcher3)
    experiment7.researchers.add(researcher1)
    experiment7.researchers.add(researcher2)
    experiment7.researchers.add(researcher5)
    experiment7.qualifications.add(qualification2)
    experiment7.qualifications.add(qualification3)
    experiment7.qualifications.add(qualification1)
    experiment8.researchers.add(researcher4)
    experiment8.researchers.add(researcher5)
    experiment8.researchers.add(researcher1)
    experiment8.researchers.add(researcher2)
    experiment8.qualifications.add(qualification2)
    experiment8.qualifications.add(qualification3)
    experiment9.researchers.add(researcher2)
    experiment9.researchers.add(researcher5)
    experiment9.qualifications.add(qualification1)
    experiment9.qualifications.add(qualification2)
    experiment9.qualifications.add(qualification3)

    import datetime

    t = datetime.date.today() - datetime.date(2011, 10, 21)

    experiment_date1 = ExperimentDate.objects.create(experiment=experiment5, date=datetime.date(2011, 10, 22) + t)
    experiment_date_time_range1 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date1, start_time=datetime.time(19, 15), end_time=datetime.time(20, 15))
    experiment_date_time_range1.create_slots()
    experiment_date_time_range2 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date1, start_time=datetime.time(17, 50), end_time=datetime.time(19, 55))
    experiment_date_time_range2.create_slots()
    experiment_date2 = ExperimentDate.objects.create(experiment=experiment6, date=datetime.date(2011, 10, 27) + t)
    experiment_date_time_range3 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date2, start_time=datetime.time(15, 45), end_time=datetime.time(17, 40))
    experiment_date_time_range3.create_slots()
    experiment_date_time_range4 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date2, start_time=datetime.time(18, 25), end_time=datetime.time(21, 30))
    experiment_date_time_range4.create_slots()
    experiment_date3 = ExperimentDate.objects.create(experiment=experiment6, date=datetime.date(2011, 10, 21) + t)
    experiment_date4 = ExperimentDate.objects.create(experiment=experiment6, date=datetime.date(2011, 10, 25) + t)
    experiment_date_time_range5 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date4, start_time=datetime.time(13, 15), end_time=datetime.time(16, 15))
    experiment_date_time_range5.create_slots()
    experiment_date_time_range6 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date4, start_time=datetime.time(12, 20), end_time=datetime.time(15, 15))
    experiment_date_time_range6.create_slots()
    experiment_date5 = ExperimentDate.objects.create(experiment=experiment2, date=datetime.date(2011, 10, 21) + t)
    experiment_date_time_range7 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date5, start_time=datetime.time(9, 35), end_time=datetime.time(10, 30))
    experiment_date_time_range7.create_slots()
    experiment_date_time_range8 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date5, start_time=datetime.time(12, 15), end_time=datetime.time(15, 10))
    experiment_date_time_range8.create_slots()
    experiment_date6 = ExperimentDate.objects.create(experiment=experiment7, date=datetime.date(2011, 10, 21) + t)
    experiment_date_time_range9 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date6, start_time=datetime.time(13, 20), end_time=datetime.time(15, 20))
    experiment_date_time_range9.create_slots()
    experiment_date7 = ExperimentDate.objects.create(experiment=experiment7, date=datetime.date(2011, 10, 26) + t)
    experiment_date_time_range10 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date7, start_time=datetime.time(16, 50), end_time=datetime.time(19, 55))
    experiment_date_time_range10.create_slots()
    experiment_date_time_range11 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date7, start_time=datetime.time(19, 30), end_time=datetime.time(20, 35))
    experiment_date_time_range11.create_slots()
    experiment_date8 = ExperimentDate.objects.create(experiment=experiment7, date=datetime.date(2011, 10, 22) + t)
    experiment_date_time_range12 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date8, start_time=datetime.time(10, 25), end_time=datetime.time(11, 25))
    experiment_date_time_range12.create_slots()
    experiment_date_time_range13 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date8, start_time=datetime.time(10, 30), end_time=datetime.time(14, 30))
    experiment_date_time_range13.create_slots()
    experiment_date9 = ExperimentDate.objects.create(experiment=experiment1, date=datetime.date(2011, 10, 25) + t)
    experiment_date_time_range14 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date9, start_time=datetime.time(14, 30), end_time=datetime.time(16, 30))
    experiment_date_time_range14.create_slots()
    experiment_date10 = ExperimentDate.objects.create(experiment=experiment9, date=datetime.date(2011, 10, 21) + t)
    experiment_date_time_range15 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date10, start_time=datetime.time(8, 45), end_time=datetime.time(9, 40))
    experiment_date_time_range15.create_slots()
    experiment_date_time_range16 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date10, start_time=datetime.time(8, 25), end_time=datetime.time(10, 25))
    experiment_date_time_range16.create_slots()
    experiment_date11 = ExperimentDate.objects.create(experiment=experiment9, date=datetime.date(2011, 10, 27) + t)
    experiment_date_time_range17 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date11, start_time=datetime.time(12, 30), end_time=datetime.time(15, 35))
    experiment_date_time_range17.create_slots()
    experiment_date_time_range18 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date11, start_time=datetime.time(8, 30), end_time=datetime.time(12, 30))
    experiment_date_time_range18.create_slots()
    experiment_date12 = ExperimentDate.objects.create(experiment=experiment9, date=datetime.date(2011, 10, 24) + t)
    experiment_date_time_range19 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date12, start_time=datetime.time(7, 40), end_time=datetime.time(11, 45))
    experiment_date_time_range19.create_slots()
    experiment_date_time_range20 = ExperimentDateTimeRange.objects.create(experiment_date=experiment_date12, start_time=datetime.time(10, 20), end_time=datetime.time(11, 15))
    experiment_date_time_range20.create_slots()

    participant1 = Participant.objects.create(user=User.objects.get(username='loaj'), phone_number='(123) 123-1236')
    participant2 = Participant.objects.create(user=User.objects.get(username='mayhewsw'), phone_number='(123) 123-1237')