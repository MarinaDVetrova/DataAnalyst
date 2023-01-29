#!/usr/bin/env python
# coding: utf-8

# # Исследование надежности заемщиков
# 

# Во второй части проекта вы выполните шаги 3 и 4. Их вручную проверит ревьюер.
# Чтобы вам не пришлось писать код заново для шагов 1 и 2, мы добавили авторские решения в ячейки с кодом. 
# 
# 

# ## Откройте таблицу и изучите общую информацию о данных

# **Задание 1. Импортируйте библиотеку pandas. Считайте данные из csv-файла в датафрейм и сохраните в переменную `data`. Путь к файлу:**
# 
# `/datasets/data.csv`

# In[1]:


import pandas as pd

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('https://code.s3.yandex.net/datasets/data.csv')


# **Задание 2. Выведите первые 20 строчек датафрейма `data` на экран.**

# In[2]:


data.head(20)


# **Задание 3. Выведите основную информацию о датафрейме с помощью метода `info()`.**

# In[3]:


data.info()


# ## Предобработка данных

# ### Удаление пропусков

# **Задание 4. Выведите количество пропущенных значений для каждого столбца. Используйте комбинацию двух методов.**

# In[4]:


data.isna().sum()


# **Задание 5. В двух столбцах есть пропущенные значения. Один из них — `days_employed`. Пропуски в этом столбце вы обработаете на следующем этапе. Другой столбец с пропущенными значениями — `total_income` — хранит данные о доходах. На сумму дохода сильнее всего влияет тип занятости, поэтому заполнить пропуски в этом столбце нужно медианным значением по каждому типу из столбца `income_type`. Например, у человека с типом занятости `сотрудник` пропуск в столбце `total_income` должен быть заполнен медианным доходом среди всех записей с тем же типом.**

# In[5]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['total_income'].isna()), 'total_income'] = \
    data.loc[(data['income_type'] == t), 'total_income'].median()


# ### Обработка аномальных значений

# **Задание 6. В данных могут встречаться артефакты (аномалии) — значения, которые не отражают действительность и появились по какой-то ошибке. таким артефактом будет отрицательное количество дней трудового стажа в столбце `days_employed`. Для реальных данных это нормально. Обработайте значения в этом столбце: замените все отрицательные значения положительными с помощью метода `abs()`.**

# In[6]:


data['days_employed'] = data['days_employed'].abs()


# **Задание 7. Для каждого типа занятости выведите медианное значение трудового стажа `days_employed` в днях.**

# In[7]:


data.groupby('income_type')['days_employed'].agg('median')


# У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставьте их как есть.

# **Задание 8. Выведите перечень уникальных значений столбца `children`.**

# In[8]:


data['children'].unique()


# **Задание 9. В столбце `children` есть два аномальных значения. Удалите строки, в которых встречаются такие аномальные значения из датафрейма `data`.**

# In[9]:


data = data[(data['children'] != -1) & (data['children'] != 20)]


# **Задание 10. Ещё раз выведите перечень уникальных значений столбца `children`, чтобы убедиться, что артефакты удалены.**

# In[10]:


data['children'].unique()


# ### Удаление пропусков (продолжение)

# **Задание 11. Заполните пропуски в столбце `days_employed` медианными значениями по каждого типа занятости `income_type`.**

# In[11]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['days_employed'].isna()), 'days_employed'] = \
    data.loc[(data['income_type'] == t), 'days_employed'].median()


# **Задание 12. Убедитесь, что все пропуски заполнены. Проверьте себя и ещё раз выведите количество пропущенных значений для каждого столбца с помощью двух методов.**

# In[12]:


data.isna().sum()


# ### Изменение типов данных

# **Задание 13. Замените вещественный тип данных в столбце `total_income` на целочисленный с помощью метода `astype()`.**

# In[13]:


data['total_income'] = data['total_income'].astype(int)


# ### Обработка дубликатов

# **Задание 14. Обработайте неявные дубликаты в столбце `education`. В этом столбце есть одни и те же значения, но записанные по-разному: с использованием заглавных и строчных букв. Приведите их к нижнему регистру.**

# In[14]:


data['education'] = data['education'].str.lower()


# **Задание 15. Выведите на экран количество строк-дубликатов в данных. Если такие строки присутствуют, удалите их.**

# In[15]:


data.duplicated().sum()


# In[16]:


data = data.drop_duplicates()


# ### Категоризация данных

