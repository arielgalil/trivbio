import json
import re

def parse_text_to_json(file_path):
    # מבנה נתונים התחלתי
    data = {
        "players": {},
        "questions": {
            "cell": [],
            "human-body": [],
            "ecology": []
        }
    }
    
    current_topic = None
    question_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        for line in lines:
            line = line.strip()  # הסרת רווחים ותווי שורה מיותרים
            
            # דילוג על שורות ריקות
            if not line:
                continue
            
            # זיהוי תגית נושא חדש (עם או בלי רווחים לפני/אחרי ה-#)
            if line.startswith('#'):
                # אם יש שאלה שנאספה לפני כן, נעבד אותה
                if question_lines:
                    process_question(question_lines, data, current_topic)
                    question_lines = []
                
                # הסרת ה-# ורווחים משני הצדדים
                current_topic = line.replace('#', '').strip()
                continue
                
            # איסוף שורות של שאלות אם יש נושא נוכחי
            if current_topic:
                question_lines.append(line)
                
                # בדיקה אם יש מספר בסוגריים מרובעים - סימן לתשובה נכונה
                if re.search(r'\[\d\]', line):
                    process_question(question_lines, data, current_topic)
                    question_lines = []
                    
        # עיבוד השאלה האחרונה אם קיימת
        if question_lines:
            process_question(question_lines, data, current_topic)
    
    return data

def process_question(lines, data, topic):
    # חילוץ השאלה (השורה הראשונה)
    question = lines[0]
    
    # חילוץ התשובות (4 השורות הבאות)
    answers = lines[1:5]
    
    # חילוץ המספר בסוגריים מהשורה האחרונה לקביעת התשובה הנכונה
    correct_match = re.search(r'\[\d\]', lines[-1])
    correct = int(correct_match.group(0)[1]) - 1 if correct_match else 0  # המרה ל-0-3
    
    # יצירת מבנה השאלה
    question_obj = {
        "question": question,
        "answers": answers,
        "correct": correct
    }
    
    # הוספת השאלה לנושא המתאים
    if topic in data["questions"]:
        data["questions"][topic].append(question_obj)
    else:
        print(f"Warning: Topic '{topic}' not found in predefined topics.")

def main():
    # נתיב הקובץ - יש להתאים לפי מיקום הקובץ שלך
    file_path = "questions.txt"
    
    # המרת הקובץ ל-JSON
    result = parse_text_to_json(file_path)
    
    # שמירת התוצאה לקובץ JSON
    with open("questions.json", 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
    
    print("הקובץ הומר בהצלחה ל-JSON ונשמר כ-'questions.json'")
    
    # הדפסת מספר השאלות בכל נושא לבדיקה
    for topic, questions in result["questions"].items():
        print(f"Topic '{topic}' contains {len(questions)} questions")

if __name__ == "__main__":
    main()