from app.retriever import search_assessments
from app.llm import generate_response
from app.prompts import SYSTEM_PROMPT


def needs_clarification(user_message):

    message = user_message.lower()

    role_keywords = [
        "developer",
        "engineer",
        "manager",
        "analyst",
        "sales",
        "java",
        "python",
        "finance",
        "hr",
        "marketing",
        "support"
    ]

    seniority_keywords = [
        "entry",
        "junior",
        "mid",
        "senior",
        "lead",
        "manager",
        "executive"
    ]

    has_role = any(
        word in message
        for word in role_keywords
    )

    has_seniority = any(
        word in message
        for word in seniority_keywords
    )

    too_short = len(message.split()) < 5

    return too_short or not has_role or not has_seniority


def is_off_topic(user_message):

    blocked_phrases = [
        "ignore previous instructions",
        "bypass",
        "hack",
        "illegal",
        "amazon test",
        "google test",
        "openai test"
    ]

    message = user_message.lower()

    return any(
        phrase in message
        for phrase in blocked_phrases
    )


def is_comparison_query(message):

    comparison_words = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    return any(
        word in message.lower()
        for word in comparison_words
    )


def is_refinement_query(message):

    refinement_words = [
        "shorter",
        "longer",
        "easier",
        "harder",
        "remote",
        "adaptive",
        "more technical",
        "less technical",
        "another",
        "better"
    ]

    return any(
        word in message.lower()
        for word in refinement_words
    )


def process_chat(messages):

    latest_user_message = messages[-1]["content"]

    # STEP 1 — Off-topic / prompt injection protection
    if is_off_topic(latest_user_message):

        return {
            "reply": (
                "I can only provide recommendations "
                "related to SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # STEP 2 — Comparison handling
    if is_comparison_query(latest_user_message):

        results = search_assessments(
            latest_user_message,
            top_k=2
        )

        comparison_text = ""

        for r in results:

            comparison_text += f"""
            Name: {r['name']}
            Description: {r['description']}
            Assessment Types: {r['assessment_types']}
            """

        prompt = f"""
        {SYSTEM_PROMPT}

        Compare these SHL assessments:

        {comparison_text}

        Explain:
        - Key differences
        - Best use cases
        - Hiring scenarios
        - Skill focus
        """

        reply = generate_response(prompt)

        recommendations = []

        for r in results:

            recommendations.append({
                "name": r["name"],
                "url": r["url"],
                "test_type": (
                    r["assessment_types"][0]
                    if r["assessment_types"]
                    else "Unknown"
                )
            })

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # STEP 3 — Refinement handling
    if is_refinement_query(latest_user_message):

        results = search_assessments(
            latest_user_message,
            top_k=5
        )

        refinement_text = ""

        for r in results:

            refinement_text += f"""
            Name: {r['name']}
            Description: {r['description']}
            Duration: {r.get('duration', 'Unknown')}
            Remote Support: {r.get('remote', 'Unknown')}
            Adaptive: {r.get('adaptive', 'Unknown')}
            """

        prompt = f"""
        {SYSTEM_PROMPT}

        USER FOLLOW-UP REQUEST:
        {latest_user_message}

        AVAILABLE SHL ASSESSMENTS:
        {refinement_text}

        Refine the recommendations based on the user's updated preferences.
        """

        reply = generate_response(prompt)

        recommendations = []

        for r in results:

            recommendations.append({
                "name": r["name"],
                "url": r["url"],
                "test_type": (
                    r["assessment_types"][0]
                    if r["assessment_types"]
                    else "Unknown"
                )
            })

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # STEP 4 — Clarification handling
    if needs_clarification(latest_user_message):

        return {
            "reply": (
                "Could you provide more details about the role, "
                "experience level, and required skills?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # STEP 5 — Semantic retrieval
    results = search_assessments(
        latest_user_message,
        top_k=5
    )

    recommendations = []

    for r in results:

        recommendations.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": (
                r["assessment_types"][0]
                if r["assessment_types"]
                else "Unknown"
            )
        })

    # STEP 6 — Build assessment context
    assessment_text = ""

    for r in results:

        assessment_text += f"""
        Name: {r['name']}
        Description: {r['description']}
        URL: {r['url']}
        Types: {r['assessment_types']}
        """

    # STEP 7 — Create LLM prompt
    prompt = f"""
    {SYSTEM_PROMPT}

    USER REQUEST:
    {latest_user_message}

    RETRIEVED SHL ASSESSMENTS:
    {assessment_text}

    Generate a professional recommendation response.
    """

    # STEP 8 — Generate AI response
    reply = generate_response(prompt)

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": False
    }