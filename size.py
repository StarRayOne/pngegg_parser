import os
num = 1
for i in range(6878):
    stats = os.stat(f'/home/hack/PycharmProjects/1. Заказы фриланс в работе/png_parser/all/images/pngimage_{num}.zip')
    print(num, stats.st_size)
    if stats.st_size <= 100:
        break
    num += 1
