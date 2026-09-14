#!/usr/bin/env python3
"""Generate the dependency-free GitHub Pages site from reviewed course data."""
from pathlib import Path
from html import escape as e
from urllib.parse import urlparse
import json
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'site.json').read_text())
for key in ['bot_url','chat_url','grades_url','organization_url','archive_folder_url']:
    value=cfg.get(key)
    if value and (urlparse(value).scheme!='https' or not urlparse(value).netloc):
        raise ValueError(f'{key} must be an absolute HTTPS URL')
archive=json.loads((ROOT/'archive.json').read_text())
archive.sort(key=lambda x:int(x['title'].split('.')[0].split()[-1]))
archive_links=''.join(f'<li><a href="{e(x["url"],quote=True)}">{e(x["title"])}</a></li>' for x in archive)
bot_link=(f'<a class="button" href="{e(cfg["bot_url"],quote=True)}">Открыть TAIGA в Telegram</a>' if cfg.get('bot_url') else '<p class="note">Ссылка на бота будет добавлена. Ниже — инструкция по регистрации и получению онлайн-домашнего задания.</p>')
chat_link=(f'<a href="{e(cfg["chat_url"],quote=True)}">Чат курса</a>' if cfg.get('chat_url') else '')
legacy=[('hw1-stat-basics','Основы статистики'),('hw2-eda-dim-reduction','EDA и уменьшение размерности'),('hw3-knn-metrics','kNN и метрики качества'),('hw4-lin-reg','Линейная регрессия'),('hw5-svm','SVM'),('hw7-bayes-clustering','Байесовские методы и кластеризация'),('hw8-deep-learning','Глубокое обучение'),('hw9-cnn-rnn','CNN и RNN')]
legacy_links=''.join(f'<li><a href="https://github.com/ITMO-SE-ML/{slug}">{e(title)}</a></li>' for slug,title in legacy)
html='''<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Машинное обучение · ИТМО · 2026/27</title>
<meta name="description" content="Курс машинного обучения ИТМО: лекции, домашние задания, TAIGA, ведомость и правила оценивания. 2026/27 учебный год.">
<meta name="theme-color" content="#101f38"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Перейти к материалам</a>
<aside class="sidebar"><a class="brand" href="#main">ИТМО <span>/ ML</span></a><p class="semester">2026/27 учебный год</p>
<nav aria-label="Разделы курса"><a href="#materials">Материалы</a><a href="#homework">Домашние задания</a><a href="#taiga">Бот TAIGA</a><a href="#grades">Ведомость</a><a href="#assessment">Оценивание</a><a href="#team">Команда</a><a href="#archive">Архив</a></nav>
<div class="sidefoot">Машинное обучение<br>Университет ИТМО<br><br><a href="@@organization_url@@">Организация на GitHub</a></div></aside>
<main id="main"><header><div class="topline"><span class="eyebrow">Машинное обучение</span><span>Осенний семестр · 2026</span></div>
<h1>Материалы курса</h1><p class="intro">Лекции, задания и всё, что нужно для учёбы в течение семестра.</p>
<div class="quick"><a href="#homework"><strong>Домашние задания</strong><small>Условия и репозитории</small></a><a href="@@grades_url@@"><strong>Ведомость</strong><small>Журнал проверок ДЗ 2026</small></a><a href="#taiga"><strong>Бот TAIGA</strong><small>Получение онлайн-домашек</small></a></div></header>
<section id="materials"><div class="sectionhead"><h2>Лекции и практика</h2><span>Актуальные материалы · 2026/27</span></div><p class="note">Новые лекции публикуются только на этом сайте. Скачивайте PDF по ссылкам ниже.</p>
<div class="lectures">
<article class="lecture"><div class="number">01</div><div><h3>Машинное обучение и анализ данных</h3><p>Задачи ML, этапы работы с данными, признаки, визуализация и базовый EDA.</p><div class="links"><a href="materials/lecture-01.pdf">Слайды · PDF</a><a href="materials/eda-wine.py" download>Пример EDA · Python</a></div></div></article>
<article class="lecture"><div class="number">02</div><div><h3>EDA и уменьшение размерности</h3><p>Распределения, статистический анализ, стандартизация, проклятие размерности и PCA.</p><div class="links"><a href="materials/lecture-02.pdf">Слайды · PDF</a></div></div></article>
<article class="lecture"><div class="number">03</div><div><h3>kNN, метрики и оценка качества</h3><p>Повторение стандартизации и PCA. kNN, SMOTE, train/validation/test, cross-validation, confusion matrix, ROC/PR. Применение ближайших соседей в поиске и RAG.</p><div class="links"><a href="materials/lecture-03.pdf">Слайды · PDF</a></div></div></article>
</div></section>
<section id="homework"><div class="sectionhead"><h2>Домашние задания</h2><span>Условия доступны на GitHub</span></div>
<div class="homeworks"><article class="homework"><p class="eyebrow">ДЗ 01 · Онлайн</p><h3>First Date with Data</h3><p>NumPy и pandas на данных WFP Food Prices: обработка таблиц и временных рядов, реализация функций и открытые тесты.</p><a class="button" href="https://github.com/ITMO-SE-ML/hw01-y26-first-date-with-data/blob/main/HW01.md">Открыть условие</a><p class="meta"><strong>Дедлайн:</strong> 11 сентября, 23:59 МСК<br><a href="https://github.com/ITMO-SE-ML/hw01-y26-first-date-with-data">Репозиторий и запуск тестов</a></p></article>
<article class="homework"><p class="eyebrow">ДЗ 02 · Очная защита</p><h3>EDA: исследование ДТП</h3><p>Данные своего региона, визуализации и карты, три статистические гипотезы, PCA и t-SNE. Результат — дашборд и отчёт.</p><a class="button" href="https://github.com/ITMO-SE-ML/hw02-y26-eda">Открыть условие</a><p class="meta"><strong>Дедлайн:</strong> будет объявлен<br><a href="https://github.com/ITMO-SE-ML/hw02-y26-eda/blob/main/docs/README.md">Документация и быстрый старт</a></p></article></div>
<p class="note"><strong>Онлайн-домашки:</strong> личный репозиторий получите через TAIGA — <a href="#taiga">инструкция ниже</a>.</p><p class="note"><strong>Домашки с очной защитой:</strong> откройте условие по ссылке на GitHub и выполняйте работу удобным способом. Принимать задание или создавать репозиторий через бота не нужно. Результат покажите на очной защите по требованиям задания.</p></section>
<section id="taiga"><div class="sectionhead"><h2>Онлайн-домашки через TAIGA</h2><span>TAIGA · Telegram</span></div><div class="botbox"><h3>Получите репозиторий для онлайн-домашки</h3>@@bot_link@@
<ol><li>В боте отправьте <code>/start</code> и введите номер ИСУ.</li><li>Проверьте найденные ФИО и группу. Если записи нет в списке, укажите ФИО и выберите группу.</li><li>Введите свой GitHub login <strong>без @ и без ссылки</strong>.</li><li>Откройте <code>/assignments</code>, выберите онлайн-домашку и нажмите «Создать репу».</li><li>Сначала примите приглашение на GitHub, затем откройте созданный репозиторий. Выполните работу по её README.</li></ol>
<div class="commands"><span><code>/accepted</code> Полученные задания</span><span><code>/settings</code> Настройки GitHub</span><span><code>/help</code> Меню и помощь</span></div><p class="note">«Принятые ДЗ» в меню бота — задания, для которых вы получили репозиторий. Этот статус не означает, что работа сдана или зачтена.</p></div>
<p class="note">Если репозиторий не открывается, проверьте, что приглашение принято и вы вошли именно в тот GitHub-аккаунт, который указали при регистрации.</p></section>
<section id="grades"><div class="sectionhead"><h2>Ведомость</h2></div><div class="gradesbox"><h3>Журнал проверок ДЗ 2026</h3><p>Результаты проверок и баллы за домашние задания находятся в общей таблице. Найдите свою группу и строку с результатами.</p><a class="button" href="@@grades_url@@">Открыть таблицу с оценками</a><p class="note">Если Google запрашивает доступ, войдите в аккаунт, которому открыт доступ к ведомости.</p></div></section>
<section id="assessment"><div class="sectionhead"><h2>Как складывается оценка</h2><span>Максимум — 100 баллов</span></div>
<div class="scorebar" aria-label="60 баллов за лабораторные, 20 за две рубежки, 20 за экзамен"><div><strong>60</strong><span>Лабораторные работы</span></div><div><strong>20</strong><span>Две рубежки</span></div><div><strong>20</strong><span>Экзамен</span></div></div>
<div class="tablewrap"><table><caption class="skip">Пороги итоговой оценки и формат экзамена</caption><thead><tr><th scope="col">Оценка</th><th scope="col">Сумма баллов</th><th scope="col">Экзамен</th></tr></thead><tbody><tr><th scope="row">3 · Удовлетворительно</th><td>от 60 до 75</td><td>Теоретический</td></tr><tr><th scope="row">4 · Хорошо</th><td>от 75 до 90</td><td>Теория или итоговый проект</td></tr><tr><th scope="row">5 · Отлично</th><td>от 90 до 100 включительно</td><td>Итоговый проект</td></tr></tbody></table></div><p class="note">Верхняя граница диапазонов для «3» и «4» не включается. Для положительной оценки обе рубежки должны быть закрыты: <strong>минимум 6 из 10 за каждую</strong>.</p>
<div class="rules"><article><h3>Онлайн-работы</h3><p>После сдачи — мини-тест на практике: 5 минут, 5 вопросов. Балл за лабораторную: <strong>X × max(0,5; T)</strong>, где X — балл за решение, а T — доля баллов за тест от 0 до 1.</p><p>Мини-тест не переписывается. При пропуске T = 0, поэтому сохраняется половина баллов за решение.</p></article><article><h3>Очные защиты</h3><p>Условие берите по прямой ссылке на GitHub. Выполняйте работу удобным способом; получать её через TAIGA не требуется.</p><p>Покажите результат и объясните постановку задачи, выбор данных, методов и метрик, эксперименты и выводы. Формат и критерии указаны в условии конкретной работы.</p><p>LLM можно использовать как инструмент. Свои решения и полученные результаты нужно уметь объяснить самостоятельно.</p></article></div>
<details><summary>Рубежки и экзамен</summary><p class="note">Рубежные работы: <strong>20 октября</strong> и <strong>15 декабря 2026</strong>, во время практических занятий. Письменно, на бумаге; без конспектов, других материалов и электронных устройств.</p><p>Для «3» предусмотрен теоретический экзамен. Для «4» можно выбрать теорию или проект. Для «5» нужен итоговый практический проект в формате мини-курсовой.</p></details></section>
<section id="team"><div class="sectionhead"><h2>Команда курса</h2></div><div class="team"><div><h3>Лектор</h3><p>Елизавета Власова</p></div><div><h3>Практики</h3><p>Кирилл Захаров<br>Камила Насибуллина<br>Михаил Подсытник<br>Игорь Толстокулаков</p></div><div><h3>Менторы</h3><p>Анастасия Минская<br>Мария Сафронова</p></div></div>@@chat_link@@</section>
<section id="archive"><div class="sectionhead"><h2>Материалы прошлого года</h2></div><p class="muted">Материалы предыдущего потока для самостоятельного изучения. Их нумерация, сроки и правила сдачи не относятся к текущему семестру.</p><p class="note"><a href="@@archive_folder_url@@">Прошлогодние презентации на Google Drive</a>. На диске находятся только материалы прошлого года.</p><details><summary>Презентации предыдущего потока · 14 файлов</summary><ul>@@archive_links@@</ul></details><details><summary>Задания предыдущего потока · 8 тем</summary><ul>@@legacy_links@@</ul></details></section>
<footer><span>ИТМО · Машинное обучение · 2026/27</span><span>Обновлено: @@updated@@</span></footer></main></body></html>'''
for key in ['organization_url','grades_url','archive_folder_url','updated']:
 html=html.replace('@@'+key+'@@',e(cfg[key],quote=True))
for key,val in [('bot_link',bot_link),('chat_link',chat_link),('archive_links',archive_links),('legacy_links',legacy_links)]:html=html.replace('@@'+key+'@@',val)
assert '@@' not in html
(ROOT/'docs/index.html').write_text(html)
print('Built docs/index.html')
