import datetime

from dateutil import parser
from django.http import HttpResponse
from django.shortcuts import render
from zeep import Client


def index(request):
    city_service = Client('http://localhost:8080/soap-api/CityService?wsdl')
    flight_service = Client('http://localhost:8080/soap-api/FlightService?wsdl')
    cities = city_service.service.findAll()
    flights = flight_service.service.findAll()
    context = {
        'cities': cities,
        'flights': flights
    }
    return render(request, 'cities/cities.html', context)


def search(request):
    city_service = Client('http://localhost:8080/soap-api/CityService?wsdl')
    flight_service = Client('http://localhost:8080/soap-api/FlightService?wsdl')
    cities = city_service.service.findAll()

    date = parser.parse(request.GET.get('date'))
    time = datetime.datetime.strptime(request.GET.get('time'), "%H:%M")
    combined_date = datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
    flights = flight_service.service.getFlightsByCitiesAndDates(request.GET.get('from'), request.GET.get('to'),
                                                                combined_date)
    context = {
        'cities': cities,
        'flights': flights
    }
    return render(request, 'cities/cities.html', context)


def buy_ticket(request):
    flight_service = Client('http://localhost:8080/soap-api/FlightService?wsdl')
    flight = flight_service.service.findById(request.GET.get('flight_id'))
    context = {
        'flight': flight
    }
    return render(request, 'cities/buy_ticket.html', context)


def confirm_ticket(request):
    flight_service = Client('http://localhost:8080/soap-api/FlightService?wsdl')
    flight_code = flight_service.service.bookFlight(request.GET.get('flight_id'))
    context = {
        'flight_code': flight_code
    }
    return render(request, 'cities/confirm_ticket.html', context)


def find_ticket(request):
    ticket_service = Client('http://localhost:8080/soap-api/TicketService?wsdl')
    ticket = ticket_service.service.findByCode(request.GET.get('code'))
    context = {
        'ticket': ticket
    }
    return render(request, 'cities/find_ticket.html', context)


def find_ticket_confirmation(request):
    ticket_service = Client('http://localhost:8080/soap-api/TicketService?wsdl')
    file = ticket_service.service.getTicketConfirmation(request.GET.get('flight_code'))
    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bilet.pdf"'
    return response
