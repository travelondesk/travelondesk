from django.shortcuts import render
from django.views import generic
from travelondesk.forms import ServiceTicketForm, DemandTicketForm, CountryForm, UserForm, ContactForm
from travelondesk.models import ServiceTicket, DemandTicket, Country
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import auth
#from django.core.context_processors import csrf
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.urlresolvers import reverse
from pip._vendor.requests.packages.urllib3.request import RequestMethods
from django.db.models import Q 
#Страница пользователя
def accountView(request, user):
    userAccount = User.objects.get(username=user)
    template_name = 'travelondesk/account.html'
    context = {'userAccount': userAccount}
    return render(request, template_name, context)
###################################################################################################    

#Главная страница 
def index(request):
    model = Country
    template_name = 'travelondesk/index.html'
    country_list = Country.objects.order_by('name')[:270]
    context = {'country_list': country_list}
    return render(request, template_name, context)
###################################################################################################

#Список услуг
def serviceListView(request):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/serviceTickets.html' 
    latest_serviceTickets_list = ServiceTicket.objects.filter(state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        latest_serviceTickets_list = latest_serviceTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not latest_serviceTickets_list :
            return render(request, 'travelondesk/serviceTickets.html', {'ticket_list': latest_serviceTickets_list, 'categorys': categorys})
    paginator = Paginator(latest_serviceTickets_list, 15)
    page = request.GET.get('page')    
    try:
        latest_serviceTickets_list = paginator.page(page)
    except PageNotAnInteger:
        latest_serviceTickets_list = paginator.page(1)
    except EmptyPage:
        latest_serviceTickets_list = paginator.page(paginator.num_pages)   
    context = {'ticket_list': latest_serviceTickets_list, 'categorys': categorys}
    return render(request, template_name, context) 
###################################################################################################

#Список услуг по категориям  
def categoryServiceListView(request, ticket_category):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/categoryServiceTickets.html'
    category_serviceTickets_list = ServiceTicket.objects.filter(category=ticket_category, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        category_serviceTickets_list = category_serviceTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not category_serviceTickets_list :
            return render(request, 'travelondesk/categoryServiceTickets.html', {'ticket_list': category_serviceTickets_list, 'ticket_category': ticket_category, 'categorys': categorys})

    paginator = Paginator(category_serviceTickets_list, 15)
    page = request.GET.get('page')
    try:
        category_serviceTickets_list = paginator.page(page)
    except PageNotAnInteger:
        category_serviceTickets_list = paginator.page(1)
    except EmptyPage:
        category_serviceTickets_list = paginator.page(paginator.num_pages)        
    context = {'ticket_list': category_serviceTickets_list, 'ticket_category': ticket_category, 'categorys': categorys}
    return render(request, template_name, context) 
###################################################################################################

#Список услуг по пользователю  
def userServiceListView(request, user):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/userServiceTickets.html'
    userId = User.objects.get(username=user)
    user_serviceTickets_list = ServiceTicket.objects.filter(author=userId).order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        user_serviceTickets_list = user_serviceTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not user_serviceTickets_list :
            return render(request, 'travelondesk/userServiceTickets.html', {'ticket_list': user_serviceTickets_list, 'username': user})

    paginator = Paginator(user_serviceTickets_list, 15)
    page = request.GET.get('page')
    try:
        user_serviceTickets_list = paginator.page(page)
    except PageNotAnInteger:
        user_serviceTickets_list = paginator.page(1)
    except EmptyPage:
        user_serviceTickets_list = paginator.page(paginator.num_pages)        
    context = {'ticket_list': user_serviceTickets_list, 'username': user}
    return render(request, template_name, context) 
###################################################################################################

#Список услуг по стране
def countryServiceListView(request, country_shortName):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/countryServiceTickets.html'
    countryId = Country.objects.filter(shortName=country_shortName)
    country_serviceTickets_list = ServiceTicket.objects.filter(countryTable=countryId, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        country_serviceTickets_list = country_serviceTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not country_serviceTickets_list :
            return render(request, 'travelondesk/countryServiceTickets.html', {'ticket_list': country_serviceTickets_list, 'categorys': categorys})

    paginator = Paginator(country_serviceTickets_list, 15)
    page = request.GET.get('page') 
    try:
        country_serviceTickets_list = paginator.page(page)
    except PageNotAnInteger:
        country_serviceTickets_list = paginator.page(1)
    except EmptyPage:
        country_serviceTickets_list = paginator.page(paginator.num_pages)  
    context = {'ticket_list': country_serviceTickets_list, 'country_shortName': country_shortName, 'categorys': categorys}
    return render(request, template_name, context)
###################################################################################################

#Список услуг по стране и по категории
def countryCategoryServiceListView(request, country_shortName, ticket_category):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/countryCategoryServiceTickets.html'
    countryId = Country.objects.filter(shortName=country_shortName)
    country_serviceTickets_list = ServiceTicket.objects.filter(countryTable=countryId, category=ticket_category, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        country_serviceTickets_list = country_serviceTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not country_serviceTickets_list :
            return render(request, 'travelondesk/countryCategoryServiceTickets.html', {'ticket_list': country_serviceTickets_list, 'country_shortName': country_shortName, 'ticket_category': ticket_category, 'categorys': categorys})

    paginator = Paginator(country_serviceTickets_list, 15)
    page = request.GET.get('page')     
    try:
        country_serviceTickets_list = paginator.page(page)
    except PageNotAnInteger:
        country_serviceTickets_list = paginator.page(1)
    except EmptyPage:
        country_serviceTickets_list = paginator.page(paginator.num_pages)  
    context = {'ticket_list': country_serviceTickets_list, 'country_shortName': country_shortName, 'ticket_category': ticket_category, 'categorys': categorys}
    return render(request, template_name, context)  
###################################################################################################

#Список запросов
def demandListView(request):
    model = DemandTicket
    categorys = model.category_choices
    template_name = 'travelondesk/demandTickets.html'
    latest_demandTickets_list = DemandTicket.objects.filter(state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        latest_demandTickets_list = latest_demandTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not latest_demandTickets_list :
            return render(request, 'travelondesk/demandTickets.html', {'ticket_list': latest_demandTickets_list, 'categorys': categorys})

    paginator = Paginator(latest_demandTickets_list, 15)
    page = request.GET.get('page')     
    try:
        latest_demandTickets_list = paginator.page(page)
    except PageNotAnInteger:
        latest_demandTickets_list = paginator.page(1)
    except EmptyPage:
        latest_demandTickets_list = paginator.page(paginator.num_pages)
    context = {'ticket_list': latest_demandTickets_list, 'categorys': categorys}
    return render(request, template_name, context) 
###################################################################################################

#Список запросов по категориям  
def categoryDemandListView(request, ticket_category):
    model = DemandTicket
    categorys = model.category_choices
    template_name = 'travelondesk/categoryDemandTickets.html'
    category_demandTickets_list = DemandTicket.objects.filter(category=ticket_category, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        category_demandTickets_list = category_demandTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not category_demandTickets_list :
            return render(request, 'travelondesk/categoryDemandTickets.html', {'ticket_list': category_demandTickets_list, 'categorys': categorys, 'ticket_category': ticket_category})

    paginator = Paginator(category_demandTickets_list, 15)
    page = request.GET.get('page')     
    try:
        category_demandTickets_list = paginator.page(page)
    except PageNotAnInteger:
        category_demandTickets_list = paginator.page(1)
    except EmptyPage:
        category_demandTickets_list = paginator.page(paginator.num_pages)
    context = {'ticket_list': category_demandTickets_list, 'categorys': categorys, 'ticket_category': ticket_category, 'categorys': categorys}
    return render(request, template_name, context)
###################################################################################################

#Список запросов по пользователю  
def userDemandListView(request, user):
    model = ServiceTicket
    categorys = model.category_choices
    template_name = 'travelondesk/userDemandTickets.html'
    userId = User.objects.get(username=user)
    user_demandTickets_list = DemandTicket.objects.filter(author=userId).order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        user_demandTickets_list = user_demandTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not user_demandTickets_list :
            return render(request, 'travelondesk/userDemandTickets.html', {'ticket_list': user_demandTickets_list, 'username': user})

    paginator = Paginator(user_demandTickets_list, 15)
    page = request.GET.get('page')
    try:
        user_demandTickets_list = paginator.page(page)
    except PageNotAnInteger:
        user_demandTickets_list = paginator.page(1)
    except EmptyPage:
        user_demandTickets_list = paginator.page(paginator.num_pages)        
    context = {'ticket_list': user_demandTickets_list, 'username': user}
    return render(request, template_name, context) 
###################################################################################################

#Список запросов по стране
def countryDemandListView(request, country_shortName):
    model = DemandTicket
    categorys = model.category_choices
    template_name = 'travelondesk/countryDemandTickets.html'
    countryId = Country.objects.filter(shortName=country_shortName)
    country_demandTickets_list = DemandTicket.objects.filter(countryTable=countryId, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        country_demandTickets_list = country_demandTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not country_demandTickets_list :
            return render(request, 'travelondesk/countryDemandTickets.html', {'ticket_list': country_demandTickets_list, 'categorys': categorys})

    paginator = Paginator(country_demandTickets_list, 15)
    page = request.GET.get('page')     
    try:
        country_demandTickets_list = paginator.page(page)
    except PageNotAnInteger:
        country_demandTickets_list = paginator.page(1)
    except EmptyPage:
        country_demandTickets_list = paginator.page(paginator.num_pages)   
    context = {'ticket_list': country_demandTickets_list, 'country_shortName': country_shortName, 'categorys': categorys}
    return render(request, template_name, context)
###################################################################################################

#Список запросов по стране и по категории
def countryCategoryDemandListView(request, country_shortName, ticket_category):
    model = DemandTicket
    categorys = model.category_choices
    template_name = 'travelondesk/countryCategoryDemandTickets.html'
    countryId = Country.objects.filter(shortName=country_shortName)
    print(ticket_category)
    country_demandTickets_list = DemandTicket.objects.filter(countryTable=countryId, category=ticket_category, state='active').order_by('-modifyDate')
    query = request.GET.get('search')
    if query :
        country_demandTickets_list = country_demandTickets_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(email__icontains=query) |
            Q(place__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query) |
            Q(phone__icontains=query)
            ).distinct().order_by('-modifyDate')
        if not country_demandTickets_list :
            return render(request, 'travelondesk/countryCategoryDemandTickets.html', {'ticket_list': country_demandTickets_list, 'ticket_category': ticket_category, 'categorys': categorys})

    paginator = Paginator(country_demandTickets_list, 15)
    page = request.GET.get('page')     
    try:
        country_demandTickets_list = paginator.page(page)
    except PageNotAnInteger:
        country_demandTickets_list = paginator.page(1)
    except EmptyPage:
        country_demandTickets_list = paginator.page(paginator.num_pages)
    print(country_demandTickets_list)
    context = {'ticket_list': country_demandTickets_list, 'country_shortName': country_shortName, 'ticket_category': ticket_category, 'categorys': categorys}
    return render(request, template_name, context)
###################################################################################################

#Просмотр услуги  
class ServiceDetailView(generic.DetailView):
    model = ServiceTicket
    template_name = 'travelondesk/serviceDetail.html'
###################################################################################################

#Просмотр заявки        
class DemandDetailView(generic.DetailView):
    model = DemandTicket
    template_name = 'travelondesk/demandDetail.html'
###################################################################################################

#Редактирование юзера
def userEdit(request, user):
    user = User.objects.get(username=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            userData = form.cleaned_data
            user = form.save(commit=False)
            user.first_name = userData['first_name']
            user.last_name = userData['last_name']
            user.save()
            return HttpResponseRedirect(reverse('travelondesk:account', args=(user.username,)))
    else:
        form = UserChangeForm(instance=user)   
    return render(request, 'travelondesk/userEdit.html', {'form': form, 'username': user}) 
###################################################################################################

#Редактирование услуги
def serviceEdit(request, pk):
    ticket = get_object_or_404(ServiceTicket, pk=pk)
    authorTicket = ticket.author
    country = Country()
    if request.method == "POST":
        form = ServiceTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticketData = form.cleaned_data
            ticket = form.save(commit=False)
            #ticket.pubDate = timezone.now()
            ticket.author = auth.get_user(request)
            ticket.name = ticketData['name']
            ticket.description = ticketData['description']
            ticket.phone = ticketData['phone']
            ticket.coast = ticketData['coast']
            ticket.place = ticketData['place']
            ticket.latitude = ticketData['latitude']
            ticket.longitude = ticketData['longitude']
            ticket.country = ticketData['country']
            ticket.countryShort = ticketData['countryShort']
            ticket.region = ticketData['region']
            ticket.city = ticketData['city']
            ticket.img = ticketData['img']
            ticket.email = ticketData['email']
            ticket.state = ticketData['state']
            ticket.category = ticketData['category']
            try:
                country = Country.objects.get(shortName__exact=ticket.countryShort)
            except Country.DoesNotExist:
                country.name = ticketData['country']
                country.shortName = ticketData['countryShort']
                country.save() 
            ticket.countryTable = country
            ticket.save()
            return HttpResponseRedirect(reverse('travelondesk:serviceDetail', args=(ticket.id,)))
    else:
        form = ServiceTicketForm(instance=ticket)   
    return render(request, 'travelondesk/serviceEdit.html', {'form': form, 'authorTicket': authorTicket})        
###################################################################################################

#Редактирование запроса
def demandEdit(request, pk):
    ticket = get_object_or_404(DemandTicket, pk=pk)
    authorTicket = ticket.author
    country = Country()
    if request.method == "POST":
        form = DemandTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticketData = form.cleaned_data
            ticket = form.save(commit=False)
            #ticket.pubDate = timezone.now()
            #ticket.author = auth.get_user(request)
            ticket.name = ticketData['name']
            ticket.description = ticketData['description']
            ticket.phone = ticketData['phone']
            ticket.coast = ticketData['coast']
            ticket.place = ticketData['place']
            ticket.latitude = ticketData['latitude']
            ticket.longitude = ticketData['longitude']
            ticket.country = ticketData['country']
            ticket.countryShort = ticketData['countryShort']
            ticket.region = ticketData['region']
            ticket.city = ticketData['city']
            ticket.img = ticketData['img']
            ticket.email = ticketData['email']
            ticket.state = ticketData['state']
            ticket.category = ticketData['category']
            try:
                country = Country.objects.get(shortName__exact=ticket.countryShort)
            except Country.DoesNotExist:
                country.name = ticketData['country']
                country.shortName = ticketData['countryShort']
                country.save() 
            ticket.countryTable = country
            ticket.save()
            return HttpResponseRedirect(reverse('travelondesk:demandDetail', args=(ticket.id,)))
    else:
        form = DemandTicketForm(instance=ticket)   
    return render(request, 'travelondesk/demandEdit.html', {'form': form, 'authorTicket': authorTicket})
###################################################################################################    

#Создание нового тикета услуги
def serviceTicketNew(request):
    ticket = ServiceTicket()
    country = Country()
    if request.method == "POST":
        form = ServiceTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticketData = form.cleaned_data
            print(ticketData)
            ticket = form.save(commit=False)
            ticket.pubDate = timezone.now()
            ticket.author = auth.get_user(request)
            ticket.name = ticketData['name']
            ticket.description = ticketData['description']
            ticket.phone = ticketData['phone']
            ticket.coast = ticketData['coast']
            ticket.place = ticketData['place']
            ticket.latitude = ticketData['latitude']
            ticket.longitude = ticketData['longitude']
            ticket.country = ticketData['country']
            ticket.countryShort = ticketData['countryShort']
            ticket.region = ticketData['region']
            ticket.city = ticketData['city']
            ticket.img = ticketData['img']
            ticket.email = ticketData['email']
            ticket.state = ticketData['state']
            ticket.category = ticketData['category']
            #countryShortName = request.POST['countryShort']
            try:
                country = Country.objects.get(shortName__exact=ticket.countryShort)
            except Country.DoesNotExist:
                country.name = ticketData['country']
                country.shortName = ticketData['countryShort']
                country.save() 
            ticket.countryTable = country
            ticket.save()
            return HttpResponseRedirect(reverse('travelondesk:serviceDetail', args=(ticket.id,)))
    else:
        form = ServiceTicketForm()   
    return render(request, 'travelondesk/serviceTicketNew.html', {'form': form})
###################################################################################################

#Создание нового тикета заявки
def demandTicketNew(request):
    ticket = DemandTicket()
    country = Country()
    if request.method == "POST":
        form = DemandTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticketData = form.cleaned_data
            ticket = form.save(commit=False)
            ticket.pubDate = timezone.now()
            ticket.author = auth.get_user(request)
            ticket.name = ticketData['name']
            ticket.description = ticketData['description']
            ticket.phone = ticketData['phone']
            ticket.coast = ticketData['coast']
            ticket.place = ticketData['place']
            ticket.latitude = ticketData['latitude']
            ticket.longitude = ticketData['longitude']
            ticket.country = ticketData['country']
            ticket.countryShort = ticketData['countryShort']
            ticket.region = ticketData['region']
            ticket.city = ticketData['city']
            ticket.img = ticketData['img']
            ticket.email = ticketData['email']
            ticket.state = ticketData['state']
            ticket.category = ticketData['category']
            try:
                country = Country.objects.get(shortName__exact=ticket.countryShort)
            except Country.DoesNotExist:
                country.name = ticketData['country']
                country.shortName = ticketData['countryShort']
                country.save() 
            ticket.countryTable = country
            ticket.save()
            return HttpResponseRedirect(reverse('travelondesk:demandDetail', args=(ticket.id,)))
    else:
        form = DemandTicketForm()   
    return render(request, 'travelondesk/demandTicketNew.html', {'form': form})

def contactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipients = ['travelondesk.contact@gmail.com']
            if copy:
                recipients.append(sender)
            else:
                message = 'sender: ' + sender + ' mail: ' + message
            try:
                send_mail(subject,  message, 'travelondesk.adm@gmail.com', recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return render(request, 'travelondesk/thanks.html')
    else:
        form = ContactForm()
    return render(request, 'travelondesk/contact.html', {'form': form})

def thanksView(reguest):
    thanks = 'thanks'
    return render(reguest, 'travelondesk/thanks.html', {'thanks': thanks})

def aboutView(reguest):
    about = 'about'
    return render(reguest, 'travelondesk/about.html', {'about': about})

def termOfServiceView(reguest):
    term = 'term'
    return render(reguest, 'travelondesk/term.html', {'term': term})

def deleteServiceTicket(request, pk):
    ServiceTicket.objects.get(id=pk).delete()
    if request.GET['next']:
        return HttpResponseRedirect(request.GET['next'])
    return render(request, 'travelondesk/deleteService.html')
    
def deleteDemandTicket(request, pk):
    DemandTicket.objects.get(id=pk).delete()
    if request.GET['next']:
        return HttpResponseRedirect(request.GET['next'])
    return render(request, 'travelondesk/deleteDemand.html')