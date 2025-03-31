from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .models import Resume  # Import the Resume model
import PyPDF2
import pytesseract
from PIL import Image
import io
import re
import spacy
from datetime import datetime

# Load Spacy's NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def extract_text_from_image(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        image = page.to_image()
        text += pytesseract.image_to_string(image)
    return text

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_mobile_number(text):
    mobile_pattern = r"\b\d{10}\b"
    match = re.search(mobile_pattern, text)
    return match.group(0) if match else None

def extract_skills(text):
    skills = ["Python", "Django", "Machine Learning", "SQL", "JavaScript"]  # Add more skills
    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return ", ".join(found_skills)

def calculate_experience(text):
    date_pattern = r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)[a-z]* \d{4}\b)"
    dates = re.findall(date_pattern, text)
    
    if len(dates) >= 2:
        try:
            start_date = datetime.strptime(dates[0], "%b %Y" if len(dates[0].split()[0]) == 3 else "%B %Y")
            end_date = datetime.strptime(dates[-1], "%b %Y" if len(dates[-1].split()[0]) == 3 else "%B %Y")
            total_experience = (end_date - start_date).days / 365.25
            return round(total_experience, 2)
        except ValueError:
            return 0
    return 0

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            text = extract_text_from_pdf(resume_file)
            if not text.strip():
                text = extract_text_from_image(resume_file)

            # Extract fields
            name = extract_name(text)
            email = extract_email(text)
            mobile_number = extract_mobile_number(text)
            skills = extract_skills(text)
            total_experience = calculate_experience(text)

            # Save to database
            resume = Resume(
                name=name,
                email=email,
                mobile_number=mobile_number,
                skills=skills,
                total_experience=total_experience,
                extracted_text=text
            )
            resume.save()

            return render(request, 'pdf_upload/upload.html', {
                'form': form,
                'extracted_text': text,
                'name': name,
                'email': email,
                'mobile_number': mobile_number,
                'skills': skills,
                'total_experience': total_experience
            })
    else:
        form = ResumeUploadForm()
    return render(request, 'pdf_upload/upload.html', {'form': form})