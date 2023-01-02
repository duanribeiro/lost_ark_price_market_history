from settings import mongo_db, logger
import json
from bson.json_util import dumps
from datetime import datetime
import yagmail



mongo_collection_emails = mongo_db["email_events"]
mongo_collection_prices = mongo_db["prices"]


def send_email(to, data, id):
    logger.warning(f'Sending email to {to}')

    user = 'lostarkmarketalerts@gmail.com'
    app_password = 'qodnrjopvnrxhcrw'  # a token for gmail
    subject = 'lostarkmarket.com - Alert item founded'
    body = """
    <h3>Email alert from www.lostarkmarket.com</h3>
    <table>
      <tr>
        <th>Name</th>
        <th>Minimum bid</th>
        <th>Buy now price</th>
        <th>Quality</th>
        <th>Time Left</th>
        <th>Bonus Effect</th>
        <th>Engraving Effect</th>
      </tr>
    """
    for item in data:
        body += f"""
          <tr>
            <td>{item['name']}</td>
            <td>{item['minimum_bid']}</td>
            <td>{item['buy_now_price']}</td>
            <td>{item['quality']}</td>
            <td>{item['time_left']}</td>
            <td>{json.dumps(item['bonus_effect'])}</td>
            <td>{json.dumps(item['engraving_effect'])}</td>
          </tr>
        """
    body += f"""
        </table>
        <p>If you dont want to receive more emails on this alert <a href="https://lostarkmarket.com/delete_email_alert?id={id}">CLICK HERE TO UNSUBSCRIBE!</a></p>
    """

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, body)


def switch_operator(operation):
    if operation == '>=':
        return '$gte'
    if operation == '>':
        return '$gt'
    if operation == '=':
        return '$eq'
    if operation == '<=':
        return '$lte'
    if operation == '>=':
        return '$lt'


def search_item(payload):
    pipeline = []
    pipeline.append({"$project": {"_id": 0}})
    if payload['region']:
        pipeline.append({"$match": {"region": payload['region']}})
    if payload['name']:
        pipeline.append({"$match": {"name": payload['name']}})
    if payload['type']:
        pipeline.append({"$match": {"type": payload['type']}})
    if payload['minimum_bid']['value']:
        value = payload['minimum_bid']['value']
        operation = payload['minimum_bid']['operation']
        pipeline.append({"$match": {"minimum_bid": {switch_operator(operation): value}}})
    if payload['buy_now_price']['value']:
        value = payload['buy_now_price']['value']
        operation = payload['buy_now_price']['operation']
        pipeline.append({"$match": {"buy_now_price": {switch_operator(operation): value}}})
    if payload['traded_times']['value']:
        value = payload['traded_times']['value']
        operation = payload['traded_times']['operation']
        pipeline.append({"$match": {"traded_times": {switch_operator(operation): value}}})
    if payload['quality']['value']:
        value = payload['quality']['value']
        operation = payload['quality']['operation']
        pipeline.append({"$match": {"quality": {switch_operator(operation): value}}})

    if payload['basic_effect']['Strength']['value']:
        value = payload['basic_effect']['Strength']['value']
        operation = payload['basic_effect']['Strength']['operation']
        pipeline.append({"$match": {'basic_effect.Strength': {switch_operator(operation): value}}})
    if payload['basic_effect']['Dexterity']['value']:
        value = payload['basic_effect']['Dexterity']['value']
        operation = payload['basic_effect']['Dexterity']['operation']
        pipeline.append({"$match": {'basic_effect.Dexterity': {switch_operator(operation): value}}})
    if payload['basic_effect']['Intelligence']['value']:
        value = payload['basic_effect']['Intelligence']['value']
        operation = payload['basic_effect']['Intelligence']['operation']
        pipeline.append({"$match": {'basic_effect.Intelligence': {switch_operator(operation): value}}})
    if payload['basic_effect']['Vitality']['value']:
        value = payload['basic_effect']['Vitality']['value']
        operation = payload['basic_effect']['Vitality']['operation']
        pipeline.append({"$match": {'basic_effect.Vitality': {switch_operator(operation): value}}})

    if payload['bonus_effect']['Crit']['value']:
        value = payload['bonus_effect']['Crit']['value']
        operation = payload['bonus_effect']['Crit']['operation']
        pipeline.append({"$match": {'bonus_effect.Crit': {switch_operator(operation): value}}})
    if payload['bonus_effect']['Specialization']['value']:
        value = payload['bonus_effect']['Specialization']['value']
        operation = payload['bonus_effect']['Specialization']['operation']
        pipeline.append({"$match": {'bonus_effect.Specialization': {switch_operator(operation): value}}})
    if payload['bonus_effect']['Domination']['value']:
        value = payload['bonus_effect']['Domination']['value']
        operation = payload['bonus_effect']['Domination']['operation']
        pipeline.append({"$match": {'bonus_effect.Domination': {switch_operator(operation): value}}})
    if payload['bonus_effect']['Swiftness']['value']:
        value = payload['bonus_effect']['Swiftness']['value']
        operation = payload['bonus_effect']['Swiftness']['operation']
        pipeline.append({"$match": {'bonus_effect.Swiftness': {switch_operator(operation): value}}})
    if payload['bonus_effect']['Endurance']['value']:
        value = payload['bonus_effect']['Endurance']['value']
        operation = payload['bonus_effect']['Endurance']['operation']
        pipeline.append({"$match": {'bonus_effect.Endurance': {switch_operator(operation): value}}})
    if payload['bonus_effect']['Expertise']['value']:
        value = payload['bonus_effect']['Expertise']['value']
        operation = payload['bonus_effect']['Expertise']['operation']
        pipeline.append({"$match": {'bonus_effect.Expertise': {switch_operator(operation): value}}})

    if payload['engraving_effect']['engraving_1']['name']:
        name = payload['engraving_effect']['engraving_1']['name']
        value = payload['engraving_effect']['engraving_1']['value']
        operation = payload['engraving_effect']['engraving_1']['operation']
        pipeline.append({"$match": {f"engraving_effect.{name}": {switch_operator(operation): value}}})
    if payload['engraving_effect']['engraving_2']['name']:
        name = payload['engraving_effect']['engraving_2']['name']
        value = payload['engraving_effect']['engraving_2']['value']
        operation = payload['engraving_effect']['engraving_2']['operation']
        pipeline.append({"$match": {f"engraving_effect.{name}": {switch_operator(operation): value}}})
    if payload['engraving_effect']['engraving_3']['name']:
        name = payload['engraving_effect']['engraving_3']['name']
        value = payload['engraving_effect']['engraving_3']['value']
        operation = payload['engraving_effect']['engraving_3']['operation']
        pipeline.append({"$match": {f"engraving_effect.{name}": {switch_operator(operation): value}}})

    response = list(mongo_collection_prices.aggregate(pipeline=pipeline))

    if response:
        for item in response:
            item["timestamp"] = datetime.strftime(item["timestamp"], "%Y-%m-%d %H:%M")
        return {
            "data": json.loads(dumps(response)),
        }
    else:
        return []


def send_emails():
    responses = list(mongo_collection_emails.find())
    for response in responses:
        payload = response['searchBoxState']
        has_item = search_item(payload=payload)
        if has_item:
            data = has_item['data']
            send_email(to=response['email'], data=data, id=response['_id'])


if __name__ == "__main__":
    send_emails()
    print('sending emails')