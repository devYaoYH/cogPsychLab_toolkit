#################################
# COSINE From Euclidean L1-Norm #
#################################
def eu_to_cosine(eu):
    return 1-(eu**2)/2

#############################
# Wrap to-lower as function #
#############################
def sanitize_lower(raw):
    return raw.lower()