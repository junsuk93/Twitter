from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import operator
app = Flask(__name__)
client = MongoClient()
db = client['tw_db']
collection = db.tweet


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        input1 = request.form['Finput']
        input2 = request.form['Sinput']
        db1 = collection.find({'text': {'$regex': input1}})
        db2 = collection.find({'text': {'$regex': input2}})
        ne1 = {}
        ne2 = {}
        analy1 = []
        analy2 = []
        result1 = []
        result2 =[]

        for k in db1:
            result1.append(k)
            list1 = k['NE']
            for p in list1:
                if p in ne1.keys():
                    ne1[p] += 1
                else:
                    ne1[p] = 1
        for k in db2:
            result2.append(k)
            list2 = k['NE']
            for p in list2:
                if p in ne2.keys():
                    ne2[p] += 1
                else:
                    ne2[p] = 1

        sorted1 = sorted(ne1.items(), key = operator.itemgetter(1), reverse = True)
        sorted2 = sorted(ne2.items(), key = operator.itemgetter(1), reverse = True)

        index = 0
        for t in sorted1:
            if index is 15:
                break
            analy1.append(list(t))
            index += 1

        index = 0
        for t in sorted2:
            if index is 15:
                break
            analy2.append(list(t))
            index += 1

    print(analy1)
    print(analy2)
    return render_template('search.html',
                           input1 = input1,
                           input2 = input2,
                           result1=result1,
                           result2=result2,
                           analy1 = analy1,
                           analy2 = analy2)



if __name__ == '__main__':
    app.run()
