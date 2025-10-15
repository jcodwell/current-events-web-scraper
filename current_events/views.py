from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from .models import CurrentEvent


def scrape_current_events(request):
    """Scrape Wikipedia current events page and save to database"""
    # Get date range from query params
    start_date_param = request.GET.get('start_date', '2025-10-2')
    end_date_param = request.GET.get('end_date', None)

    try:
        # Parse the date parameters
        start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date() if end_date_param else start_date

        # Ensure start_date is before or equal to end_date
        if start_date > end_date:
            return JsonResponse({'error': 'start_date must be before or equal to end_date'}, status=400)

        all_events_data = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Loop through each date in the range
        current_date = start_date
        while current_date <= end_date:
            # Format URL with year_month_day format
            url = f"https://en.wikipedia.org/wiki/Portal:Current_events/{current_date.year}_{current_date.strftime('%B')}_{current_date.day}"

            print(f"Scraping: {url}")

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the current events content
            events_container = soup.find('div', {'class': 'current-events-content'})

            if not events_container:
                print(f"Could not find events container for {current_date}")
                current_date += timedelta(days=1)
                continue

            events_data = []
            b_tags = events_container.find_all('b')
            events_list = []

            for idx, b_tag in enumerate(b_tags):
                cat = b_tag.get_text(strip=True)
                print("Category:", idx, cat)

                parent_p = b_tag.find_parent('p')
                if parent_p:
                    # Get next <p> with <b> tag
                    next_p = b_tags[idx + 1].find_parent('p') if idx + 1 < len(b_tags) else None

                    # Find all <ul> between current and next <p>
                    current_elem = parent_p.find_next_sibling('ul')
                    while current_elem and current_elem != next_p:
                        if current_elem.name == 'ul':
                            print("  <ul> found")
                            # Find all <li> tags within this <ul>
                            for li in current_elem.find_all('li', recursive=False):
                                li_text = li.get_text(strip=False)
                                print("<li>:", li_text)
                                

                                # Create a new event for each <li>
                                event = {
                                    "title": cat,
                                    "category": cat,
                                    "description": li_text,
                                    "url": url,
                                    "date": current_date,
                                    "scraped_at": datetime.now()
                                }
                                events_list.append(event)

                        current_elem = current_elem.find_next_sibling()

            print(f"Events List for {current_date}:", len(events_list))

            # Save events to database
            for event_data in events_list:
                # Create or update event in database
                event_obj, created = CurrentEvent.objects.get_or_create(
                    title=event_data['title'][:500],
                    date=event_data['date'],
                    defaults={
                        'description': event_data['description'],
                        'category': event_data['category'],
                        'url': event_data['url']
                    }
                )

                events_data.append({
                    'title': event_obj.title,
                    'category': event_obj.category,
                    'description': event_obj.description,
                    'url': event_obj.url,
                    'date': str(event_obj.date),
                    'created': created
                })

            all_events_data.extend(events_data)

            # Move to next date
            current_date += timedelta(days=1)

        return JsonResponse({
            'success': True,
            'events_scraped': len(all_events_data),
            'events': all_events_data
        })

    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch page: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Error processing data: {str(e)}'}, status=500)


def list_events(request):
    """Display all scraped current events"""
    events = CurrentEvent.objects.all()
    return render(request, 'current_events/events_list.html', {'events': events})
