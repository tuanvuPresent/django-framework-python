from apps.e_learning.models.question import Question


def get_score(correct_answer, your_answers):
    score = 0
    detail = []
    for count, answer in enumerate(your_answers):
        question_id = answer.get('question_id')
        key = answer.get('key')
        result = {
            'question': question_id,
            'key': correct_answer.get(question_id),
            'is_correct': False,
            'your_answer': key
        }
        if correct_answer.get(question_id) is None:
            continue
        if correct_answer.get(question_id) == key:
            score = score + 1
            result['is_correct'] = True
        detail.append(result)

    return score, detail


def get_question(exams):
    if exams.exam_config_id.show_random_question is False:
        return exams.question_id
    config_data = exams.exam_config_id.config.all()
    question = []
    for config_item in config_data:
        number = config_item.number
        category_id = config_item.category_id
        level = config_item.level
        queryset = Question.objects.filter(category_id=category_id,
                                           level=level
                                           ).order_by('?').prefetch_related('answers')[0:number]
        question.extend(queryset)
    exams.question_id.set(question)
    return question
