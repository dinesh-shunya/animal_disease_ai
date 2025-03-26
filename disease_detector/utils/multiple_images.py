
import base64
import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

def generate_diagnosis2(image_paths, animal_info, problem_area, questions_and_answers):
    print("animal_info")
    print(animal_info)
    images = []
    for path in image_paths:
        try:
            with open(path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read())
                images.append(Part.from_data(
                    mime_type="image/jpeg",  # Assuming JPEG, adjust if needed
                    data=base64.b64decode(encoded_string)
                ))
        except FileNotFoundError:
            print(f"Error: File not found at path: {path}")
            return None  # Or handle the error as needed
        except Exception as e:
            print(f"Error processing image {path}: {e}")
            return None
    answers_text = "\n".join([
            f"Q{i+1}: {question}\nA: {answer}" 
            for i, (question, answer) in enumerate(questions_and_answers)
        ])
    print("answers_text")
    print(answers_text)
    text_part2 = """
        Tell me if both are same also you can find any disease in the images and list all animal names in JSON format (return just JSON).
    """

    text_part = f"""
    You are a veterinary AI assistant. Analyze the provided information about the animal.

    Always respond in a valid JSON format with no additional explanation.

    Animal Details:
    - Animal Type: {animal_info.get('animal_type')}
    - Breed: {animal_info.get('breed', 'Unknown')}
    - Age: {animal_info.get('estimated_age', 'Unknown')}
    - Reported Problem Area: {problem_area}
    
    Additional Information:
    {answers_text}

    Your JSON response must include the following fields:
  
    {{
        "number_of_images": "Number of images analyzed",
        "disease_name": "Most probable disease based on the reported symptoms",
        "probability": "Probability of the disease in percentage (e.g., '85%')",
        "urgency_level": "Urgency level (low, medium, high, critical)",
        "symptoms_analysis": "Detailed analysis of the reported symptoms",
        "recommended_actions": "Step-by-step recommended actions to take immediately",
        "preventive_care": "Suggestions to prevent this disease in the future"
    }}

    Important:
    - If no disease is detected, set 'disease_name' to 'None', 'probability' to '0%', and 'urgency_level' to 'low'.
    - The JSON should be properly formatted. Return ONLY the JSON object, with no additional commentary.
    - dont enclose json in ``` give only json object
    """

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),

        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]

    vertexai.init(project="white-smile-435206-g8", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001" ,
        system_instruction=[text_part]
                            )
 

    contents = [text_part] + images

    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
        # system_instruction=[types.Part.from_text(text=text_part)]
    )

    finalResponse = ""
    for response in responses:
        finalResponse += response.text
    print("final response",finalResponse)
    return json.loads(finalResponse)






def find_animal_images(image_paths,animal_name,age):
    print("images recieved in find animal are ",image_paths)
    images = []
    for path in image_paths:
        try:
            with open(path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read())
                images.append(Part.from_data(
                    mime_type="image/jpeg",  # Assuming JPEG, adjust if needed
                    data=base64.b64decode(encoded_string)
                    
                ))
        except FileNotFoundError:
            print(f"Error: File not found at path: {path}")
            return None  # Or handle the error as needed
        except Exception as e:
            print(f"Error processing image {path}: {e}")
            return None
    print("images_opened")
    


    text_part = f"""You are analyzing multiple images to identify a real, living {animal_name}. Ignore any illustrations, toys, statues, paintings, or AI-generated unrealistic images.

    Analyze the provided animal images carefully (the recieved animal age is {age}) and return ONLY a valid JSON object with the following structure and details if there is any error return same json but with empty string keys :

    {{
        "animal_type": "Type of animal (must be one of the following: cow, cat, hen, ox, horse)",
        "breed": "Specific breed if identifiable, otherwise use 'unknown'",
        "estimated_age": "Approximate age range (e.g., '1-2 years', '5-7 years')",
        "notable_features": ["List", "any", "distinctive", "physical features", "or", "markings"],
        "all_images_match": "True if all images are of the same animal (same entity), False otherwise",
        "list_of_images": {{ 
                list item contains key image_name which stores image name as value and second item in list is matches which stores boolean value if image is of same entity or not make sure you give this format for each image
                 ["image_name" : "image's name as string", 
                "matches" : "True if it's of the same entity (same animal and same person(entity)), False otherwise , format should be exactly same image_name is fix key whose value is image name and matches is fix key whose value is boolean"],
                ["image_name" : "image's name as string",
                              "matches" : "True if it's of the same entity (same animal and same person(entity)), False otherwise , format should be exactly same image_name is fix key whose value is image name and matches is fix key whose value is boolean"],
            and all other images... 
        }}
    }}
    

    Important Guidelines:
    - Ensure the images are of the same entity (not different animals).
    - Ensure the {animal_name} is REAL and alive.
    - Ensure your JSON is properly formatted with no extra commentary or explanation outside of the JSON object.
    - Don't enclose the JSON in triple backticks, just provide the JSON object.
    - always return valid json and only json and dont enclose it with ```
    """


    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),

    ]

    vertexai.init(project="white-smile-435206-g8", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001" ,
        system_instruction=[text_part]
                            )
 

    contents = [text_part] + images

    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
        # system_instruction=[types.Part.from_text(text=text_part)]
    )

    finalResponse = ""
    for response in responses:
        finalResponse += response.text
    return json.loads(finalResponse)




