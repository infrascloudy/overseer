import calendar
from datetime import date, timedelta, datetime
from .models import Service, Status
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404


def get_past_days(num):
    today = date.today()
    dates = []
    for i in range(1, num + 1):
        dates.append(today - timedelta(days=i))
    return dates


class BoardMixin:
    def get_context_data(self, **kwargs):
        context = super(BoardMixin, self).get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        return context


class IndexView(BoardMixin, ListView):
    context_object_name = "services"
    queryset = Service.objects.all()
    template_name = "board/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["default"] = Status.objects.filter(severity=10)
        context["past"] = get_past_days(5)


class ServiceView(BoardMixin, DetailView):
    model = Service
    template_name = "board/service_detail.html"

    def get(self, request, slug=None, year=None, month=None, day=None):

        data = get_object_or_404(self.model, slug=slug)

        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)

        if day:
            start_date = datetime.date(year, month, day)
            end_date = start_date + datetime.timedelta(days=1)
        elif month:
            start_date = datetime.date(year, month, 1)
            days = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = start_date + datetime.timedelta(days=days)
        elif year:
            leap = 366 if calendar.isleap(year) else 365
            start_date = datetime.date(year, 1, 1)
            end_date = start_date + datetime.timedelta(days=leap)
        else:
            # get last 30 days
            start_date = datetime.now() + timedelta(days=30)
            end_date = datetime.now()

        events = data.events.filter(start__gte=start_date).filter(start__lt=end_date)

        no_events = None
        if len(events) == 0:
            no_events = "No events found."

        context = {"service": data, "events": events, "no_events": no_events}
        return render(
            request=request, template_name=self.template_name, context=context
        )
