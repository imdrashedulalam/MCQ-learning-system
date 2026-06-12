import random, secrets
from models import Question, Option, AttemptShuffle

def create_shuffles(attempt_id, bank_id):
    questions = list(Question.select().where(Question.bank_id == bank_id))
    rng = secrets.SystemRandom()
    rng.shuffle(questions)
    
    for display_order, q in enumerate(questions):
        opts = list(Option.select().where(Option.question_id == q.id))
        rng.shuffle(opts)
        labels = ['ক','খ','গ','ঘ']
        shuffled_ids = []
        correct_label = None
        for i, opt in enumerate(opts):
            shuffled_ids.append(opt.id)
            if opt.is_correct:
                correct_label = labels[i]
        AttemptShuffle.create(
            attempt_id=attempt_id,
            question_id=q.id,
            display_order=display_order,
            shuffled_option_ids=shuffled_ids,
            correct_label=correct_label
        )