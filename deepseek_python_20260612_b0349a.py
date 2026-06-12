def grade(attempt_id, user_responses):
    attempt = get_attempt(attempt_id)
    if attempt.status != 'in_progress':
        raise Exception("Invalid state")
    if datetime.utcnow() > attempt.start_time + timedelta(minutes=60):
        attempt.status = 'timeout'  # still grade
    
    shuffles = get_shuffles(attempt_id)
    total = len(shuffles)
    correct = 0
    review = []
    
    labels = ['ক','খ','গ','ঘ']
    for sh in shuffles:
        q = sh.question
        # Find response
        resp = next((r for r in user_responses if r['question_id'] == q.id), None)
        selected_label = resp['selected_label'] if resp else None
        
        # Determine correct option
        correct_index = labels.index(sh.correct_label)
        correct_option_id = sh.shuffled_option_ids[correct_index]
        
        # Determine selected option
        selected_option_id = None
        if selected_label and selected_label in labels:
            idx = labels.index(selected_label)
            selected_option_id = sh.shuffled_option_ids[idx]
        
        is_correct = (selected_option_id == correct_option_id)
        if is_correct:
            correct += 1
        
        # Store response
        save_response(attempt_id, q.id, selected_option_id, is_correct)
        
        # Build review item
        review.append({
            "question_text": q.question_text,
            "options": [
                {"label": lbl, "text": get_option_text(oid)}
                for lbl, oid in zip(labels, sh.shuffled_option_ids)
            ],
            "selected_label": selected_label,
            "correct_label": sh.correct_label,
            "is_correct": is_correct
        })
    
    percentage = (correct / total) * 100
    update_attempt(attempt_id, score=correct, percentage=percentage,
                   status='completed', end_time=datetime.utcnow())
    return {"total": total, "correct": correct, "wrong": total-correct,
            "percentage": percentage, "review": review}