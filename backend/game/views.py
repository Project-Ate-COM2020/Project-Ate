from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

from core.models import Badges
from core.serializers import BadgeSerializer

from core.models import Badges
from core.serializers import BadgeSerializer
from game.models import Consumer, Reservation, BundlePosting
from django.utils import timezone
from .serializers import ReservationSerializer
import json

# Create your views here.

try:
    for b in VARIETY_BADGES + IMPACT_BADGES:
        if not Badges.objects.filter(name=b["name"]).exists():
            Badges.objects.create(
                name=b["name"],
                min_co2=b["min_co2"],
                min_categories=b["min_categories"],
            )
except:
    pass


from authentication.permissions import IsConsumer

"""
class GameSummaryView(APIView):
    permission_classes = [IsConsumer]

    serializer_class = ReservationSerializer

    # def get(self, request, *args, **kwargs):
    #     # Mock summary data
    #     data = {
    #         "current_streak_weeks": 3,
    #         "has_rescued_this_week": True,
    #         "total_rescued_bundles": 12,
    #
    #         "estimated_co2e_saved_kg": 28.5,
    
    #         "badges": ["Explorer", "Discoverer", "Eco Starter"],
    #         "unique_categories_rescued": 3,
    #     }
    #     return Response(data)
    
     def get(self, request):
         consumer = Consumer.objects.get()
         collected = Reservation.objects.filter(Consumer=consumer, status="collected").select_related("posting")
         total_co2 = 0
         categories = set()
         for reservation in collected:
             posting = reservation.posting
             co2_per_item = CO2_PER_ITEM.get(posting.category, 1.0)
             total_co2 += co2_per_item * posting.quantity
             categories.add(posting.category)

         # Calculate if rescued this week
        now = timezone.now()
         current_week = now.isocalendar()[1]
         current_year = now.year
         has_rescued_this_week = collected.filter(
             collected_at__week=current_week,
             collected_at__year=current_year
         ).exists()

         # calculate badges
         earned_badges = []

         # variety badges
         for badge in VARIETY_BADGES:
            if len(categories) >= badge["min_categories"]:
                 earned_badges.append(badge["name"])

         # impact badges
         for badge in IMPACT_BADGES:
             if total_co2 >= badge["min_co2"]:
                 earned_badges.append(badge["name"])

         # save badges to consumer
         consumer.badges = json.dumps(earned_badges)
         consumer.save()

         return Response({
             "current_streak_weeks": consumer.streak,
             "has_rescued_this_week": has_rescued_this_week,
             "total_rescued_bundles": collected.count(),
             "estimated_co2e_saved_kg": total_co2,
             "badges": earned_badges,
             "unique_categories_rescued": len(categories)
         })
"""


class GameSummaryView(APIView):
    name = "game-summary"
    permission_classes = [IsConsumer]
    serializer_class = ReservationSerializer

    # def get(self, request, *args, **kwargs):
    #     # Mock summary data
    #     data = {
    #         "current_streak_weeks": 3,
    #         "has_rescued_this_week": True,
    #         "total_rescued_bundles": 12,
    #
    #         "estimated_co2e_saved_kg": 28.5,
    #         "badges": ["Explorer", "Discoverer", "Eco Starter"],
    #         "unique_categories_rescued": 3,
    #     }
    #     return Response(data)
    """
     def get(self, request):
         consumer = Consumer.objects.get()
         collected = Reservation.objects.filter(Consumer=consumer, status="collected").select_related("posting")
         total_co2 = 0
         categories = set()
         for reservation in collected:
             posting = reservation.posting
             co2_per_item = CO2_PER_ITEM.get(posting.category, 1.0)
             total_co2 += co2_per_item * posting.quantity
             categories.add(posting.category)

         # Calculate if rescued this week
        now = timezone.now()
         current_week = now.isocalendar()[1]
         current_year = now.year
         has_rescued_this_week = collected.filter(
             collected_at__week=current_week,
             collected_at__year=current_year
         ).exists()

         # calculate badges
         earned_badges = []

         # variety badges
         for badge in VARIETY_BADGES:
            if len(categories) >= badge["min_categories"]:
                 earned_badges.append(badge["name"])

         # impact badges
         for badge in IMPACT_BADGES:
             if total_co2 >= badge["min_co2"]:
                 earned_badges.append(badge["name"])

         # save badges to consumer
         consumer.badges = json.dumps(earned_badges)
         consumer.save()

         return Response({
             "current_streak_weeks": consumer.streak,
             "has_rescued_this_week": has_rescued_this_week,
             "total_rescued_bundles": collected.count(),
             "estimated_co2e_saved_kg": total_co2,
             "badges": earned_badges,
             "unique_categories_rescued": len(categories)
         })
"""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        consumer = Consumer.objects.get(user=user)

        return Response(
            {
                "streak": consumer.streak,
                "total": consumer.co2_saved,
                "categories_collected": consumer.categories_collected,
            }
        )


class RecentRescuesView(ListAPIView):
    name = "game-rescues"
    permission_classes = [IsConsumer]
    pagination_class = PageNumberPagination
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        consumer = Consumer.objects.get(user=user)

        return Reservation.objects.filter(
            consumer=consumer, status="collected"
        ).order_by("collected_at")

        return Reservation.objects.filter(
            consumer=consumer, status="collected"
        ).order_by("collected_at")


class ConsumerBadgesView(ListAPIView):
    permission_classes = [IsConsumer]
    serializer_class = BadgeSerializer
    serializer_class = BadgeSerializer

    def get_queryset(self):
        user = self.request.user
    def get_queryset(self):
        user = self.request.user
        consumer = Consumer.objects.get(user=user)

        return Badges.objects.filter(consumers_who_have_earned__consumer=consumer)
