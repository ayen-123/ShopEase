from static import app, db
from flask import render_template, redirect, url_for, request,flash, get_flashed_messages
#import the classes from entities.py
from static.entities import *
import locale
from datetime import datetime
from static.forms import *
from flask_login import current_user, login_user,logout_user,login_required
from sqlalchemy import or_


@app.route('/')
@app.route('/main')
@login_required
def index():
    return redirect(url_for('search'))


def get():
    non_deleted_records = Item.query.filter_by(isDeleted=False).all()
    query = request.args.get('query', '')
    category = request.args.get('category', 'All')
   
    if category == 'Electronics':
        results = Electronics.query.filter((Electronics.name.ilike(f"%{query}%") | Electronics.id.ilike(f"%{query}%")) & Electronics.id.in_([item.id for item in non_deleted_records])).all()
    elif category == 'Clothing':
        results = Clothing.query.filter((Clothing.name.ilike(f"%{query}%") | Clothing.id.ilike(f"%{query}%")) & Clothing.id.in_([item.id for item in non_deleted_records])).all()
    elif category == 'Food':
        results = Food.query.filter((Food.name.ilike(f"%{query}%") | Food.id.ilike(f"%{query}%")) & Food.id.in_([item.id for item in non_deleted_records])).all()
    else:
        results = Item.query.filter((Item.name.ilike(f"%{query}%") | Item.id.ilike(f"%{query}%")) & Item.id.in_([item.id for item in non_deleted_records])).all()
   
    itemsFormatted = FormatItem(results)
    return itemsFormatted, query, category


@app.route('/search',methods=['GET', 'POST'])
@login_required
def search():
    itemsFormatted, query, category = get()
    form = AllForm()
    return render_template('index.html', items=itemsFormatted, query=query,form=form,category=category)


@app.route('/register_electronics', methods=['GET', 'POST'])
@login_required
def RegisterElectronics():
    form = ElectronicsForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        manufacturer = form.manufacturer.data
        elec_to_create = Electronics(name=name, price=price,description=description, quantity=quantity, manufacturer=manufacturer)
        similarElectronics = Electronics.query.filter(Electronics.name.like(f'%{elec_to_create.name}')).all()
        if similarElectronics:
            flash(f'Item {elec_to_create.name} is already in the database!',category='warning')
            return redirect(url_for('index'))
        else:
            db.session.add(elec_to_create)
            db.session.commit()
            flash(f'Success! Item {elec_to_create.name} has been created!', category='success')
            query = request.args.get('query','')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            itemsFormatted = FormatItem(results)
            itemsFormatted = [itemsFormatted[-1]] + itemsFormatted[:-1]
            form = ElectronicsForm()
            return render_template('index.html', items=itemsFormatted, query=query,form=form)
    
    CheckFormError(form)
    return render_template('AddElectronics.html', form=form)
   
   
@app.route('/register_clothing', methods=['GET', 'POST'])
@login_required
def RegisterClothing():
    form = ClothingForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        brand = form.brand.data
        size = form.size.data
        clothing_to_create = Clothing(name=name, price=price, description=description, quantity=quantity, brand=brand, size=size)
        similarClothing = Clothing.query.filter(Clothing.name.like(f'%{clothing_to_create.name}%')).all()
        if similarClothing:
            flash(f'Item {clothing_to_create.name} is already in the database!', category='warning')
            return redirect(url_for('index'))
        else:
            db.session.add(clothing_to_create)
            db.session.commit()
            flash(f'Success! Item {clothing_to_create.name} has been created!', category='success')
            query = request.args.get('query', '')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            itemsFormatted = FormatItem(results)
            itemsFormatted = [itemsFormatted[-1]] + itemsFormatted[:-1]
            form = ClothingForm()
            return render_template('index.html', items=itemsFormatted, query=query, form=form)

    CheckFormError(form)
    return render_template('AddClothing.html', form=form)


@app.route('/register_food', methods=['GET', 'POST'])
@login_required
def RegisterFood():
    form = FoodForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        brand = form.brand.data
        isHalalCertified = form.isHalalCertified.data
        food_to_create = Food(name=name, price=price, description=description, quantity=quantity, brand=brand, isHalalCertified=isHalalCertified)
        similar_food = Food.query.filter(Food.name.like(f'%{food_to_create.name}%')).all()
        if similar_food:
            flash(f'Item {food_to_create.name} is already in the database!', category='warning')
            return redirect(url_for('index'))
        else:
            db.session.add(food_to_create)
            db.session.commit()
            flash(f'Success! Item {food_to_create.name} has been created!', category='success')
            query = request.args.get('query', '')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            items_formatted = FormatItem(results)
            items_formatted = [items_formatted[-1]] + items_formatted[:-1]
            form = FoodForm()
            return render_template('index.html', items=items_formatted, query=query, form=form)

    CheckFormError(form)
    return render_template('AddFood.html', form=form)


@app.route('/UpdateItem/<item_id>', methods=['GET', 'POST'])
def UpdateItem(item_id):
    ItemToUpdate = Item.query.filter_by(id=item_id).first()
    if ItemToUpdate.type == "electronics":
        form = ElectronicsForm(obj=ItemToUpdate)
    elif ItemToUpdate.type == "clothing":
        form = ClothingForm(obj=ItemToUpdate)
    elif ItemToUpdate.type == "food":
        form = FoodForm(obj=ItemToUpdate)
    if form.validate_on_submit():
        form.populate_obj(ItemToUpdate)
        db.session.commit()
        flash(f'Success! The update has been committed to the database', category='success')
        return redirect(url_for('index'))
    else:
        CheckFormError(form)
    return render_template('UpdateItem.html',form=form,type=ItemToUpdate.type)


