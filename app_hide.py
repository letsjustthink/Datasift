from flask import Flask, render_template, request, jsonify
from prisma import Prisma

app = Flask(__name__)
db = Prisma()

@app.route('/')
async def index():
    await db.connect()
    bills = await db.bill.find_many(where={"hidden": False})  # Only show non-hidden bills
    await db.disconnect()
    return render_template('index.html', bills=bills)

@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('query', '')
    tracker_filter = request.args.get('tracker', None)
    sponsor_filter = request.args.get('sponsor', None)
    cosponsor_filter = request.args.get('cosponsor', None)

    await db.connect()
    filters = {"hidden": False}  # Filter out hidden records
    
    if query:
        filters['description'] = {'contains': query}
    if tracker_filter:
        filters['tracker'] = {'equals': tracker_filter}
    if sponsor_filter:
        filters['sponsors'] = {'contains': sponsor_filter}
    if cosponsor_filter:
        filters['cosponsors'] = {'contains': cosponsor_filter}

    bills = await db.bill.find_many(where=filters)
    await db.disconnect()
    return jsonify(bills)

@app.route('/hide/<int:bill_id>', methods=['PUT'])
async def hide_bill(bill_id):
    await db.connect()
    await db.bill.update(where={"id": bill_id}, data={"hidden": True})  # Mark as hidden
    await db.disconnect()
    return jsonify({"message": "Bill hidden from results"})

@app.route('/unhide/<int:bill_id>', methods=['PUT'])
async def unhide_bill(bill_id):
    await db.connect()
    await db.bill.update(where={"id": bill_id}, data={"hidden": False})  # Mark as visible again
    await db.disconnect()
    return jsonify({"message": "Bill restored to results"})

if __name__ == '__main__':
    app.run(debug=True)
