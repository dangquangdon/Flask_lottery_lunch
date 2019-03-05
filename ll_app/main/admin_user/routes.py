from flask import (render_template,
                   flash,
                   redirect,
                   url_for,
                   abort,
                   request)
from main.admin_user import adm
from main.admin_user.forms import AdminLoginForm, CreateAdminForm

from main.subscribers.models import Subscriber
from main import bcrypt, db

from flask_login import (login_user,
                         logout_user,
                         current_user,
                         login_required)

from .utils import is_safe_url
from datetime import datetime



# ADMIN HOME PAGE
@adm.route('/admin-home')
@login_required
def admin_home():
    all = len(Subscriber.query.all())
    num_admin = len(Subscriber.query.filter_by(is_admin=True).all())
    num_active = len(Subscriber.query.filter_by(is_active=True).all())

    active_rate = round(num_active/all,3)*100

    print("From home ",current_user)
    return render_template('admin_dashboard.html',
                           all = all,
                           num_admin = num_admin,
                           num_active = num_active,
                           active_rate = active_rate)

# ADMIN LOGIN PAGE
@adm.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        subscriber = Subscriber.query.filter_by(email=email).first()

        if subscriber and bcrypt.check_password_hash(subscriber.password,
                                                    form.password.data):
            login_user(subscriber, remember = form.remember.data)
            print("after check password",subscriber)
            flash('Welcome back, {}'.format(subscriber.first_name), 'success')
            next_page = request.args.get('next')

            if not is_safe_url(next_page):
                print(current_user)
                return abort(400)

            print("From login form",current_user)

            return redirect(next_page or url_for('adm.admin_home'))
        else:
            flash('Invalid Credentials','danger')

    return render_template('admin_login.html', form=form)

# ADMIN ADD NEW USER PAGE
@adm.route('/admin-add-user', methods=['GET','POST'])
@login_required
def admin_add_user():
    form = CreateAdminForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_admin = True

        new_admin = Subscriber(first_name = first_name,
                               last_name = last_name,
                               email = email,
                               password = password,
                               is_admin = is_admin)
        db.session.add(new_admin)
        db.session.commit()

        flash('New admin user is created for {}'.format(first_name), 'success')
        return redirect(url_for('adm.admin_home'))
    return render_template('admin_add_user.html', form=form)

# ADMIN LOGOUT
@adm.route('/admin-logout')
def admin_logout():
    logout_user()
    return redirect(url_for('adm.admin_login'))

# SHOW TABLE OF ALL SUBSCRIBERS
@adm.route('/datatable')
@login_required
def data_table():
    subscribers = Subscriber.query.filter_by(is_admin=False).order_by(Subscriber.join_date.desc())
    return render_template('subscriber_datatable.html',
                           subscribers = subscribers)

# SHOW TABLE OF ALL ADMIN USERS
@adm.route('/admin-table')
@login_required
def admin_table():
    admins = Subscriber.query.filter_by(is_admin=True)
    return render_template('admin_datatable.html',
                           admins = admins)

# PROMOTE TO ADMIN USER
@adm.route('/promote-to-admin/<public_id>', methods=['GET','POST'])
@login_required
def promote(public_id):
    user = Subscriber.query.filter_by(public_id = public_id).first()

    if not user.is_admin:
        user.is_admin = True

        db.session.commit()
        flash('Promoted {} to Admin'.format(user.first_name))

    return redirect(url_for('adm.admin_table'))

# DEMOTE TO SUBSCRIBER
@adm.route('/remove-admin-right/<public_id>', methods=['GET','POST'])
@login_required
def remove_admin_right(public_id):
    user = Subscriber.query.filter_by(public_id = public_id).first()

    if user.is_admin:
        user.is_admin = False

        db.session.commit()
        flash('Move {} to Subscribers list'.format(user.first_name))

    return redirect(url_for('adm.data_table'))

# CHANGE ACTIVE STATUS
@adm.route('/activate/<public_id>', methods=['GET','POST'])
@login_required
def activate(public_id):
    user = Subscriber.query.filter_by(public_id = public_id).first()

    if user:
        user.is_active_status = not user.is_active_status

        db.session.commit()
        flash('Status changed!', 'success')

    return redirect(url_for('adm.data_table'))
