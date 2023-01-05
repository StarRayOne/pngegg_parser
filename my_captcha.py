import os
# directory = '/home/hack/Загрузки/'
directory = '/home/hack/Загрузки/'
files = [file for file in os.listdir(directory) if os.path.isfile(f'{directory}/{file}')]

print(len(files))
