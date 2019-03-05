from flask import render_template, redirect, url_for,flash, request, jsonify
from main import db
from main.subscribers import subs
from main.subscribers.models import Subscriber, PairWith

from main.admin_user.utils import pop_rand

from datetime import datetime

@subs.route('/')
def home():
    return jsonify({'message':'Hello'})

@subs.route('/subscriber/<public_id>')
def pair_history(public_id):
    subscriber = Subscriber.query.filter_by(public_id=public_id).first_or_404()

    history = PairWith.query.filter_by(email = subscriber.email).all()
    paired_with = []
    for each in history:
        hist = Subscriber.query.filter_by(id=each.subs_id).first()
        hist_date = each.paired_date.strftime("%b-%d-%Y")
        paired_with.append({
                           'pair': hist,
                           'date': hist_date
                           })
    print(paired_with)
    return render_template('pair_history.html', subscriber = subscriber, paired_with = paired_with)

#GENERATE PAIRS
@subs.route('/monthly-pairing', methods=['GET','POST'])
def pairing():
    all_active = Subscriber.query.filter_by(is_active_status=True).all()

    result = []
    while len(all_active) > 0:
        rand1 = pop_rand(all_active)

        rand1_hist = PairWith.query.filter_by(email=rand1.email).all()

        rand1_hist_id = [each.subs_id for each in rand1_hist]

        try:
            rand2 = pop_rand(all_active)
        except ValueError:
            rand2 = Subscriber.query.filter_by(email = 'don@theshortcut.org').first()
        if rand2.id in rand1_hist_id:
            continue
        else:
            pair = (rand1, rand2)
            result.append(pair)

    if request.method == 'POST':

        for each, other in result:
            history = PairWith(email = each.email, subs_id= other.id)
            history2 = PairWith(email = other.email, subs_id= each.id)

            db.session.add(history)
            db.session.add(history2)
            db.session.commit()

        flash('Pairing is done.', 'success')
        return redirect(url_for('subs.monthly_history'))


    this_month = datetime.utcnow().strftime('%b-%Y')
    return render_template('pair_this_month.html', result=result, this_month=this_month, save=True)

@subs.route('/monthly-history')
def monthly_history():
    this_month = datetime.utcnow()
    year = this_month.year
    month = this_month.month
    get_date = datetime(year, month, 1)
    history = PairWith.query.all()
    pairs = [each for each in history if each.paired_date > get_date]
    result = []
    for each in pairs:
        one = Subscriber.query.filter_by(email=each.email).first()
        two = Subscriber.query.filter_by(id=each.subs_id).first()
        result.append((one,two))

    return render_template('pair_this_month.html',
                           result=result,
                           this_month=this_month.strftime("%b-%Y"))



