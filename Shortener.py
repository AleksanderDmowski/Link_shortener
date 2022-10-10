import random


def shorter(link):
    auto_grow = True
    txt_dict = {}
    id_start = 10000
    id_end = 10999
    with open('links_database.txt', mode='r+') as database:
        for line in database:
            (k, v) = line.split()
            txt_dict.update({k: v})

        if auto_grow:
            if len(dict(txt_dict)) >= id_end-id_start:
                while id_end-id_start < len(dict(txt_dict)):
                    id_end += 1000

        if link in txt_dict:
            return str(dict(txt_dict).get(link))
        else:
            id_ = random.randint(id_start, id_end)
            x = (f'http://127.0.0.1:5000/linkShorter/{id_}')
            while x in txt_dict.values():
                id_ = random.randint(id_start, id_end)
                x = (f'http://127.0.0.1:5000/linkShorter/{id_}')
            database.write(
                f'{link} {x}\n')
            txt_dict.update({link: x})
            print(dict(txt_dict).get(link))

            return str(dict(txt_dict).get(link))


for i in range(134):
    shorter(str(i)+'s')


# def shorter(link):
#     auto_grow = True
#     txt_dict = {}
#     id_start = 10
#     id_end = 19
#     with open('links_database.txt', mode='r+') as database:
#         for line in database:
#             (k, v) = line.split()
#             txt_dict.update({k: v})
#         if auto_grow:
#             if len(dict(txt_dict)) >= id_end:

#                 while id_end < len(dict(txt_dict)):
#                     id_end += 10

#         if link in txt_dict:
#             return str(dict(txt_dict).get(link))
#         else:
#             newlink = random.randint(id_start, id_end)
#             database.write(
#                 f'{link} http://127.0.0.1:5000/linkShorter/{newlink}\n')
#             txt_dict.update({link: newlink})
#             return str(dict(txt_dict).get(link))
