from flask import Flask, request, jsonify

from db import db, init_db
# from db import *
from users import Users
from organizations import Organizations

app = Flask(__name__)
#                                               VVVV conn = psycopg2.connect("dbname='usermgt' user='blake' host='localhost'")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user@localhost:5432/alchemy'
# normally definition is kept in private environment so it doesn't become publicly available. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app,db)

def create_all():
    with app.app_context():
        print('Creating tables...')
        db.create_all()
        print('All done')



@app.route('/user/add', methods=['POST'])
def user_add():
    post_data = request.form
    if not post_data:
        post_data = request.json

    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    add_user(first_name, last_name, email, phone, city, state, org_id, active)

    return jsonify('User created'), 201

def add_user(f_name,l_name,email,phone,city,state,org_id,active):
    new_user = Users(f_name, l_name, email, phone, city, state, org_id, active)

    db.session.add(new_user)
    #     ^^ this statement is where the magic happens, 

    db.session.commit()


@app.route('/user/get-all', methods=['GET'])
def get_all_active_users():
    users_data = db.session.query(Users).filter(Users.active == True).all()

    formatted_users_data = []
    for user_data in users_data:
        user = {
          'user_id':user_data.user_id,
          'first_name':user_data.first_name,
          'last_name':user_data.last_name,
          'email':user_data.email,
          'phone':user_data.phone,
          'city':user_data.city,
          'state':user_data.state,
          'org_id':user_data.org_id,
          'active':user_data.active
        }
        formatted_users_data.append(user)

    if users_data:
        return jsonify(formatted_users_data), 200

    else: 
        return jsonify('No Users found'), 404

# breaks if duplicate email is put in. 
# also breaks if invalid user_id is put in 
@app.route('/user/update/<user_id>', methods=['POST', 'PUT', 'PATCH'])
def update_user(user_id):
    post_data = request.json
    if not post_data:
       post_data = request.form

    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    user_data = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_data:
        user_data.user_id = user_id
        if first_name is not None:
            user_data.first_name = first_name
        if last_name is not None:
            user_data.last_name = last_name
        if email is not None:
            user_data.email = email
        if phone is not None:
            user_data.phone = phone
        if city is not None:
            user_data.city = city
        if state is not None:
            user_data.state = state
        if org_id is not None:
            user_data.org_id = org_id
        if active is not None:
            user_data.active = active

        db.session.commit()
        user_data = db.session.query(Users).filter(Users.user_id == user_id).first()


        user_obj = {
          'user_id': user_data.user_id,
          'first_name':user_data.first_name,
          'last_name':user_data.last_name,
          'email':user_data.email,
          'phone':user_data.phone,
          'city':user_data.city,
          'state':user_data.state,
          'org_id':user_data.org_id,
          'active':user_data.active
        }
        
        return jsonify(user_obj), 200
    
    else:
        return jsonify('No User Found'), 404


@app.route('/user/delete', methods=['DELETE'])
def delete_user():
    post_data = request.json
    if not post_data:
        post_data = request.form

    user_id = post_data.get('user_id')
    user_data = db.session.query(Users).filter(Users.user_id == user_id).first()
    username = f'{user_data.first_name} {user_data.last_name}'
    db.session.delete(user_data)
    db.session.commit()

    return jsonify(f'User: {username} deleted'), 200
            

@app.route('/org/add', methods=['POST'])
def add_org_route():
    data = request.form if request.form else request.json
    print(data)

    name = data.get('name')
    phone = data.get('phone')
    city = data.get('city')
    state = data.get('state')
    active = data.get('active')

    add_org(name,phone,city,state,active)

    return jsonify('Org Created'), 200


def add_org(name,phone,city,state,active):
    new_org = Organizations(name, phone, city, state, active)
    db.session.add(new_org)
    db.session.commit()

@app.route('/org/get-all', methods=['GET'])
def get_all_active_orgs():
    orgs_data = db.session.query(Organizations).filter(Organizations.active == True).all()

    formatted_orgs_data = []
    for org_data in orgs_data:
        org = {
            'org_id':org_data.org_id,  
            'name':org_data.name,  
            'phone':org_data.phone,  
            'city':org_data.city,  
            'state':org_data.state,  
            'active':org_data.active  
        }
        formatted_orgs_data.append(org)

    if orgs_data:
        return jsonify(formatted_orgs_data), 200

    else: 
        return jsonify('No Organizations found'), 404


@app.route('/org/update/<org_id>', methods=['POST', 'PUT', 'PATCH'])
def update_org(org_id):
    post_data = request.json
    if not post_data:
       post_data = request.form

    name = post_data.get('name')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    active = post_data.get('active')

    org_data = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

    if org_data:
        org_data.org_id = org_id
        if name is not None:
            org_data.name = name
        if phone is not None:
            org_data.phone = phone
        if city is not None:
            org_data.city = city
        if state is not None:
            org_data.state = state
        if active is not None:
            org_data.active = active

        db.session.commit()

        org_data = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
        org_obj = {
          'name': org_data.name,
          'phone': org_data.phone,
          'city': org_data.city,
          'state': org_data.state,
          'active': org_data.active
        }
        
        return jsonify(org_obj), 200

@app.route('/org/delete', methods=['DELETE'])
def delete_org():
    post_data = request.json
    if not post_data:
        post_data = request.form

    org_id = post_data.get('org_id')
    org_data = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    org_name = org_data.name
    db.session.delete(org_data)
    db.session.commit()

    return jsonify(f'Organization: {org_name} deleted'), 200

'''
TODO: CRUDDA
Users
(√)Get all
(√)Update
()Delete
()Deactivate
()Activate

Organizations:
(√)Get all
(√)Update
()Delete
()Deactivate
()Activate

    post_data = request.json
    if not post_data:
        post_data = request.form
    
'''









if __name__ == '__main__':
    create_all()
    app.run(port=8089)