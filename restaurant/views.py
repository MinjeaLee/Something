from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import xml.etree.ElementTree as ET
from haversine import haversine

@api_view(['GET'])  
def near_restaurant(request):
    user_loc = (float(request.GET.get('latitude')), float(request.GET.get('longitude')))
	# TODO : gps 통해 현재 내 위치 받아오는 작업 -> 프론트단에서 해결
	## http://127.0.0.1:8000/restaurant/get_good/?latitude=37.21302637&longitude=127.0536683

	#! 목표는 gps 좌표를 받을 거지만, 서비스 지역이 경기도이기 때문에, 좌표를 하드코딩 하겠음
    radius = float(request.GET.get('radius')) if 'radius' in request.GET else 2.5
    user_loc = (37.21302637, 127.0536683)
    
    tree = ET.parse('restaurant/restaurants.xml')
    root = tree.getroot()

    nearby_restaurants = []

    for i, restaurant in enumerate(root.findall('row')):
        if i == 0:
            continue

        rest_loc = (float(restaurant.find('REFINE_WGS84_LAT').text), float(restaurant.find('REFINE_WGS84_LOGT').text))
        distance = haversine(user_loc, rest_loc)

        # 주어진 반경 내의 식당만 선택
        if distance <= radius:
            nearby_restaurants.append({
                'name': restaurant.find('BIZEST_NM').text,
                'type': restaurant.find('BIZCOND_NM').text,
                'main_menu': restaurant.find('MAIN_MENU_NM').text,
                'tel': restaurant.find('TELNO').text,
                'addr': restaurant.find('REFINE_ROADNM_ADDR').text,
                'loc': rest_loc,
                'distance': distance
            })

    return Response(nearby_restaurants, status=status.HTTP_200_OK)