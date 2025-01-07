import requests

def get_tags(champ):
    clas = ""
    for g in data(champ, 'tags'):
        print(g)

        clas += str(champ_class.get(g)) + ", "

    return clas[:-2]
def dat(champion, what):
    url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion/{champion}.json"

    response = requests.get(url)
    response.raise_for_status()
    data1 = response.json()
    lore = data1.get("data", {}).get(champion, {}).get(what)
    i = lore
    print(i)


    return i


def reworked_chams(champs):

    url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion.json"

    response = requests.get(url)
    response.raise_for_status()
    data1 = response.json()

    key = data1.get("data", {}).get(champs, {}).get("key")

    ro = key + "/" + key + "000"

    don = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/{ro}.jpg"

    return don


champions_by_letter = [
    ['Azir', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Ahri', 'Aatrox', 'AurelionSol', 'Aphelios', 'Aurora', 'Ambessa'],
    ['Bard', 'Belveth', 'Blitzcrank', 'Briar', 'Braum', 'Brand'],
    ['Warwick', 'Varus', 'Veigar', 'Vayne', 'Vi', 'Viktor', 'Vladimir', 'Volibear'],
    ['Galio', 'Gangplank', 'Garen', 'Gwen', 'Graves', 'Gragas', 'Gnar'],
    ['Darius', 'Jax', 'JarvanIV', 'Jayce', 'Jhin', 'Jinx', 'Diana', 'DrMundo', 'Draven'],
    ['Yone'],
    ['Janna'],
    ['Zyra', 'Zac', 'Zed', 'Xerath', 'Ziggs', 'Zilean', 'Zoe'],
    ['Ivern', 'Illaoi', 'Irelia'],
    ['Khazix', 'Kayn', 'Kaisa', 'Kalista', 'Camille', 'Karma', 'Karthus', 'Kassadin', 'Cassiopeia', 'Katarina', 'Quinn', 'Kayle', 'Caitlyn', 'Kennen', 'Qiyana', 'Kindred', 'Kled', 'KogMaw', 'Corki'],
    ['Leblanc', 'Leona', 'LeeSin', 'Lillia', 'Lissandra', 'Lulu', 'Lux', 'Lucian'],
    ['Malzahar', 'Malphite', 'Maokai', 'MasterYi', 'Milio', 'MissFortune', 'Morgana', 'Mordekaiser'],
    ['Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Nidalee', 'Neeko', 'Nilah', 'Nocturne', 'Nunu'],
    ['Olaf', 'Orianna', 'Ornn'],
    ['Pyke', 'Pantheon', 'Poppy'],
    ['Ryze', 'Rumble', 'Rammus', 'Rakan', 'RekSai', 'Renata', 'Rengar', 'Renekton', 'Riven', 'Rell'],
    ['Sylas', 'Samira', 'Swain', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Sivir', 'Syndra', 'Sion', 'Sona', 'Soraka','Shaco', 'Xayah', 'Shen', 'Shyvana', 'Smolder'],
    ['Talon', 'Taric', 'TwistedFate', 'Twitch', 'Teemo', 'Trundle', 'Thresh', 'Tryndamere', 'Tristana'],
    ['Udyr', 'Urgot'],
    ['Fiddlesticks', 'Fizz', 'Fiora'],
    ['Hwei', 'Heimerdinger'],
    ['Evelynn', 'Ezreal', 'Ekko', 'Elise', 'Annie'],
    ['Yuumi'],
]

champ_class = {
    'Tank': 'Танк',
    'Support': 'Поддержка',
    'Marksman': 'Стрелок',
    'Mage': 'Маг',
    'Fighter': 'Воин',
    'Assassin': 'Убийца'
}

letter_to_number = {
    'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ё': 5, 'ж': 6, 'з': 7, 'и': 8,
    'к': 9, 'л': 10, 'м': 11, 'н': 12, 'о': 13, 'п': 14, 'р': 15, 'с': 16, 'т': 17,
    'у': 18, 'ф': 19, 'х': 20, 'э': 21, 'ю': 22
}

ru_to_en = {
    'амбесса':'Ambessa',
    'азир': 'Azir',
    'аврора':'Aurora',
    'акали': 'Akali',
    'акшан': 'Akshan',
    'алистар': 'Alistar',
    'амуму': 'Amumu',
    'анивия': 'Anivia',
    'ари': 'Ahri',
    'атрокс': 'Aatrox',
    'аурелион сол': 'AurelionSol',
    'афелий': 'Aphelios',
    'бард': 'Bard',
    'бел вет': 'Belveth',
    'блицкранк': 'Blitzcrank',
    'бриар': 'Briar',
    'браум': 'Braum',
    'брэнд': 'Brand',
    'варвик': 'Warwick',
    'варус': 'Varus',
    'вейгар': 'Veigar',
    'вейн': 'Vayne',
    'вай': 'Vi',
    'виктор': 'Viktor',
    'владимир': 'Vladimir',
    'волибир': 'Volibear',
    'галио': 'Galio',
    'гангпланк': 'Gangplank',
    'гарен': 'Garen',
    'гвен': 'Gwen',
    'грейвз': 'Graves',
    'грагас': 'Gragas',
    'гнар': 'Gnar',
    'дариус': 'Darius',
    'джакс': 'Jax',
    'джарван iv': 'JarvanIV',
    'джейc': 'Jayce',
    'джин': 'Jhin',
    'джинкс': 'Jinx',
    'диана': 'Diana',
    'доктор мундо': 'DrMundo',
    'дрейвен': 'Draven',
    'ёнэ': 'Yone',
    'жанна': 'Janna',
    'зайра': 'Zyra',
    'зак': 'Zac',
    'зед': 'Zed',
    'зерат': 'Xerath',
    'зиггс': 'Ziggs',
    'зилеан': 'Zilean',
    'зои': 'Zoe',
    'иверн': 'Ivern',
    'иллаой': 'Illaoi',
    'ирелия': 'Irelia',
    'казикс': 'Khazix',
    'каин': 'Kayn',
    'кайса': 'Kaisa',
    'калиста': 'Kalista',
    'камилла': 'Camille',
    'карма': 'Karma',
    'картус': 'Karthus',
    'кассадин': 'Kassadin',
    'кассиопея': 'Cassiopeia',
    'катарина': 'Katarina',
    'квинн': 'Quinn',
    'кейл': 'Kayle',
    'кейтлин': 'Caitlyn',
    'кеннен': 'Kennen',
    'киана': 'Qiyana',
    'киндред': 'Kindred',
    'клед': 'Kled',
    'когмао': 'KogMaw',
    'корки': 'Corki',
    'ле блан': 'Leblanc',
    'леона': 'Leona',
    'ли син': 'LeeSin',
    'лиллия': 'Lillia',
    'лиссандра': 'Lissandra',
    'лулу': 'Lulu',
    'люкс': 'Lux',
    'люциан': 'Lucian',
    'мальзахар': 'Malzahar',
    'мальфит': 'Malphite',
    'маокай': 'Maokai',
    'мастер йи': 'MasterYi',
    'милио': 'Milio',
    'мисc фортуна': 'MissFortune',
    'моргана': 'Morgana',
    'мордекайзер': 'Mordekaiser',
    'наафири': 'Naafiri',
    'нами': 'Nami',
    'насус': 'Nasus',
    'наутилус': 'Nautilus',
    'нидали': 'Nidalee',
    'нико': 'Neeko',
    'нила': 'Nilah',
    'ноктюрн': 'Nocturne',
    'нуну': 'Nunu',
    'олаф': 'Olaf',
    'орианна': 'Orianna',
    'орн': 'Ornn',
    'пайк': 'Pyke',
    'пантеон': 'Pantheon',
    'поппи': 'Poppy',
    'райз': 'Ryze',
    'рамбл': 'Rumble',
    'раммус': 'Rammus',
    'рэйкан': 'Rakan',
    'рек сай': 'RekSai',
    'рената': 'Renata',
    'ренгар': 'Rengar',
    'ренектон': 'Renekton',
    'ривен': 'Riven',
    'релл': 'Rell',
    'сайлас': 'Sylas',
    'самира': 'Samira',
    'свейн': 'Swain',
    'седжуани': 'Sejuani',
    'сенна': 'Senna',
    'серафина': 'Seraphine',
    'сетт': 'Sett',
    'сивир': 'Sivir',
    'синдра': 'Syndra',
    'сион': 'Sion',
    'сона': 'Sona',
    'сорака': 'Soraka',
    'шако': 'Shaco',
    'шая': 'Xayah',
    'шен': 'Shen',
    'шивана': 'Shyvana',
    'смолдер': 'Smolder',
    'талон': 'Talon',
    'тарик': 'Taric',
    'твитед фэйт': 'TwistedFate',
    'твитч': 'Twitch',
    'тимо': 'Teemo',
    'трандл': 'Trundle',
    'треш': 'Thresh',
    'триндамир': 'Tryndamere',
    'тристана': 'Tristana',
    'удир': 'Udyr',
    'ургот': 'Urgot',
    'фиддлстикс': 'Fiddlesticks',
    'физз': 'Fizz',
    'фиора': 'Fiora',
    'хеймердингер': 'Heimerdinger',
    'эвелинн': 'Evelynn',
    'эзреаль': 'Ezreal',
    'экко': 'Ekko',
    'элиза': 'Elise',
    'энни': 'Annie',
    'юми': 'Yuumi'
}


def find_letter(letter):
    list = []
    for key in ru_to_en:
        if key.startswith(letter):
            list.append(key)
    return list









async def inline_query(update, context):

    global result_id, ur, clas
    global mes_id
    query = update.inline_query.query
    results = []
    ur = ''
    clas = ""



    if query[:1] in letter_to_number.keys():
        index = letter_to_number[query[:1]]

        jj = champions_by_letter[index]

        for full in jj:
            if full in ru_to_en.values():
                en_word = ru_to_en[full].values()
                if query in ru_to_en[full].values():
                    if full in chams:
                        ur = full
                        dd = reworked_chams(ur)

                    else:
                        dd = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{ur}_0.jpg"
            else:
                print('no')

            results.append(
                InlineQueryResultArticle(
                    input_message_content=InputTextMessageContent(
                        f"*{data(ur, 'name').title()}* \n\n*Лор*💬: {data(ur, 'lore')}\n\nКласс: {get_tags(ur)}\n\n{dd}"),
                    id=ur + str(random()),
                    title=data(ur, "name").title(),
                    description=data(ur, "title"),
                    thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{ur}.png",

                )
            )
    await update.inline_query.answer(results, cache_time=1)





async def inline_query(update, context):
    query = update.inline_query.query.lower()  # Convert to lowercase for case-insensitive search
    results = []

    # Find all potential matches that start with the query string
    potential_matches = [key for key in ru_to_en if key.startswith(query)]

    if potential_matches:
        for match in potential_matches:
            ur = ru_to_en[match]
            full = ur

            dd = reworked_chams(ur) if ur in chams else f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{ur}_0.jpg"

            results.append(
                InlineQueryResultArticle(
                    input_message_content=InputTextMessageContent(
                        f"*{data(ur, 'name').title()}* \n\n*Лор*💬: {data(ur, 'lore')}\n\nКласс: {get_tags(ur)}\n\n{dd}"
                    ),
                    id=ur + str(random()),
                    title=data(ur, "name").title(),
                    description=data(ur, "title"),
                    thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{ur}.png",
                )
            )
    else:
        print(f"No match for: {query}")

    await update.inline_query.answer(results, cache_time=1)

    last_query_time = 0
    DEBOUNCE_DELAY = 1

    async def inline_query(update: Update, context):
        global last_query_time
        global ur, clas, mes_id

        query = update.inline_query.query
        ur = ''
        clas = ''

        current_time = time()

        # Debounce mechanism: Skip processing if typing/removing letters too quickly
        if current_time - last_query_time < DEBOUNCE_DELAY:
            last_query_time = current_time  # Update the last query time
            return  # Do nothing until user stops typing for the debounce period

        # Proceed if debounce delay has passed
        if query:
            last_query_time = current_time

            loading_result = InlineQueryResultArticle(
                input_message_content=InputTextMessageContent(
                    "🔍 Searching... Please wait!"
                ),
                id="loading",  # This can be any unique value
                title="Searching...",
                description="Searching for champions...",
            )

            # Send the loading result to the user

            results = []
            champ_list = find_letter(query[:1])
            for ru in champ_list:
                if ru.startswith(query):
                    en_word = ru_to_en[ru]
                    ur = en_word

                    if en_word in chams:
                        dd = reworked_chams(ur)
                    else:
                        dd = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{ur}_0.jpg"

                    # Add result to the list
                    results.append(
                        InlineQueryResultArticle(
                            input_message_content=InputTextMessageContent(
                                f"*{data(ur, 'name').title()}* \n\n*Лор*💬: {data(ur, 'lore')}\n\nКласс: {get_tags(ur)}\n\n{dd}"
                            ),
                            id=ur + str(random()),
                            title=data(ur, "name").title(),
                            description=data(ur, "title"),
                            thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{ur}.png",
                        )
                    )
                else:
                    print('no match')

            await update.inline_query.answer(results, cache_time=1)