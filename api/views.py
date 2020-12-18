from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import jwt
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import get_authorization_header
from .models import Contact, Number
from .serializers import ContactSerializer


class SignupView(APIView):
    def post(self, request):
        phone = request.data.get('phone', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)

        try:
            user = User.objects.create_user(
                username=phone, email=email, password=password, first_name=name)
            user.save()

            token = jwt.encode(
                {'id': user.id}, 'keepasecreat', algorithm='HS256')
            return Response({"token": token}, status=200)
        except Exception as e:
            return Response({"error": "Phone no is already registered!!"}, status=400)


class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)
        user = authenticate(username=phone, password=password)
        if user is not None:
            token = jwt.encode({'id': user.id},
                               'keepasecreat', algorithm='HS256')
            return Response({"token": token}, status=200)
        else:
            return Response({"error": "Invalid Credentials!!"}, status=400)


def authenticateToken(request):
    token = get_authorization_header(request).split()[1]
    try:
        id = jwt.decode(token, 'keepasecreat', algorithms=['HS256'])['id']
        user = User.objects.get(id=id)
        return (user, '')
    except:
        return ('', {"error": "plz do authenticate!!"})


class SpamView(APIView):
    def post(self, request):
        user, error = authenticateToken(request)
        if(error):
            return Response(error, status=400)
        else:
            phone = request.data.get('phone', None)
            try:
                number = Number.objects.get(phone=phone)
                number.spam = True
                number.save()
                return Response({'message': "Successfully marked as spam!!"}, status=200)
            except Exception as e:
                return Response({'message': "There is no Number!!"}, status=400)


class SearchView(APIView):
    def get(self, request):
        user, error = authenticateToken(request)
        searchterm = request.GET.get('searchterm', None)
        if(searchterm is None):
            error = {"error": "provide a searchterm!"}
        if error:
            return Response(error, status=400)
        else:
            try:
                phone = int(searchterm)
                try:
                    number = Number.objects.get(phone=phone)
                    contacts = Contact.objects.filter(number=number)
                    serializedData = ContactSerializer(
                        contacts, many=True).data
                    return Response({'data': serializedData}, status=200)
                except:
                    numbers = Number.objects.filter(phone__contains=phone)
                    contacts = None
                    for number in numbers:
                        contact = Contact.objects.filter(number=number)
                        if contacts is None:
                            contacts = contact
                        else:
                            contacts = contacts.union(contact)
                    serializedData = ContactSerializer(
                        contacts, many=True).data
                    return Response({'data': serializedData}, status=200)

            except:
                exact = Contact.objects.filter(name=searchterm)
                contains = Contact.objects.filter(name__contains=searchterm)
                contactsList = (exact | contains).distinct()
                serializedData = ContactSerializer(
                    contactsList, many=True).data
                return Response({'data': serializedData}, status=200)


class ContactsView(APIView):
    def get(self, request):
        user, error = authenticateToken(request)
        if(error):
            return Response(error, status=400)
        else:
            contacts = Contact.objects.filter(contactof=user)
            serializedData = ContactSerializer(contacts, many=True).data
            return Response({'data': serializedData}, status=200)
