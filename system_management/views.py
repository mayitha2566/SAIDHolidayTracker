from django.shortcuts import render
from .models import SAID, Holiday
from datetime import datetime
import requests
from django.conf import settings
from django.views.decorators.cache import cache_control

def is_valid_id_number(id_number):
    """
    Validate a South African ID number using the Luhn algorithm.

    The ID number format is: YYMMDDSSSSCAZ
    - YYMMDD: Date of birth
    - SSSS: Sequence number defining gender
    - C: Citizenship status (0 for SA citizen, 1 for permanent resident)
    - A: Usually 8 or 9 (assumed to be 8 in this context)
    - Z: Checksum digit

    Args:
        id_number (str): The 13-digit South African ID number to validate.

    Returns:
        bool: True if the ID number is valid, False otherwise.
    """
    if len(id_number) != 13 or not id_number.isdigit():
        return False

    digits = [int(d) for d in id_number]

    # Step 1: Sum of digits in the odd positions (excluding last digit)
    sum_odd = sum(digits[::2][:6])

    # Step 2: Concatenate digits in even positions to form a number, then multiply by 2
    even_digits = ''.join(str(d) for d in digits[1:12:2])
    even_number = int(even_digits) * 2

    # Step 3: Sum the digits of the result from step 2
    sum_even = sum(int(d) for d in str(even_number))

    # Step 4: Total sum = sum from step 1 + sum from step 3
    total_sum = sum_odd + sum_even

    # Step 5: Calculate the checksum digit
    checksum_digit = (10 - (total_sum % 10)) % 10

    # Step 6: Check if the checksum digit matches the last digit of the ID number
    return checksum_digit == digits[-1]

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    """
    Handle the home view for processing South African ID numbers.

    This view accepts POST requests containing an ID number, validates it,
    decodes information, retrieves public holidays on the date of birth,
    and renders the results.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with context data.
    """
    if request.method == 'POST':
        id_number = request.POST.get('id_number')

        # Validate ID number
        if not is_valid_id_number(id_number):
            context = {'error_message': 'Invalid South African ID number.'}
            return render(request, 'system_management/results.html', context)

        # Decode ID Number
        try:
            date_of_birth_str = id_number[:6]
            date_of_birth = datetime.strptime(date_of_birth_str, '%y%m%d').date()

            current_year = datetime.now().year
            # Adjust for century
            if date_of_birth.year > current_year:
                date_of_birth = date_of_birth.replace(year=date_of_birth.year - 100)

            gender_code = int(id_number[6:10])
            gender = 'female' if gender_code < 5000 else 'male'

            citizenship_digit = int(id_number[10])
            is_citizen = True if citizenship_digit == 0 else False
        except ValueError:
            context = {'error_message': 'Invalid date in ID number.'}
            return render(request, 'system_management/results.html', context)

        # Save or Update SAID Record
        said_record, created = SAID.objects.get_or_create(
            id_number=id_number,
            defaults={
                'date_of_birth': date_of_birth,
                'gender': gender,
                'is_citizen': is_citizen,
                'search_count': 1
            }
        )
        if not created:
            said_record.search_count += 1
            said_record.save()

        # Call API to get holidays
        api_key = settings.CALENDARIFIC_API_KEY
        url = 'https://calendarific.com/api/v2/holidays'
        params = {
            'api_key': api_key,
            'country': 'ZA',
            'year': date_of_birth.year,
            'day': date_of_birth.day,
            'month': date_of_birth.month,
            'type': 'national'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['meta']['code'] == 200:
                response_data = data.get('response', {})
                if isinstance(response_data, dict) and 'holidays' in response_data:
                    holidays_data = response_data['holidays']
                    if holidays_data:
                        # Save Holidays
                        for holiday_data in holidays_data:
                            Holiday.objects.get_or_create(
                                said=said_record,
                                name=holiday_data['name'],
                                description=holiday_data['description'],
                                date=holiday_data['date']['iso'],
                                type=','.join(holiday_data.get('type', []))
                            )
                    else:
                        # No holidays found on this date
                        pass
                else:
                    # Handle empty or invalid response
                    pass
            else:
                context = {'error_message': 'Error fetching holidays from API.'}
                return render(request, 'system_management/results.html', context)

        except requests.RequestException:
            context = {'error_message': 'Network error occurred while fetching holidays.'}
            return render(request, 'system_management/results.html', context)
        except ValueError:
            context = {'error_message': 'Error parsing data from API response.'}
            return render(request, 'system_management/results.html', context)

        # Retrieve holidays from database
        holidays = Holiday.objects.filter(said=said_record)

        context = {
            'said': said_record,
            'holidays': holidays
        }
        return render(request, 'system_management/results.html', context)
    else:
        return render(request, 'system_management/home.html')