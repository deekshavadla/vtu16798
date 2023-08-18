import requests
from flask import Flask, request, jsonify
import concurrent.futures
import time

app=Flask(__name__)
def fetch_numbers_from_url(url):
    try:
        response=requests.get(url,timeout=0.5)
        if(response.status_code==200):
            return response.json().get("numbers",[])
    except requests.exceptions.Timeout:
        pass
    except Exception as e:
        print("error in fetching the numbers from url",e)
    return[]

@app.route('/numbers',methods=['GET'])
def get_numbers():
    urls=request.args.getlist('url')
    all_numbers=set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls))as executor:
        results=executor.map(fetch_numbers_from_url,urls)

        for numbers in results:
            all_numbers.update(numbers)
    sorted_numbers=sorted(all_numbers)
    return jsonify(numbers=sorted_numbers)
if __name__=='__main__':
    app.run(host='localhost',port=8008)