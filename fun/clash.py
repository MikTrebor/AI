import requests
import json
project_token = "tjDTVPaSxmmN"
run_token = "tmKTCC8QnwxF"
params = {
  "api_key": "tm2Q-fTJrnHw",
}
r = requests.post("https://www.parsehub.com/api/v2/projects/"  + project_token + "/run", data=params)

print(r.text)
print(json.load(r.text))






# import requests
# import json

# params = {
#   "api_key": "tm2Q-fTJrnHw",
#   "format": "json"
# }
# # project_token = 'tjDTVPaSxmmN'
# project_token = 'tBXSHY7TeQgN'
# r = requests.get('https://www.parsehub.com/api/v2/runs/' + project_token + '/data', params=params)
# print(r.text)
# scores = json.loads(r.text)
# print(scores)
# print(scores["akuDonates"])
