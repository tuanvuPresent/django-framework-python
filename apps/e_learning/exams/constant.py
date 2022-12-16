from apps.common.enum import EnumMeta


class AnswersType(EnumMeta):
    ANSWER_A = (0, 'A')
    ANSWER_B = (0, 'B')
    ANSWER_C = (0, 'C')
    ANSWER_D = (0, 'D')


class LevelQuestion(EnumMeta):
    KNOW = (0, 'Know')
    UNDERSTANDING = (1, 'Understanding')
    MANIPULATE = (2, 'Manipulate')
    HIGH_MANIPULATE = (3, 'High Manipulate')
