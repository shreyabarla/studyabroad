from flask import Flask, render_template, request, send_file, session, redirect, url_for
from recommendation import recommend_country
from pdf_generator import generate_pdf
from services import (
    get_or_create_user,
    save_student_response,
    save_report,
    get_reports_by_email,
    get_report_by_id,
    get_report_details,
    update_report_details,
    update_generated_report,
    delete_report,
    get_country_id,
    get_top_universities,
    get_recommended_course
)

app = Flask(__name__)

app.secret_key = "studyabroad123"

@app.route("/")
def home():
    return render_template("questions.html")

@app.route("/generate-report", methods=["POST"])
def generate_report():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]

    destination = request.form["destination"]
    education = request.form["education"]
    cgpa = float(request.form["cgpa"])

    field = request.form["field"]
    budget = request.form["budget"]

    scholarship = request.form["scholarship"]
    pr = request.form["pr"]

    part_time = request.form["part_time"]

    ielts = float(request.form["ielts"])

    tuition_budget = int(request.form["tuition_budget"])

    best_country, reasons, scores = recommend_country(
        destination,
        cgpa,
        pr,
        scholarship,
        field,
        part_time,
        ielts,
        tuition_budget
    )
    country_id = get_country_id(best_country)

    universities = get_top_universities(country_id)

    recommended_course = None

    if universities:
        university_id = universities[0][0]
        recommended_course = get_recommended_course(
            university_id,
            field,
            education
        )

    user_id = get_or_create_user(
        name,
        email,
        phone
    )

    response_id = save_student_response(
        user_id,
        destination,
        education,
        cgpa,
        field,
        budget,
        scholarship,
        pr,
        part_time,
        ielts,
        tuition_budget
    )

    sorted_scores = dict(
        sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    save_report(
        response_id,
        best_country,
        reasons
    )

    session["report"] = {
        "country": best_country,
        "reasons": reasons,
        "universities": universities,
        "course": list(recommended_course) if recommended_course else None
    }

    return render_template(
        "report.html",
        country=best_country,
        reasons=reasons,
        scores=sorted_scores,
        universities=universities,
        recommended_course=recommended_course,
        education=education,

        name=name,
        cgpa=cgpa,
        field=field,
        ielts=ielts,
        budget=tuition_budget
    )

@app.route("/view-reports")
def view_reports():

    return render_template("view_reports.html")

@app.route("/search-report", methods=["POST"])
def search_report():

    email = request.form["email"]

    reports = get_reports_by_email(email)

    return render_template(
        "view_reports.html",
        reports=reports
    )

@app.route("/report/<int:report_id>")
def view_report(report_id):

    report = get_report_details(report_id)

    if report is None:
        return "Report not found"

    ielts = report["ielts"] if report["ielts"] is not None else 0.0

    best_country, reasons, scores = recommend_country(
        report["destination"],
        report["cgpa"],
        report["pr"],
        report["scholarship"],
        report["field"],
        report["part_time"],
        ielts,
        report["tuition_budget"]
    )
    sorted_scores = dict(
        sorted(scores.items(), key=lambda x: x[1], reverse=True)
    )

    country_id = get_country_id(best_country)
    universities = get_top_universities(country_id)

    recommended_course = None
    if universities:
        recommended_course = get_recommended_course(
            universities[0][0],
            report["field"],
            report["education"]
        )

    currency_map = {
        "Canada": "CAD",
        "Australia": "AUD",
        "USA": "USD",
        "UK": "GBP",
        "Germany": "EUR"
    }

    return render_template(
        "report.html",
        country=best_country,
        reasons=reasons,
        scores=sorted_scores,
        universities=universities,
        recommended_course=recommended_course,
        currency=currency_map.get(best_country, ""),
        education=report["education"],
        name=report["name"],
        cgpa=report["cgpa"],
        field=report["field"],
        ielts=report["ielts"],
        budget=report["tuition_budget"]
    )

@app.route("/edit-report/<int:report_id>")
def edit_report(report_id):

    report = get_report_details(report_id)

    if report is None:
        return "Report not found"

    return render_template(
        "edit_report.html",
        report=report,
        report_id=report_id
    )

@app.route("/update-report/<int:report_id>", methods=["POST"])
def update_report(report_id):

    name = request.form["name"]
    phone = request.form["phone"]

    destination = request.form["destination"]
    education = request.form["education"]
    cgpa = float(request.form["cgpa"])

    field = request.form["field"]
    budget = request.form["budget"]

    scholarship = request.form["scholarship"]
    pr = request.form["pr"]
    part_time = request.form["part_time"]

    # IELTS only
    ielts = float(request.form["ielts"])

    tuition_budget = int(request.form["tuition_budget"])

    # Generate updated recommendation
    best_country, reasons, scores = recommend_country(
        destination,
        cgpa,
        pr,
        scholarship,
        field,
        part_time,
        ielts,
        tuition_budget
    )

    # Get universities for recommended country
    country_id = get_country_id(best_country)
    universities = get_top_universities(country_id)

    # Get recommended course
    recommended_course = None

    if universities:
        recommended_course = get_recommended_course(
            universities[0][0],
            field,
            education
        )

    # Update student response
    update_report_details(
        report_id,
        name,
        phone,
        destination,
        education,
        cgpa,
        field,
        budget,
        scholarship,
        pr,
        part_time,
        ielts,
        tuition_budget
    )

    # Update generated recommendation
    update_generated_report(
        report_id,
        best_country,
        reasons
    )

    # Currency
    currency_map = {
        "Canada": "CAD",
        "Australia": "AUD",
        "USA": "USD",
        "UK": "GBP",
        "Germany": "EUR"
    }

    currency = currency_map.get(best_country, "")

    # Sort scores
    sorted_scores = dict(
        sorted(scores.items(), key=lambda x: x[1], reverse=True)
    )

    return render_template(
        "report.html",
        country=best_country,
        reasons=reasons,
        scores=sorted_scores,
        universities=universities,
        recommended_course=recommended_course,
        currency=currency,
        education=education,
        name=name,
        cgpa=cgpa,
        field=field,
        ielts=ielts,
        budget=tuition_budget
    )

@app.route("/delete-report/<int:report_id>")
def delete_report_route(report_id):

    delete_report(report_id)

    return redirect(url_for("view_reports"))

@app.route("/download-report")
def download_report():

    report = session.get("report")

    if not report:
        return "No report available"

    filepath = "study_abroad_report.pdf"

    generate_pdf(
        filepath,
        report["country"],
        report["reasons"],
        report["universities"],
        report["course"]
    )

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)