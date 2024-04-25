

def chunk_text(text_list, max_length=2048):
    chunks = []
    current_chunk = ""
    words_line = []  # Инициализируем список для хранения слов текущей строки
    for line in text_list:
        if len(line) <= max_length:  # Проверяем, что длина строки не превышает максимальный лимит
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + "\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
        else:
            words = line.split()
            for word in words:
                if len(" ".join(words_line + [word])) <= max_length:  # Проверяем, что добавление слова не превышает максимальный лимит
                    words_line.append(word)
                else:
                    chunk_part = " ".join(words_line)  # Сохраняем текущую часть
                    chunks.append(chunk_part.strip())  # Добавляем текущую часть в список
                    words_line = [word]  # Начинаем новую часть с текущего слова
    if words_line:  # Проверяем, остались ли слова в последней части
        chunk_part = " ".join(words_line)  # Сохраняем последнюю часть
        chunks.append(chunk_part.strip())  # Добавляем последнюю часть в список
    return chunks

