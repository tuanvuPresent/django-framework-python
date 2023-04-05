import re

import requests

from django.conf import settings


def send_chatwork(message, subject):
    room_id = '194304153'
    url = f'https://api.chatwork.com/v2/rooms/{room_id}/messages'
    headers = {'X-ChatWorkToken': settings.X_CHATWORKTOKEN}

    data = {
        'body': f'[info][title]{subject}[/title]{message}[/info]',
        'self_unread': 0,
    }

    requests.post(url, headers=headers, data=data)


def get_weather():
    url = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/353412'
    params = {
        'apikey': 'kDJ6a6fH9jAPQUUeUSiqoSbA0Yf78AzN',
        'language': 'vi',
        'metric': True,
    }

    response = requests.get(url, params).json()

    effectiveDate = response.get('Headline').get('EffectiveDate').split('T')[0]
    text = response.get('Headline').get('Text')

    date = response.get('DailyForecasts')[0].get('Date').split('T')[0]
    min_temperature = response.get('DailyForecasts')[0].get('Temperature').get('Minimum').get('Value')
    max_temperature = response.get('DailyForecasts')[0].get('Temperature').get('Maximum').get('Value')

    day_detail_phrase = response.get('DailyForecasts')[0].get('Day').get('IconPhrase')
    day_detail_hasPrecipitation = response.get('DailyForecasts')[0].get('Day').get('HasPrecipitation')

    day_detail_precipitationIntensity = response.get('DailyForecasts')[0].get('Day').get('PrecipitationIntensity')
    if day_detail_precipitationIntensity:
        day_detail_precipitationIntensity = (
            f'\n\t+Cường độ mưa: {day_detail_precipitationIntensity}'
        )
    else:
        day_detail_precipitationIntensity = ''

    night_detail_phrase = response.get('DailyForecasts')[0].get('Night').get('IconPhrase')
    night_detail_hasPrecipitation = response.get('DailyForecasts')[0].get('Night').get('HasPrecipitation')
    night_detail_precipitationIntensity = response.get('DailyForecasts')[0].get('Night').get('PrecipitationIntensity')
    if night_detail_precipitationIntensity:
        night_detail_precipitationIntensity = (
            f'\n\t+Cường độ mưa: {night_detail_precipitationIntensity}'
        )
    else:
        night_detail_precipitationIntensity = ''

    data = (
        f'DATE: {effectiveDate}\nNOTE: {text}'
        + f'\n\nDailyForecasts: {date}\nNhiệt độ thấp nhất: {min_temperature}\nNhiệt độ cao nhất: {max_temperature}'
    )
    data += f'\nThời tiết ban ngày:\n\t+{day_detail_phrase}\n\t+Khả năng có mưa: {day_detail_hasPrecipitation}{day_detail_precipitationIntensity}'

    data += f'\nThời tiết ban đêm:\n\t+{night_detail_phrase}\n\t+Khả năng có mưa: {night_detail_hasPrecipitation}{night_detail_precipitationIntensity}'
    return data


def get_xskt():
    try:
        url = 'https://xskt.com.vn/rss-feed/mien-bac-xsmb.rss'
        response = requests.get(url).text

        data = re.split('<description>|</description>', response)
        date = re.split('<title>|</title>', data[2])[1]

        return f'{date}\n{data[3]}'
    except Exception:
        return 'kqxs is postpone'
