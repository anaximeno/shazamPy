import os

def set_file(file):
    def analyze_file(x):
        def ext(y):
            file_name, file_extension = os.path.splitext(y)
            return file_extension
        if ext(x) == ".txt":
            needTo = True
        else:
            needTo = False
        return needTo
    if analyze_file(file) is True:
        with open(file, "rt") as m:
            while True:
                sum_text = m.read()
                if not sum_text:
                    break
                return sum_text
    else:
        return file
