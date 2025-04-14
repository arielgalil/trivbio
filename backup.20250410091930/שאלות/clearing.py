import re

def clean_text(input_file, output_file):
    # קריאת הקובץ
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_tag = None
    final_lines = []
    current_block = []

    # עיבוד השורות
    for line in lines:
        line = line.strip()

        # דילוג על שורות ריקות
        if not line:
            continue

        # בדיקה אם השורה היא תגית
        if line.startswith('#'):
            if current_block:  # סיום מקטע קודם אם קיים
                final_lines.extend(current_block)
                final_lines.append('')
                current_block = []
            current_tag = line
            continue

        # הסרת מיספור
        cleaned_line = re.sub(r'^\d+\.?\s*', '', line).strip()

        # אם אין תגית עדיין, זו השאלה הראשונה במקטע
        if not current_block:
            current_block.append(current_tag)
            current_block.append(cleaned_line)
        else:
            current_block.append(cleaned_line)

    # הוספת המקטע האחרון
    if current_block:
        final_lines.extend(current_block)

    # ניקוי רווחים מיותרים
    cleaned_lines = []
    for line in final_lines:
        if line:  # בדיקה שהשורה אינה None או ריקה
            cleaned_line = re.sub(r'\s+', ' ', line).strip()
            cleaned_lines.append(cleaned_line)

    # כתיבה לקובץ חדש
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_lines))

# שימוש בפונקציה
input_file = 'input.txt'  # שם הקובץ המקורי
output_file = 'output.txt'  # שם הקובץ המעובד
clean_text(input_file, output_file)
print("הקובץ עובד בהצלחה ונשמר כ-'output.txt'")