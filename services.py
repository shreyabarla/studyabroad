import ast
from database import get_connection

def get_or_create_user(name, email, phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE email=%s
        """,
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        user_id = existing_user[0]

    else:

        cursor.execute(
            """
            INSERT INTO users(name,email,phone)
            VALUES(%s,%s,%s)
            RETURNING user_id
            """,
            (name, email, phone)
        )

        user_id = cursor.fetchone()[0]

        conn.commit()

    cursor.close()
    conn.close()

    return user_id

def save_student_response(
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
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO student_responses(
        user_id,
        preferred_destination,
        education,
        cgpa,
        study_field,
        budget,
        scholarship,
        pr,
        part_time,
        ielts_score,
        tuition_budget
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    RETURNING response_id
    """, (
        user_id,
        destination,
        education,
        cgpa,
        field,
        budget,
        scholarship == "yes",
        pr == "yes",
        part_time,
        ielts,
        tuition_budget
    ))

    response_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return response_id

def save_report(response_id, country, reasons):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports(response_id, recommended_country, reasons)
        VALUES (%s, %s, %s)
    """, (
        response_id,
        country,
        "\n".join(reasons)
    ))

    conn.commit()
    cursor.close()
    conn.close()

def get_reports_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        reports.report_id,
        reports.recommended_country,
        TO_CHAR(
            reports.generated_at,
            'DD Mon YYYY | HH12:MI AM'
        ) AS generated_at

        FROM reports

        JOIN student_responses

        ON reports.response_id = student_responses.response_id

        JOIN users

        ON users.user_id = student_responses.user_id

        WHERE users.email=%s

        ORDER BY reports.generated_at DESC
        """,
        (email,)
    )

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports

def get_report_by_id(report_id):

    

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            recommended_country,
            reasons

        FROM reports

        WHERE report_id=%s
        """,
        (report_id,)
    )

    report = cursor.fetchone()

    cursor.close()
    conn.close()

    return report

def get_report_details(report_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            users.name,
            users.phone,
            users.email,
            student_responses.preferred_destination,
            student_responses.education,
            student_responses.cgpa,
            student_responses.study_field,
            student_responses.budget,
            student_responses.scholarship,
            student_responses.pr,
            student_responses.part_time,
            student_responses.ielts_score,
            student_responses.tuition_budget,
            reports.recommended_country,
            reports.reasons
        FROM reports
        JOIN student_responses
            ON reports.response_id = student_responses.response_id
        JOIN users
            ON student_responses.user_id = users.user_id
        WHERE reports.report_id = %s
    """, (report_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "phone": row[1],
        "email": row[2],
        "destination": row[3],
        "education": row[4],
        "cgpa": row[5],
        "field": row[6],
        "budget": row[7],
        "scholarship": "yes" if row[8] else "no",
        "pr": "yes" if row[9] else "no",
        "part_time": row[10],
        "ielts": row[11],
        "tuition_budget": row[12],
        "country": row[13],
        "reasons": row[14].split("\n") if row[14] else []
    }

def update_report_details(
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
):

    conn = get_connection()
    cursor = conn.cursor()

    # Update Users Table
    cursor.execute(
        """
        UPDATE users
        SET
            name=%s,
            phone=%s
        WHERE user_id=(
            SELECT student_responses.user_id
            FROM reports
            JOIN student_responses
                ON reports.response_id=student_responses.response_id
            WHERE reports.report_id=%s
        )
        """,
        (
            name,
            phone,
            report_id
        )
    )

    # Update Student Responses Table
    cursor.execute(
        """
        UPDATE student_responses
        SET
            preferred_destination=%s,
            education=%s,
            cgpa=%s,
            study_field=%s,
            budget=%s,
            scholarship=%s,
            pr=%s,
            part_time=%s,
            ielts_score=%s,
            tuition_budget=%s
        WHERE response_id=(
            SELECT response_id
            FROM reports
            WHERE report_id=%s
        )
        """,
        (
            destination,
            education,
            cgpa,
            field,
            budget,
            scholarship == "yes",
            pr == "yes",
            part_time,
            ielts,
            tuition_budget,
            report_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def update_generated_report(
    report_id,
    country,
    reasons
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reports

        SET

            recommended_country=%s,
            reasons=%s

        WHERE report_id=%s
        """,
        (
            country,
            "\n".join(reasons),
            report_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def delete_report(report_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Delete from reports table
    cursor.execute(
        """
        DELETE FROM reports
        WHERE report_id=%s
        """,
        (report_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_countries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            country_name,
            min_cgpa,
            avg_tuition,
            avg_living_cost,
            scholarship_available,
            pr_available,
            part_time_hours,
            min_ielts,
            work_visa_years
        FROM countries
    """)

    countries = cursor.fetchall()

    cursor.close()
    conn.close()

    return countries

def get_country_id(country_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT country_id
        FROM countries
        WHERE country_name = %s
    """, (country_name,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]

    return None


def get_top_universities(country_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            university_id,
            university_name,
            city,
            qs_rank,
            tuition_fee,
            min_ielts,
            duration,
            intake
        FROM universities
        WHERE country_id=%s
        ORDER BY qs_rank ASC
        LIMIT 3
    """, (country_id,))

    universities = cursor.fetchall()

    cursor.close()
    conn.close()

    return universities

def get_recommended_course(university_id, field, education):

    conn = get_connection()
    cursor = conn.cursor()

    # Field keywords
    mapping = {
        "Engineering": ["Computer", "Software", "Engineering", "AI", "Cyber", "Robotics"],
        "Business & Management": ["Business", "MBA", "Management", "Analytics"],
        "Medical": ["Biomedical", "Medicine", "Clinical", "Nursing"],
        "Finance": ["Finance"]
    }

    keywords = mapping.get(field, [])

    # First try to find a field-related course
    for keyword in keywords:

        cursor.execute("""
            SELECT
                course_name,
                degree,
                duration,
                tuition_fee
            FROM courses
            WHERE university_id = %s
              AND eligibility = %s
              AND course_name ILIKE %s
            LIMIT 1
        """, (
            university_id,
            education,
            "%" + keyword + "%"
        ))

        course = cursor.fetchone()

        if course:
            cursor.close()
            conn.close()
            return course

    # If no field-specific course is found,
    # return ANY eligible course
    cursor.execute("""
        SELECT
            course_name,
            degree,
            duration,
            tuition_fee
        FROM courses
        WHERE university_id = %s
          AND eligibility = %s
        LIMIT 1
    """, (
        university_id,
        education
    ))

    course = cursor.fetchone()

    cursor.close()
    conn.close()

    return course

