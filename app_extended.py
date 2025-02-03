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

@app.route('/add', methods=['POST'])
async def add_bill():
    data = request.json
    await db.connect()
    new_bill = await db.bill.create(data={"description": data["description"]})
    await db.disconnect()
    return jsonify(new_bill)

@app.route('/edit/<int:bill_id>', methods=['PUT'])
async def edit_bill(bill_id):
    data = request.json
    await db.connect()
    updated_bill = await db.bill.update(where={"id": bill_id}, data={"description": data["description"]})
    await db.disconnect()
    return jsonify(updated_bill)

@app.route('/delete/<int:bill_id>', methods=['DELETE'])
async def delete_bill(bill_id):
    await db.connect()
    await db.bill.delete(where={"id": bill_id})
    await db.disconnect()
    return jsonify({"message": "Bill deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
