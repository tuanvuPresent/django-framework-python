from apps.e_learning.exams.models import Configuration


def update_exams(questions, exams):
    for exam in exams:
        questions_in_exam = exam.question_id.all()
        q = set(questions_in_exam).difference(questions)
        exam.question_id.set(q)
        exam.exam_config_id.quantity_question = questions_in_exam.count() - questions.count()
        exam.exam_config_id.save()
        exam.save()


def update_exam_config(questions, exams):
    for exam in exams:
        configs = Configuration.objects.filter(is_active=True, exam_config_id=exam.pk)
        for question_item in questions:
            configuration = configs.filter(category_id=question_item.category_id, level=question_item.level).first()
            if configuration is not None:
                configuration.number -= 1
                configuration.save()
