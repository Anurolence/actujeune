
Acujeune

The pulse of Cameroonian youth: opportunities, entrance exams, scholarships and innovations.

What is Acujeune

Acujeune is a modern platform built for young Cameroonians. It is made for high school graduates, university students, young graduates, startup creators and agro pastoral entrepreneurs.

It brings together in one place reliable information, national competitive exams, scholarships and opportunities from the ten regions of Cameroon.

Features made for Cameroonian youth

1. Direct WhatsApp sharing and quick contact
In Cameroon, WhatsApp is the main channel for students and job seekers. Each post has a Share on WhatsApp button that automatically formats the title, summary and link for groups and status. Opportunities also include a direct link to the recruiter WhatsApp number.

2. Data Saver Mode for mobile connections
Made for mobile data users on Orange, MTN, Camtel. There is an Eco Mode switch in the navigation bar that reduces data usage by disabling heavy images.

3. Tracking of entrance exams to top schools
A module dedicated to exams like ENS, ENAM, Polytechnique Yaounde and Douala, FMSB, IRIC, ENSET, and others. Clear display of deadlines and diploma requirements.

4. Scholarships and funding in FCFA
Information in local currency, XAF. Includes youth programs like the Special Three Year Youth Program from MINJEC, FONIJ, and AUF scholarships.

5. Full coverage of the 10 regions of Cameroon
Quick filter by region:
Centre, Littoral, South West, West, North, Far North, Adamawa, North West, South, East, and National.

6. Official bilingualism, French and English
Instant language switch without reloading the page.

7. Integration of support services
Reminder of the MINJEC Youth toll free number: 1515, free call for civic guidance and support for youth projects.

Automated tests

A full test suite validates all features.

Results:
Home page renders successfully
Metadata and opportunity statistics working
Retrieved concours posts from API
Created Cameroonian opportunity post ID
Retrieved single post
Detail HTML page renders with FCFA and WhatsApp info
Updated post
Like and unlike working
Added comment
Deleted post and verified 404
ALL CAMEROONIAN ENHANCEMENT TESTS PASSED SUCCESSFULLY

Project structure

acujeune/
 app/
 http://main.py FastAPI server, web routes and REST API
 http://database.py SQLite and automatic migrations
 http://models.py Pydantic models with opportunity fields
 http://crud.py Business logic and regional filters
 seed_data.py Real data on Cameroonian youth
 static/
 css/
 http://style.css Tricolor palette, WhatsApp buttons, eco mode
 js/
 http://app.js Client logic, WhatsApp direct, filters, CRUD
 http://i18n.js Bilingual dictionary French and English
 uploads/ Directory for uploaded images
 templates/
 http://index.html Main responsive page with filters
 post_detail.html Detail page with WhatsApp contacts and FCFA
 tests/
 test_api.py Integration test suite
 http://requirements.txt Python dependencies
 http://run.py Python entry point
 http://run.sh Quick start bash script
