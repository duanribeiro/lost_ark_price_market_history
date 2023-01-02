from settings import mongo_db, logger

mongo_collection_prices = mongo_db["prices"]
mongo_collection_builds = mongo_db["builds"]


def discover_unique_list(dup_list):
    res_list = []
    for i in range(len(dup_list)):
        if dup_list[i] not in dup_list[i + 1:]:
            res_list.append(dup_list[i])
    return res_list


def discover_stones_combinations(build):
    stones = []
    stones_keys = list(build['engravings_to_max'].keys())

    for engraving_1 in stones_keys:
        for engraving_2 in stones_keys:
            if engraving_1 == engraving_2:
                continue
            stones.append({engraving_1: 7,  engraving_2: 7})

    return discover_unique_list(dup_list=stones)


def discover_books_combinations(engravings_to_max):
    books = []
    book_keys = list(engravings_to_max.keys())

    for engraving_1 in book_keys:
        for engraving_2 in book_keys:
            if engraving_1 == engraving_2:
                continue
            books.append({
                engraving_1: 12,
                engraving_2: 9
            })
            books.append({
                engraving_1: 9,
                engraving_2: 12
            })

    return discover_unique_list(dup_list=books)


def discover_engravings_to_find(engravings_to_max, stone, book):
    engravings_to_find = {}
    for engraving_name, engraving_value in engravings_to_max.items():
        book_value = book.get(engraving_name, 0)
        stone_value = stone.get(engraving_name, 0)
        result = engraving_value - book_value - stone_value
        if result > 0:
            engravings_to_find[engraving_name] = engraving_value - book_value - stone_value
        else:
            engravings_to_find[engraving_name] = 0

    engravings_names = list(engravings_to_find.keys())
    engravings_values = list(engravings_to_find.values())

    return engravings_names, engravings_values


def query_mongo(build, engravings_names, region):
    pipeline = [
        {"$match": {"$or": []}},
        {"$match": {"$or": []}},
        {"$match": {"region": region}},
    ]
    for engraving1 in engravings_names:
        for engraving2 in engravings_names:
            if engraving1 == engraving2:
                continue
            pipeline[0]['$match']['$or'].append({
                f"engraving_effect.{engraving1}": {"$exists": True},
                f"engraving_effect.{engraving2}": {"$exists": True},
                f"engraving_effect.{engraving1}": {"$gte": 3},
                f"engraving_effect.{engraving2}": {"$gte": 5}
            })
    for stats in build['stats']:
        pipeline[1]['$match']['$or'].append({
            f"bonus_effect.{stats}": {"$exists": True}
        })
    all_items = list(mongo_collection_prices.aggregate(pipeline=pipeline))

    necklaces, rings, earrings = [], [], []
    for item in all_items:
        if item['type'] == 'Necklace':
            necklaces.append(item)
        elif item['type'] == 'Ring':
            rings.append(item)
        elif item['type'] == 'Earring':
            earrings.append(item)
    return necklaces, rings, earrings


