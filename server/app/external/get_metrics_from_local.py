import os
from collections import defaultdict
import os
import random
import subprocess
import git
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional
from app.schemas.schema import UserCompetencyProfile, Score
class ScoreWithCategory(BaseModel):
    name: str = Field(..., description="Название компетенции")
    score: int = Field(..., ge=1, le=10, description="Оценка (1-10)")
    category: Literal["frontend", "backend", "data_science", "devops", "qa", "gamedev", "mobile", "embedded", "other"] = Field(..., description="Категория компетенции")

   
# Список разрешённых расширений файлов по категориям
ALLOWED_EXTENSIONS = {
    "frontend": [
        ".html",
        ".css",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".scss",
        ".sass",
        ".json",
        ".vue",
    ],
    "backend": [
        ".py",
        ".java",
        ".js",
        ".rb",
        ".php",
        ".go",
        ".c",
        ".cpp",
        ".cs",
        ".sql",
    ],
    "data_science": [".ipynb", ".py", ".r", ".csv", ".json", ".xlsx", ".sql", ".txt"],
    "devops": [".yml", ".yaml", ".json", ".sh", ".dockerfile", ".tf", ".ps1"],
    "qa": [".py", ".java", ".rb", ".js", ".feature", ".xml", ".json", ".yaml"],
    "embedded": [".c", ".cpp", ".h", ".ino", ".asm", ".vhdl", ".verilog"],
    "gamedev": [".cs", ".unity", ".gd", ".hlsl", ".glsl", ".json", ".fbx", ".obj"],
    "mobile": [".java", ".kt", ".swift", ".xml", ".json", ".dart", ".js"],
    "other": [".txt", ".md", ".pdf", ".docx", ".pptx"],
}

# Собираем все разрешенные расширения в один набор
ALLOWED_EXTENSIONS_SET = {
    ext for extensions in ALLOWED_EXTENSIONS.values() for ext in extensions
}
def ask_llama_for_hardskills_resume(prompt):
    url = "https://vk-devinsight-case.olymp.innopolis.university/generate"
    # url = "https://vk-devinsight-case-backup.olymp.innopolis.university/generate" # backup
    data = {
        "prompt": [prompt],
        "stream": False,
        "max_tokens": 200,
        "temperature": 0.5,
        "seed": 42,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"


def checkout_technologies_with_llama(prompt):
    url = "https://vk-devinsight-case.olymp.innopolis.university/generate"
    # url = "https://vk-devinsight-case-backup.olymp.innopolis.university/generate" # backup
    score_with_category_schema = {
        "type": "array",
        "items": ScoreWithCategory.model_json_schema(),
    }

    data = {
        "prompt": [prompt],
        "stream": False,
        "max_tokens": 300,
        "temperature": 0.5,
        "seed": 42,
        # "frequency_penalty": 0.2,
        "schema": score_with_category_schema,
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
def get_final_code_lines(commit, file_path):
    """Получает строки кода, которые есть в финальной версии файла и написаны разработчиком."""
    try:
        # Получаем финальное содержимое файла в последнем коммите
        final_content = commit.tree[file_path].data_stream.read()

        # Проверяем, является ли файл текстовым
        if final_content.startswith(b"\x89PNG"):
            # Это может быть изображение PNG, возвращаем пустой набор
            return set()

        final_lines = set(final_content.decode("utf-8", errors="ignore").splitlines())
    except KeyError:
        # Если файл не найден в текущем коммите, возвращаем пустой набор
        return set()
    except UnicodeDecodeError:
        # Если возникла ошибка декодирования, возвращаем пустой набор
        return set()

    return final_lines  # Возвращаем все строки

def commit_file_generator(repo_path, author_name):
    """Генератор, который возвращает коммиты и связанную с ними информацию."""
    # Открываем репозиторий
    repo = git.Repo(repo_path)

    # Получаем коммиты от заданного автора
    commits = list(repo.iter_commits(author=author_name))
    for commit in commits:

        # Список файлов, затронутых в коммите
        changed_files = []
        for file_path in commit.stats.files:
            # Проверяем расширение файла
            if os.path.splitext(file_path)[1] not in ALLOWED_EXTENSIONS_SET:
                continue  # Пропускаем файлы с неподдерживаемыми расширениями

            # Получаем финальные строки кода, написанные разработчиком
            final_code_lines = get_final_code_lines(commit, file_path)
            changed_files.append(
                {"file_path": file_path, "final_code_lines": final_code_lines}
            )

        if changed_files:  # Проверяем, были ли изменения в разрешенных файлах
            # Возвращаем информацию о коммите и измененных файлах
            yield changed_files

    return None

def get_hardskills_from_llama(repo_path: str, user_names: list[str]) -> UserCompetencyProfile:
    username, name, email = user_names
    author_name = username
    generator = commit_file_generator(repo_path, author_name)
    k = 0
    # Получаем и выводим информацию о коммитах и измененных файлах
    prompt = "Извлеки из текста изменений коммита ниже используемые технологии, библиотеки, языки и инструменты. Определи уровень владения каждой технологией на основе внесенных изменений (от 1 до 10, где 1-3 junior, 4-7 middle, 8-10 senior). Отнеси их к соответствующим областям деятельности, таким как frontend, backend, data_science, devops, qa, embedded, gamedev, mobile и other\n"
    for commit_info in generator:
        k += 1
        if k > 3:
            break
        changes = str(commit_info[random.randint(0, len(commit_info) - 1)])
        changes = changes[:5000]
        prompt += changes

    data = checkout_technologies_with_llama(prompt)
    data = json.loads(data)
    competencies = {
        "frontend": [],
        "backend": [],
        "data_science": [],
        "devops": [],
        "qa": [],
        "embedded": [],
        "gamedev": [],
        "mobile": [],
        "other": [],
    }
    for values in data:
        name = values["name"]
        score = values["score"]
        category = values["category"]
        competencies[category].append({"name": name, "score": score})

    resume_prompt = "В 2-3 предложениях сделай общее резюме разработчика по его компетенциям, дающее представление о его квалификации, укажи сильные и слабые стороны, не указывай числа.\n"
    for category, technologies in competencies.items():
        if len(technologies) == 0:
            continue
        
        for technology in technologies:
            resume_prompt += f"{technology['name']}: {technology['score']}\n"
            
    # Отправляем запрос для Llama
    resume = ask_llama_for_hardskills_resume(resume_prompt)
    response = {
        "competencies": competencies,
        "resume": resume,
    }
    return UserCompetencyProfile(**response)

