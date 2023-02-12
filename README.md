# RAINBOW ENGINE Документация
Краткое описание того, как работать со сценой и 3D движком

# Сцена
### Все объекты обрабатываются через класс сцены
Сцена служит для обработки взаимодействия между объектами

# Работа со сценой

## Создание объектов на сцене
Объект на сцену добавляется функцией `add_object`. 
Она принимает в параметры экземпляр класса `GameObject` и добавляет его на сцену.
Далее можно будет получить ссылку на этот объект через функцию `get_object_by_id` по его id 
или же через функцию `get_object_by_name` по его имени.  
Пример:
```python
cat = GameObject("cat")
cat.set_component(Model(app, cat, "cat_model", "cat_texture"))
cat.transform.position = glm.vec3(0, -2, 0)
cat.transform.scale = glm.vec3(0.5, 0.5, 0.5)
self.add_object(cat)
```
Тут мы создаём экземпляр класса `GameObject`, добавляем компонент `Model`, задаём позицию и размер, и затем мы добавляем
его на сцену.

## Создание освещения на сцене
Работа со светом похожа на работу с объектами. 
Для создания источника света используется функция `add_light_source(light_source)` как параметр она принимает экземпляр
класса `LightSource`. 
Ссылку на экземпляр класса `LightSource` на сцене можно получить через функцию `get_light_by_id`, посылая на вход id
источника света.  
Пример:
```python
self.add_light_source(LightSource(glm.vec3(0, 8, 0), glm.vec3(0, 1, 0)))
```
Тут мы добавляем экземпляр класса `LightSource` на сцену.

# Класс GameObject
### Класс GameObject служит для хранения данных об объекте на сцене.
##  Компоненты
У экземпляра класса `GameObject` есть словарь с компонентами (экземплярами класса `Component`). 
Объекты класса `Component` хранят в себе описания для поведения экземпляра класса `GameObject`.  
Пример:
```python
cat = GameObject("cat")
cat.set_component(Model(app, cat, "cat_model", "cat_texture"))
```
Тут мы создаём экземпляр класса `GameObject` и добавляем к нему компонент `Model` для того, что-бы привязать 3D модель
к экземпляру класса `GameObject`. 

Что-бы как-то изменять компоненты, можно воспользоваться функцией `get_component`, она вернёт ссылку на компонент,
в котором уже можно будет совершать изменения.  
Пример:
```python
cat_rb = cat.get_component("RigidBody")
cat_rb.mass = 50
```
Тут мы получаем ссылку на компонент RigidBody, у экземпляра класса `GameObject`, с именем cat, и изменяем его массу

У каждого созданного экземпляра класса `GameObject` есть стандартный компонент `Transform`. Компонент `Transform` 
хранит в себе данные об положении, размере и вращении объекта.  
Пример:
```python
cat.transform.position = glm.vec3(0, 0, 0)
```
Тут мы изменяем позицию, экземпляра класса `GameObject`, с именем cat

## "Дети"
У каждого экземпляра класса `GameObject` есть массив "детей". "Дети" - это другие экземпляры класса `GameObject`.
"Дети" нужны для древовидной структуры сцены.  
Пример:
```python
cat_parent = GameObject("big cat")
cat_child = GameObject("small cat")
cat_parent.add_child(cat_child)
self.add_object(cat_parent)
```
Тут мы создаём два экземпляра класса `GameObject` и добавляем один из них (`cat_child`), как ребёнок для второго 
(`cat_parent`).

Получить ссылку на "ребёнка" можно через функции `get_child_by_id` или `get_child_by_name`, по id и имени соответственно.

# Класс LightSource
Он не имеет какой-либо сложной структуры, он лишь хранить в себе настройки для источника света (цвет и положение).  
Пример:
```python
light = LightSource(glm.vec3(0, 8, 0), glm.vec3(0, 1, 0))
```
Первый аргумент - положение в пространстве. Второй - цвет света, в формате RGB (яркость цвета записывается в диапазоне 
от 0.0 до 1.0)

# Добавление своих 3D моделей и текстур
Для загрузки 3D моделей и текстур используется скрипт `resource_loader.py`.   

Для загрузки 3D модели используется функция `load_3d_model`. На вход она принимает два аргумента, название модели и 
путь до самой 3D модели. Движок может работать только с объектами с расширением `.obj`.  
Пример:
```python
load_3d_model("cat_model", "models/cat.obj")
```
Тут мы загружаем модель `cat.obj` под именем `cat_model`

Для загрузки текстур используется функция `load_texture`. На вход она как и `load_3d_model` принимает два аргумента,
название текстуры и путь до самой текстуры.  
Пример:
```python
load_texture("cat_texture", "textures/cat.jpg")
```
Тут мы загружаем текстуру `cat.jpg` под именем `cat_texture`

# P.S.
Настройки (скорость перемещения и чувствительность мыши) изменяются в классе `Player`, который находиться в скрипте 
`player.py`

Если нужно изменить размер окна или выключить режим полного окна, это можно изменить в функции `main` (скрипт `main.py`)

Базовое управление камерой:  
WASD - перемещение по горизонтали  
SPACE - взлёт вверх  
C - спуск вниз  
Мышь - вращение камеры

Если будут какие-либо вопросы, можете писать мне в viber