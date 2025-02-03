from flask import Flask, render_template, request, jsonify
from prisma import Prisma

app = Flask(__name__)
db = Prisma()

@app.route('/')
async def index():
    await db.connect()
    bills = await db.bill.find_many()
    await db.disconnect()
    return render_template('index.html', bills=bills)

@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('query', '')
    await db.connect()
    bills = await db.bill.find_many(where={'description': {'contains': query}})
    await db.disconnect()
    return jsonify(bills)

if __name__ == '__main__':
    app.run(debug=True)
