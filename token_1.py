import spacy

def suggest_correction(token, candidates, threshold=0.5):
    nlp = spacy.load("en_core_web_md")
    token_doc = nlp(token)

    # Check if token is recognized by the model
    if not token_doc.has_vector:
        return token

    best_match = None
    best_similarity = 0.0

    # Iterate over each candidate correction
    for candidate in candidates:
        candidate_doc = nlp(candidate)

        # Check if candidate token is recognized by the model
        if not candidate_doc.has_vector:
            continue

        similarity = token_doc.similarity(candidate_doc)

        # Update the best match if the current candidate has a higher similarity
        if similarity > best_similarity:
            best_match = candidate
            best_similarity = similarity

    # Check if the similarity meets the threshold for a valid suggestion
    if best_similarity >= threshold:
        return best_match
    else:
        return token  # Return the original token if no suitable correction found


def correct_text(input_text, candidates, threshold=0.5):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(input_text)

    corrected_text = []
    for token in doc:
        corrected_token = suggest_correction(token.text, candidates, threshold)
        corrected_text.append(corrected_token)

    return " ".join(corrected_text)


# Example usage
input_text = input("Enter the text: ")
candidates = ["This", "is", "an", "example", "of", "a", "misspelled", "text"]
threshold = 0.7

corrected = correct_text(input_text, candidates, threshold)
print("Corrected text:", corrected)