# **Задание 16. На основании диапазонов, указанных ниже, создайте в датафрейме `data` столбец `total_income_category` с категориями:**
# 
# - 0–30000 — `'E'`;
# - 30001–50000 — `'D'`;
# - 50001–200000 — `'C'`;
# - 200001–1000000 — `'B'`;
# - 1000001 и выше — `'A'`.
# 
# 
# **Например, кредитополучателю с доходом 25000 нужно назначить категорию `'E'`, а клиенту, получающему 235000, — `'B'`. Используйте собственную функцию с именем `categorize_income()` и метод `apply()`.**

# In[17]:


def categorize_income(income):
    try:
        if 0 <= income <= 30000:
            return 'E'
        elif 30001 <= income <= 50000:
            return 'D'
        elif 50001 <= income <= 200000:
            return 'C'
        elif 200001 <= income <= 1000000:
            return 'B'
        elif income >= 1000001:
            return 'A'
    except:
        pass


# In[18]:


data['total_income_category'] = data['total_income'].apply(categorize_income)


# **Задание 17. Выведите на экран перечень уникальных целей взятия кредита из столбца `purpose`.**

# In[19]:


data['purpose'].unique()


# **Задание 18. Создайте функцию, которая на основании данных из столбца `purpose` сформирует новый столбец `purpose_category`, в который войдут следующие категории:**
# 
# - `'операции с автомобилем'`,
# - `'операции с недвижимостью'`,
# - `'проведение свадьбы'`,
# - `'получение образования'`.
# 
# **Например, если в столбце `purpose` находится подстрока `'на покупку автомобиля'`, то в столбце `purpose_category` должна появиться строка `'операции с автомобилем'`.**
# 
# **Используйте собственную функцию с именем `categorize_purpose()` и метод `apply()`. Изучите данные в столбце `purpose` и определите, какие подстроки помогут вам правильно определить категорию.**

# In[20]:


def categorize_purpose(row):
    try:
        if 'автом' in row:
            return 'операции с автомобилем'
        elif 'жил' in row or 'недвиж' in row:
            return 'операции с недвижимостью'
        elif 'свад' in row:
            return 'проведение свадьбы'
        elif 'образов' in row:
            return 'получение образования'
    except:
        return 'нет категории'


# In[21]:


data['purpose_category'] = data['purpose'].apply(categorize_purpose)


# ### Шаг 3. Исследуйте данные и ответьте на вопросы

# #### 3.1 Есть ли зависимость между количеством детей и возвратом кредита в срок?

# In[22]:


data.pivot_table(index = 'children', values = 'debt', aggfunc = ['count', 'sum', 'mean'])\
    .sort_values(by = ('mean', 'debt'), ascending = False)\
    .style.format({('mean', 'debt') : '{:.2%}'})


# In[23]:


def categorize_children(children):
    if children > 0:
        return 'C детьми'
    if children == 0:
        return 'Без детей'

data['have_children'] = data['children'].apply(categorize_children)

data.groupby('have_children')['debt'].sum() / data.groupby('have_children')['debt'].count()


# **Вывод:** 

# У заемщиков с детьми больше просрочек выплат. 

# У заемщиков с детьми больше просрочек выплат. Больше всего просрочек в семьях, где 4 ребенка. 
# При этом в семьях, где 5 детей просрочек нет. Но делать выводы на основе этих данных не корректно, т.к. таких семей мало.

# #### 3.2 Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[25]:


def categorize_family_status(family_status):
    if 'женат' in family_status:
        return 'В браке'
    return 'Холост/Не замужем'

data['family_status_catecory'] = data['family_status'].apply(categorize_family_status)

data.groupby('family_status_catecory')['debt'].sum() / data.groupby('family_status_catecory')['debt'].count()


# **Вывод:** 

# У людей, состоящих в браке, меньше просрочек.

# #### 3.3 Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# In[26]:


data.pivot_table(index = 'total_income_category', values = 'debt', aggfunc = ['count', 'sum', 'mean'])\
    .sort_values(by = ('mean', 'debt'), ascending = False)\
    .style.format({('mean', 'debt') : '{:.2%}'})


# In[27]:


data.groupby('total_income_category')['debt'].sum() / data.groupby('total_income_category')['debt'].count()


# **Вывод:** 

# Больше всего просрочек у клиентов с низким доходом из категории E (до 30 000) и доходом из категории С (от 50 001 до 200 000). 
# Меньше всего просрочек у клиентов из категории D (от 30 001 до 50 000).

