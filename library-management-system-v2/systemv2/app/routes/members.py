from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Member

bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/')
def members():
    member_list = Member.get_all()
    return render_template('members/members.html', members=member_list)


@bp.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        if Member.create(name, email, phone, address):
            flash('Member added successfully!', 'success')
        else:
            flash('Member with this email already exists!', 'danger')

        return redirect(url_for('members.members'))

    return render_template('members/add_member.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        status = request.form['status']

        Member.update(id, name, email, phone, address, status)
        flash('Member updated successfully!', 'success')
        return redirect(url_for('members.members'))

    member = Member.get_by_id(id)
    return render_template('members/edit_member.html', member=member)


@bp.route('/delete/<int:id>')
def delete_member(id):
    Member.delete(id)
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('members.members'))
