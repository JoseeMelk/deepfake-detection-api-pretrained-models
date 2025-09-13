from app.models.response import DecisionResult
def majority_vote(results):
        # 🔹 Votación mayoritaria
    fake_votes = sum(1 for r in results if r.prediction == "fake")
    real_votes = sum(1 for r in results if r.prediction == "real")
    total_votes = len(results)

    if fake_votes > real_votes:
        majority_prediction = "fake"
        majority_confidence = fake_votes / total_votes
    else:
        majority_prediction = "real"
        majority_confidence = real_votes / total_votes

    return DecisionResult(
        prediction=majority_prediction,
        confidence=round(majority_confidence, 6)
    )

def average_probabilities(results):
        # 🔹 Promedio de probabilidades
    avg_real = sum(r.real for r in results) / len(results)
    avg_fake = sum(r.fake for r in results) / len(results)
    if avg_fake > avg_real:
        average_prediction = "fake"
        average_confidence = avg_fake
    else:
        average_prediction = "real"
        average_confidence = avg_real
        
    return DecisionResult(
            prediction=average_prediction,
            confidence=round(average_confidence, 6)
        )