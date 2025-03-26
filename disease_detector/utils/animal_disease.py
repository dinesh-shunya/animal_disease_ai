import os
import json
import mimetypes
from PIL import Image
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def initialize_vertexai():
    vertexai.init(project="white-smile-435206-g8", location="us-central1")

def analyze_image(image_path):
    if not os.path.exists(image_path):
        raise ValueError(f"Image file does not exist: {image_path}")

    image_part = Part.from_data(
        mime_type=get_mime_type(image_path),
        data=encode_image(image_path)
    )
    
    prompt = """You are analyzing an image to identify a real, living animal. Ignore any illustrations, toys, statues, paintings, or AI-generated unrealistic images.

                Analyze the provided animal image carefully and return ONLY a valid JSON object with the following structure and details:

                {
                    "animal_type": "Type of animal (must be one of the following: cow, cat, hen, ox, horse)",
                    "breed": "Specific breed if identifiable, otherwise use 'unknown'",
                    "estimated_age": "Approximate age range (e.g., '1-2 years', '5-7 years')",
                    "notable_features": ["List", "any", "distinctive", "physical features", "or", "markings"]
                }

                Important Guidelines:
                - Make sure the animal is REAL and alive.
                - Ensure your JSON is properly formatted with no extra commentary or explanation outside of the JSON object.
                """
    
    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content([prompt, image_part])
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "animal_type": "Unknown",
            "breed": "Unknown",
            "estimated_age": "Unknown",
            "notable_features": []
        }

def multiple_images(image_paths):
    if not image_paths or not isinstance(image_paths, list):
        raise ValueError("Please provide a list of image paths.")

    # Check if all image paths exist
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise ValueError(f"Image file does not exist: {image_path}")

    # Prepare image parts for the model
    image_parts = [
        Part.from_data(
            mime_type=get_mime_type(image_path),
            data=encode_image(image_path)
        )
        for image_path in image_paths
    ]

    # Prompt for analyzing multiple images
    prompt = """You are analyzing multiple images to identify a real, living animal. Ignore any illustrations, toys, statues, paintings, or AI-generated unrealistic images.

                Analyze the provided animal images carefully and return ONLY a valid JSON object with the following structure and details:

                {
                    "animal_type": "Type of animal (must be one of the following: cow, cat, hen, ox, horse)",
                    "breed": "Specific breed if identifiable, otherwise use 'unknown'",
                    "estimated_age": "Approximate age range (e.g., '1-2 years', '5-7 years')",
                    "notable_features": ["List", "any", "distinctive", "physical features", "or", "markings"],
                    "all_images_match": "True if all images are of the same animal (same entity), False otherwise",
                    "list_of_images": {
                        "image1": 1 or 0 (1 if it's of the same entity (same entity, same animal) else 0),
                        "image2": 0 or 0 (0 if it's not of the same animal (same entity, same animal) else 1),
                        "image3": 1 or 0 (1 if it's of the same entity (same entity, same animal) or 0),
                    }
                }

                Important Guidelineb s:
                - Ensure the images are of the same entity (not different animals).
                - Ensure the animal is REAL and alive.
                - Ensure your JSON is properly formatted with no extra commentary or explanation outside of the JSON object.
                """

    # Initialize the model
    model = GenerativeModel("gemini-1.5-flash-001")

    # Generate content using the model
    response = model.generate_content([prompt] + image_parts)

    try:
        # Parse the response as JSON
        result = json.loads(response.text)
        print(result)
        return result

    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return {
            "animal_type": "Unknown",
            "breed": "Unknown",
            "estimated_age": "Unknown",
            "notable_features": [],
            "all_images_match": False,
            "list_of_images": {}
        }


