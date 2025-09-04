# -*- coding: utf-8 -*-

"""
Словник азіатських імен та їх варіантів
Містить китайські, японські, корейські та інші азіатські імена
"""

NAMES = {
    # Chinese names
    'Вей': {
        'gender': 'masc',
        'variants': ['Wei', 'Way'],
        'diminutives': ['Вей', 'Wei'],
        'transliterations': ['Wei', 'Way'],
        'declensions': ['Вей', 'Вей', 'Вей', 'Вей', 'Вей']
    },
    'Лі': {
        'gender': 'masc',
        'variants': ['Li', 'Lee'],
        'diminutives': ['Лі', 'Li'],
        'transliterations': ['Li', 'Lee'],
        'declensions': ['Лі', 'Лі', 'Лі', 'Лі', 'Лі']
    },
    'Чжан': {
        'gender': 'masc',
        'variants': ['Zhang', 'Chang'],
        'diminutives': ['Чжан', 'Zhang'],
        'transliterations': ['Zhang', 'Chang'],
        'declensions': ['Чжан', 'Чжан', 'Чжан', 'Чжан', 'Чжан']
    },
    'Ван': {
        'gender': 'masc',
        'variants': ['Wang', 'Wong'],
        'diminutives': ['Ван', 'Wang'],
        'transliterations': ['Wang', 'Wong'],
        'declensions': ['Ван', 'Ван', 'Ван', 'Ван', 'Ван']
    },
    'Лю': {
        'gender': 'masc',
        'variants': ['Liu', 'Lau'],
        'diminutives': ['Лю', 'Liu'],
        'transliterations': ['Liu', 'Lau'],
        'declensions': ['Лю', 'Лю', 'Лю', 'Лю', 'Лю']
    },
    
    # Japanese names
    'Хіроші': {
        'gender': 'masc',
        'variants': ['Hiroshi', 'Hiro'],
        'diminutives': ['Хіро', 'Hiro'],
        'transliterations': ['Hiroshi', 'Hiro'],
        'declensions': ['Хіроші', 'Хіроші', 'Хіроші', 'Хіроші', 'Хіроші']
    },
    'Такаші': {
        'gender': 'masc',
        'variants': ['Takashi', 'Taka'],
        'diminutives': ['Така', 'Taka'],
        'transliterations': ['Takashi', 'Taka'],
        'declensions': ['Такаші', 'Такаші', 'Такаші', 'Такаші', 'Такаші']
    },
    'Юкі': {
        'gender': 'femn',
        'variants': ['Yuki', 'Yukiko'],
        'diminutives': ['Юкі', 'Yuki'],
        'transliterations': ['Yuki', 'Yukiko'],
        'declensions': ['Юкі', 'Юкі', 'Юкі', 'Юкі', 'Юкі']
    },
    'Акіко': {
        'gender': 'femn',
        'variants': ['Akiko', 'Aki'],
        'diminutives': ['Акі', 'Aki'],
        'transliterations': ['Akiko', 'Aki'],
        'declensions': ['Акіко', 'Акіко', 'Акіко', 'Акіко', 'Акіко']
    },
    'Кенджі': {
        'gender': 'masc',
        'variants': ['Kenji', 'Ken'],
        'diminutives': ['Кен', 'Ken'],
        'transliterations': ['Kenji', 'Ken'],
        'declensions': ['Кенджі', 'Кенджі', 'Кенджі', 'Кенджі', 'Кенджі']
    },
    
    # Korean names
    'Кім': {
        'gender': 'masc',
        'variants': ['Kim', 'Gim'],
        'diminutives': ['Кім', 'Kim'],
        'transliterations': ['Kim', 'Gim'],
        'declensions': ['Кім', 'Кім', 'Кім', 'Кім', 'Кім']
    },
    'Пак': {
        'gender': 'masc',
        'variants': ['Park', 'Pak'],
        'diminutives': ['Пак', 'Park'],
        'transliterations': ['Park', 'Pak'],
        'declensions': ['Пак', 'Пак', 'Пак', 'Пак', 'Пак']
    },
    'Чой': {
        'gender': 'masc',
        'variants': ['Choi', 'Choe'],
        'diminutives': ['Чой', 'Choi'],
        'transliterations': ['Choi', 'Choe'],
        'declensions': ['Чой', 'Чой', 'Чой', 'Чой', 'Чой']
    },
    'Джунг': {
        'gender': 'masc',
        'variants': ['Jung', 'Jeong'],
        'diminutives': ['Джунг', 'Jung'],
        'transliterations': ['Jung', 'Jeong'],
        'declensions': ['Джунг', 'Джунг', 'Джунг', 'Джунг', 'Джунг']
    },
    'Хан': {
        'gender': 'masc',
        'variants': ['Han', 'Hahn'],
        'diminutives': ['Хан', 'Han'],
        'transliterations': ['Han', 'Hahn'],
        'declensions': ['Хан', 'Хан', 'Хан', 'Хан', 'Хан']
    },
    
    # Vietnamese names
    'Нгуєн': {
        'gender': 'masc',
        'variants': ['Nguyen', 'Nguyễn'],
        'diminutives': ['Нгуєн', 'Nguyen'],
        'transliterations': ['Nguyen', 'Nguyễn'],
        'declensions': ['Нгуєн', 'Нгуєн', 'Нгуєн', 'Нгуєн', 'Нгуєн']
    },
    'Тран': {
        'gender': 'masc',
        'variants': ['Tran', 'Trần'],
        'diminutives': ['Тран', 'Tran'],
        'transliterations': ['Tran', 'Trần'],
        'declensions': ['Тран', 'Тран', 'Тран', 'Тран', 'Тран']
    },
    'Ле': {
        'gender': 'masc',
        'variants': ['Le', 'Lê'],
        'diminutives': ['Ле', 'Le'],
        'transliterations': ['Le', 'Lê'],
        'declensions': ['Ле', 'Ле', 'Ле', 'Ле', 'Ле']
    },
    'Фам': {
        'gender': 'masc',
        'variants': ['Pham', 'Phạm'],
        'diminutives': ['Фам', 'Pham'],
        'transliterations': ['Pham', 'Phạm'],
        'declensions': ['Фам', 'Фам', 'Фам', 'Фам', 'Фам']
    },
    'Хо': {
        'gender': 'masc',
        'variants': ['Ho', 'Hồ'],
        'diminutives': ['Хо', 'Ho'],
        'transliterations': ['Ho', 'Hồ'],
        'declensions': ['Хо', 'Хо', 'Хо', 'Хо', 'Хо']
    },
    
    # Additional Chinese names
    'Чень': {
        'gender': 'masc',
        'variants': ['Chen', 'Chin'],
        'diminutives': ['Чень', 'Chen'],
        'transliterations': ['Chen', 'Chin'],
        'declensions': ['Чень', 'Чень', 'Чень', 'Чень', 'Чень']
    },
    'Лінь': {
        'gender': 'masc',
        'variants': ['Lin', 'Ling'],
        'diminutives': ['Лінь', 'Lin'],
        'transliterations': ['Lin', 'Ling'],
        'declensions': ['Лінь', 'Лінь', 'Лінь', 'Лінь', 'Лінь']
    },
    'Хуан': {
        'gender': 'masc',
        'variants': ['Huang', 'Wong'],
        'diminutives': ['Хуан', 'Huang'],
        'transliterations': ['Huang', 'Wong'],
        'declensions': ['Хуан', 'Хуан', 'Хуан', 'Хуан', 'Хуан']
    },
    'Чжао': {
        'gender': 'masc',
        'variants': ['Zhao', 'Chao'],
        'diminutives': ['Чжао', 'Zhao'],
        'transliterations': ['Zhao', 'Chao'],
        'declensions': ['Чжао', 'Чжао', 'Чжао', 'Чжао', 'Чжао']
    },
    'У': {
        'gender': 'masc',
        'variants': ['Wu', 'Woo'],
        'diminutives': ['У', 'Wu'],
        'transliterations': ['Wu', 'Woo'],
        'declensions': ['У', 'У', 'У', 'У', 'У']
    },
    
    # Additional Japanese names
    'Сато': {
        'gender': 'masc',
        'variants': ['Sato', 'Sato'],
        'diminutives': ['Сато', 'Sato'],
        'transliterations': ['Sato', 'Sato'],
        'declensions': ['Сато', 'Сато', 'Сато', 'Сато', 'Сато']
    },
    'Танака': {
        'gender': 'masc',
        'variants': ['Tanaka', 'Tanaka'],
        'diminutives': ['Танака', 'Tanaka'],
        'transliterations': ['Tanaka', 'Tanaka'],
        'declensions': ['Танака', 'Танака', 'Танака', 'Танака', 'Танака']
    },
    'Ватанабе': {
        'gender': 'masc',
        'variants': ['Watanabe', 'Watanabe'],
        'diminutives': ['Ватанабе', 'Watanabe'],
        'transliterations': ['Watanabe', 'Watanabe'],
        'declensions': ['Ватанабе', 'Ватанабе', 'Ватанабе', 'Ватанабе', 'Ватанабе']
    },
    'Іто': {
        'gender': 'masc',
        'variants': ['Ito', 'Ito'],
        'diminutives': ['Іто', 'Ito'],
        'transliterations': ['Ito', 'Ito'],
        'declensions': ['Іто', 'Іто', 'Іто', 'Іто', 'Іто']
    },
    'Ямада': {
        'gender': 'masc',
        'variants': ['Yamada', 'Yamada'],
        'diminutives': ['Ямада', 'Yamada'],
        'transliterations': ['Yamada', 'Yamada'],
        'declensions': ['Ямада', 'Ямада', 'Ямада', 'Ямада', 'Ямада']
    },
    
    # Additional Korean names
    'Сін': {
        'gender': 'masc',
        'variants': ['Shin', 'Sin'],
        'diminutives': ['Сін', 'Shin'],
        'transliterations': ['Shin', 'Sin'],
        'declensions': ['Сін', 'Сін', 'Сін', 'Сін', 'Сін']
    },
    'Юн': {
        'gender': 'masc',
        'variants': ['Yoon', 'Yun'],
        'diminutives': ['Юн', 'Yoon'],
        'transliterations': ['Yoon', 'Yun'],
        'declensions': ['Юн', 'Юн', 'Юн', 'Юн', 'Юн']
    },
    'Чо': {
        'gender': 'masc',
        'variants': ['Cho', 'Jo'],
        'diminutives': ['Чо', 'Cho'],
        'transliterations': ['Cho', 'Jo'],
        'declensions': ['Чо', 'Чо', 'Чо', 'Чо', 'Чо']
    },
    'Сонг': {
        'gender': 'masc',
        'variants': ['Song', 'Sung'],
        'diminutives': ['Сонг', 'Song'],
        'transliterations': ['Song', 'Sung'],
        'declensions': ['Сонг', 'Сонг', 'Сонг', 'Сонг', 'Сонг']
    },
    'Квон': {
        'gender': 'masc',
        'variants': ['Kwon', 'Kwon'],
        'diminutives': ['Квон', 'Kwon'],
        'transliterations': ['Kwon', 'Kwon'],
        'declensions': ['Квон', 'Квон', 'Квон', 'Квон', 'Квон']
    },
    
    # Additional Thai names
    'Прачута': {
        'gender': 'masc',
        'variants': ['Prachuta', 'Prachut'],
        'diminutives': ['Прачута', 'Prachuta'],
        'transliterations': ['Prachuta', 'Prachut'],
        'declensions': ['Прачути', 'Прачуті', 'Прачуту', 'Прачутою', 'Прачуті']
    },
    'Сіріпон': {
        'gender': 'femn',
        'variants': ['Siriporn', 'Porn'],
        'diminutives': ['Сіріпон', 'Siriporn'],
        'transliterations': ['Siriporn', 'Porn'],
        'declensions': ['Сіріпон', 'Сіріпон', 'Сіріпон', 'Сіріпон', 'Сіріпон']
    },
    'Сомчай': {
        'gender': 'masc',
        'variants': ['Somchai', 'Chai'],
        'diminutives': ['Сомчай', 'Somchai'],
        'transliterations': ['Somchai', 'Chai'],
        'declensions': ['Сомчая', 'Сомчаю', 'Сомчая', 'Сомчаєм', 'Сомчаї']
    },
    'Сомкіт': {
        'gender': 'masc',
        'variants': ['Somkit', 'Kit'],
        'diminutives': ['Сомкіт', 'Somkit'],
        'transliterations': ['Somkit', 'Kit'],
        'declensions': ['Сомкіта', 'Сомкіту', 'Сомкіта', 'Сомкітом', 'Сомкіті']
    },
    'Сомпон': {
        'gender': 'femn',
        'variants': ['Sompon', 'Pon'],
        'diminutives': ['Сомпон', 'Sompon'],
        'transliterations': ['Sompon', 'Pon'],
        'declensions': ['Сомпон', 'Сомпон', 'Сомпон', 'Сомпон', 'Сомпон']
    },
    
    # Additional Vietnamese names
    'Нгуєн Ван': {
        'gender': 'masc',
        'variants': ['Nguyen Van', 'Van'],
        'diminutives': ['Нгуєн Ван', 'Nguyen Van'],
        'transliterations': ['Nguyen Van', 'Van'],
        'declensions': ['Нгуєн Ван', 'Нгуєн Ван', 'Нгуєн Ван', 'Нгуєн Ван', 'Нгуєн Ван']
    },
    'Тран Тхі': {
        'gender': 'femn',
        'variants': ['Tran Thi', 'Thi'],
        'diminutives': ['Тран Тхі', 'Tran Thi'],
        'transliterations': ['Tran Thi', 'Thi'],
        'declensions': ['Тран Тхі', 'Тран Тхі', 'Тран Тхі', 'Тран Тхі', 'Тран Тхі']
    },
    'Ле Ван': {
        'gender': 'masc',
        'variants': ['Le Van', 'Van'],
        'diminutives': ['Ле Ван', 'Le Van'],
        'transliterations': ['Le Van', 'Van'],
        'declensions': ['Ле Ван', 'Ле Ван', 'Ле Ван', 'Ле Ван', 'Ле Ван']
    },
    'Фам Тхі': {
        'gender': 'femn',
        'variants': ['Pham Thi', 'Thi'],
        'diminutives': ['Фам Тхі', 'Pham Thi'],
        'transliterations': ['Pham Thi', 'Thi'],
        'declensions': ['Фам Тхі', 'Фам Тхі', 'Фам Тхі', 'Фам Тхі', 'Фам Тхі']
    },
    'Хо Ван': {
        'gender': 'masc',
        'variants': ['Ho Van', 'Van'],
        'diminutives': ['Хо Ван', 'Ho Van'],
        'transliterations': ['Ho Van', 'Van'],
        'declensions': ['Хо Ван', 'Хо Ван', 'Хо Ван', 'Хо Ван', 'Хо Ван']
    },
    
    # Additional Malaysian names
    'Ахмад': {
        'gender': 'masc',
        'variants': ['Ahmad', 'Ahmed'],
        'diminutives': ['Ахмад', 'Ahmad'],
        'transliterations': ['Ahmad', 'Ahmed'],
        'declensions': ['Ахмада', 'Ахмаду', 'Ахмада', 'Ахмадом', 'Ахмаді']
    },
    'Саліха': {
        'gender': 'femn',
        'variants': ['Saliha', 'Salihah'],
        'diminutives': ['Саліха', 'Saliha'],
        'transliterations': ['Saliha', 'Salihah'],
        'declensions': ['Саліхи', 'Салісі', 'Саліху', 'Саліхою', 'Салісі']
    },
    'Мохамед': {
        'gender': 'masc',
        'variants': ['Mohamed', 'Muhammad'],
        'diminutives': ['Мохамед', 'Mohamed'],
        'transliterations': ['Mohamed', 'Muhammad'],
        'declensions': ['Мохамеда', 'Мохамеду', 'Мохамеда', 'Мохамедом', 'Мохамеді']
    },
    'Нур': {
        'gender': 'femn',
        'variants': ['Noor', 'Nur'],
        'diminutives': ['Нур', 'Noor'],
        'transliterations': ['Noor', 'Nur'],
        'declensions': ['Нур', 'Нур', 'Нур', 'Нур', 'Нур']
    },
    'Ісмаїл': {
        'gender': 'masc',
        'variants': ['Ismail', 'Ismael'],
        'diminutives': ['Ісмаїл', 'Ismail'],
        'transliterations': ['Ismail', 'Ismael'],
        'declensions': ['Ісмаїла', 'Ісмаїлу', 'Ісмаїла', 'Ісмаїлом', 'Ісмаїлі']
    }
}

# All Asian names
# ALL_NAMES = list(NAMES.keys())

# Example output of name count in dictionary
# Total Asian names count: {len(ALL_ASIAN_NAMES)}
