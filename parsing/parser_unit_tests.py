from parse import GoodOnYou
import unittest

class GoodOnYouTests:
    def __init__(self):
        self._GoodOnYou = GoodOnYou()
        self._tests =[
            # {brand_tag:{brand_name:data}}
            {'132-5-issey-miyake':{'132 5. Issey Miyake':{'rating': 'It\'s a start', 'price': '$$$', \
                'planet_rating': '3', 'people_rating': '2', 'animals_rating': '4', \
                    'message': 'Issey Miyake uses eco-friendly materials but is not taking adequate ' +\
                        'steps to ensure payment of a living wage for its workers', \
                            'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/132-5-issey-miyake'}}}, \
            {'angela-roi':{'Angela Roi':{'rating': 'It\'s a start', 'price': '$$', 'planet_rating': '2', \
                'people_rating': '3', 'animals_rating': '5', 'message': 'Angela Roi is a luxury designer ' +\
                     'vegan handbag brand', \
                         'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/angela-roi'}}}, \
            {'appletrees':{'APPLETREES':{'rating': 'Not good enough', 'price': '$$', 'planet_rating': '2', \
                'people_rating': '2', 'animals_rating': '2', 'message': 'APPLETREES is committed to ' +\
                     'create long lasting, high quality unisex products that are designed to function ' +\
                          'well in daily life.', \
                              'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/appletrees'}}}, \
            {'bjorn-borg':{'Bjorn Borg':{'rating': 'It\'s a start', 'price': '$', 'planet_rating': '2', \
                'people_rating': '3', 'animals_rating': '3', 'message': 'Bjorn Borg has good policies ' +\
                     'to audit suppliers but is not taking adequate steps to eliminate hazardous ' + \
                         'chemicals in its supply chain', \
                             'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/bjorn-borg'}}}, \
            {'citizens-mark':{'Citizen\'s Mark':{'rating': 'Good', 'price': '$$$', 'planet_rating': '4', \
                'people_rating': '4', 'animals_rating': '4', 'message': 'Modern suiting for a ' + \
                    'generation of socially conscious, empowered women on the rise', \
                        'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/citizens-mark'}}}, \
            {'gunas':{'GUNAS':{'rating': 'Good', 'price': '$$', 'planet_rating': '3', \
                'people_rating': '2', 'animals_rating': '5', 'message': 'GUNAS are American designer ' + \
                    'handbags that are 100% vegan and animal friendly', \
                        'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/gunas'}}}, \
            {'gymshark':{'Gymshark':{'rating': 'We avoid', 'price': '$$', 'planet_rating': '0', \
                'people_rating': '0', 'animals_rating': '0', 'message': 'Gymshark provides insufficient ' +\
                     'relevant information about how it reduces its impact on people, the planet or ' +\
                          'animals. You have a right to know how the products you buy affect the ' +\
                               'issues you care about', \
                                   'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/gymshark'}}}, \
            {'see-u-soon':{'See U Soon':{'rating': 'Not good enough', 'price': '$$', 'planet_rating': '2', \
                'people_rating': '0', 'animals_rating': '2', 'message': 'See U Soon provides ' +\
                     'insufficient relevant information about how it reduces its impact on people, ' + \
                         'the planet or animals. You have a right to know how the products you buy ' + \
                             'affect the issues you care about.', \
                                 'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/see-u-soon'}}}, \
            {'the-green-wave':{'The Green Wave':{'rating': 'Great', 'price': '$$', 'planet_rating': '5', \
                'people_rating': '5', 'animals_rating': '4', 'message': 'The Green Wave is a UK ' +\
                     'online surf shop dedicated to eco-friendly surf gear.', \
                         'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/the-green-wave'}}}, \
            {'zella':{'Zella':{'rating': 'Not Good Enough', 'price': '$$', 'planet_rating': '2', \
                'people_rating': '2', 'animals_rating': '0', 'message': 'Zella independently has ' + \
                    'made a public commitment to reduce its carbon emissions but there is no evidence ' + \
                        'it provides a living wage for its workers', \
                            'GoodOnYou_url': 'https://directory.goodonyou.eco/brand/zella'}}}, \
            ]

    # passes a single test brand_tag and calls get_data
    # as many times as there are tests
    def run_tests_separately(self):
        for idx, test in enumerate(self._tests):
            brand_tag = next(iter(test))
            correct_mapping = test[brand_tag]
            returned_mapping = self._GoodOnYou.get_data([brand_tag])
            if returned_mapping == correct_mapping:
                test_result = 'PASSED'
            else:
                test_result = 'FAILED'
            print('{} test #{} (brand_tag={}) in run_tests_separately()'.format(test_result, idx, brand_tag))

    # passes all test brand_tags in one call to get_data
    def run_tests_simultaneously(self):
        brand_tags = [next(iter(test)) for test in self._tests]
        full_data = self._GoodOnYou.get_data(brand_tags)
        for idx, test in enumerate(self._tests):
            brand_tag = next(iter(test))
            data = test[brand_tag]
            brand_name = next(iter(data))
            if brand_name in full_data and data[brand_name] == full_data[brand_name]:
                test_result = 'PASSED'
            else:
                test_result = 'FAILED'
            print('{} test #{} (brand_tag={}) in run_tests_simultaneously()'.format(test_result, idx, brand_tag))


# t = GoodOnYouTests()
# t.run_tests_separately()
# t.run_tests_simultaneously()