def find_animal_multiple(image_paths):
    if not image_paths or not isinstance(image_paths, list):
        raise ValueError("Please provide a list of image paths.")

    # Check if all image paths exist
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise ValueError(f"Image file does not exist: {image_path}")

    # Prepare image parts for the model
    image_parts = [
        Part.from_data(
            mime_type=get_mime_type(image_path),
            data=encode_image(image_path)
        )
        for image_path in image_paths
    ]

    # Prompt for analyzing multiple images
    prompt = """You are analyzing multiple images to identify a real, living animal. Ignore any illustrations, toys, statues, paintings, or AI-generated unrealistic images.

                Analyze the provided animal images carefully and return ONLY a valid JSON object with the following structure and details:

                {
                    "animal_type": "Type of animal (must be one of the following: cow, cat, hen, ox, horse)",
                    "breed": "Specific breed if identifiable, otherwise use 'unknown'",
                    "estimated_age": "Approximate age range (e.g., '1-2 years', '5-7 years')",
                    "notable_features": ["List", "any", "distinctive", "physical features", "or", "markings"],
                    "all_images_match": "True if all images are of the same animal (same entity), False otherwise",
                    "list_of_images": {
                        "image1": 1 or 0 (1 if it's of the same entity (same entity, same animal) else 0),
                        "image2": 0 or 0 (0 if it's not of the same animal (same entity, same animal) else 1),
                        "image3": 1 or 0 (1 if it's of the same entity (same entity, same animal) or 0),
                    }
                }

                Important Guidelineb s:
                - Ensure the images are of the same entity (not different animals).
                - Ensure the animal is REAL and alive.
                - Ensure your JSON is properly formatted with no extra commentary or explanation outside of the JSON object.
                """

    # Initialize the model
    model = GenerativeModel("gemini-1.5-flash-001")

    # Generate content using the model
    response = model.generate_content([prompt] + image_parts)

    try:
        # Parse the response as JSON
        result = json.loads(response.text)
        print(result)
        return result

    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return {
            "animal_type": "Unknown",
            "breed": "Unknown",
            "estimated_age": "Unknown",
            "notable_features": [],
            "all_images_match": False,
            "list_of_images": {}
        }






def verify_animal(detected_animal, selected_animal):

    return detected_animal.get("animal_type", "").lower() == selected_animal.lower()

def generate_questions(animal_type, problem_area):

    questions = [
        f"How long has your {animal_type} been showing symptoms in the {problem_area} area?",
        f"Have you noticed any changes in your {animal_type}'s eating or drinking habits?",
        f"Has your {animal_type} experienced any trauma or injury recently?",
        f"Are there any environmental changes that might have affected your {animal_type}?"
    ]
    

    if animal_type.lower() == "cow":
        questions.append("Has milk production changed recently?")
        questions.append("Have you changed the feed or grazing area recently?")
    elif animal_type.lower() == "horse":
        questions.append("Has the horse's gait or mobility changed?")
        questions.append("Have you changed the exercise routine or terrain recently?")
    elif animal_type.lower() == "hen":
        questions.append("Has egg production changed?")
        questions.append("Have you noticed any changes in the flock's behavior?")
    
    return questions

def generate_diagnosis(image_path, animal_info, problem_area, questions_and_answers):
    image_part = Part.from_data(
        mime_type=get_mime_type(image_path),
        data=encode_image(image_path)
    )
    
    answers_text = "\n".join([
        f"Q{i+1}: {question}\nA: {answer}" 
        for i, (question, answer) in enumerate(questions_and_answers)
    ])
    
    prompt = f"""
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
    """

    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content([prompt, image_part])
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "disease_name": "Unknown",
            "probability": "0%",
            "urgency_level": "low",
            "symptoms_analysis": "Error processing diagnosis",
            "recommended_actions": "Please consult with a veterinarian",
            "preventive_care": "Regular check-ups recommended"
        }

def display_diagnosis(diagnosis):
    print("\n" + "="*60)
    print(" "*20 + "DIAGNOSIS REPORT")
    print("="*60)
    
    # Urgency level with color coding
    urgency = diagnosis.get("urgency_level", "unknown").lower()
    urgency_colors = {
        "low": "\033[92m",      # Green
        "medium": "\033[93m",   # Yellow
        "high": "\033[91m",     # Red
        "critical": "\033[31m"  # Dark Red
    }
    reset_color = "\033[0m"
    
    print(f"\nURGENCY LEVEL: {urgency_colors.get(urgency, '')}{urgency.upper()}{reset_color}")
    
    # Disease and probability
    print(f"\nDIAGNOSIS: {diagnosis.get('disease_name', 'Unknown')}")
    print(f"PROBABILITY: {diagnosis.get('probability', 'Unknown')}")
    
    # Symptoms analysis
    print("\nSYMPTOMS ANALYSIS:")
    print("-" * 60)
    print(wrap_text(diagnosis.get("symptoms_analysis", "No analysis available"), 60))
    
    # Recommended actions
    print("\nRECOMMENDED ACTIONS:")
    print("-" * 60)
    print(wrap_text(diagnosis.get("recommended_actions", "No recommendations available"), 60))
    
    # Preventive care
    print("\nPREVENTIVE CARE:")
    print("-" * 60)
    print(wrap_text(diagnosis.get("preventive_care", "No preventive care suggestions available"), 60))
    
    print("\n" + "="*60)

