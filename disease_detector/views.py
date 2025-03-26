import json
import os
import tempfile
import uuid
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse  
from django.views import View
from django.utils.decorators import method_decorator
from .utils.animal_disease_run import find_animal
from .utils.animal_disease_run import diagnose
from .serializers import DiseaseRecordSerializer , DiseaseImageSerializer
from .models import DiseaseRecord , DiseaseImage
@method_decorator(csrf_exempt, name='dispatch')

class DiseaseDetector(View):

    def post(self, request):
        try:
            images = request.FILES.getlist('images')
            if not images:
                return JsonResponse({'error': 'No images uploaded'}, status=400)
            
            temp_image_paths = []
            for image in images:
                temp_path = os.path.join(tempfile.gettempdir(), f"temp_{uuid.uuid4()}.jpg")
                with open(temp_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                temp_image_paths.append(temp_path)
            problem_area = request.POST.get('problem_area')
            animal_info = request.POST.get('animal_info')
            output = diagnose(temp_image_paths, problem_area=problem_area)
            print()
            print("output is ")
            print(output)
            print()
            output_dict = json.loads(output)
            
            # Create the main DiseaseRecord entry
            record = DiseaseRecord.objects.create(
                 # Store the first image in the DiseaseRecord model
                user_id=request.POST.get('user_id'),
                disease_name=output_dict.get('disease_name'),
                probability=output_dict.get('probability'),
                urgency_level=output_dict.get('urgency_level'),
                symptoms_analysis=output_dict.get('symptoms_analysis'),
                recommended_actions=output_dict.get('recommended_actions'),
                preventive_care=output_dict.get('preventive_care'),
            )
            
            for image in images:
                disease_image = DiseaseImage.objects.create(
                    disease_record=record,
                    user_id   = request.POST.get('user_id'),
                    image=image
                )
            
            for temp_path in temp_image_paths:
                os.remove(temp_path)
            
            serialized_record = DiseaseRecordSerializer(record)
            return JsonResponse(serialized_record.data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




@method_decorator(csrf_exempt, name='dispatch')
class GetAnimal(View):
    def get(self, request):
        return JsonResponse({'message': 'get'}, status=200)

    def post(self, request):
        try:
            images = request.FILES.getlist('images')
            if not images:
                return JsonResponse({'error': 'No images uploaded'}, status=400)

            temp_image_paths = []
            for image in images:
                temp_path = os.path.join(tempfile.gettempdir(), f"temp_{uuid.uuid4()}.jpg")
                with open(temp_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                temp_image_paths.append(temp_path)

            # Additional metadata from request
            animal_id = request.POST.get('animal_id')
            owner_id = request.POST.get('owner_id')
            animal_name = request.POST.get('animal_name')
            age = request.POST.get('age')
            # Process images
            output = find_animal(temp_image_paths,animal_name,age)
            print("***********output***************")
            print()
            print()
            print()
            print(output)
            print()
            print()
            print()
            print("***********output***************")
            output_dict = json.loads(output)

            # Create the main CowRecord entry
            # record = CowRecord.objects.create(
            #     animal_id=animal_id,
            #     owner_id=owner_id,
            #     breed=output_dict.get('breed'),
            #     age=output_dict.get('age'),
            #     gender=output_dict.get('gender'),
            #     health_status=output_dict.get('health_status')
            # )

            # Store each uploaded image in CowImage model
            # for image in images:
            #     CowImage.objects.create(
            #         cow_record=record,
            #         image=image
            #     )

            # Clean up temporary image files
            for temp_path in temp_image_paths:
                os.remove(temp_path)

            # Serialize and return the response
            # serialized_record = CowRecordSerializer(record)
            return JsonResponse(output_dict, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
