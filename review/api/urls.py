from django.urls import path
from review.api.views import ReviewCreateAPIView

urlpatterns = [
    path("<int:order_pk>/create/", ReviewCreateAPIView.as_view(), name="createReview"),
]