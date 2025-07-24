def definition(metric: str):
    if metric == "Fluency":
        return "Is the response fluent and understandable?"
    elif metric == "Empathy":
        return "Measure the frequency and depth of empathy exhibited by the response. Evaluate whether the response shows a genuine understanding of the post's emotions and whether its responses reflect timely and appropriate concern."
    elif metric == "Helpfulness":
        return "Evaluate the ability of the response to provide practical solutions and assistance during the dialogue. Consider whether the model offers effective advice and actionable steps tailored to the post's specific problems, such as emotional distress or requests for help."
    elif metric == "Socio political influence":
        return "The responder understands the current sociopolitical system and its impact on the author of the post."
    elif metric == "Knowledge":
        return "The responder demonstrates knowledge about the author of the post's culture."
    elif metric == "Communication":
        return "The responder's communication is appropriate for the author of the post."
    elif metric == "Cultural context":
        return "The responder perceives the problem within the appropriate cultural context of the author of the post."
    else:
        raise ValueError(f"Invalid metric: {metric}")

def steps(metric:str):
    """
    This function returns the steps that the evaluator should follow when evaluating a response.
    params:
        metric: str - the metric to be evaluated.
    """

    if metric == "Fluency":
        return '''
        1. Read the Post and Response
            Carefully read the post provided by the individual to understand the context, tone, and intent behind the message. Then, read the potential response to evaluate how well it meets the criteria.
        2. Focus on Fluency
            Evaluate the response solely based on fluency, which means assessing the following:
                Grammar and Syntax: Is the response free from grammatical errors or awkward phrasing?
                Clarity: Is the message easy to read and understand?
                Naturalness: Does the response sound like it could naturally come from a human?
                Flow: Do the sentences connect smoothly without abrupt or disjointed ideas?
        3. Ignore Other Factors
            While evaluating, ignore elements like relevance, emotional support, or appropriateness. Only focus on the fluency of the response, not how well it aligns with the original post or its context.
        4. Rate the Response on a Scale of 1-5
            Use the following scale to assign a score:
                1: The response is not fluent and difficult to understand (e.g., contains significant grammar issues or incomprehensible phrasing).
                2: The response has noticeable issues with fluency, but the meaning can still be understood with effort.
                3: The response is somewhat fluent but has minor awkward phrasing or grammar issues that may disrupt the flow.
                4: The response is fluent and mostly natural, with very minor issues that do not hinder understanding.
                5: The response is highly fluent, natural, and flows smoothly without any noticeable errors or awkwardness.
        5. Document Your Rating
            Only record your score and do NOT provide a whole sentence.'''
    elif metric == "Empathy":
        return '''
        1. Read the Post and Response Carefully
            Begin by reading the post thoroughly to understand its emotional tone, context, and any expressed or implied concerns.
            Then, read the response to assess how well it addresses the emotions and concerns presented in the post.
        2. Identify Empathetic Elements in the Response
            Look for signs of empathy in the response, including:
                Acknowledgment: Does the response recognize and validate the emotions expressed in the post?
                Understanding: Does the response demonstrate a clear and accurate understanding of the individual's feelings and situation?
                Supportiveness: Does the response offer appropriate reassurance, concern, or support without being dismissive or overly generic?
        3. Assess the Depth of Empathy
            Evaluate how deeply the response connects to the emotions and context of the post:
            Does it feel genuine and considerate, or does it come across as superficial or robotic?
            Is the response tailored to the individual's situation, or is it overly broad and impersonal?
        4. Rate the Response on a Scale of 1-5
            Use the following scale to assign a score:
                1: The response shows little or no empathy. It fails to acknowledge emotions or provide any support.
                2: The response shows limited empathy. It may vaguely acknowledge emotions but lacks depth or sincerity.
                3: The response demonstrates moderate empathy. It recognizes emotions and offers some support, but it could be more thoughtful or personalized.
                4: The response is empathetic and considerate, addressing emotions effectively with only minor areas for improvement.
                5: The response is highly empathetic, deeply understanding and addressing emotions with genuine care and tailored support.
        5. Document Your Rating
            Only record your score and do NOT provide a whole sentence.'''
    elif metric == "Helpfulness":
        return '''
        1. Read the Post and Response Carefully
            Begin by reading the individual's post to fully understand their specific problems, emotional state, or requests for help.
            Read the response to evaluate how well it addresses the individual's concerns and provides solutions.
        2. Analyze the Practicality of the Response
            Examine whether the response offers effective and actionable solutions:
                Relevance: Does the response address the main concerns or requests expressed in the post?
                Actionable Steps: Are the suggestions or advice practical, clear, and feasible for the individual to implement?
                Specificity: Does the response avoid vague or generic advice by offering detailed and relevant steps?
        3. Assess the Assistance Provided
            Consider the depth of support offered in the response:
                Problem-Solving: Does the response provide a tangible path toward resolving the issues raised?
                Emotional Support: If the individual is in distress, does the response combine practical advice with empathetic and supportive language?
                Adaptability: Does the response show an understanding of the individual's unique situation and offer advice tailored to their needs?
        4. Rate the Response on a Scale of 1-5
            Use the following scale to assign a score:
                1: The response is unhelpful, providing no meaningful advice or assistance related to the individual's problem.
                2: The response offers limited or generic advice with minimal practical application to the specific issue.
                3: The response provides moderately helpful advice, but it may lack depth, specificity, or alignment with the individual's unique circumstances.
                4: The response is helpful, offering practical, relevant, and mostly actionable advice with minor room for improvement.
                5: The response is highly helpful, delivering clear, tailored, and actionable solutions that directly address the individual's concerns with exceptional clarity and support.
        5. Document Your Rating
            Only record your score and do NOT provide a whole sentence. '''
    elif metric == "Socio political influence":
        return '''
        1. Read the Original Post Carefully
            - Identify any mention of the sociopolitical system or structures (e.g., racism, immigration policies, gender inequality, class issues, systemic barriers, etc.).
            - Understand how the author is affected by these systems — are they marginalized, angry, disillusioned, or seeking validation?
        2. Read the Response Carefully
            - Look for evidence that the responder acknowledges or engages with the sociopolitical context brought up in the post.
            - Determine whether the response aligns with or ignores the structural or systemic issues mentioned by the author.
        3. Assign a Socio-political influence Score (1-5)
            - Use the rubric below to rate the sociopolitical influence:
            Score	Description
                5	The response demonstrates deep understanding of the sociopolitical issues affecting the poster. It explicitly recognizes systemic factors and validates the poster's experience in that context.
                4	The response shows solid awareness of relevant sociopolitical dynamics but may not fully explore them. It still affirms the poster's struggle in a systemically grounded way.
                3	The response is neutral or superficial about sociopolitical context. It might acknowledge the poster's emotions but fails to meaningfully engage with systemic issues.
                2	The response minimizes or misses the sociopolitical context, offering platitudes or individualistic framing where structural understanding is needed.
                1	The response is ignorant, dismissive, or contradicts the sociopolitical reality expressed in the post. It may invalidate or erase structural struggles.'''
    elif metric == "Knowledge":
        return '''
        1. Read the Original Post Carefully
            - Identify explicit or implicit cultural references (e.g., language, religion, traditions, holidays, values, family structure, gender norms, immigration experiences, etc.).
            - Consider how the author's cultural identity shapes their experience or distress.
        2. Read the Response Carefully
            - Look for signs that the speaker understands, respects, or accurately refers to the author's culture.
            - Evaluate the specificity and accuracy of any cultural references or framing.
            - Check for stereotyping, assumptions, or inappropriate generalizations.
        3. Assign a Knowledge Score (1-5)
            - Use this rubric:
            Score	Description
                5	The response shows strong, accurate, and nuanced knowledge of the author's culture. It reflects deep familiarity and avoids stereotypes.
                4	The response demonstrates clear and respectful understanding of relevant cultural context, with some specific references or insights.
                3	The response shows general cultural sensitivity, but with limited or vague cultural specificity. No harmful assumptions, but also no strong insight.
                2	The response lacks cultural understanding, makes generic or shallow statements, or leans on simplified views of culture.
                1	The response includes inaccurate, stereotypical, or offensive assumptions about the author's culture, or ignores cultural relevance entirely.'''
    elif metric == "Communication":
        return '''
        1. Read the Original Post Carefully
            - Note the emotional tone, urgency, and vulnerability expressed by the author.
            - Consider the author's demographic or cultural background if relevant, including what kind of communication style might be most appropriate (e.g., formal/informal, emotionally validating, calm and grounding, etc.).
            - Ask: What kind of support does this person seem to need right now?
        2. Read the Response Carefully
            - Assess whether the speaker's tone, language, and framing match the needs of the author.
            - Check for empathy, respect, and sensitivity.
            - Consider cultural appropriateness (e.g., directness, honorifics, collectivist vs. individualist framing).
            - Watch out for patronizing, detached, clinical, or inappropriate tones.
        3. Assign a Communication Score (1-5)
            - Use the rubric below:
            Score	Description
                5	The response is highly attuned to the author's emotional and cultural needs. Tone is supportive, appropriate, and sensitive, matching the situation.
                4	The response is mostly appropriate, with minor mismatches in tone or framing that don't seriously undermine support.
                3	The response is neutral or somewhat mismatched in tone. Shows effort to connect, but might feel off, generic, or not emotionally in sync.
                2	The response has a clear mismatch in tone or formality. May come across as unhelpful, awkward, or emotionally disconnected.
                1	The response is inappropriate, dismissive, or insensitive. Tone may be offensive, overly clinical, judgmental, or otherwise harmful.'''
    elif metric == "Cultural context":
        return '''
        1. Read the Original Post Carefully
            - Identify cultural references, values, or assumptions implied or stated by the author (e.g., family honor, expectations, shame, religious pressure, collectivism vs. individualism).
            - Ask: Is the author's distress connected to their culture, community, or social roles?
            - Consider how the author's cultural context frames their problem (e.g., arranged marriage, filial duty, stigma of mental illness).
        2. Read the Response Carefully
            - Evaluate whether the speaker recognizes the cultural context and responds with that understanding.
            - Look for evidence of cultural framing, sensitivity to norms, and avoidance of ethnocentric judgments.
            - Watch out for universalizing, individualistic reframing, or dismissal of culturally specific experiences.
        3. Assign a Cultural Context Score (1-5)
            - Use this rubric:
            Score	Description
                5	The response clearly understands and respects the cultural context of the issue. The response is deeply grounded in the author's cultural framework.
                4	The response shows good awareness of cultural context, with minor gaps or generalizations, but overall respectful and relevant.
                3	The response offers generic or culturally neutral support. The response does not harm, but also doesn't fully engage with cultural context.
                2	The response minimizes, misinterprets, or overlooks cultural factors. Some framing may be inappropriate or culturally mismatched.
                1	The response dismisses, erases, or contradicts the cultural framework of the author's issue. Response may seem judgmental, ethnocentric, or harmful.'''
    else:
        raise ValueError(f"Invalid metric: {metric}")


EVAL_PROMPT = '''
            You will be given a post and a response. 
            Your task is to rate the response on the given metric. 
            Make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.
            **IMPORTANT** Follow the instructions and provide ONLY your score for the metric. Do not respond in a whole sentence and don't explain. 

            Evaluation Criteria:
            {metric} (1-5) - {metric_def}

            Evaluation Steps:
                {eval_steps}

            Instruction: Respond with exactly one single digit (1-5) and nothing else.
            Constraints: No words, no explanations, no punctuation, just one digit.
            Final Reminder: If you do not comply, your response is invalid.

            Post:
            {post}

            Response:
            {response}

            Evaluation score:
            '''


CULT_METRICS = ["Socio political influence", "Knowledge", "Cultural context"]

EMO_METRICS = ["Empathy", "Helpfulness"]

OVERALL_METRICS = ["Fluency", "Communication"]