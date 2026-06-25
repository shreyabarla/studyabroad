from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def question():

    if request.method == "POST":

        destination = request.form["destination"]
        cgpa = float(request.form["cgpa"])
        pr = request.form["pr"]
        scholarship = request.form["scholarship"]
        field = request.form["field"]
        part_time = request.form["part_time"]
        test = request.form["test"]
        score = float(request.form["score"])
        tuition_budget = int(request.form["tuition_budget"])

        reasons = []

        canada = 0
        australia = 0
        us = 0

        if destination == "Canada":
            canada += 5
        elif destination == "Australia":
            australia += 5
        elif destination == "US":
            us += 5

        if cgpa > 8:
            us += 3
            canada += 2
            australia += 2

            reasons.append(
                "Your strong CGPA makes you eligible for competitive universities."
            )

        elif cgpa >= 7:
            canada += 2
            australia += 2

            reasons.append(
                "Your CGPA meets the academic requirements of many universities."
            )

        if pr == "yes":
            canada += 5
            australia += 4

            reasons.append(
                "You are looking for PR opportunities."
            )

        else:
            us += 3

        if scholarship == "yes":
            canada += 3
            australia += 2

            reasons.append(
                "You are looking for scholarships."
            )

        if field == "Engineering":
            us += 3
            canada += 2
            australia += 2

            reasons.append(
                "Engineering programs are strong in your recommended destination."
            )

        elif field == "Business & Management":
            us += 4
            canada += 2

            reasons.append(
                "Business & Management programs are strong in your recommended destination."
            )

        elif field == "Medical":
            australia += 4
            us += 2

            reasons.append(
                "Medical programs are strong in your recommended destination."
            )

        elif field == "Finance":
            us += 4
            canada += 2

            reasons.append(
                "Finance programs are strong in your recommended destination."
            )

        if part_time == "High":
            canada += 3
            australia += 3

            reasons.append(
                "Part-time work opportunities are important to you."
            )

        elif part_time == "Medium":
            canada += 2
            australia += 2

        if test == "IELTS":

            if score >= 7:
                canada += 2
                us += 2
                australia += 2

                reasons.append(
                    "Your IELTS score strengthens your admission prospects."
                )

        elif test == "PTE":

            if score >= 65:
                canada += 2
                us += 2
                australia += 2

                reasons.append(
                    "Your PTE score strengthens your admission prospects."
                )

        elif test == "TOEFL":

            if score >= 90:
                canada += 2
                us += 2
                australia += 2

                reasons.append(
                    "Your TOEFL score strengthens your admission prospects."
                )

        if tuition_budget < 1000000:
            canada += 3

            reasons.append(
                "Your annual tuition budget is best suited for affordable study options."
            )

        elif tuition_budget <= 2000000:
            canada += 2
            australia += 2

            reasons.append(
                "Your annual tuition budget is suitable for study options."
            )

        else:
            us += 3
            australia += 2

        countries = {
            "Canada": canada,
            "US": us,
            "Australia": australia
        }

        best_country = max(countries, key=countries.get)

        return render_template(
            "report.html",
            country=best_country,
            reasons=reasons,
            scores=countries
        )

    return render_template("questions.html")

if __name__ == "__main__":
    app.run(debug=True)