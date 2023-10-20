
def get_first_error(errors):
    for key, value in errors.items():
        return f"{key}:{value[0]}"