export interface CommandRequest {
    cred: AccountRegister;
    command: Command;
}

export interface AccountInfo {
    login: string; // Логин аккаунта
    command_list: Command[]; // Список команд
    favorites: string[]; // Любимые разработчики
};

export interface AccountRegister {
    login: string; // Логин аккаунта
    password: string; // Пароль аккаунта
};

export interface BodyPostCommandCommandPost {
    cred: AccountRegister;
    command: Command;
};

export interface BodyPostCommandDelCommandDeletePost {
    cred: AccountRegister;
    command: Command;
};

export interface Command {
    command_name: string; // Название команды
    participants: string[]; // Участники команды
};

export interface HTTPValidationError {
    detail?: ValidationError[];
};

export interface SearchResult {
    developers: UserInfo[]; // Массив информации о пользователях
};

export interface Summary {
    summary: string; // Описание разработчика
};

export interface UserGlobalStat {
    username: string; // Имя пользователя на GitHub
    public_repos: number; // Количество публичных репозиториев
    contributed_repos: number; // Количество репозиториев, к которым пользователь внес вклад
    commits_total: number; // Общее количество коммитов
    commits_per_day: number; // Среднее количество коммитов в день
    commits_per_week: number; // Среднее количество коммитов в неделю
    commits_per_year: number; // Среднее количество коммитов в год
    average_commit_size: number; // Средний размер коммита
    languages: Array<Record<string, number>>; // Используемые языки программирования и количество строк кода
    competencies: string[]; // Компетенции разработчика (направления разработки)
    using_github_features: string[]; // Используемые функции GitHub, такие как 'issues' или 'actions'
    stack: string[]; // Технологический стек, используемый в проекте
    score: Array<Record<string, number>>; // Оценки по стеку технологий (от 0 до 10)
    prep_repos: string[]; // Список репозиториев по которым имеется статистика
};

export interface UserInfo {
    username: string; // Имя пользователя на GitHub
    name?: string | null; // Полное имя пользователя
    email?: string | null; // Электронная почта пользователя
    team_projects?: number | null; // Количество проектов в команде
    solo_projects?: number | null; // Количество личных проектов
    solo_gist?: number | null; // Количество публичных гистов
    account_age?: number | null; // Возраст аккаунта
    avatar_url?: string | null; // Ссылка на аватар пользователя
    html_url?: string | null; // Ссылка на профиль пользователя
    followers?: number | null; // Количество подписчиков
    following?: number | null; // Количество отслеживаемых пользователей
    repos: string[]; // Названия всех репозиториев, в которые пользователь контрибьютил
};

export interface UserRepoStat {
    username: string; // Имя пользователя на GitHub
    repo_name: string; // Название репозитория
    repo_html_url: string; // URL-адрес репозитория
    languages: Array<Record<string, number>>; // Используемые языки программирования и количество строк кода
    competencies: string[]; // Компетенции разработчика (направления разработки)
    using_github_features: string[]; // Используемые функции GitHub, такие как 'issues' или 'actions'
    stack: string[]; // Технологический стек, используемый в проекте
    score: Array<Record<string, number>>; // Оценки по стеку технологий (от 0 до 10)
    commits_total: number; // Общее количество коммитов в репозитории
    commits_per_day: number; // Среднее количество коммитов в день
    commits_per_week: number; // Среднее количество коммитов в неделю
    commits_per_year: number; // Среднее количество коммитов в год
    average_commit_size: number; // Средний размер коммита
};

export interface ValidationError {
    loc: (string | number)[]; // Location of the error
    msg: string; // Message
    type: string; // Error Type
};