@app.route('/register_user', methods=['GET', 'POST'])
def RegisterUser():
    form = UserForm()
    if form.validate_on_submit():
        user_to_create = User(
            name=form.name.data,
            balance = form.balance.data,
            passwordHash = form.password1.data,
            birthDate = form.birthDate.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Success! User has been created!', category='success')
        return redirect(url_for('index'))
    else:
        CheckFormError(form)
    return render_template('RegisterUser.html',form=form)


@app.route('/purchase/<int:item_id>', methods =['GET', 'POST'])
def RegisterPurchase(item_id):
    ItemToBuy = Item.query.filter_by(id=item_id).first()
    form = PurchaseForm()
    form.itemToBuy.choices = [(ItemToBuy.id, f'{ItemToBuy.id}  ||   {ItemToBuy.name}')] 
   
    form.buyer.choices = [(current_user.id, f'{current_user.id}  ||   {current_user.name}')]
    if form.validate_on_submit():
        if current_user.balance >= ItemToBuy.price:
            association = item_user_association.insert().values(
                item_id=form.itemToBuy.data, 
                user_id=form.buyer.data,
                datePurchased=form.datePurchased.data)
            db.session.execute(association) 
            db.session.commit()
             
            # Update user's balance and item quantity
            current_user.balance -= ItemToBuy.price
            ItemToBuy.quantity -= 1
            db.session.commit()
            
            flash('Success! Purchase has been created', category='success')
            
            query = request.args.get('query','')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            results = FormatItem(results)
            form = ElectronicsForm()
            return redirect(url_for('index'))
        else:
            flash('Insufficient balance!', category='danger')
            return redirect(url_for('index'))
            
    CheckFormError(form)
    return render_template('RegisterPurchase.html',form=form)


@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.name.data).first()
        if attempted_user and attempted_user.checkPassword(attemptedPassword=form.password.data):
            login_user(attempted_user)
            flash(f'Success. You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('index'))
        else:
            flash('Name and/or Password does not exist in the database!',category='danger')
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('index'))


def CheckFormError(form):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

def FormatItem(items):
    locale.setlocale(locale.LC_ALL,'')
    for item in items:
        item.price = locale.format_string("%.2f", item.price, grouping=True)
    return items


@app.route('/delete/<int:item_id>', methods =['GET', 'POST'])
def Delete(item_id):
    ItemToDelete = Item.query.filter_by(id=item_id).first()
    ItemToDelete.isDeleted = True
    db.session.commit()
    flash(f'Success! Item has been deleted!', category='success')
    return redirect(url_for('index'))

@app.route('/deposit/',methods=['GET', 'POST'])
@login_required
def deposit():
    form = DepositForm()
    if form.validate_on_submit():
        amount = form.amount.data
        current_user.balance += amount
        db.session.commit()
        flash(f'Success! ₱{amount} has been added to your account!', category='success')
                   
        query = request.args.get('query','')
        results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
        results = FormatItem(results)
        form = ElectronicsForm()
        return redirect(url_for('index'))
    CheckFormError(form)
    return render_template('deposit.html',form=form)
    

@app.route('/purchaseHistory', methods =['GET','POST'])
@login_required
def PurchaseHistory():
    purchases = db.session.query(item_user_association).filter_by(user_id=current_user.id).filter_by(isDeleted=False).all()
    purchases_with_details = []
    for purchase in purchases:
        item = db.session.query(Item).filter_by(id=purchase.item_id).first()
        purchases_with_details.append({'item_name': item.name, 'datePurchased': purchase.datePurchased, 'item_price': item.price, 'id': purchase.id})
    return render_template('PurchaseHistory.html', purchases=purchases_with_details, associations=purchases)


@app.route('/deletePurchase/<int:item_user_association_id>', methods =['GET', 'POST'])
def DeletePurchase(item_user_association_id):
    db.session.execute(item_user_association.update().where(
            (item_user_association.c.id == item_user_association_id)
        ).values(isDeleted=True))
    db.session.commit()
    flash(f'Success! Purchase has been deleted!', category='success')
    return redirect(url_for('PurchaseHistory'))

@app.route('/searchPurchases', methods=['GET', 'POST'])
@login_required
def SearchPurchases():
    query = request.form.get('query', '')
    purchases = db.session.query(item_user_association).join(Item).filter(
        (item_user_association.c.user_id == current_user.id) &
        (item_user_association.c.isDeleted == False) &
        (or_(
            Item.name.ilike(f'%{query}%'),
            item_user_association.c.datePurchased.ilike(f'%{query}%'),
            Item.price.ilike(f'%{query}%'),
            item_user_association.c.id.ilike(f'%{query}%')
        ))
    ).all()

    purchases_with_details = []
    for purchase in purchases:
        item = db.session.query(Item).filter_by(id=purchase.item_id).first()
        purchases_with_details.append({'item_name': item.name, 'datePurchased': purchase.datePurchased, 'item_price': item.price, 'id': purchase.id})

    # Fetch all associations (necessary for the delete function)
    associations = db.session.query(item_user_association).filter_by(user_id=current_user.id).all()

    return render_template('PurchaseHistory.html', purchases=purchases_with_details, associations=associations)


