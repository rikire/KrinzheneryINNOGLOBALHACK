"""
Алгоритм получения компетенций
1) Получить названия всех уникальных файлов через 'git log --shortstat --pretty=format: --name-only'
2) Сгруппировать их по расширению или названию файла, если расширение отсутствует
3) Из каждой группы получить по одному файлу (оптимизация, т.к. анализ одного файла занимает много времени)
4) Получить изменения по по каждому файлу через 'git log -p --author="author_name" --pretty=format: -- path/to/file'
5) Сформировать запрос для Llama для получения компетенций
6) Сформировать запрос для Llama из компетенция для получения резюме

"""

import os
from collections import defaultdict
import os
import subprocess
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional

class ScoreWithCategory(BaseModel):
    name: str = Field(..., description="Название компетенции")
    score: int = Field(..., ge=1, le=10, description="Оценка (1-10)")
    category: Literal["frontend", "backend", "data_science", "devops", "qa", "gamedev", "mobile", "embedded", "other"] = Field(..., description="Категория компетенции")


class Score(BaseModel):
    name: str = Field(..., description="Название компетенции")
    score: int = Field(..., description="Оценка (1-10)")


class UserCompetencyProfile(BaseModel):
    competencies: Dict[str, List[Score]] = Field(..., description="Категории и соответствующие компетенции с оценками")
    resume: Optional[str] = Field(None, description="Описание компетенций пользователя")

    class Config:
        json_schema_extra = {
            "example": {
                "competencies": {
                    "frontend": [{"name": "SVG", "score": 8}],
                    "backend": [{"name": "go", "score": 9}, {"name": "ruby", "score": 6}],
                    "devops": [{"name": "Docker", "score": 8}],
                    "other": [{"name": "bash", "score": 8}]
                },
                "resume": "Эксперт в контейнеризации и виртуализации."
            }
        }



def get_all_unique_filenames(author_name: str, repo_path: str) -> List[str]:
    """
    Получение списка уникальных файлов, которые изменял разработчик

    Parameters
    ----------
    author_name : str
        Имя автора или email разработчика в git 
    repo_path : str
        путь до 

    Returns
    -------
    List[str]
        Список уникальных путей файлов
        
    """    
    try:
        # Перемещаемся в директорию с репозиторием
        current_directory = os.getcwd()
        os.chdir(repo_path)
    except FileNotFoundError:
        print(f"Error: The directory {repo_path} does not exist.")
        return []

    # Выполнение команды git log для получения списка файлов
    git_log_command = [
        "git",
        "log",
        "--name-only",
        "--author=" + author_name,
        "--pretty=format:",
    ]
    result = subprocess.run(git_log_command, stdout=subprocess.PIPE, text=True)

    # Перемещаемся в исходную директорию
    os.chdir(current_directory)
    # Разделение вывода на строки, удаление пустых строк и повторений
    files = result.stdout.splitlines()
    unique_files = set(filename.strip() for filename in files if filename.strip())

    return list(unique_files)


def group_by_extensions(unique_filenames: List[str]) -> Dict[str, List[str]]:
    groups = defaultdict(list)
    for filename in unique_filenames:
        extension = os.path.splitext(filename)[1] # получаем расширение
        if extension:
            groups[extension].append(filename)
        else:
            basename = os.path.basename(filename) # файлы без расширения формируются как отдельная группа
            groups[basename].append(filename)
    return groups


def get_git_log_changes(author_name, file_path):
    # Выполнение команды git log для получения изменений по указанному файлу
    current_directory = os.getcwd()
    os.chdir(file_path.split("/")[0])
    file_path = "/".join(file_path.split("/")[1:])
    command = [
        "git",
        "log",
        "-p",
        f"--author={author_name}",
        '--pretty=format:""',
        "--",
        file_path,
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    except Exception as e:
        print(e)
        return ""
    
    os.chdir(current_directory)
    # Получаем вывод и разбиваем его на строки
    changes = result.stdout.splitlines()
    
    # Фильтруем ненужные строки
    filtered_changes = [
        line
        for line in changes
        if not (
            line.startswith("diff --git")
            or line.startswith("index")
            or line.startswith("---")
            or line.startswith("+++")
            or line.startswith("@@")
        )
    ]
    return "\n".join(filtered_changes)


def checkout_technologies_with_llama(prompt):
    url = "https://vk-devinsight-case.olymp.innopolis.university/generate"
    # url = "https://vk-devinsight-case-backup.olymp.innopolis.university/generate" # backup
    score_with_category_schema = {"type": "array", "items": ScoreWithCategory.model_json_schema()}

    data = {
        "prompt": [prompt],
        "stream": False,
        "max_tokens": 200,
        "temperature": 0.5,
        "seed": 42,
        "frequency_penalty": 0.1,
        "schema": score_with_category_schema,
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

def ask_llama_for_hardskills_resume(prompt):

    url = "https://vk-devinsight-case.olymp.innopolis.university/generate"
    # url = "https://vk-devinsight-case-backup.olymp.innopolis.university/generate" # backup
    data = {
        "prompt": [prompt],
        "stream": False,
        "max_tokens": 200,
        "temperature": 0.2,
        "seed": 42,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

    
def get_hardskills_from_llama(repo_path: str, author_name: str) -> UserCompetencyProfile:
    # Получаем уникальные имена файлов
    unique_filenames = get_all_unique_filenames(author_name, repo_path)
    if len(unique_filenames) == 0:
        return {}

    # Получаем уникальные расширения и сгруппированные по расширениям файлы
    groups = group_by_extensions(unique_filenames)

    # Формируем словарь для группировки компетенций для анализа
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

    len_groups = len(groups)
    for i, (_, filenames) in enumerate(groups.items()):
        # Формируем запрос для извлечения компетенций
        prompt = "Извлеки из текста изменений коммита используемые технологии, библиотеки, языки и инструменты для разработки программного обеспечения. Определи уровень владения каждой технологией на основе внесенных изменений (от 1 до 10, где 1 - худшая оценка, 10 - лучшая). Отнеси их к соответствующим областям деятельности, таким как frontend, backend, data_science, devops, qa, embedded, gamedev, mobile и other"
        changes = get_git_log_changes(author_name, f"{repo_path}/{filenames[0]}") # Получаем только первый файл для уменьшения времени анализа
        if not changes:
            continue
        prompt += changes
        
        # Отправляем запрос для Llama
        response = checkout_technologies_with_llama(prompt)
        
        try:
            # Декодируем ответ
            response = json.loads(response)
            if not response:
                continue
            
            # Распределение технологий по группам competencies
            for technology in response:
                category = technology["category"]
                name = technology["name"]
                score = technology["score"]
                
                # Удаление дублирования
                if name.lower() not in [competence['name'].lower() for competence in competencies[category]]: 
                    competencies[category].append({"name": name, "score": score})
        except:
            pass

    # Формрование запроса для создания резюме
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
    return response