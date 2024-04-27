from cgi import print_exception
from flask import Flask, redirect, render_template, request, abort
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms.forms import AddItem, RegisterForm, LoginForm, ChangeLogin, ChangePassword, ChangeSity, ChangeGender, ChangeProductInterest, BalanceIn, BalanceOut, AddStore
from data import db_session, api
from data.users import User
from data.items import Item
from data.stores import Store
from data.want_buy_item import WantBuyItem
from data.buy_item import BuyItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Item) 
    return render_template("index.html", title='Товары', current_user=current_user, items=items)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", current_user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", current_user=current_user)
        user_invite = 0
        is_invite = False
        if form.is_invite.data:
            user_invite = form.user_invite.data
            is_invite = True
        user = User(
            email=form.email.data,
            gender=form.gender.data,
            user_invite=user_invite,
            is_invite=is_invite
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Логин', form=form, current_user=current_user)


@app.route('/change_login', methods=['GET', 'POST'])
@login_required
def change_login():
    form = ChangeLogin()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('change_login.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", current_user=current_user)
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.login = form.login.data
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('change_login.html', title='Смена логина', form=form, current_user=current_user)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if form.new_password.data != form.new_password_again.data:
            return render_template('change_password.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", current_user=current_user)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db_sess.commit()
            return redirect("/personal_account")
        return render_template('change_password.html', title='Регистрация',
                                   form=form,
                                   message="Неправильный пароль", current_user=current_user)
    return render_template('change_password.html', title='Смена логина', form=form, current_user=current_user)


@app.route('/change_sity', methods=['GET', 'POST'])
@login_required
def change_sity():
    form = ChangeSity()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.sity = form.sity.data
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('change_sity.html', title='Смена города', form=form, current_user=current_user)


@app.route('/change_gender', methods=['GET', 'POST'])
@login_required
def change_gender():
    form = ChangeGender()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.gender = form.gender.data
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('change_gender.html', title='Смена пола', form=form, current_user=current_user)


@app.route('/change_product_interest', methods=['GET', 'POST'])
@login_required
def change_product_interest():
    form = ChangeProductInterest()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.the_product_of_interest = form.product_interest.data
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('change_product_interest.html', title='Смена города', form=form, current_user=current_user)


@app.route('/balance_in', methods=['GET', 'POST'])
@login_required
def balance_in():
    form = BalanceIn()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        money = int(form.money.data)
        user.balance = money + int(user.balance)
        user.all_balance_in = money + int(user.all_balance_in)
        if user.is_bonus:
            user.balance = 500 + int(user.balance)
            user.all_balance_in = 500 + int(user.all_balance_in)
            user.is_bonus = False
        if user.is_invite:
            invite_user = db_sess.query(User).filter(User.id == current_user.user_invite).first()
            invite_user.balance = int(invite_user.balance) + money * 0.1
            invite_user.all_balance_in = int(invite_user.all_balance_in) + money * 0.1
        if money >= 5000:
            user.is_bonus = True
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('balance_in.html', title='Пополнение', form=form, current_user=current_user)


@app.route('/balance_out', methods=['GET', 'POST'])
@login_required
def balance_out():
    form = BalanceOut()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        money = int(form.money.data)
        if money > int(user.balance):
            return render_template('balance_out.html', title='Вывод',
                                   form=form,
                                   message="Нельзя вывести больше чем у вас есть", current_user=current_user)
        user.balance = int(user.balance) - money
        user.all_balance_out = money * 0.8 + int(user.all_balance_out)
        db_sess.commit()
        return redirect('/personal_account')
    return render_template('balance_out.html', title='Вывод', form=form, current_user=current_user)


@app.route('/personal_account', methods=['GET', 'POST'])
@login_required
def personal_account():
    db_sess = db_session.create_session()
    want_buy_list = current_user.want_buy_list[:]
    buy_list = current_user.buy_list
    for want_buy_item in want_buy_list:
        item = db_sess.query(Item).filter(Item.id == want_buy_item.id_original_item).first()
        if item:
            want_buy_item.name = item.name
            want_buy_item.price = item.price - item.price_down
        else:
            current_user.want_buy_list.remove(want_buy_item)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/personal_account')
    return render_template("personal_account.html", title='Personal account', current_user=current_user, want_buy_list=want_buy_list, buy_list=buy_list)


@app.route('/item<id_item>', methods=['GET', 'POST'])
def items(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()
    if item:
        return render_template("item.html", title='Предмет', current_user=current_user, item=item)
    return render_template("item.html", title='Предмет', current_user=current_user, item='None')


@app.route('/additem<id_item>', methods=['GET', 'POST'])
@login_required
def add_item_count(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()
    item.count += 1
    db_sess.commit()
    return redirect('/storage')


@app.route('/changeitemsee<id_item>', methods=['GET', 'POST'])
@login_required
def change_item_see(id_item):
    if current_user.is_admin:
        db_sess = db_session.create_session()
        item = db_sess.query(Item).filter(Item.id == id_item).first()
        if item.is_see:
            item.is_see = False
        else:
            item.is_see = True
        db_sess.commit()
        return redirect('/storage')
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route('/removeitem<id_item>', methods=['GET', 'POST'])
@login_required
def remove_item(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()
    if item.count != 0:
        item.count -= 1
    db_sess.commit()
    return redirect('/storage')


@app.route('/deleteitem<id_item>', methods=['GET', 'POST'])
@login_required
def delete_item(id_item):
    if current_user.is_admin:
        db_sess = db_session.create_session()
        item = db_sess.query(Item).filter(Item.id == id_item).first()
        db_sess.delete(item)
        db_sess.commit()
        return redirect('/storage')
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route("/storage")
@login_required
def storage():
    if current_user.is_admin:
        db_sess = db_session.create_session()
        items = db_sess.query(Item)
        return render_template("storage.html", title='Склад', current_user=current_user, items=items)
    else:
            return render_template("no_permission.html", title='Недостаточно прав')


@app.route("/store_in_sity")
def store_in_sity():
    db_sess = db_session.create_session()
    stores = db_sess.query(Store)
    return render_template("store_in_sity.html", title='Наши магазины', current_user=current_user, stores=stores)


@app.route("/add_store", methods=['GET', 'POST'])
@login_required
def add_store():
    if current_user.is_admin:
        form = AddStore()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            
            store = Store(
                address=form.address.data,
                sity=form.sity.data,
                update=form.update.data
            )
            db_sess.add(store)
            db_sess.commit()

            return redirect(f'/store_in_sity')
        return render_template('add_store.html', title='Добавление магазина', form=form, current_user=current_user)
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route('/delete_store<id_store>', methods=['GET', 'POST'])
@login_required
def delete_store(id_store):
    if current_user.is_admin:
        db_sess = db_session.create_session()
        store = db_sess.query(Store).filter(Store.id == id_store).first()
        db_sess.delete(store)
        db_sess.commit()
        return redirect('/store_in_sity')
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route("/add_item", methods=['GET', 'POST'])
@login_required
def add_item():
    if current_user.is_admin:
        form = AddItem()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            
            item = Item(
                name=form.name.data,
                img=form.img.data,
                price=form.price.data,
                price_down = form.price_down.data,
                size = form.size.data,
                count = form.count.data,
                type_wear = form.type_wear.data
            )
            db_sess.add(item)
            db_sess.commit()

            return redirect(f'/item{item.id}')
        return render_template('add_item.html', title='Добавление предмета', form=form, current_user=current_user)
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route('/edit_item<id>', methods=['GET', 'POST'])
@login_required
@login_required
def edit_item(id):
    if current_user.is_admin:
        form = AddItem()
        if request.method == "GET":
            db_sess = db_session.create_session()
            item = db_sess.query(Item).filter(Item.id == id).first()
            if item:
                form.name.data = item.name
                form.img.data = item.img 
                form.price.data = item.price
                form.price_down.data = item.price_down
                form.size.data = item.size
                form.count.data = item.count
                form.type_wear.data = item.type_wear
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            item = db_sess.query(Item).filter(Item.id == id).first()
            if item:
                item.name = form.name.data
                item.img  = form.img.data
                item.price = form.price.data
                item.price_down = form.price_down.data
                item.size = form.size.data
                item.count = form.count.data
                item.type_wear = form.type_wear.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('add_item.html', title='Добавление предмета', form=form, current_user=current_user)
    else:
        return render_template("no_permission.html", title='Недостаточно прав')



@app.route("/wantbuyitem<id_item>", methods=['GET', 'POST'])
@login_required
def want_buy_item(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()
    want_buy_item = WantBuyItem(
        id_original_item=item.id,
        name=item.name,
        price=item.price - item.price_down
    )
    current_user.want_buy_list.append(want_buy_item)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/')


@app.route("/buyitem<id_item>", methods=['GET', 'POST'])
@login_required
def buy_item(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()
    want_buy_item = db_sess.query(WantBuyItem).filter(WantBuyItem.id_original_item == id_item).first()
    if want_buy_item.price <= current_user.balance and item.count > 0:
        buy_item = BuyItem(
            id_original_item=item.id,
            name=item.name,
            price=item.price - item.price_down
        )
        current_user.buy_list.append(buy_item)
        item.count -= 1
        item.count_buy += 1
        db_sess.delete(want_buy_item)
        db_sess.merge(current_user)
        db_sess.commit()
    return redirect('/personal_account')


@app.route("/removewantitem<id_item>", methods=['GET', 'POST'])
@login_required
def remove_want_item(id_item):
    db_sess = db_session.create_session()
    want_buy_item = db_sess.query(WantBuyItem).filter(WantBuyItem.id_original_item == id_item).first()
    db_sess.delete(want_buy_item)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/personal_account')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.register_blueprint(api.blueprint)
    app.run(port=8080, host='127.0.0.1')
    