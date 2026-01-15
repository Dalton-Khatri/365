scores = [45, 78, 92, 34, 67, 88]
names= ["john doe", "JANE SMITH", "bOb WiLsOn"]

def process_student_scores(scores):
    return [score +5 for score in scores if score >=50]

def format_names(names):
    return [str.title() for str in names]

print(f"The Processes scores are {process_student_scores(scores)}\n")
print(f"Formatted Names: {format_names(names)}")