def match_engravings(build, region):
    counter = {
        'build': 0,
        'stone': 0,
        'book': 0,
        'combination': 0,
        'founded': 0
    }

    stones_combinations = discover_stones_combinations(build=build)
    books_combinations = discover_books_combinations(engravings_to_max=build['engravings_to_max'])
    counter['stone'] = 0

    necklaces, rings, earrings = query_mongo(
        build=build,
        engravings_names=list(build['engravings_to_max'].keys()),
        region=region
    )

    for stone in stones_combinations:
        counter['stone'] += 1
        counter['book'] = 0

        for book in books_combinations:
            counter['book'] += 1
            logger.warning(f'----------------------')
            logger.warning(f'{build["name"]} | {region}')
            logger.warning(f'Necklaces: {len(necklaces)} | Rings: {len(rings)} | Earrings: {len(earrings)}')
            logger.warning(f'Stone: {counter["stone"]} of {len(stones_combinations)}')
            logger.warning(f'Book: {counter["book"]} of {len(books_combinations)}')

            engravings_names, engravings_values = discover_engravings_to_find(
                engravings_to_max=build['engravings_to_max'],
                stone=stone,
                book=book
            )

            if sum(engravings_values) > 40 or not necklaces or not rings or not earrings:
                continue

            counter['combination'] = 0
            for necklace1 in necklaces:
                for ring1 in rings:
                    for ring2 in rings:
                        if ring1['name'] == ring2['name']:
                            continue
                        for earrings1 in earrings:
                            for earrings2 in earrings:
                                if earrings1['name'] == earrings2['name']:
                                    continue
                                counter['combination'] += 1
                                engraving_1 = necklace1['engraving_effect'].get(engravings_names[0], 0) + \
                                              ring1['engraving_effect'].get(engravings_names[0], 0) + \
                                              ring2['engraving_effect'].get(engravings_names[0], 0) + \
                                              earrings1['engraving_effect'].get(engravings_names[0], 0) + \
                                              earrings2['engraving_effect'].get(engravings_names[0], 0)

                                engraving_2 = necklace1['engraving_effect'].get(engravings_names[1], 0) + \
                                              ring1['engraving_effect'].get(engravings_names[1], 0) + \
                                              ring2['engraving_effect'].get(engravings_names[1], 0) + \
                                              earrings1['engraving_effect'].get(engravings_names[1], 0) + \
                                              earrings2['engraving_effect'].get(engravings_names[1], 0)

                                engraving_3 = necklace1['engraving_effect'].get(engravings_names[2], 0) + \
                                              ring1['engraving_effect'].get(engravings_names[2], 0) + \
                                              ring2['engraving_effect'].get(engravings_names[2], 0) + \
                                              earrings1['engraving_effect'].get(engravings_names[2], 0) + \
                                              earrings2['engraving_effect'].get(engravings_names[2], 0)

                                engraving_4 = necklace1['engraving_effect'].get(engravings_names[3], 0) + \
                                              ring1['engraving_effect'].get(engravings_names[3], 0) + \
                                              ring2['engraving_effect'].get(engravings_names[3], 0) + \
                                              earrings1['engraving_effect'].get(engravings_names[3], 0) + \
                                              earrings2['engraving_effect'].get(engravings_names[3], 0)


                                engraving_5 = necklace1['engraving_effect'].get(engravings_names[4], 0) + \
                                              ring1['engraving_effect'].get(engravings_names[4], 0) + \
                                              ring2['engraving_effect'].get(engravings_names[4], 0) + \
                                              earrings1['engraving_effect'].get(engravings_names[4], 0) + \
                                              earrings2['engraving_effect'].get(engravings_names[4], 0)

                                if engraving_1 >= engravings_values[0] and \
                                   engraving_2 >= engravings_values[1] and \
                                   engraving_3 >= engravings_values[2] and \
                                   engraving_4 >= engravings_values[3] and \
                                   engraving_5 >= engravings_values[4]:
                                    counter['founded'] += 1
                                    if counter['founded'] > 100:
                                        logger.warning(f'100 COMBINATIONS FOUNDED')
                                        return

                                    mongo_collection_builds.insert_one({
                                        'max_engravings': 5,
                                        'region': region,
                                        'build': build['name'],
                                        'total_gold': necklace1['minimum_bid'] + ring1['minimum_bid'] + ring2['minimum_bid'] + earrings1['minimum_bid'] + earrings2['minimum_bid'],
                                        'stats':  build['stats'],
                                        'engravings_to_max': list(build['engravings_to_max'].keys()),
                                        'stone': stone,
                                        'book': book,
                                        'necklace1': necklace1,
                                        'ring1': ring1,
                                        'ring2': ring2,
                                        'earrings1': earrings1,
                                        'earrings2': earrings2,
                                    })
                                # elif engraving_1 >= engravings_values[0] and \
                                #      engraving_2 >= engravings_values[1] and \
                                #      engraving_3 >= engravings_values[2] and \
                                #      engraving_4 >= engravings_values[3]:
                                #
                                #     mongo_collection_builds.insert_one({
                                #         'max_engravings': 4,
                                #         'build': build['name'],
                                #         'necklace1': necklace1,
                                #         'ring1': ring1,
                                #         'ring2': ring2,
                                #         'earrings1': earrings1,
                                #         'earrings2': earrings2,
                                #     })
                                # elif engraving_1 >= engravings_values[0] and \
                                #      engraving_2 >= engravings_values[1] and \
                                #      engraving_3 >= engravings_values[2]:
                                #
                                #     results.append({
                                #         'max_engravings': 3,
                                #         'build': build['name'],
                                #         'necklace1': necklace1,
                                #         'ring1': ring1,
                                #         'ring2': ring2,
                                #         'earrings1': earrings1,
                                #         'earrings2': earrings2,
                                #     })
                                #     mongo_collection_builds.insert_one({
                                #         'max_engravings': 3,
                                #         'build': build['name'],
                                #         'necklace1': necklace1,
                                #         'ring1': ring1,
                                #         'ring2': ring2,
                                #         'earrings1': earrings1,
                                #         'earrings2': earrings2,
                                #     })

