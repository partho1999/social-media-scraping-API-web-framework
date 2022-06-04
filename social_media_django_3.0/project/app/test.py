def normalize_value(negative, neutral, positive):
    positive = 0.9 - negative
    negative = 0.9 - positive
    neutral = 1 - (negative + positive)
    return (negative, neutral, positive)
