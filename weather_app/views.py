import http
from io import BytesIO

from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile, Subscription

import boto3

#
# note order of decorators

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    curr_user = request.user
    # if curr_user.is_anonymous
    # userprofile = UserProfile.objects.get(user=curr_user)
    data = {
        "first_name": curr_user.first_name,
        "last_name": curr_user.last_name
    }
    return Response(data)

# current_user = api_view(['GET'])(authentication_classes([TokenAuthentication])(permission_classes([IsAuthenticated])(current_user)))


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscriptions(request):
    if request.method == 'GET':
        subs = Subscription.objects.filter(user=request.user)
        subs_list = []
        for sub in subs:
            subs_list.append({'id': sub.id, 'country': sub.country, 'city': sub.city})
        return Response(subs_list)
    elif request.method == 'POST':
        Subscription.objects.create(country=request.data['country'], city=request.data['city'], user=request.user)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_details(request, id):
    sub = Subscription.objects.get(user=request.user, id=id)
    sub.delete()
    return Response(200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_import(request):
    file_content = request.FILES['file'].file.read()
    file_as_str = file_content.decode()
    print(file_content)
    print(file_as_str)
    return Response(200)


@api_view(['GET'])
def download_file(request):
    with open('/Users/valeria/src/weather-django/weather/weather_app/urls.py', 'rb') as f:
        file_buffer = BytesIO(f.read())
        resp = FileResponse(file_buffer, as_attachment=True, filename='urls.py')
    return resp


@api_view(['GET'])
def get_countries_capitals(request):
    #https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
    try:
        s3_client = boto3.client('s3')
    except ClientError as e:
        print('Error connecting to s3 client', e)

    # # Print out bucket names
    # for bucket in s3.buckets.all():
    #     print(bucket.name)
