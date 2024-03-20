from django.urls import path
from review.api.views import ReviewCreateAPIView, ReviewListAPIView

urlpatterns = [
    path("", ReviewListAPIView.as_view(), name="review"),
    path("<int:order_pk>/create/", ReviewCreateAPIView.as_view(), name="createReview"),
]