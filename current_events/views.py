from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .models import CurrentEvent


def scrape_current_events(request):
    """Scrape Wikipedia current events page and save to database"""
    url = "https://en.wikipedia.org/wiki/Portal:Current_events/2025_October_2"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the current events content
        events_container = soup.find('div', {'class': 'current-events-content'})

        if not events_container:
            return JsonResponse({'error': 'Could not find events container'}, status=404)

        events_data = []
        event_date = datetime(2025, 10, 2).date()

        # Find all event categories
        categories = events_container.find_all('table', {'class': 'vevent'})

        for category_table in categories:
            # Get category name
            category_header = category_table.find('th')
            category_name = category_header.get_text(strip=True) if category_header else 'General'

            # Get all event items in this category
            event_items = category_table.find_all('li')

            for item in event_items:
                event_text = item.get_text(strip=True)

                # Create or update event in database
                event, created = CurrentEvent.objects.get_or_create(
                    title=event_text[:500],
                    date=event_date,
                    defaults={
                        'description': event_text,
                        'category': category_name,
                        'url': url
                    }
                )

                events_data.append({
                    'title': event.title,
                    'category': event.category,
                    'created': created
                })

        return JsonResponse({
            'success': True,
            'events_scraped': len(events_data),
            'events': events_data
        })

    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch page: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Error processing data: {str(e)}'}, status=500)


def list_events(request):
    """Display all scraped current events"""
    events = CurrentEvent.objects.all()
    return render(request, 'current_events/events_list.html', {'events': events})
