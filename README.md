# Altiora – Study Abroad Recommendation System

Altiora is a web-based Study Abroad Recommendation System that helps students find suitable countries, universities, and courses based on their academic details, preferences, IELTS score, and budget.

The main idea of this project is to make the initial study-abroad decision easier by comparing the student's requirements with information stored in the database and generating a personalized recommendation.

---

## Features

- Student questionnaire
- Country recommendation
- Supports 5 countries:
  - Canada
  - Australia
  - USA
  - UK
  - Germany
- CGPA-based recommendation
- IELTS-based recommendation
- Tuition budget consideration
- Scholarship preference
- PR preference
- Part-time work preference
- Study field consideration
- Country-wise scores
- University recommendations
- Course recommendations
- Personalized recommendation reasons
- Save student reports
- View saved reports
- Edit reports
- Delete reports
- Generate PDF reports
- PostgreSQL database integration

---

## How the Project Works

The student first fills in a questionnaire with details such as:

- Name
- Phone number
- Email
- Preferred destination
- Education level
- CGPA
- Preferred study field
- Budget
- Scholarship requirement
- PR preference
- Importance of part-time jobs
- IELTS score
- Maximum annual tuition budget

After submitting the form, the system processes these details and calculates a score for each country.

The country with the highest score is selected as the recommended destination.

After selecting the country, the system also shows the top universities available in that country and recommends a suitable course based on the student's education level and study field.

Finally, a complete report is generated with the recommendation, reasons, country scores, universities, and course details.

---

## How the Recommendation Works

The system checks different details entered by the student and gives scores to each country.

It mainly considers:

- Preferred destination – gives extra points to the country selected by the student.
- CGPA – checks whether the student's CGPA meets the country's requirement.
- IELTS score – checks whether the IELTS score is enough for the country.
- Scholarship – considers whether scholarships are available when the student needs one.
- PR – considers PR opportunities when the student prefers them.
- Tuition budget – checks whether the student's budget is enough for the country.
- Study field – gives extra points based on the student's preferred field.
- Part-time work – gives extra points to countries with better part-time opportunities when this is important to the student.

After checking all these factors, the scores of all countries are compared and the country with the highest score is recommended.

---

## University Recommendation

After a country is recommended, the system retrieves the top universities for that country from the database.

The universities are sorted based on their QS ranking and the top 3 universities are displayed in the report.

The university information includes details such as:

- University name
- City
- QS ranking
- Tuition fee
- Minimum IELTS
- Duration
- Intake

---

## Course Recommendation

The system also recommends a suitable course based on the student's education level and preferred study field.

For example:

If the student has completed 12th Grade, the system looks for courses suitable for that education level.

If the student has completed a Bachelor's Degree, the system looks for suitable Master's courses.

The system also checks the study field while selecting a course.

For example, for Engineering, it looks for courses related to areas such as:

- Computer Science
- Software
- Engineering
- Artificial Intelligence
- Cybersecurity
- Robotics

---

## Countries Supported

The system currently supports:

- Canada
- Australia
- USA
- UK
- Germany

The country information is stored in the PostgreSQL database.

---

## Technology Used

### Frontend

- HTML
- CSS
- Jinja2 Templates

### Backend

- Python
- Flask

### Database

- PostgreSQL
- psycopg2

### Other

- ReportLab for generating PDF reports
- Git and GitHub for version control

---

## Project Structure

```text
Altiora/
│
├── app.py
├── database.py
├── services.py
├── recommendation.py
├── pdf_generator.py
│
├── templates/
│   ├── questions.html
│   ├── report.html
│   ├── view_reports.html
│   ├── view_report.html
│   └── edit_report.html
│
├── static/
│   └── styles.css
│
├── README.md
├── requirements.txt
└── .gitignore