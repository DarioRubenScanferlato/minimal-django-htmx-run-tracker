from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models.functions import TruncMonth
from django.views.decorators.http import require_http_methods
from .models import Run

def index(request):
    
    return render(request, 'index.html')

def add_run(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        distance = request.POST.get('distance')
        time = request.POST.get('time')
        note = request.POST.get('note')

        # Create a new Run object
        Run.objects.create(
            date=date,
            distance=float(distance),
            time=time,
            note=note
        )

        return run_list(request)

    # If not a POST request, redirect to the index page
    return redirect('index')


def run_list(request):
    runs = Run.objects.all().order_by('-date')
    paginator = Paginator(runs, 10)  # Show 10 runs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'run_list.html', {'page_obj': page_obj})


def yearly_total(request):
    current_date = timezone.now().date()
    current_year = current_date.year
    current_month = current_date.month

    # Calculate total distance for current year from Jan 1 to current month's end (or current date if it's the current month)
    end_date = min(current_date, datetime(current_year, current_month, 1).replace(day=1, month=current_month % 12 + 1).date() - timezone.timedelta(days=1))
    
    current_year_total = Run.objects.filter(
        date__year=current_year,
        date__lte=end_date
    ).aggregate(total=Sum('distance'))['total'] or 0

    # Calculate total distance for previous year for the same period
    previous_year_end_date = end_date.replace(year=current_year - 1)
    previous_year_total = Run.objects.filter(
        date__year=current_year - 1,
        date__lte=previous_year_end_date
    ).aggregate(total=Sum('distance'))['total'] or 0

    # Calculate percentage difference
    if previous_year_total > 0:
        percentage_diff = ((current_year_total - previous_year_total) / previous_year_total) * 100
    else:
        percentage_diff = 100  # If previous year total is 0, consider it as 100% increase

    context = {
        'yearly_total': current_year_total,
        'percentage_diff': percentage_diff,
        'previous_year': current_year - 1,
        'current_month': current_date,
    }

    return render(request, 'yearly_total.html', context)


def weekly_total(request):
    seven_days_ago = timezone.now().date() - timedelta(days=7)
    total = Run.objects.filter(date__gte=seven_days_ago).aggregate(Sum('distance'))['distance__sum'] or 0
    return render(request, 'weekly_total.html', {'weekly_total': total})



def yearly_distance_data(request):
    current_year = timezone.now().year
    monthly_data = Run.objects.filter(date__year=current_year)\
        .annotate(month=TruncMonth('date'))\
        .values('month')\
        .annotate(total_distance=Sum('distance'))\
        .order_by('month')

    data = {
        'labels': [],
        'datasets': [{
            'label': 'Monthly Distance (km)',
            'data': [],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }

    for entry in monthly_data:
        data['labels'].append(entry['month'].strftime('%B'))
        data['datasets'][0]['data'].append(float(entry['total_distance']))

    return JsonResponse(data)

@require_http_methods(["DELETE"])
def delete_run(request, run_id):
    run = get_object_or_404(Run, id=run_id)
    run.delete()
    return HttpResponse(status=204)  # No content
