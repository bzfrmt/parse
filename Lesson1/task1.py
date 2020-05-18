from pprint import pprint
import requests
import json
main_link = 'https://api.github.com/users/bzfrmt/repos'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}

response = requests.get(main_link,headers=header)
#print (response)
if response.ok:
    data = json.loads(response.text)
    if len(data)>0:
        print('Список репозиториев пользователя:')
        for repo in data:
            print(repo['name'],repo['url'])

        with open('task1.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    else:
        print('Репозитории у пользователя отсутствуют')









# with open('file.pdf','wb') as f:
#     f.write(response.content)
