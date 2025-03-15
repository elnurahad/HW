import requests

def get_response(url):
    response = requests.get(url)
    return response


url = "https://api.github.com/elnurahad"  
response = get_response(url)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
print("Response Headers:", response.headers)