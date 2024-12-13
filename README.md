# QC-app-clone
Приложение (Vue.js, Django Rest API, PostgreSQL) для загрузки данных из масс-спектрометра, парсинга, предобработки, визуализации/анализа, и затем сохранения в базу данных. Реализована резиновая верстка, маршрутизация с помощью Vue Router, временное хранение данных с помощью Pinia и localStorage.

Загружается файл, который представляет из себя эксель таблицу, где каждая строка это образец, а столбцы говорят о группе образца, имени образца и концентрациях десятков метаболитов в крови.
Затем пользователь либо выбирает существующий проект, к которому прикрпепиться этот батч (цикл анализа), или создает новый проект. Также можно загрузить батч сразу из базы, не загружая новый файл.
Главная страница AnalysisView.vue наиболее полно сделана в плане визуала и функицональности компонентов внутри. Она содержит главные таблицы, которые являются индикацией выхода за пределы нормы концентрации веществ в загружаемом файле. Таблица подсвечивается по строке и столбцу при наведении мышкой для удобного просмотра, хэдер таблицы со свойством display: sticky, благодаря чему всегда виден даже при прокруте вниз таблицы. Второй компонент открывается при нажатии на строку с названием метаболита, строка стразу подсвечивается, а справа появлются графики для каждой группы образцов, на которых точкой показана концентрация метаболита в границах нормы и за её пределами. Также можно нажать кнопку "сравнить батчи внутри проекта" и из базы данных подхватятся батчи этого проекта и будут отображены на одном графике в хронологическом порядке. Также сделана светлая/темная тема на приложение с помощью своей "палитры" для primary/secondary/text/... color и глобального флажка состояния. 

Проект в сжатых сроках начался (разработано это за 3 недели от начала обсуждений) и был сразу отложен в долгий ящик взамен другому приложению, поэтому бэкенд часть и общение с базой данных оптимизировать правильно не было возможности...
