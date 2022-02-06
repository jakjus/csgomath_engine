import pickle
from components.helpers import text_to_price


class Extractor:
    # Key: Item appearing in box description
    # Value: Search phrase to find the item
    special_items = [
        {'box_desc_name': 'Special Item', 'search_phrase': 'Knife |'},
        {'box_desc_name': 'Rare Gloves', 'search_phrase': 'Gloves'},
        {'box_desc_name': 'Falchion Knife', 'search_phrase': 'Falchion Knife'},
        {'box_desc_name': 'Shadow Daggers', 'search_phrase': 'Shadow Daggers'},
        {'box_desc_name': 'Bowie Knife', 'search_phrase': 'Bowie Knife'},
        {'box_desc_name': 'Butterfly Knife',
            'search_phrase': 'Butterfly Knife'},
        {'box_desc_name': 'Classic Knife', 'search_phrase': 'Classic Knife'},
        {'box_desc_name': 'Huntsman Knife', 'search_phrase': 'Huntsman Knife'}
    ]

    # Data from Valve due to Chinese market regulations regarding lootboxes
    odds_rarity = {'4b69ff': 0.7992327, '8847ff': 0.1598465,
                   'd32ce6': 0.0319693, 'eb4b4b': 0.0063939,
                   'ffd700': 0.0025575}
    odds_wear = {'Factory New': 0.1471, 'Minimal Wear': 0.2468,
                 'Field-Tested': 0.4318, 'Battle-Scarred': 0.0993,
                 'Well-Worn': 0.0792}

    keys_off_market = [
            {'name': 'Fracture Case Key', 'icon_url': 'https://static.wikia.nocookie.net/cswikia/images/2/2a/Fracture_Case_Key.png/revision/latest?cb=20201207135639', 'asset_description': {'descriptions': ['This key opens only Fracture Cases']}},
            {'name': 'Dreams & Nightmares Case', 'icon_url': 'https://static.wikia.nocookie.net/cswikia/images/2/21/Crate_key_community_30.png/revision/latest?cb=20220121083708', 'asset_description': {'descriptions': ['This key opens only Dreams & Nightmares Cases']}},
            {'name': 'Shattered Web Case Key', 'icon_url': 'https://static.wikia.nocookie.net/cswikia/images/2/2f/Shattered_Web_Case_Key.png/revision/latest?cb=20201206140152', 'asset_description': {'descriptions': ['This key opens only Shattered Web Cases']}},
            {'name': 'Snakebite Case Key', 'icon_url': 'https://static.wikia.nocookie.net/cswikia/images/5/51/Snakebite-case-key.png/revision/latest?cb=20210528135645', 'asset_description': {'descriptions': ['This key opens only Snakebite Cases']}}
            ]

    def __init__(self, all_items=[], pickle_name=''):
        self.all_items = all_items
        if pickle_name:
            self.load_from_pickle(pickle_name)
        self.cases = self.filter_items_end('Case', self.all_items)
        self.case_keys = self.filter_items_end('Case Key', self.all_items)
        self.case_keys += self.filter_items_end('eSports Key', self.all_items)
        self.case_keys += self.keys_off_market
        self.special_items_found = {}

    def load_from_pickle(self, pickle_name):
        with open(pickle_name+'.pickle', 'rb') as handle:
            self.all_items = pickle.load(handle)

    def remove_duplicates(self):
        for index, case in enumerate(self.cases):
            if case['name'] in list(map(lambda x: x['name'], self.cases[index+1:])):
                self.cases.remove(case)

    def add_sale_price(self):
        for case in self.cases:
            case['sale_price'] = text_to_price(case['sale_price_text'])

    def add_key(self):
        for case in self.cases:
            for key in self.case_keys:
                if case['name'] in key['name']:
                    case['key'] = key
                    break
            if 'key' in case.keys():
                continue
            for key in self.case_keys:
                if case['name'].split()[0] in key['name'].split() and case['name'].split()[1] in key['name'].split():
                    case['key'] = key
                    break
            if 'key' in case.keys():
                continue
            for key in self.case_keys:
                if case['name'].split()[0] in key['name'].split():
                    case['key'] = key
                    break
            if 'key' not in case.keys():
                print('Key not found for', case['name'])

    def add_case_value(self):
        if len(self.cases) == 0:
            raise Exception('There is no case key list')
        if 'total' in self.cases[0]:
            raise Exception('Chest [0] already has a value')
        for case in self.cases:
            case['total'] = self.get_estimated_case_value(case)['total']

    def get_estimated_one_weapon_value(self, name, toadd=True):
        total = 0
        if toadd:
            items = self.filter_items(name + " (", self.all_items)
        else:
            items = self.filter_items(name, self.all_items)

        ss = ' '.join(list(map(lambda x: x['name'], items)))
        # item_details = []

        try:
            if 'StatTrak' in ss:
                found = 0
                for item in items:
                    for odd in self.odds_wear:
                        if odd in item['name'] \
                           and 'StatTrak' not in item['name']:
                            todd = 0.9*self.odds_wear[odd]
                            tsale_price = float(text_to_price(
                                item['sale_price_text']))
                            found += todd
                            total += todd*tsale_price
                            # item_details.append({'name':item['name'],
                            # 'odd': todd, 'sale_price': tsale_price,
                            # 'img': item['asset_description']['icon_url']})
                        elif odd in item['name'] \
                                and 'StatTrak' in item['name']:
                            todd = 0.1*self.odds_wear[odd]
                            tsale_price = float(
                                text_to_price(item['sale_price_text']))
                            found += todd
                            total += todd*tsale_price
                            # item_details.append({'name':item['name'],
                            # 'odd': todd, 'sale_price': tsale_price,
                            # 'img': item['asset_description']['icon_url']})
                if found < 1:
                    total /= found
            else:
                found = 0
                for item in items:
                    for odd in self.odds_wear:
                        if odd in item['name']:
                            found += self.odds_wear[odd]
                            total += float(text_to_price(
                                item['sale_price_text']))*self.odds_wear[odd]
                            item['odd'] = self.odds_wear[odd]
                            item['sale_price'] = float(
                                text_to_price(item['sale_price_text']))
                if found < 1:
                    total /= found
        except Exception as e:
            print(f'Error: {e}\nWhile processing: {name}')
            raise
        return {'total': round(total)}  # , 'item_details': item_details}

    def get_estimated_case_value(self, case):
        try:
            desc = case['asset_description']['descriptions']
        except KeyError:
            print('Error getting descriptions for', case['name'])
            print(case)
            raise
        total_d = {}
        for odd_rarity in self.odds_rarity:
            total_d[odd_rarity] = {}
            total_d[odd_rarity]['total'] = 0
            total_d[odd_rarity]['occurences'] = 0
        total = 0
        for item in desc:
            found_special_item = 0
            # Making sure it is content description, not a side note
            if 'color' not in item:
                continue
            if not item['color'] in self.odds_rarity:
                continue
            if item['value'] not in self.special_items_found:
                for special_item in self.special_items:
                    if special_item['box_desc_name'] in item['value']:
                        item_value = self.get_many_weapon_value(
                            special_item['search_phrase'])
                        self.special_items_found[item['value']] = item_value
                        found_special_item = 1
                        break
                if not found_special_item:
                    item_value = self.get_estimated_one_weapon_value(
                        item['value'])
            item['total'] = item_value['total']
            # item['item_details'] = item_value['item_details']
            total_d[item['color']]['total'] += item_value['total'] * \
                self.odds_rarity[item['color']]
            total_d[item['color']]['occurences'] += 1
        for el in total_d:
            total += total_d[el]['total']/total_d[el]['occurences']
        return {'total': round(total)}

    def get_unique_itemname_list(self, name):
        items = self.filter_items(name, self.all_items)
        itemname_list = list(map(lambda x: x['name'], items))
        unique_itemname_list = []
        for itemname in itemname_list:
            u = itemname.replace('StatTrak™ ', '')\
                .replace(' (Factory New)', '')\
                .replace(' (Minimal Wear)', '')\
                .replace(' (Field-Tested)', '')\
                .replace(' (Battle-Scarred)', '')\
                .replace(' (Well-Worn)', '')
            if itemname not in unique_itemname_list:
                unique_itemname_list.append(u)
        return unique_itemname_list

    def get_many_weapon_value(self, name):
        # Calculates many weapons under the name, i.e. Gloves, Knives
        total = 0
        newlist = self.get_unique_itemname_list(name)
        # item_details = []
        for name0 in newlist:
            owv = self.get_estimated_one_weapon_value(name0, toadd=False)
            w = owv['total']
            # item_details.append(owv['item_details'])
            total += w
        return {'total': round(total/len(newlist))}
        # 'item_details': item_details}

    def filter_items_end(self, name, items):
        return list(filter(
            lambda x: name in x['name']
            and x['name'].index(name) == len(x['name']) - len(name),
            items))

    def filter_items(self, name, items):
        return list(filter(
            lambda x: name.replace('★ ', '') in x['name'],
            items))

    def extract_full(self):
        print('Removing duplicates...')
        self.remove_duplicates()
        print('Done')
        print('Adding keys...')
        self.add_key()
        print('Done')
        print('Adding sale price...')
        self.add_sale_price()
        print('Done')
        print('Adding case value...')
        self.add_case_value()
        print('Done')