# Самые многочисленные группы B (от 200 001 до 1 000 000) и C (от 50 001 до 200 000). 
# В группе В, с доходом выше среднего, процент просрочек низкий (ниже среднего). 
# Эту группу можно реклмендовать для кредитования.
# 
# В группе C, со средним доходом, процент просрочек высокий (выше среднего). 
# При выдаче кредита можно порекомендовать учитывать этот фактор как негативный при принятии решения.

# #### 3.4 Как разные цели кредита влияют на его возврат в срок?

# In[ ]:


data.groupby('purpose_category')['debt'].sum() / data.groupby('purpose_category')['debt'].count()


# **Вывод:** 

# Клиенты, которые берут кредиты на автомобиль или образование чаще совершают просрочки. 
# Реже допускают просрочки по кредитам на недвижимость и свадьбу.

# #### 3.5 Приведите возможные причины появления пропусков в исходных данных.

# *Ответ:* 

# Это может быть ошибка переноса данных или заполнения анкет.

# #### 3.6 Объясните, почему заполнить пропуски медианным значением — лучшее решение для количественных переменных.

# *Ответ:* 

# Медианное значение свидет к минимому дальнейшие погрешности в расчетах. 
# Это важно, когда мы будет выполнять операции деления с этими данными, чтобы не было деления на ноль. 
# Также, когда мы знаем, что показатель не может быть "0", а отсутствующие значения могут исказить выводы. 
# Логичнее заполнить их средним значением, т.к. оно не будет кардинально влиять на выводы.

# ### Шаг 4: общий вывод.

# Напишите ваш общий вывод.

# При выполнении проекта были обработаны и проанализированы социально-демографические данные по клиентам банка,
# которые пользовались услугами кредитования.
# 
# На основе выборки проанализированы зависимости:
# 
#     1. Семейное положение и просрочки по кредиту
#     Вывод: У людей, состоящих в браке, меньше просрочек.
#     Метод: разделила всех заемщиков на 2 группы:
#             - "В браке" для тех, у кото статус "женат / замужем"
#             - "Холост/Не замужем" для всех остальных групп
#     Подготовила таблицу с указанием семейного статуса и процента по просрочке кредита в этих группах.
#     2. Наличие или отсутствие детей и просрочки по кредиту
#     Вывод: У заемщиков с детьми больше просрочек выплат. Больше всего просрочек в семьях, где 4 ребенка. 
#     Метод: После очистки данных от статистических выбросов подготовила таблицу с категориями заемщиков, 
#     у которых есть от 1 до 5 детей и бездетными, и процентами по просрочке кредита.
#     3. Уровень дохода и просрочки по кредиту
#     Вывод: Больше всего просрочек у клиентов с низким доходом из категории E (до 30 000) 
#     и доходом из категории С (от 50 001 до 200 000). 
#     Меньше всего просрочек у клиентов из категории D (от 30 001 до 50 000).
#     Метод: Привела данные к единообразию для корректной обработки, использовав медианные значения в случаях 
#     с пропущенными данными. 
#     Размеры доход для удобства обработки разбила на 5 категорий, присвоив им индексы A-E. 
#     Подготовила таблицу по категориям дохода и процентом просрочек. 
#     4. Цель кредита и возможность просрочки
#     Вывод: Клиенты, которые берут кредиты на автомобиль или образование чаще совершают просрочки. 
#     Реже допускают просрочки по кредитам на недвижимость и свадьбу.
#     Метод: Многочисленные цели кредита агрегировала в 4 раздела по смыслу. 
#     Подготовила таблицу с данными по базовой цели кредитования и процентом просрочек.  
#     
# Для выдачи кредитов можно порекомендовать выдавать их: 
# 
#     1. Людям, состоящим в браке 
#     2. Людям без детей 
#     3. Людям с доходом из категории D (от 30 001 до 50 000) 
#     4. Цели кредита "операции с недвижимостью" и "проведение свадьбы" предпочтительные. 
# 
# Также всем этим группам можно предлагать кредит или предодобрить его, если они являются клиентами банка, но не подавали заявку на кредит.

# Для выдачи кредитов можно порекомендовать выдавать их:
#     1. Людям, состоящим в браке
#     2. Людям без детей
#     3. Людям с доходом из категории D (от 30 001 до 50 000)
#     4. Цели кредита "операции с недвижимостью" и "проведение свадьбы" предпочтительные.
# Также всем этим группам можно предлагать кредит или предодобрять его, если они являются киентами банка, 
# но не подавали заявку на кредит.
