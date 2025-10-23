import time

def save_text(outputmoji: str) -> str:

    filename = time.strftime("%Y%m%d_%H%M%S") + "_transcript.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(outputmoji + "\n")
   
    return filename

