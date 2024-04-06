# [1]. 데이터 : 사용자의 기본 주소지
    # 사용자의 기본 주소지의 위/경도 값
# [2]. 데이터 : 식당의 주소지
    # 식당의 위/경도 값
# [3]. 카카오 모빌리티 API 호출
    # 호출 방식 : GET	https://apis-navi.kakaomobility.com/v1/future/directions
    # 요청 헤더 Authorization	KakaoAK ${REST_API_KEY}
    #                          {REST_API_KEY}: 카카오디벨로퍼스에서 발급 받은 REST API 키
    #                          Content-Type	application/json
# [4]. 요청 파라미터
    # departure_time(출발 시간, String) ▶ YYYYMMDDHHMM 형식
    # origin(출발지, String) ▶ ${X좌표},${Y좌표}
    # destination(도착지, String) ▶ ${X좌표},${Y좌표}
    # priority(경로 탐색 우선순위 옵션, String) ▶ DISTANCE: 최단 경로
    # roadevent(유고(교통사고, 행사, 재난, 도로 공사 등의 교통 장애)로 인한 도로 통제 정보 반영 옵션, Int) ▶ 0: 도로 전면 통제 정보 반영
    # summary(요약 정보 제공 여부) ▶ true: 요약 정보 제공

import requests
from datetime import datetime
from order.models import Order
from users.models import Address, User
from restaurant.models import Restaurant
from rest_framework import permissions, status
from rest_framework.response import Response
from django.conf import settings

def get_estimated_time(order_id, user):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "주문 내역이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    try:
        # 주문의 식당 정보를 출발지로 설정
        origin_latitude = order.restaurant.latitude
        origin_longitude = order.restaurant.longitude
    except Restaurant.DoesNotExist:
        return Response({"error": "주문에 대한 식당 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    try:
        # 사용자가 등록한 기본 주소를 도착지로 설정
        default_address = Address.objects.get(user=user, is_default=True)
        destination_latitude = default_address.latitude
        destination_longitude = default_address.longitude
    except Address.DoesNotExist:
        return Response({"error": "기본 주소지로 등록된 주소가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 음식점별 조리 시간이 필요할 것으로 보임(일단은 접수 후 바로 출발하는 것으로 가정)
    departure_time = datetime.now().strftime("%Y%m%d%H%M")
    origin = origin_longitude, origin_latitude
    destination = destination_longitude, destination_latitude
    priority = "DISTANCE"
    car_type = 7

    # 카카오 모빌리티 API GET 호출
    KAKAO_REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY')
    headers = {
        'Authorization': f'KakaoAK {KAKAO_REST_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "departure_time": departure_time,
        "origin": origin,
        "destination": destination,
        "priority": priority,
        "car_type": car_type,
    }
    response = requests.get('https://apis-navi.kakaomobility.com/v1/future/directions', headers=headers, params=data)
    if response.status_code == 200:
        info = response.json()
        # summary의 duration(초 단위)값을 가져와 분으로 변환
        duration_minutes = info['routes'][0]['summary']['duration'] // 60
        return duration_minutes
    else:
        return 0 #Response({"error": "카카오 모빌리티 API 호출에 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
