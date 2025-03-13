import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import json
import string
import logging
import pymorphy3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация лемматизатора
morph = pymorphy3.MorphAnalyzer()

def lemmatize_and_clean_text(text):
    """Лемматизация и очистка текста от пунктуации, предлогов и союзов."""
    tokens = text.split()
    tokens = [word.lower().strip(string.punctuation) for word in tokens]
    lemmatized_tokens = [
        morph.parse(token)[0].normal_form
        for token in tokens
        if token and morph.parse(token)[0].tag.POS not in {'PREP', 'CONJ'}  # Исключаем предлоги и союзы
    ]
    return lemmatized_tokens


questions = []
current_question_index = 0
student_answers = []

def load_questions():
    """Функция для загрузки файла с вопросами."""
    global questions, current_question_index, student_answers
    file_path = filedialog.askopenfilename(
        title="Открыть файл с вопросами",
        filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)

        if not isinstance(questions, list) or not all("question" in q and "answer" in q for q in questions):
            raise ValueError("Неверный формат файла. Ожидается список с объектами 'question' и 'answer'.")

        current_question_index = 0
        student_answers = [{} for _ in range(len(questions))]
        display_question()

    except Exception as e:
        logging.error(f"Не удалось загрузить файл: {e}")
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

def display_question():
    """Отображает текущий вопрос на экране."""
    global current_question_index, questions
    if current_question_index < len(questions):
        question_label.config(text=f"Вопрос {current_question_index + 1}: {questions[current_question_index]['question']}")
        student_answer_entry.delete("1.0", tk.END)

        if student_answers[current_question_index].get("student_answer"):
            student_answer_entry.insert("1.0", student_answers[current_question_index]["student_answer"])
    else:
        messagebox.showinfo("Завершено", "Все вопросы пройдены. Отображение результатов.")
        display_results()

def save_current_answer():
    """Сохраняет текущий ответ студента."""
    global current_question_index, student_answers

    if 0 <= current_question_index < len(student_answers):
        student_answer = student_answer_entry.get("1.0", tk.END).strip()
        student_answers[current_question_index]["student_answer"] = student_answer
    else:
        logging.error(f"Недопустимый индекс вопроса: {current_question_index}")

def check_answer(index):
    """Проверяет ответ студента для указанного вопроса."""
    global questions, student_answers

    question = questions[index]["question"]
    correct_answer = questions[index]["answer"]
    student_answer = student_answers[index].get("student_answer", "").strip()

    if not student_answer:
        return None

    try:
        # Лемматизация ключевых слов из правильного ответа
        correct_answer_tokens = set(lemmatize_and_clean_text(correct_answer))
        student_answer_tokens = set(lemmatize_and_clean_text(student_answer))

        # Подсчет совпадающих ключевых слов
        matched_keywords = len(correct_answer_tokens & student_answer_tokens)
        keyword_score = round((matched_keywords / len(correct_answer_tokens)) * 10, 1) if correct_answer_tokens else 0

        # GPT-оценка
        prompt = (
            f"Вопрос: {question}\n"
            f"Правильный ответ: {correct_answer}\n"
            f"Ответ студента: {student_answer}\n"
            "Оцени ответ студента по 10-ти бальной системе, где 0 - абсолютно неверно, 10 - идеальный ответ. Напечатай только число."
        )

        url = "https://api.proxyapi.ru/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer sk-V5Nsf1jfsU2JMuUNtACHMJ3LRsl9b5Pt",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "Ты являешься ассистентом преподавателя, который проверяет ответы студентов."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        gpt_feedback = float(result["choices"][0]["message"]["content"].strip())

        # Комбинированная оценка
        combined_score = round((gpt_feedback + keyword_score) / 2, 1)

        student_answers[index].update({
            "question": question,
            "correct_answer": correct_answer,
            "student_answer": student_answer,
            "gpt_score": gpt_feedback,
            "keyword_score": keyword_score,
            "combined_score": combined_score
        })

    except requests.RequestException as e:
        logging.error(f"Ошибка соединения с API: {e}")
        messagebox.showerror("Ошибка", f"Ошибка соединения с API: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка при проверке ответа: {e}")
        messagebox.showerror("Ошибка", f"Произошла ошибка при проверке ответа: {e}")

def check_all_answers():
    """Проверяет ответы для всех вопросов."""
    for i in range(len(questions)):
        check_answer(i)
    display_results()

def next_question():
    """Переход к следующему вопросу."""
    global current_question_index
    save_current_answer()
    if current_question_index < len(questions) - 1:
        current_question_index += 1
        display_question()
    else:
        messagebox.showinfo("Конец", "Вы достигли конца вопросов.")

def previous_question():
    """Переход к предыдущему вопросу."""
    global current_question_index
    save_current_answer()
    if current_question_index > 0:
        current_question_index -= 1
        display_question()

def display_results():
    """Отображает результаты всех ответов."""
    results_text.delete("1.0", tk.END)
    for i, ans in enumerate(student_answers, start=1):
        if "question" in ans:
            results_text.insert(tk.END, f"Вопрос {i}: {ans['question']}\n")
            results_text.insert(tk.END, f"Правильный ответ: {ans['correct_answer']}\n")
            results_text.insert(tk.END, f"Ответ студента: {ans['student_answer']}\n")
            results_text.insert(tk.END, f"Оценка GPT: {ans['gpt_score']}\n")
            results_text.insert(tk.END, f"Оценка по ключевым словам: {ans['keyword_score']}\n")
            # results_text.insert(tk.END, f"Комбинированная оценка: {ans['combined_score']}\n\n")

root = tk.Tk()
root.title("Проверка ответов студентов")

question_label = tk.Label(root, text="Загрузите файл с вопросами.", wraplength=500, justify="left")
question_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)

tk.Label(root, text="Ответ студента:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
student_answer_entry = tk.Text(root, height=5, width=60)
student_answer_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

load_button = tk.Button(root, text="Загрузить файл", command=load_questions)
load_button.grid(row=2, column=0, sticky="e", padx=10, pady=10)

prev_button = tk.Button(root, text="Назад", command=previous_question)
prev_button.grid(row=2, column=1, sticky="e", padx=10, pady=10)

next_button = tk.Button(root, text="Далее", command=next_question)
next_button.grid(row=2, column=2, sticky="w", padx=10, pady=10)

check_all_button = tk.Button(root, text="Проверить все ответы", command=check_all_answers)
check_all_button.grid(row=3, column=1, sticky="w", padx=10, pady=10)

results_label = tk.Label(root, text="Результаты:")
results_label.grid(row=4, column=0, sticky="nw", padx=10, pady=5)
results_text = tk.Text(root, height=20, width=80, state="normal")
results_text.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

root.mainloop()