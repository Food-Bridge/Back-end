from rest_framework import serializers
from search.models import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField(read_only=True)
    rank_change = serializers.CharField(read_only=True)

    class Meta:
        model = SearchHistory
        fields = ['keyword', 'search_count', 'rank', 'rank_change']