from services import get_countries


def recommend_country(
    destination,
    cgpa,
    pr,
    scholarship,
    field,
    part_time,
    ielts,
    tuition_budget
):

    countries_data = get_countries()

    reasons = []
    scores = {}

    # Initialize scores for all countries
    for country in countries_data:
        country_name = country[0]
        scores[country_name] = 0

    # User preferred destination
    if destination in scores:
        scores[destination] += 5

    # Evaluate each country
    for country in countries_data:

        country_name = country[0]
        min_cgpa = float(country[1])
        avg_tuition = int(country[2])
        scholarship_available = country[4]
        pr_available = country[5]
        min_ielts = float(country[7])

        # CGPA
        if cgpa >= min_cgpa:
            scores[country_name] += 3

        # PR Preference
        if pr == "yes" and pr_available:
            scores[country_name] += 3

        # Scholarship Preference
        if scholarship == "yes" and scholarship_available:
            scores[country_name] += 2

        # Tuition Budget
        if tuition_budget >= avg_tuition:
            scores[country_name] += 2

        # IELTS
        if ielts >= min_ielts:
            scores[country_name] += 2

        # Add reason only once
        if ielts >= 7 and "Your IELTS score strengthens your admission prospects." not in reasons:
            reasons.append(
                "Your IELTS score strengthens your admission prospects."
            )
            

    # Field Preference
    if field == "Engineering":

        if "USA" in scores:
            scores["USA"] += 3

        if "Canada" in scores:
            scores["Canada"] += 2

        if "Australia" in scores:
            scores["Australia"] += 2

        reasons.append(
            "Engineering programs are highly regarded in the recommended destination."
        )

    elif field == "Business & Management":

        if "USA" in scores:
            scores["USA"] += 4

        if "Canada" in scores:
            scores["Canada"] += 2

        reasons.append(
            "Business & Management programs are strong in the recommended destination."
        )

    elif field == "Medical":

        if "Australia" in scores:
            scores["Australia"] += 4

        if "USA" in scores:
            scores["USA"] += 2

        reasons.append(
            "Medical education opportunities align well with your interests."
        )

    elif field == "Finance":

        if "USA" in scores:
            scores["USA"] += 4

        if "Canada" in scores:
            scores["Canada"] += 2

        reasons.append(
            "Finance programs are well established in the recommended destination."
        )

    # Part-time Preference
    if part_time == "High":

        if "Canada" in scores:
            scores["Canada"] += 3

        if "Australia" in scores:
            scores["Australia"] += 3

        reasons.append(
            "Part-time work opportunities are important to you."
        )

    elif part_time == "Medium":

        if "Canada" in scores:
            scores["Canada"] += 2

        if "Australia" in scores:
            scores["Australia"] += 2

    # Budget Reasons
    if tuition_budget < 1000000:

        reasons.append(
            "Your budget is suitable for affordable study destinations."
        )

    elif tuition_budget <= 2000000:

        reasons.append(
            "Your budget supports several international study options."
        )

    else:

        reasons.append(
            "Your budget allows you to consider premium universities."
        )

    # Academic Reasons
    if cgpa >= 8:

        reasons.append(
            "Your strong academic performance improves your chances of admission."
        )

    elif cgpa >= 7:

        reasons.append(
            "Your academic profile meets the requirements of many universities."
        )

    best_country = max(scores, key=scores.get)

    return best_country, reasons, scores