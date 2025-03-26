from .animal_disease import initialize_vertexai, interactive_diagnosis , find_animal_multiple , generate_diagnosis
from .multiple_images import generate_diagnosis2 , find_animal_images
import json
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
def find_animal(images,animal_name,age):
    initialize_vertexai()
    found = find_animal_images(images,animal_name,age)
    return json.dumps(found, indent=4)

animal_info = {
        'animal_type': 'ox',
        'breed': 'unknown',
        'estimated_age': '2-5 years',
        'notable_features': ['white and brown coloring', 'large, fleshy growths on neck'],
        'all_images_match': 'True',
        'list_of_images': {'image1': 1, 'image2': 1, 'image3': 1}
    }

questions_and_answers = [
        ("How long has your cow been showing symptoms in the neck area?", "no"),
        ("Have you noticed any changes in your cow's eating or drinking habits?", "no"),
        ("Has your cow experienced any trauma or injury recently?", "no"),
        ("Are there any environmental changes that might have affected your cow?", "no"),
        ("Has milk production changed recently?", "no"),
        ("Have you changed the feed or grazing area recently?", "no")
    ]
def diagnose(image_path, problem_area="neck", animal_info=animal_info, questions_and_answers=questions_and_answers):
    initialize_vertexai()
    print("images recieved are ",image_path)
    diagnosis = generate_diagnosis2(image_path, animal_info, problem_area, questions_and_answers)
    return json.dumps(diagnosis, indent=4)
