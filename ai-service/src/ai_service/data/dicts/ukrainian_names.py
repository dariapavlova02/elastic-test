# -*- coding: utf-8 -*-

"""
Extended dictionary of Ukrainian names, their variants, declensions and transliterations.
"""

NAMES = {
    'Сергій': {
        'gender': 'masc',
        'variants': ['Сергей'],
        'diminutives': ['Сергійко', 'Сержик', 'Сергійчик', 'Сергійонько', 'Сірко'],
        'transliterations': ['Serhii', 'Serhiy', 'Sergiy'],
        'declensions': ['Сергія', 'Сергію', 'Сергія', 'Сергієм', 'Сергієві']
    },
    'Володимир': {
        'gender': 'masc',
        'variants': ['Владимир'],
        'diminutives': ['Володя', 'Вова', 'Володька', 'Вовчик', 'Володимирко'],
        'transliterations': ['Volodymyr', 'Vladimir'],
        'declensions': ['Володимира', 'Володимиру', 'Володимира', 'Володимиром', 'Володимирові']
    },
    'Петро': {
        'gender': 'masc',
        'variants': ['Петр'],
        'diminutives': ['Петя', 'Петенька', 'Петрик', 'Петрусь', 'Петруся', 'Петрунько'],
        'transliterations': ['Petro', 'Peter', 'Petr'],
        'declensions': ['Петра', 'Петрові', 'Петра', 'Петром', 'Петрові']
    },
    'Іван': {
        'gender': 'masc',
        'variants': ['Иван'],
        'diminutives': ['Івасик', 'Івасько', 'Іванько', 'Ваня'],
        'transliterations': ['Ivan', 'Ioan'],
        'declensions': ['Івана', 'Іванові', 'Івана', 'Іваном', 'Іванові']
    },
    'Олексій': {
        'gender': 'masc',
        'variants': ['Алексей'],
        'diminutives': ['Олесь', 'Олесик', 'Олежко', 'Олексійко', 'Льоша'],
        'transliterations': ['Oleksii', 'Oleksiy', 'Alexey'],
        'declensions': ['Олексія', 'Олексію', 'Олексія', 'Олексієм', 'Олексієві']
    },
    'Дарія': {
        'gender': 'femn',
        'variants': ['Дарья', 'Одарка', 'Дарʼя'],
        'diminutives': ['Даша', 'Дарочка', 'Дашенька', 'Даринка', 'Даруся'],
        'transliterations': ['Dariia', 'Daria', 'Darya'],
        'declensions': ['Дарії', 'Дарії', 'Дарію', 'Дарією', 'Дарії']
    },
    'Анна': {
        'gender': 'femn',
        'variants': ['Ганна'],
        'diminutives': ['Аня', 'Аннуся', 'Ганя', 'Ганнуся', 'Анечка'],
        'transliterations': ['Anna', 'Hanna'],
        'declensions': ['Анни', 'Анні', 'Анну', 'Анною', 'Анні']
    },
    'Марія': {
        'gender': 'femn',
        'variants': ['Мария'],
        'diminutives': ['Марічка', 'Маруся', 'Машенька', 'Марійка', 'Маруня'],
        'transliterations': ['Mariia', 'Mariya', 'Maria'],
        'declensions': ['Марії', 'Марії', 'Марію', 'Марією', 'Марії']
    },
    'Олена': {
        'gender': 'femn',
        'variants': ['Елена', 'Альона'],
        'diminutives': ['Лена', 'Леночка', 'Ленуся', 'Оленка', 'Оленочка'],
        'transliterations': ['Olena', 'Elena', 'Aliona'],
        'declensions': ['Олени', 'Олені', 'Олену', 'Оленою', 'Олені']
    },
    'Наталія': {
        'gender': 'femn',
        'variants': ['Наталия'],
        'diminutives': ['Наталя', 'Наталочка', 'Наталюся', 'Наталка', 'Тала'],
        'transliterations': ['Nataliia', 'Natalia', 'Nataliya'],
        'declensions': ['Наталії', 'Наталії', 'Наталію', 'Наталією', 'Наталії']
    },
    'Михайло': {
        'gender': 'masc',
        'variants': ['Михаил'],
        'diminutives': ['Михайлик', 'Михась', 'Мишко', 'Михайлусь'],
        'transliterations': ['Mykhailo', 'Mikhail', 'Michael'],
        'declensions': ['Михайла', 'Михайлові', 'Михайла', 'Михайлом', 'Михайлові']
    },
    'Андрій': {
        'gender': 'masc',
        'variants': ['Андрей'],
        'diminutives': ['Андрійко', 'Андрійчик', 'Андрусь'],
        'transliterations': ['Andrii', 'Andriy', 'Andrey'],
        'declensions': ['Андрія', 'Андрію', 'Андрія', 'Андрієм', 'Андрієві']
    },
    'Василь': {
        'gender': 'masc',
        'variants': ['Василий'],
        'diminutives': ['Василько', 'Васильчик', 'Василюсь', 'Вася'],
        'transliterations': ['Vasyl', 'Vasyliy', 'Basil'],
        'declensions': ['Василя', 'Василю', 'Василя', 'Василем', 'Василеві']
    },
    'Ірина': {
        'gender': 'femn',
        'variants': ['Ирина', 'Ярина'],
        'diminutives': ['Іринка', 'Іриночка', 'Іруся', 'Яринка', 'Іра'],
        'transliterations': ['Iryna', 'Yaryna', 'Irina'],
        'declensions': ['Ірини', 'Ірині', 'Ірину', 'Іриною', 'Ірині']
    },
    'Тетяна': {
        'gender': 'femn',
        'variants': ['Татьяна'],
        'diminutives': ['Таня', 'Танюся', 'Тетянка', 'Танечка'],
        'transliterations': ['Tetiana', 'Tetyana', 'Tatyana'],
        'declensions': ['Тетяни', 'Тетяні', 'Тетяну', 'Тетяною', 'Тетяні']
    },
    'Олександр': {
        'gender': 'masc',
        'variants': ['Александр'],
        'diminutives': ['Сашко', 'Олесь', 'Лесь', 'Саня', 'Шурик', 'Олександрик'],
        'transliterations': ['Oleksandr', 'Alexander', 'Olexandr'],
        'declensions': ['Олександра', 'Олександру', 'Олександра', 'Олександром', 'Олександрові']
    },
    'Дмитро': {
        'gender': 'masc',
        'variants': ['Дмитрий'],
        'diminutives': ['Діма', 'Дмитрик', 'Митя', 'Дмитрусь'],
        'transliterations': ['Dmytro', 'Dmitry'],
        'declensions': ['Дмитра', 'Дмитрові', 'Дмитра', 'Дмитром', 'Дмитрові']
    },
    'Богдан': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Богданко', 'Бодя', 'Даник', 'Богдась'],
        'transliterations': ['Bohdan', 'Bogdan'],
        'declensions': ['Богдана', 'Богданові', 'Богдана', 'Богданом', 'Богданові']
    },
    'Роман': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Рома', 'Ромко', 'Романко', 'Ромчик'],
        'transliterations': ['Roman'],
        'declensions': ['Романа', 'Романові', 'Романа', 'Романом', 'Романові']
    },
    'Тарас': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Тарасик', 'Тараско', 'Тарасунько'],
        'transliterations': ['Taras'],
        'declensions': ['Тараса', 'Тарасові', 'Тараса', 'Тарасом', 'Тарасові']
    },
    'Юрій': {
        'gender': 'masc',
        'variants': ['Юрий', 'Георгій'],
        'diminutives': ['Юра', 'Юрчик', 'Юрко', 'Юрась'],
        'transliterations': ['Yurii', 'Yuriy', 'Yury'],
        'declensions': ['Юрія', 'Юрію', 'Юрія', 'Юрієм', 'Юрієві']
    },
    'Віктор': {
        'gender': 'masc',
        'variants': ['Виктор'],
        'diminutives': ['Вітя', 'Вітько', 'Віктусь', 'Вікторик'],
        'transliterations': ['Viktor', 'Victor'],
        'declensions': ['Віктора', 'Вікторові', 'Віктора', 'Віктором', 'Вікторові']
    },
    'Вікторія': {
        'gender': 'femn',
        'variants': ['Виктория'],
        'diminutives': ['Віка', 'Вікуся', 'Віточка', 'Торя'],
        'transliterations': ['Viktoriia', 'Viktoriya', 'Victoria'],
        'declensions': ['Вікторії', 'Вікторії', 'Вікторію', 'Вікторією', 'Вікторії']
    },
    'Юлія': {
        'gender': 'femn',
        'variants': ['Юлия'],
        'diminutives': ['Юля', 'Юлечка', 'Юльчик', 'Юляся'],
        'transliterations': ['Yuliia', 'Yulia', 'Julia'],
        'declensions': ['Юлії', 'Юлії', 'Юлію', 'Юлією', 'Юлії']
    },
    'Катерина': {
        'gender': 'femn',
        'variants': ['Екатерина'],
        'diminutives': ['Катя', 'Катруся', 'Катря', 'Катеринка'],
        'transliterations': ['Kateryna', 'Catherine', 'Yekaterina'],
        'declensions': ['Катерини', 'Катерині', 'Катерину', 'Катериною', 'Катерині']
    },
    'Людмила': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Люда', 'Людочка', 'Люся', 'Мила'],
        'transliterations': ['Liudmyla', 'Lyudmyla', 'Ludmila'],
        'declensions': ['Людмили', 'Людмилі', 'Людмилу', 'Людмилою', 'Людмилі']
    },
    'Світлана': {
        'gender': 'femn',
        'variants': ['Светлана'],
        'diminutives': ['Світланка', 'Лана', 'Свєта', 'Світланочка'],
        'transliterations': ['Svitlana', 'Svetlana'],
        'declensions': ['Світлани', 'Світлані', 'Світлану', 'Світланою', 'Світлані']
    },
    'Валентина': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Валя', 'Валюша', 'Тіна', 'Валентинка'],
        'transliterations': ['Valentyna', 'Valentina'],
        'declensions': ['Валентини', 'Валентині', 'Валентину', 'Валентиною', 'Валентині']
    },
    'Максим': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Макс', 'Максимко', 'Максюта'],
        'transliterations': ['Maksym', 'Maxim', 'Maksim'],
        'declensions': ['Максима', 'Максиму', 'Максима', 'Максимом', 'Максимові']
    },
    'Ярослав': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Ярик', 'Славко', 'Ярчик', 'Ярославко'],
        'transliterations': ['Yaroslav', 'Iaroslav'],
        'declensions': ['Ярослава', 'Ярославу', 'Ярослава', 'Ярославом', 'Ярославові']
    },
    'Оксана': {
        'gender': 'femn',
        'variants': ['Ксенія'],
        'diminutives': ['Ксюша', 'Оксанка', 'Ксеня', 'Ксюня'],
        'transliterations': ['Oksana', 'Kseniia'],
        'declensions': ['Оксани', 'Оксані', 'Оксану', 'Оксаною', 'Оксані']
    },
    'Софія': {
        'gender': 'femn',
        'variants': ['Софья'],
        'diminutives': ['Софійка', 'Соня', 'Сонька', 'Софа'],
        'transliterations': ['Sofiia', 'Sofiya', 'Sophia'],
        'declensions': ['Софії', 'Софії', 'Софію', 'Софією', 'Софії']
    },
    'Артем': {
        'gender': 'masc',
        'variants': ['Артём'],
        'diminutives': ['Артемко', 'Тьома', 'Артемон', 'Артемчик'],
        'transliterations': ['Artem', 'Artiom'],
        'declensions': ['Артема', 'Артему', 'Артема', 'Артемом', 'Артемові']
    },
    'Анастасія': {
        'gender': 'femn',
        'variants': ['Анастасия'],
        'diminutives': ['Настя', 'Настуся', 'Ася', 'Настенька'],
        'transliterations': ['Anastasiia', 'Anastasiya', 'Anastasia'],
        'declensions': ['Анастасії', 'Анастасії', 'Анастасію', 'Анастасією', 'Анастасії']
    },
    'Євген': {
        'gender': 'masc',
        'variants': ['Евгений', 'Євгеній'],
        'diminutives': ['Женя', 'Євгенко', 'Геник'],
        'transliterations': ['Yevhen', 'Yevgen', 'Eugene'],
        'declensions': ['Євгена', 'Євгену', 'Євгена', 'Євгеном', 'Євгенові']
    },
    'Євгенія': {
        'gender': 'femn',
        'variants': ['Евгения'],
        'diminutives': ['Женя', 'Євгенка', 'Геня'],
        'transliterations': ['Yevheniia', 'Yevgeniya', 'Eugenia'],
        'declensions': ['Євгенії', 'Євгенії', 'Євгенію', 'Євгенією', 'Євгенії']
    },
    'Павло': {
        'gender': 'masc',
        'variants': ['Павел'],
        'diminutives': ['Павлик', 'Паша', 'Павлусь'],
        'transliterations': ['Pavlo', 'Pavel', 'Paul'],
        'declensions': ['Павла', 'Павлові', 'Павла', 'Павлом', 'Павлові']
    },
    'Ольга': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Оля', 'Олечка', 'Ольгуня', 'Олюся'],
        'transliterations': ['Olha', 'Olga'],
        'declensions': ['Ольги', 'Ользі', 'Ольгу', 'Ольгою', 'Ользі']
    },
    'Ігор': {
        'gender': 'masc',
        'variants': ['Игорь'],
        'diminutives': ['Ігорко', 'Гарик', 'Ігорьок'],
        'transliterations': ['Ihor', 'Igor'],
        'declensions': ['Ігоря', 'Ігорю', 'Ігоря', 'Ігорем', 'Ігореві']
    },
    'Христина': {
        'gender': 'femn',
        'variants': ['Кристина'],
        'diminutives': ['Христя', 'Христинка', 'Тіна'],
        'transliterations': ['Khrystyna', 'Christina'],
        'declensions': ['Христини', 'Христині', 'Христину', 'Христиною', 'Христині']
    },
    'Назар': {
        'gender': 'masc',
        'variants': ['Назарий'],
        'diminutives': ['Назарко', 'Назарик', 'Зарко'],
        'transliterations': ['Nazar', 'Nazariy'],
        'declensions': ['Назара', 'Назару', 'Назара', 'Назаром', 'Назарові']
    },
    'Марта': {
        'gender': 'femn',
        'variants': ['Марфа'],
        'diminutives': ['Марточка', 'Мартуся', 'Мартуня'],
        'transliterations': ['Marta', 'Martha'],
        'declensions': ['Марти', 'Марті', 'Марту', 'Мартою', 'Марті']
    },
    'Остап': {
        'gender': 'masc',
        'variants': ['Евстафий'],
        'diminutives': ['Остапко', 'Остапчик', 'Стапко'],
        'transliterations': ['Ostap', 'Yevstafiy'],
        'declensions': ['Остапа', 'Остапові', 'Остапа', 'Остапом', 'Остапові']
    },
    'Григорій': {
        'gender': 'masc',
        'variants': ['Григорий'],
        'diminutives': ['Гриць', 'Грицько', 'Гриша', 'Григорко'],
        'transliterations': ['Hryhorii', 'Hryhoriy', 'Grigory'],
        'declensions': ['Григорія', 'Григорію', 'Григорія', 'Григорієм', 'Григорії']
    },
    'В\'ячеслав': {
        'gender': 'masc',
        'variants': ['Вячеслав'],
        'diminutives': ['Слава', 'Славко', 'В\'ячик'],
        'transliterations': ['Viacheslav', 'Vyacheslav'],
        'declensions': ["В'ячеслава", "В'ячеславу", "В'ячеслава", "В'ячеславом", "В'ячеславові"]
    },
    'Станіслав': {
        'gender': 'masc',
        'variants': ['Станислав'],
        'diminutives': ['Стас', 'Стасик', 'Славко'],
        'transliterations': ['Stanislav', 'Stanislaw'],
        'declensions': ['Станіслава', 'Станіславу', 'Станіслава', 'Станіславом', 'Станіславові']
    },
    'Владислав': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Влад', 'Владик', 'Славко'],
        'transliterations': ['Vladyslav', 'Vladislav'],
        'declensions': ['Владислава', 'Владиславу', 'Владислава', 'Владиславом', 'Владиславові']
    },
    'Данило': {
        'gender': 'masc',
        'variants': ['Даниил', 'Даниїл'],
        'diminutives': ['Данилко', 'Даня', 'Данись'],
        'transliterations': ['Danylo', 'Daniil', 'Daniel'],
        'declensions': ['Данила', 'Данилу', 'Данила', 'Данилом', 'Данилові']
    },
    'Пилип': {
        'gender': 'masc',
        'variants': ['Филипп'],
        'diminutives': ['Пилипко', 'Пилипонько', 'Філя'],
        'transliterations': ['Pylyp', 'Philip'],
        'declensions': ['Пилипа', 'Пилипу', 'Пилипа', 'Пилипом', 'Пилипові']
    },
    'Федір': {
        'gender': 'masc',
        'variants': ['Фёдор', 'Теодор'],
        'diminutives': ['Федько', 'Федя', 'Федорко'],
        'transliterations': ['Fedir', 'Fyodor', 'Theodore'],
        'declensions': ['Федора', 'Федору', 'Федора', 'Федором', 'Федорові']
    },
    'Гнат': {
        'gender': 'masc',
        'variants': ['Игнат', 'Ігнат'],
        'diminutives': ['Гнатик', 'Ігнатко'],
        'transliterations': ['Hnat', 'Ignat'],
        'declensions': ['Гната', 'Гнатові', 'Гната', 'Гнатом', 'Гнатові']
    },
    'Маргарита': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Рита', 'Марго', 'Риточка', 'Маргаритка'],
        'transliterations': ['Marharyta', 'Margarita'],
        'declensions': ['Маргарити', 'Маргариті', 'Маргариту', 'Маргаритою', 'Маргариті']
    },
    'Вероніка': {
        'gender': 'femn',
        'variants': ['Вероника'],
        'diminutives': ['Ніка', 'Веронічка', 'Рона'],
        'transliterations': ['Veronika', 'Veronica'],
        'declensions': ['Вероніки', 'Вероніці', 'Вероніку', 'Веронікою', 'Вероніці']
    },
    'Ангеліна': {
        'gender': 'femn',
        'variants': ['Ангелина'],
        'diminutives': ['Ангелінка', 'Ліна', 'Геля'],
        'transliterations': ['Anhelina', 'Angelina'],
        'declensions': ['Ангеліни', 'Ангеліні', 'Ангеліну', 'Ангеліною', 'Ангеліні']
    },
    'Іванна': {
        'gender': 'femn',
        'variants': ['Жанна'],
        'diminutives': ['Іванка', 'Яна', 'Івася'],
        'transliterations': ['Ivanna', 'Joanna'],
        'declensions': ['Іванни', 'Іванні', 'Іванну', 'Іванною', 'Іванні']
    },
    'Богдана': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Дана', 'Богданка', 'Богдася'],
        'transliterations': ['Bohdana', 'Bogdana'],
        'declensions': ['Богдани', 'Богдані', 'Богдану', 'Богданою', 'Богдані']
    },
    'Яна': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Яночка', 'Януся', 'Яся'],
        'transliterations': ['Yana', 'Jana'],
        'declensions': ['Яни', 'Яні', 'Яну', 'Яною', 'Яні']
    },
    'Діана': {
        'gender': 'femn',
        'variants': ['Диана'],
        'diminutives': ['Діанка', 'Ді', 'Діночка'],
        'transliterations': ['Diana'],
        'declensions': ['Діани', 'Діані', 'Діану', 'Діаною', 'Діані']
    },
    'Мирослава': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Мирося', 'Слава', 'Мира'],
        'transliterations': ['Myroslava', 'Miroslava'],
        'declensions': ['Мирослави', 'Мирославі', 'Мирославу', 'Мирославою', 'Мирославі']
    },
    'Олеся': {
        'gender': 'femn',
        'variants': ['Александра', 'Лариса'],
        'diminutives': ['Леся', 'Лесюня', 'Олеська'],
        'transliterations': ['Olesia', 'Olesya', 'Lesia'],
        'declensions': ['Олесі', 'Олесі', 'Олесю', 'Олесею', 'Олесі']
    },
    'Лариса': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Лора', 'Лариска', 'Лара'],
        'transliterations': ['Larysa', 'Larisa'],
        'declensions': ['Лариси', 'Ларисі', 'Ларису', 'Ларисою', 'Ларисі']
    },
    'Раїса': {
        'gender': 'femn',
        'variants': ['Раиса'],
        'diminutives': ['Рая', 'Раєчка', 'Раїска'],
        'transliterations': ['Raisa', 'Raya'],
        'declensions': ['Раїси', 'Раїсі', 'Раїсу', 'Раїсою', 'Раїсі']
    },
    'Клавдія': {
        'gender': 'femn',
        'variants': ['Клавдия'],
        'diminutives': ['Клава', 'Клавдочка', 'Клавуня'],
        'transliterations': ['Klavdiia', 'Klaudia', 'Claudia'],
        'declensions': ['Клавдії', 'Клавдії', 'Клавдію', 'Клавдією', 'Клавдії']
    },
    'Микола': {
        'gender': 'masc',
        'variants': ['Николай', 'Миколай'],
        'diminutives': ['Миколка', 'Коля', 'Колько', 'Миколайчик'],
        'transliterations': ['Mykola', 'Nikolai'],
        'declensions': ['Миколи', 'Миколі', 'Миколу', 'Миколою', 'Миколі']
    },
    'Степан': {
        'gender': 'masc',
        'variants': ['Стефан'],
        'diminutives': ['Стьопа', 'Степанко', 'Стефко', 'Степась'],
        'transliterations': ['Stepan', 'Stefan', 'Stephen'],
        'declensions': ['Степана', 'Степану', 'Степана', 'Степаном', 'Степанові']
    },
    'Денис': {
        'gender': 'masc',
        'variants': ['Дионисий'],
        'diminutives': ['Дениско', 'Денисик', 'Ден'],
        'transliterations': ['Denys', 'Denis'],
        'declensions': ['Дениса', 'Денису', 'Дениса', 'Денисом', 'Денисові']
    },
    'Олег': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Олежик', 'Олежко', 'Олесь', 'Лесь'],
        'transliterations': ['Oleh', 'Oleg'],
        'declensions': ['Олега', 'Олегу', 'Олега', 'Олегом', 'Олегові']
    },
    'Антон': {
        'gender': 'masc',
        'variants': ['Антоній'],
        'diminutives': ['Антось', 'Тоша', 'Антонко', 'Антошка'],
        'transliterations': ['Anton', 'Antin'],
        'declensions': ['Антона', 'Антону', 'Антона', 'Антоном', 'Антонові']
    },
    'Кирило': {
        'gender': 'masc',
        'variants': ['Кирилл'],
        'diminutives': ['Кирилко', 'Кирик', 'Киря'],
        'transliterations': ['Kyrylo', 'Kirill', 'Cyril'],
        'declensions': ['Кирила', 'Кирилу', 'Кирила', 'Кирилом', 'Кирилові']
    },
    'Ростислав': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Ростик', 'Слава', 'Ростиславко'],
        'transliterations': ['Rostyslav', 'Rostislav'],
        'declensions': ['Ростислава', 'Ростиславу', 'Ростислава', 'Ростиславом', 'Ростиславові']
    },
    'Лев': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Левко', 'Левчик', 'Льова'],
        'transliterations': ['Lev', 'Leo'],
        'declensions': ['Льва', 'Львові', 'Льва', 'Львом', 'Львові']
    },
    'Захар': {
        'gender': 'masc',
        'variants': ['Захарій'],
        'diminutives': ['Захарко', 'Захарчик'],
        'transliterations': ['Zakhar', 'Zachary'],
        'declensions': ['Захара', 'Захару', 'Захара', 'Захаром', 'Захарові']
    },
    'Арсен': {
        'gender': 'masc',
        'variants': ['Арсеній'],
        'diminutives': ['Арсенко', 'Арсеник', 'Сеня'],
        'transliterations': ['Arsen', 'Arseniy'],
        'declensions': ['Арсена', 'Арсену', 'Арсена', 'Арсеном', 'Арсенові']
    },
    'Віра': {
        'gender': 'femn',
        'variants': ['Вера'],
        'diminutives': ['Вірочка', 'Віруня', 'Віруся'],
        'transliterations': ['Vira', 'Vera'],
        'declensions': ['Віри', 'Вірі', 'Віру', 'Вірою', 'Вірі']
    },
    'Надія': {
        'gender': 'femn',
        'variants': ['Надежда'],
        'diminutives': ['Надійка', 'Надя', 'Надієнька'],
        'transliterations': ['Nadiia', 'Nadiya', 'Nadezhda'],
        'declensions': ['Надії', 'Надії', 'Надію', 'Надією', 'Надії']
    },
    'Любов': {
        'gender': 'femn',
        'variants': ['Любовь'],
        'diminutives': ['Люба', 'Любочка', 'Любася', 'Любуня'],
        'transliterations': ['Liubov', 'Lyubov', 'Ljubov'],
        'declensions': ['Любові', 'Любові', 'Любов', 'Любов\'ю', 'Любові']
    },
    'Поліна': {
        'gender': 'femn',
        'variants': ['Аполлінарія'],
        'diminutives': ['Поля', 'Полінка', 'Полюся'],
        'transliterations': ['Polina', 'Pauline'],
        'declensions': ['Поліни', 'Поліні', 'Поліну', 'Поліною', 'Поліні']
    },
    'Аліна': {
        'gender': 'femn',
        'variants': ['Алина'],
        'diminutives': ['Алінка', 'Аля', 'Ліна'],
        'transliterations': ['Alina'],
        'declensions': ['Аліни', 'Аліні', 'Аліну', 'Аліною', 'Аліні']
    },
    'Злата': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Златка', 'Златочка', 'Златуся'],
        'transliterations': ['Zlata'],
        'declensions': ['Злати', 'Златі', 'Злату', 'Златою', 'Златі']
    },
    'Соломія': {
        'gender': 'femn',
        'variants': ['Саломея'],
        'diminutives': ['Соломійка', 'Соля', 'Мія'],
        'transliterations': ['Solomiia', 'Solomiya', 'Salome'],
        'declensions': ['Соломії', 'Соломії', 'Соломію', 'Соломією', 'Соломії']
    },
    'Мар\'яна': {
        'gender': 'femn',
        'variants': ['Маріанна'],
        'diminutives': ['Мар\'янка', 'Яна', 'Маря'],
        'transliterations': ['Mariana', 'Maryana', 'Marianna'],
        'declensions': ["Мар'яни", "Мар'яні", "Мар'яну", "Мар'яною", "Мар'яні"]
    },
    'Лілія': {
        'gender': 'femn',
        'variants': ['Лилия'],
        'diminutives': ['Ліля', 'Лілічка', 'Лілюся'],
        'transliterations': ['Liliia', 'Liliya', 'Lilia'],
        'declensions': ['Лілії', 'Лілії', 'Лілію', 'Лілією', 'Лілії']
    },
    'Тимофій': {
        'gender': 'masc',
        'variants': ['Тимофей'],
        'diminutives': ['Тиміш', 'Тимко', 'Тимофійко'],
        'transliterations': ['Tymofii', 'Tymofiy', 'Timothy'],
        'declensions': ['Тимофія', 'Тимофію', 'Тимофія', 'Тимофієм', 'Тимофієві']
    },
    'Леонід': {
        'gender': 'masc',
        'variants': ['Леонид'],
        'diminutives': ['Льоня', 'Леонідик', 'Лесь'],
        'transliterations': ['Leonid'],
        'declensions': ['Леоніда', 'Леоніду', 'Леоніда', 'Леонідом', 'Леонідові']
    },
    'Сава': {
        'gender': 'masc',
        'variants': ['Савва'],
        'diminutives': ['Савко', 'Савка', 'Савочка'],
        'transliterations': ['Sava', 'Savva'],
        'declensions': ['Сави', 'Саві', 'Саву', 'Савою', 'Саві']
    },
    'Семен': {
        'gender': 'masc',
        'variants': ['Семён', 'Симон'],
        'diminutives': ['Сенько', 'Сеня', 'Семенко'],
        'transliterations': ['Semen', 'Semyon', 'Simon'],
        'declensions': ['Семена', 'Семену', 'Семена', 'Семеном', 'Семенові']
    },
    'Тимур': {
        'gender': 'masc',
        'variants': ['Тамерлан'],
        'diminutives': ['Тимурко', 'Тимко', 'Тима'],
        'transliterations': ['Tymur', 'Timur'],
        'declensions': ['Тимура', 'Тимуру', 'Тимура', 'Тимуром', 'Тимурові']
    },
    'Едуард': {
        'gender': 'masc',
        'variants': ['Эдуард'],
        'diminutives': ['Едик', 'Едя', 'Едуардик'],
        'transliterations': ['Eduard', 'Edward'],
        'declensions': ['Едуарда', 'Едуарду', 'Едуарда', 'Едуардом', 'Едуардові']
    },
    'Артур': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Артурчик', 'Артурик', 'Турик'],
        'transliterations': ['Artur', 'Arthur'],
        'declensions': ['Артура', 'Артуру', 'Артура', 'Артуром', 'Артурові']
    },
    'Вадим': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Вадимко', 'Вадик', 'Вадя'],
        'transliterations': ['Vadym', 'Vadim'],
        'declensions': ['Вадима', 'Вадиму', 'Вадима', 'Вадимом', 'Вадимові']
    },
    'Гліб': {
        'gender': 'masc',
        'variants': ['Глеб'],
        'diminutives': ['Глібко', 'Глібчик'],
        'transliterations': ['Hlib', 'Gleb'],
        'declensions': ['Гліба', 'Глібу', 'Гліба', 'Глібом', 'Глібові']
    },
    'Макар': {
        'gender': 'masc',
        'variants': ['Макарій'],
        'diminutives': ['Макарик', 'Макарко'],
        'transliterations': ['Makar', 'Makariy'],
        'declensions': ['Макара', 'Макару', 'Макара', 'Макаром', 'Макарові']
    },
    'Зіновій': {
        'gender': 'masc',
        'variants': ['Зиновий'],
        'diminutives': ['Зінько', 'Зеник', 'Зіновко'],
        'transliterations': ['Zinovii', 'Zinoviy'],
        'declensions': ['Зіновія', 'Зіновію', 'Зіновія', 'Зіновієм', 'Зіновієві']
    },
    'Зоряна': {
        'gender': 'femn',
        'variants': ['Зорина'],
        'diminutives': ['Зорянка', 'Зоря', 'Зіронька'],
        'transliterations': ['Zoriana', 'Zoryana'],
        'declensions': ['Зоряни', 'Зоряні', 'Зоряну', 'Зоряною', 'Зоряні']
    },
    'Руслана': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Руся', 'Лана', 'Русланка'],
        'transliterations': ['Ruslana'],
        'declensions': ['Руслани', 'Руслані', 'Руслану', 'Русланою', 'Руслані']
    },
    'Еліна': {
        'gender': 'femn',
        'variants': ['Элина'],
        'diminutives': ['Еля', 'Елінка', 'Ліна'],
        'transliterations': ['Elina'],
        'declensions': ['Еліни', 'Еліні', 'Еліну', 'Еліною', 'Еліні']
    },
    'Таміла': {
        'gender': 'femn',
        'variants': ['Тамила'],
        'diminutives': ['Тома', 'Міла', 'Тамілка'],
        'transliterations': ['Tamila'],
        'declensions': ['Таміли', 'Тамілі', 'Тамілу', 'Тамілою', 'Тамілі']
    },
    'Емілія': {
        'gender': 'femn',
        'variants': ['Эмилия'],
        'diminutives': ['Емма', 'Емілька', 'Міла'],
        'transliterations': ['Emiliia', 'Emilia', 'Emily'],
        'declensions': ['Емілії', 'Емілії', 'Емілію', 'Емілією', 'Емілії']
    },
    'Алла': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Алка', 'Аллочка', 'Алюся'],
        'transliterations': ['Alla'],
        'declensions': ['Алли', 'Аллі', 'Аллу', 'Аллою', 'Аллі']
    },
    'Регіна': {
        'gender': 'femn',
        'variants': ['Регина'],
        'diminutives': ['Регінка', 'Ріна'],
        'transliterations': ['Rehina', 'Regina'],
        'declensions': ['Регіни', 'Регіні', 'Регіну', 'Регіною', 'Регіні']
    },
    'Олесь': {
        'gender': 'masc',
        'variants': ['Олександр'],
        'diminutives': ['Лесь', 'Олесько', 'Олесик'],
        'transliterations': ['Oles'],
        'declensions': ['Олеся', 'Олесю', 'Олеся', 'Олесем', 'Олесеві']
    },
    'Ксенія': {
        'gender': 'femn',
        'variants': ['Оксана', 'Аксинья'],
        'diminutives': ['Ксеня', 'Ксюша', 'Ксенійка'],
        'transliterations': ['Kseniia', 'Kseniya'],
        'declensions': ['Ксенії', 'Ксенії', 'Ксенію', 'Ксенією', 'Ксенії']
    },
    'Таїсія': {
        'gender': 'femn',
        'variants': ['Таисия'],
        'diminutives': ['Тая', 'Тася', 'Таїсочка'],
        'transliterations': ['Taisiia', 'Taisiya'],
        'declensions': ['Таїсії', 'Таїсії', 'Таїсію', 'Таїсією', 'Таїсії']
    },
    'Давид': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Давидко', 'Давидик', 'Даня'],
        'transliterations': ['Davyd', 'David'],
        'declensions': ['Давида', 'Давиду', 'Давида', 'Давидом', 'Давидові']
    },
    'Марк': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Марко', 'Марчик', 'Маркусь'],
        'transliterations': ['Mark', 'Marko'],
        'declensions': ['Марка', 'Марку', 'Марка', 'Марком', 'Маркові']
    },
    'Святослав': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Святик', 'Славко', 'Слава'],
        'transliterations': ['Sviatoslav', 'Svyatoslav'],
        'declensions': ['Святослава', 'Святославу', 'Святослава', 'Святославом', 'Святославові']
    },
    'Любомир': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Любко', 'Любомирко', 'Мирко'],
        'transliterations': ['Liubomyr', 'Lyubomyr'],
        'declensions': ['Любомира', 'Любомиру', 'Любомира', 'Любомиром', 'Любомирові']
    },
    'Мирон': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Миронко', 'Мирось', 'Мирко'],
        'transliterations': ['Myron', 'Miron'],
        'declensions': ['Мирона', 'Мирону', 'Мирона', 'Мироном', 'Миронові']
    },
    'Панас': {
        'gender': 'masc',
        'variants': ['Афанасий'],
        'diminutives': ['Панаско', 'Панасик', 'Опанас'],
        'transliterations': ['Panas', 'Afanasiy'],
        'declensions': ['Панаса', 'Панасу', 'Панаса', 'Панасом', 'Панасові']
    },
    'Устим': {
        'gender': 'masc',
        'variants': ['Иустин'],
        'diminutives': ['Устимко', 'Устимчик'],
        'transliterations': ['Ustym', 'Justin'],
        'declensions': ['Устима', 'Устиму', 'Устима', 'Устимом', 'Устимові']
    },
    'Трохим': {
        'gender': 'masc',
        'variants': ['Трофим'],
        'diminutives': ['Трохимко', 'Троша'],
        'transliterations': ['Trokhym', 'Trofim'],
        'declensions': ['Трохима', 'Трохиму', 'Трохима', 'Трохимом', 'Трохимові']
    },
    'Орест': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Орестко', 'Орко'],
        'transliterations': ['Orest'],
        'declensions': ['Ореста', 'Оресту', 'Ореста', 'Орестом', 'Орестові']
    },
    'Наум': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Наумко', 'Наумчик'],
        'transliterations': ['Naum'],
        'declensions': ['Наума', 'Науму', 'Наума', 'Наумом', 'Наумові']
    },
    'Уляна': {
        'gender': 'femn',
        'variants': ['Юлиана', 'Іуліанія'],
        'diminutives': ['Улянка', 'Уля', 'Ляна', 'Уляся'],
        'transliterations': ['Uliana', 'Yuliana', 'Juliana'],
        'declensions': ['Уляни', 'Уляні', 'Уляну', 'Уляною', 'Уляні']
    },
    'Мілана': {
        'gender': 'femn',
        'variants': ['Милана'],
        'diminutives': ['Міланка', 'Лана', 'Міла'],
        'transliterations': ['Milana'],
        'declensions': ['Мілани', 'Мілані', 'Мілану', 'Міланою', 'Мілані']
    },
    'Єва': {
        'gender': 'femn',
        'variants': ['Ева'],
        'diminutives': ['Євочка', 'Євуся'],
        'transliterations': ['Yeva', 'Eva', 'Eve'],
        'declensions': ['Єви', 'Єві', 'Єву', 'Євою', 'Єві']
    },
    'Ніна': {
        'gender': 'femn',
        'variants': ['Нина'],
        'diminutives': ['Ніночка', 'Нінуся'],
        'transliterations': ['Nina'],
        'declensions': ['Ніни', 'Ніні', 'Ніну', 'Ніною', 'Ніні']
    },
    'Кіра': {
        'gender': 'femn',
        'variants': ['Кира'],
        'diminutives': ['Кірочка', 'Кіруся'],
        'transliterations': ['Kira'],
        'declensions': ['Кіри', 'Кірі', 'Кіру', 'Кірою', 'Кірі']
    },
    'Ярина': {
        'gender': 'femn',
        'variants': ['Ирина'],
        'diminutives': ['Яриночка', 'Яринка', 'Яруся'],
        'transliterations': ['Yaryna', 'Iryna'],
        'declensions': ['Ярини', 'Ярині', 'Ярину', 'Яриною', 'Ярині']
    },
    'Стефанія': {
        'gender': 'femn',
        'variants': ['Стефания'],
        'diminutives': ['Стефа', 'Стефка', 'Фаня'],
        'transliterations': ['Stefaniia', 'Stefania', 'Stephanie'],
        'declensions': ['Стефанії', 'Стефанії', 'Стефанію', 'Стефанією', 'Стефанії']
    },
    'Меланія': {
        'gender': 'femn',
        'variants': ['Мелания', 'Маланка'],
        'diminutives': ['Меланка', 'Міла', 'Ланя'],
        'transliterations': ['Melaniia', 'Melania'],
        'declensions': ['Меланії', 'Меланії', 'Меланію', 'Меланією', 'Меланії']
    },
    'Роксолана': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Роксоланка', 'Рокса', 'Лана', 'Рося'],
        'transliterations': ['Roksolana', 'Roxolana'],
        'declensions': ['Роксолани', 'Роксолані', 'Роксолану', 'Роксоланою', 'Роксолані']
    },
    'Мотря': {
        'gender': 'femn',
        'variants': ['Мотрона'],
        'diminutives': ['Мотренька', 'Мотруся'],
        'transliterations': ['Motria', 'Motrona'],
        'declensions': ['Мотрі', 'Мотрі', 'Мотрю', 'Мотрею', 'Мотрі']
    },
    'Валентин': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Валя', 'Валентинко', 'Валік'],
        'transliterations': ['Valentyn', 'Valentin'],
        'declensions': ['Валентина', 'Валентину', 'Валентина', 'Валентином', 'Валентинові']
    },
    'Віталій': {
        'gender': 'masc',
        'variants': ['Виталий'],
        'diminutives': ['Віталик', 'Віталько', 'Віта'],
        'transliterations': ['Vitalii', 'Vitaliy'],
        'declensions': ['Віталія', 'Віталію', 'Віталія', 'Віталієм', 'Віталієві']
    },
    'Костянтин': {
        'gender': 'masc',
        'variants': ['Константин'],
        'diminutives': ['Костя', 'Костик', 'Костянтинко'],
        'transliterations': ['Kostiantyn', 'Konstantin'],
        'declensions': ['Костянтина', 'Костянтину', 'Костянтина', 'Костянтином', 'Костянтинові']
    },
    'Анатолій': {
        'gender': 'masc',
        'variants': ['Анатолий'],
        'diminutives': ['Толя', 'Толик', 'Анатолько'],
        'transliterations': ['Anatolii', 'Anatoliy'],
        'declensions': ['Анатолія', 'Анатолію', 'Анатолія', 'Анатолієм', 'Анатолієві']
    },
    'Валерій': {
        'gender': 'masc',
        'variants': ['Валерий'],
        'diminutives': ['Валера', 'Валерко', 'Лера'],
        'transliterations': ['Valerii', 'Valeriy'],
        'declensions': ['Валерія', 'Валерію', 'Валерія', 'Валерієм', 'Валерієві']
    },
    'Геннадій': {
        'gender': 'masc',
        'variants': ['Геннадий'],
        'diminutives': ['Гена', 'Геннадько', 'Генадик'],
        'transliterations': ['Hennadii', 'Gennadiy'],
        'declensions': ['Геннадія', 'Геннадію', 'Геннадія', 'Геннадієм', 'Геннадієві']
    },
    'Миколай': {
        'gender': 'masc',
        'variants': ['Николай'],
        'diminutives': ['Миколайко', 'Коля', 'Миколайчик'],
        'transliterations': ['Mykolay', 'Nikolay'],
        'declensions': ['Миколая', 'Миколаю', 'Миколая', 'Миколаєм', 'Миколаєві']
    },
    'Руслан': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Русланко', 'Русик', 'Рус'],
        'transliterations': ['Ruslan'],
        'declensions': ['Руслана', 'Русланові', 'Руслана', 'Русланом', 'Русланові']
    },
    'Іллія': {
        'gender': 'masc',
        'variants': ['Илья'],
        'diminutives': ['Ілля', 'Ілліко', 'Іллюша'],
        'transliterations': ['Illia', 'Illya'],
        'declensions': ['Іллі', 'Іллі', 'Іллю', 'Іллею', 'Іллі']
    },
    'Назарій': {
        'gender': 'masc',
        'variants': ['Назарий'],
        'diminutives': ['Назарко', 'Назарчик', 'Зарко'],
        'transliterations': ['Nazarii', 'Nazariy'],
        'declensions': ['Назарія', 'Назарію', 'Назарія', 'Назарієм', 'Назарієві']
    },
    'Ганна': {
        'gender': 'femn',
        'variants': ['Анна'],
        'diminutives': ['Аня', 'Ганя', 'Ганнуся', 'Анечка'],
        'transliterations': ['Hanna', 'Anna'],
        'declensions': ['Ганни', 'Ганні', 'Ганну', 'Ганною', 'Ганні']
    },
    'Галина': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Галя', 'Галинка', 'Галочка'],
        'transliterations': ['Halyna', 'Galina'],
        'declensions': ['Галини', 'Галині', 'Галину', 'Галиною', 'Галині']
    },
    'Лідія': {
        'gender': 'femn',
        'variants': ['Лидия'],
        'diminutives': ['Ліда', 'Лідочка', 'Лідуся'],
        'transliterations': ['Lidiia', 'Lidiya'],
        'declensions': ['Лідії', 'Лідії', 'Лідію', 'Лідією', 'Лідії']
    },
    'Зоя': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Зоїнка', 'Зоїчка'],
        'transliterations': ['Zoia', 'Zoya'],
        'declensions': ['Зої', 'Зої', 'Зою', 'Зоєю', 'Зої']
    },
    'Тамара': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Тома', 'Томочка', 'Тамарочка'],
        'transliterations': ['Tamara'],
        'declensions': ['Тамари', 'Тамарі', 'Тамару', 'Тамарою', 'Тамарі']
    },
    'Римма': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Риммочка', 'Римка'],
        'transliterations': ['Rymma', 'Rimma'],
        'declensions': ['Римми', 'Риммі', 'Римму', 'Риммою', 'Риммі']
    },
    'Інна': {
        'gender': 'femn',
        'variants': ['Инна'],
        'diminutives': ['Інночка', 'Іннуся'],
        'transliterations': ['Inna'],
        'declensions': ['Інни', 'Інні', 'Інну', 'Інною', 'Інні']
    },
    'Жанна': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Жанночка', 'Жанка'],
        'transliterations': ['Zhanna'],
        'declensions': ['Жанни', 'Жанні', 'Жанну', 'Жанною', 'Жанні']
    },
    'Альона': {
        'gender': 'femn',
        'variants': ['Алёна', 'Олена'],
        'diminutives': ['Альонка', 'Льона', 'Альонушка'],
        'transliterations': ['Aliona', 'Alyona'],
        'declensions': ['Альони', 'Альоні', 'Альону', 'Альоною', 'Альоні']
    },
    'Марина': {
        'gender': 'femn',
        'variants': [],
        'diminutives': ['Маринка', 'Мариша', 'Марочка'],
        'transliterations': ['Maryna', 'Marina'],
        'declensions': ['Марини', 'Марині', 'Марину', 'Мариною', 'Марині']
    },
    
    # Додаткові чоловічі імена
    'Богдан': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Богдасик', 'Богданко', 'Богданчик'],
        'transliterations': ['Bohdan', 'Bogdan'],
        'declensions': ['Богдана', 'Богданові', 'Богдана', 'Богданом', 'Богданові']
    },
    'Тарас': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Тарасик', 'Тараско', 'Тарасчик'],
        'transliterations': ['Taras'],
        'declensions': ['Тараса', 'Тарасові', 'Тараса', 'Тарасом', 'Тарасові']
    },
    'Роман': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Рома', 'Ромчик', 'Ромко'],
        'transliterations': ['Roman'],
        'declensions': ['Романа', 'Романові', 'Романа', 'Романом', 'Романові']
    },
    'Віктор': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Вітя', 'Вітко', 'Вікторчик'],
        'transliterations': ['Viktor', 'Victor'],
        'declensions': ['Віктора', 'Вікторові', 'Віктора', 'Віктором', 'Вікторові']
    },
    'Олег': {
        'gender': 'masc',
        'variants': [],
        'diminutives': ['Олежко', 'Олесик', 'Олегчик'],
        'transliterations': ['Oleh', 'Oleg'],
        'declensions': ['Олега', 'Олегові', 'Олега', 'Олегом', 'Олегові']
    },
    
    # Додаткові жіночі імена
    'Вікторія': {
        'gender': 'femn',
        'variants': ['Вікторія'],
        'diminutives': ['Віка', 'Вікторійка', 'Вікторійко'],
        'transliterations': ['Viktoriia', 'Viktoriya', 'Victoria'],
        'declensions': ['Вікторії', 'Вікторії', 'Вікторію', 'Вікторією', 'Вікторії']
    },
    'Катерина': {
        'gender': 'femn',
        'variants': ['Катерина'],
        'diminutives': ['Катя', 'Катруся', 'Катеринка'],
        'transliterations': ['Kateryna', 'Katerina', 'Katherine'],
        'declensions': ['Катерини', 'Катерині', 'Катерину', 'Катериною', 'Катерині']
    },
    'Юлія': {
        'gender': 'femn',
        'variants': ['Юлія'],
        'diminutives': ['Юля', 'Юлечка', 'Юлійка'],
        'transliterations': ['Yuliia', 'Yuliya', 'Julia'],
        'declensions': ['Юлії', 'Юлії', 'Юлію', 'Юлією', 'Юлії']
    },
    'Анастасія': {
        'gender': 'femn',
        'variants': ['Анастасія'],
        'diminutives': ['Настя', 'Настенька', 'Настюша'],
        'transliterations': ['Anastasiia', 'Anastasiya', 'Anastasia'],
        'declensions': ['Анастасії', 'Анастасії', 'Анастасію', 'Анастасією', 'Анастасії']
    },
    'Світлана': {
        'gender': 'femn',
        'variants': ['Світлана'],
        'diminutives': ['Світа', 'Світланка', 'Світланочка'],
        'transliterations': ['Svitlana', 'Svetlana'],
        'declensions': ['Світлани', 'Світлані', 'Світлану', 'Світланою', 'Світлані']
    },
    
    # Додаткові сучасні українські імена
    'Максим': {
        'gender': 'masc',
        'variants': ['Максим', 'Макс', 'Максим'],
        'diminutives': ['Максим', 'Макс', 'Максим'],
        'transliterations': ['Maksym', 'Max', 'Maksym'],
        'declensions': ['Максима', 'Максиму', 'Максима', 'Максимом', 'Максимі']
    },
    'Анна': {
        'gender': 'femn',
        'variants': ['Анна', 'Анна', 'Анна'],
        'diminutives': ['Анна', 'Анна', 'Анна'],
        'transliterations': ['Anna', 'Anna', 'Anna'],
        'declensions': ['Анни', 'Анні', 'Анну', 'Анною', 'Анні']
    },
    'Денис': {
        'gender': 'masc',
        'variants': ['Денис', 'Ден', 'Денис'],
        'diminutives': ['Денис', 'Ден', 'Денис'],
        'transliterations': ['Denys', 'Den', 'Denys'],
        'declensions': ['Дениса', 'Денису', 'Дениса', 'Денисом', 'Денисі']
    },
    'Марія': {
        'gender': 'femn',
        'variants': ['Марія', 'Марія', 'Марія'],
        'diminutives': ['Марія', 'Марія', 'Марія'],
        'transliterations': ['Mariia', 'Mariia', 'Mariia'],
        'declensions': ['Марії', 'Марії', 'Марію', 'Марією', 'Марії']
    },
    'Артем': {
        'gender': 'masc',
        'variants': ['Артем', 'Артем', 'Артем'],
        'diminutives': ['Артем', 'Артем', 'Артем'],
        'transliterations': ['Artem', 'Artem', 'Artem'],
        'declensions': ['Артема', 'Артему', 'Артема', 'Артемом', 'Артемі']
    },
    'Поліна': {
        'gender': 'femn',
        'variants': ['Поліна', 'Поліна', 'Поліна'],
        'diminutives': ['Поліна', 'Поліна', 'Поліна'],
        'transliterations': ['Polina', 'Polina', 'Polina'],
        'declensions': ['Поліни', 'Поліні', 'Поліну', 'Поліною', 'Поліні']
    },
    'Ілля': {
        'gender': 'masc',
        'variants': ['Ілля', 'Ілля', 'Ілля'],
        'diminutives': ['Ілля', 'Ілля', 'Ілля'],
        'transliterations': ['Illia', 'Illia', 'Illia'],
        'declensions': ['Іллі', 'Іллі', 'Іллю', 'Іллею', 'Іллі']
    },
    'Валерія': {
        'gender': 'femn',
        'variants': ['Валерія', 'Валерія', 'Валерія'],
        'diminutives': ['Валерія', 'Валерія', 'Валерія'],
        'transliterations': ['Valeriia', 'Valeriia', 'Valeriia'],
        'declensions': ['Валерії', 'Валерії', 'Валерію', 'Валерією', 'Валерії']
    },
    'Кирило': {
        'gender': 'masc',
        'variants': ['Кирило', 'Кирило', 'Кирило'],
        'diminutives': ['Кирило', 'Кирило', 'Кирило'],
        'transliterations': ['Kyrylo', 'Kyrylo', 'Kyrylo'],
        'declensions': ['Кирила', 'Кирилу', 'Кирила', 'Кирилом', 'Кирилі']
    },
    'Аліна': {
        'gender': 'femn',
        'variants': ['Аліна', 'Аліна', 'Аліна'],
        'diminutives': ['Аліна', 'Аліна', 'Аліна'],
        'transliterations': ['Alina', 'Alina', 'Alina'],
        'declensions': ['Аліни', 'Аліні', 'Аліну', 'Аліною', 'Аліні']
    },
    
    # Additional modern Ukrainian names
    'Арсен': {
        'gender': 'masc',
        'variants': ['Арсен', 'Арсен', 'Арсен'],
        'diminutives': ['Арсен', 'Арсен', 'Арсен'],
        'transliterations': ['Arsen', 'Arsen', 'Arsen'],
        'declensions': ['Арсена', 'Арсену', 'Арсена', 'Арсеном', 'Арсені']
    },
    'Богдан': {
        'gender': 'masc',
        'variants': ['Богдан', 'Богдан', 'Богдан'],
        'diminutives': ['Богдан', 'Богдан', 'Богдан'],
        'transliterations': ['Bohdan', 'Bogdan', 'Bohdan'],
        'declensions': ['Богдана', 'Богдану', 'Богдана', 'Богданом', 'Богдані']
    },
    'Валерія': {
        'gender': 'femn',
        'variants': ['Валерія', 'Валерія', 'Валерія'],
        'diminutives': ['Валерія', 'Валерія', 'Валерія'],
        'transliterations': ['Valeriia', 'Valeriia', 'Valeriia'],
        'declensions': ['Валерії', 'Валерії', 'Валерію', 'Валерією', 'Валерії']
    },
    'Гліб': {
        'gender': 'masc',
        'variants': ['Гліб', 'Гліб', 'Гліб'],
        'diminutives': ['Гліб', 'Гліб', 'Гліб'],
        'transliterations': ['Hlib', 'Glib', 'Hlib'],
        'declensions': ['Гліба', 'Глібу', 'Гліба', 'Глібом', 'Глібі']
    },
    'Діана': {
        'gender': 'femn',
        'variants': ['Діана', 'Діана', 'Діана'],
        'diminutives': ['Діана', 'Діана', 'Діана'],
        'transliterations': ['Diana', 'Diana', 'Diana'],
        'declensions': ['Діани', 'Діані', 'Діану', 'Діаною', 'Діані']
    },
    'Єгор': {
        'gender': 'masc',
        'variants': ['Єгор', 'Єгор', 'Єгор'],
        'diminutives': ['Єгор', 'Єгор', 'Єгор'],
        'transliterations': ['Yehor', 'Egor', 'Yehor'],
        'declensions': ['Єгора', 'Єгору', 'Єгора', 'Єгором', 'Єгорі']
    },
    'Єлизавета': {
        'gender': 'femn',
        'variants': ['Єлизавета', 'Єлизавета', 'Єлизавета'],
        'diminutives': ['Єлизавета', 'Єлизавета', 'Єлизавета'],
        'transliterations': ['Yelyzaveta', 'Elizaveta', 'Yelyzaveta'],
        'declensions': ['Єлизавети', 'Єлизаветі', 'Єлизавету', 'Єлизаветою', 'Єлизаветі']
    },
    'Захар': {
        'gender': 'masc',
        'variants': ['Захар', 'Захар', 'Захар'],
        'diminutives': ['Захар', 'Захар', 'Захар'],
        'transliterations': ['Zakhar', 'Zakhar', 'Zakhar'],
        'declensions': ['Захара', 'Захару', 'Захара', 'Захаром', 'Захарі']
    },
    'Ірина': {
        'gender': 'femn',
        'variants': ['Ірина', 'Ірина', 'Ірина'],
        'diminutives': ['Ірина', 'Ірина', 'Ірина'],
        'transliterations': ['Iryna', 'Irina', 'Iryna'],
        'declensions': ['Ірини', 'Ірині', 'Ірину', 'Іриною', 'Ірині']
    },
    'Костянтин': {
        'gender': 'masc',
        'variants': ['Костянтин', 'Костянтин', 'Костянтин'],
        'diminutives': ['Костянтин', 'Костянтин', 'Костянтин'],
        'transliterations': ['Kostiantyn', 'Konstantin', 'Kostiantyn'],
        'declensions': ['Костянтина', 'Костянтину', 'Костянтина', 'Костянтином', 'Костянтині']
    }
}

# Optional: can create a final list of all names for convenience
# ALL_NAMES = list(NAMES.keys())

# Example output of name count in extended dictionary
# Total names count: {len(ALL_UKRAINIAN_NAMES)}

# Alias for compatibility with tests
UKRAINIAN_NAMES = NAMES