def wrap_text(text, width):
    """Wrap text to a specific width
    
    Args:
        text (str): Text to wrap
        width (int): Width to wrap at
        
    Returns:
        str: Wrapped text
    """
    words = text.split()
    wrapped_lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            wrapped_lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        wrapped_lines.append(" ".join(current_line))
    
    return "\n".join(wrapped_lines)

def encode_image(image_path):
    """Read image file and encode it
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bytes: Binary image data
    """
    with open(image_path, "rb") as image_file:
        return image_file.read()

def get_mime_type(image_path):

    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or "application/octet-stream"

def analyze_multiple_images(image_paths, animal_type):

    results = []
    result2 = multiple_images(image_paths)
    
    for path in image_paths:
        print(f"Analyzing image: {os.path.basename(path)}...")
        try:
            # result = analyze_image(path)
            result = multiple_images(image_paths)
            results.append({
                "image_path": path,
                "analysis": result,
                "matches_expected": verify_animal(result, animal_type)
            })
        except Exception as e:
            results.append({
                "image_path": path,
                "error": str(e)
            })
    
    return results

def interactive_diagnosis():
    """Interactive terminal-based diagnosis workflow"""
    print("\n" + "="*60)
    print(" "*15 + "VETERINARY DIAGNOSIS SYSTEM")
    print("="*60)
    
    # Get animal type
    print("\nSupported animal types: cow, cat, hen, ox, horse")
    animal_type = input("Enter animal type: ").strip().lower()
    
    # Get image paths
    print("\nEnter image paths (3-9 images of the same animal).")
    print("Type 'done' when finished.")
    
    image_paths = []
    while len(image_paths) < 9:
        path = input(f"Image path {len(image_paths) + 1} (or 'done'): ").strip()
        if path.lower() == 'done':
            if len(image_paths) >= 3:
                break
            else:
                print("Please provide at least 3 images.")
                continue
        
        if not os.path.exists(path):
            print(f"Error: File does not exist: {path}")
            continue
            
        image_paths.append(path)
    
    # Analyze images
    print("\nAnalyzing images...")
    analyses = analyze_multiple_images(image_paths, animal_type)
    
    # Display analyses
    print("\nImage Analysis Results:")
    for i, analysis in enumerate(analyses):
        print(f"\nImage {i+1}: {os.path.basename(analysis['image_path'])}")
        if "error" in analysis:
            print(f"  Error: {analysis['error']}")
            continue
            
        print(f"  Animal Type: {analysis['analysis'].get('animal_type', 'Unknown')}")
        print(f"  Breed: {analysis['analysis'].get('breed', 'Unknown')}")
        print(f"  Age: {analysis['analysis'].get('estimated_age', 'Unknown')}")
        print(f"  Matches Expected: {'Yes' if analysis['matches_expected'] else 'No'}")
    
    # Choose primary image for diagnosis
    if len(analyses) > 0:
        print("\nChoose primary image for diagnosis:")
        for i, analysis in enumerate(analyses):
            if "error" not in analysis:
                print(f"{i+1}. {os.path.basename(analysis['image_path'])}")
        
        choice = int(input("Enter image number: ")) - 1
        if 0 <= choice < len(analyses) and "error" not in analyses[choice]:
            primary_image = analyses[choice]["image_path"]
            animal_info = analyses[choice]["analysis"]
            
            # Get problem area
            problem_area = input("\nEnter problem area (e.g., leg, skin, eye): ").strip()
            
            # Get answers to diagnostic questions
            questions = generate_questions(animal_type, problem_area)
            qa_pairs = []
            
            print("\nPlease answer the following diagnostic questions:")
            for i, question in enumerate(questions):
                print(f"\nQ{i+1}: {question}")
                answer = input("A: ").strip()
                qa_pairs.append((question, answer))
            
            # Generate diagnosis
            print("\nGenerating diagnosis...")
            print()
            print()
            print()
            print(primary_image, animal_info, problem_area, qa_pairs)
            print()
            print()
            print()
            print()
            print()
            diagnosis = generate_diagnosis(primary_image, animal_info, problem_area, qa_pairs)
            
            # Display diagnosis
            display_diagnosis(diagnosis)
        else:
            print("Invalid choice or image has error.")
    else:
        print("No valid images to analyze.")

def main():
    # Initialize Vertex AI
    try:
        initialize_vertexai()
        interactive_diagnosis()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

