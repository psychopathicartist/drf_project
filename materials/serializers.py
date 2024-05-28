from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(field='video')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_subscription(self, course):
        request = self.context.get('request')
        user = request.user
        return Subscription.objects.all().filter(user=user, course=course).exists()

    @staticmethod
    def get_lessons_count(course):
        return course.lesson_set.count()
