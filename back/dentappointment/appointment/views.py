from rest_framework import viewsets
from django.core.serializers import serialize
from . import serializers as ZERS
from .models import Appointment, ConsultingRoom, Owner, Patient, Service, Treatment, Payment
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from datetime import datetime
import io
import segno
from django.core.files.base import ContentFile
from PIL import Image
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = ZERS.AppointmetSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def appointmentsConsultingRoom(self, request, pk=None):
        appointments = Appointment.objects.prefetch_related('id_patient').filter(id_consultingRoom=pk)
        respon = self.serializer_class(appointments, many= True)
        return Response(respon.data)
    
    @action(detail=True, methods=['get'],url_path='patient', url_name='patient')
    def appointmentsPatients(self, request, pk=None):
        appointments = Appointment.objects.filter(id_patient=pk).order_by('-id')
        respon = self.serializer_class(appointments, many= True)
        return Response(respon.data)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'],url_path='createappointment', url_name='createappointment',permission_classes=[AllowAny])
    def createAppointmentPublic(self, request, *args, **kwargs):
        print(request.data)
        if request.data['firstTimePatient']:
           patient_serializer = ZERS.PatientSerializer(data=request.data['patient'])
           if patient_serializer.is_valid():
                patient_instance = patient_serializer.save()
                request.data['id_patient'] = patient_instance.id
           else:
                return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone_number = request.data['patient']['PhoneNumber']
            try:
                existing_patient = Patient.objects.get(PhoneNumber=phone_number)
                request.data['id_patient'] = existing_patient.id
            except Patient.DoesNotExist:
                return Response({'error': 'Patient with the provided phone number does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
        appointment_serializer = self.serializer_class(data=request.data)
        if appointment_serializer.is_valid():
            appointment_instance = appointment_serializer.save()
            return Response(appointment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ConsultingRoomViewSet(viewsets.ModelViewSet):
    queryset = ConsultingRoom.objects.all()
    serializer_class = ZERS.ConsultingRoomSerailizer

    def list(self, request, *args, **kwargs):
        owner = Owner.objects.get(email=request.user)
        owner_serializer = ZERS.OwnerSerailizer(owner)
        consulting_rooms =  ConsultingRoom.objects.filter(id_owner=owner_serializer.data['id']).order_by('-id')
        serializer = self.serializer_class(consulting_rooms, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        instance_cr = super().create(request, *args, **kwargs)
        url = os.getenv("SITE_URL")+'/appointment/gen/'+str(instance_cr.data['id'])
        qrcode = segno.make(url)
        out = io.BytesIO()
        qrcode.save(out, kind='png', light=None, scale=5)

        room_created =  ConsultingRoom.objects.get(id=instance_cr.data['id'])
        qr_name = 'consulting_room_'+str(instance_cr.data['id'])+'.png'
        room_created.qr_code.save(qr_name, ContentFile(out.getvalue()), save=False)
        room_created.save()
        return Response(instance_cr.data, status=instance_cr.status_code)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def logo(self, request, pk=None):
        consulting_room = self.get_object()
        serializer = ZERS.ConsultingRoomLogoSerializer(consulting_room, context={'request': request})
        return Response(serializer.data)
    
class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = ZERS.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serialized_user = serialize('json', [user], fields=('id', 'username',))
            return Response({
                'token': str(refresh.access_token),
                'user': serialized_user
            },status=status.HTTP_202_ACCEPTED)

       
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = ZERS.PatientSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def patientesPerConsultingRoom(self, request,pk=None):
        patients =  Patient.objects.filter(id_consultingRoom=pk).order_by('-id')
        result = self.serializer_class(patients, many=True)
        return Response(result.data)
    
class SericeView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class =  ZERS.ServiceSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def servicesPerConsultingRoom(self, request,pk=None):
        services =  Service.objects.filter(id_consultingRoom=pk).order_by('-id')
        result = self.serializer_class(services, many=True)
        return Response(result.data)
    
class TreatmentView(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class =  ZERS.TreatmentSerializer

    def create(self, request, *args, **kwargs):
        treatment_serializer = self.get_serializer(data=request.data)
        treatment_serializer.is_valid(raise_exception=True)
        treatment_instance = treatment_serializer.save()
        consultingroom =  ConsultingRoom.objects.get(id=request.data['id_consultingRoom'])
        Payment.objects.create(id_consultingRoom=consultingroom,contribution=request.data['payment'],id_treatment=treatment_instance)
        treatment_serializer = self.serializer_class(treatment_instance)
        return Response(treatment_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'],url_path='patient', url_name='patient')
    def treatmentsPatients(self, request, pk=None):
        treatments = Treatment.objects.filter(id_patient=pk).order_by('-id')
        respon = self.serializer_class(treatments, many= True)
        return Response(respon.data)

class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class =  ZERS.PaymentSerializer

    def create(self, request, *args, **kwargs):
        instance_cr = super().create(request, *args, **kwargs)
        query = Payment.objects.filter(id_treatment=request.data['id_treatment'])
        serializer = self.serializer_class(query,many=True)
        return Response(serializer.data, status=instance_cr.status_code)
    
    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def treatmentsPatients(self, request, pk=None):
        payments = Payment.objects.filter(id_consultingRoom=pk).order_by('-id')
        respon = self.serializer_class(payments, many= True)
        return Response(respon.data)
    
    

