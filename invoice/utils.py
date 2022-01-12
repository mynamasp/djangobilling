# product_code:['name','rate 1','rate 2','rate 3']
menu = {'101A': ['Brown rice', 50, 45.50, 41.25],
        '102B': ['Whole wheat', 30, 27.45, 21.50],
        '102C': ['Tomato sauce', 25.50, 20.25, 18.70],
        '103D': ['Mustard', 40, 39.45, 37],
        '104E': ['Barbecue sauce', 45, 43, 41.50],
        '105F': ['Red-wine vinegar', 4000, 3800, 3750],
        '106G': ['Salsa', 200, 189.50, 170],
        '107H': ['Extra virgin olive oil', 500, 478.50, 455.70],
        '108I': ['canola oil', 200, 180, 118],
        '109J': ['Hot pepper sauce', 100, 98.50, 91.25],
        '110K': ['Bananas', 60, 55, 50],
        '111L': ['Apples', 300, 250, 120],
        '112M': ['Oranges', 200, 140, 110],
        '113N': ['Mangoes', 100, 80, 50],
        '114O': ['Strawberries', 100, 90, 80],
        '115P': ['Blueberries', 95, 8, 75],
        '116Q': ['Green teas', 250, 225, 200],
        '117R': ['Sparkling water', 20, 14.50, 11],
        '118S': ['Dried apricots', 270, 250, 230],
        '119T': ['Dried figs', 100, 95, 90],
        '120U': ['Dried prunes', 90, 85, 80],
        '121V': ['Almonds', 900, 870, 850],
        '122W': ['Cashews', 1000, 950, 910],
        '123X': ['Walnuts', 800, 770, 720],
        '124Y': ['Peanuts', 400, 380, 360],
        '125Z': ['Pecans', 350, 320, 300],
        '201A': ['Pistachios', 1200, 1180, 1160],
        '202B': ['Sunflower seeds', 150, 112.50, 103.45],
        '203C': ['Sesame seeds', 120.50, 110.25, 101.40],
        '204D': ['Whole flaxseeds', 95.20, 90.45, 89.20]}

# 'customer_id':['name','phone_no']
customer_registry = {'AAA1001': ['Surian', '9500012345'],
                     'AAA1002': ['Nila', '9500023456'],
                     'AAA1003': ['Arivazhagan', '9712300078'],
                     'AAA1004': ['Nithin Kumar', '9586233333'],
                     'AAA1005': ['Aravind', '6931245872']}


def calculate_discount(amount, registry_found):
    if amount >= 10000:
        if registry_found:
            discount = (3 / 100) * amount
            total_amount = amount - ((3 / 100) * amount)
        else:
            discount = (1.5 / 100) * amount
            total_amount = amount - ((1.5 / 100) * amount)
    else:
        discount = 0
        total_amount = amount
    return {'discount': round(discount,2), 'total_amount': round(total_amount,2)}



# interfacing with django

def getmenu():
    return menu


def getcustomer():
    return customer_registry
