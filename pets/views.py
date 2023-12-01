from rest_framework.views import status, Response, Request, APIView
from .serializers import PetSerializer
from .models import Pet
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination

class PetView(APIView, PageNumberPagination):
    def post(self, request:Request)-> Response:
        serializer = PetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST,
            )
        group_data = serializer.validated_data.pop('group')

        traits_data = serializer.validated_data.pop('traits')
        try:
            group = Group.objects.get(**group_data)
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data,group=group)

        traits = []

        for current_trait_data in traits_data:
            try:
                trait = Trait.objects.get(name__iexact=current_trait_data["name"])
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**current_trait_data)
            traits.append(trait)
            pet.traits.add(trait)

        serializer = PetSerializer(pet)
        return Response(serializer.data,status.HTTP_201_CREATED)

    def get(self, request:Request)-> Response:
        pets = Pet.objects.all()
        result = self.paginate_queryset(pets,request)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)
    
class PetDetailView(APIView):
    def get(self,request:Request,pet_id: int) -> Response:
        try:
            found_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({
                "detail": "Not found."
            },status.HTTP_400_BAD_REQUEST)
        serializer = PetSerializer(found_pet)
        return Response(serializer.data,status.HTTP_200_OK)
    
    def delete(self,request:Request,pet_id: int) -> Response:
        try:
            found_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({
                "detail": "Not found."
            },status.HTTP_400_BAD_REQUEST)
        found_pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request:Request,pet_id: int) -> Response:
        try:
            found_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status.HTTP_400_BAD_REQUEST
                )
        serializer = PetSerializer(data = request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST,
            )
        for key, value in serializer.validated_data.items():
            setattr(found_pet, key, value)
        found_pet.save()
        serializer = PetSerializer(found_pet)
        return Response(serializer.data, status.HTTP_200_OK)
