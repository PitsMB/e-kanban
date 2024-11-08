from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import insert_new_coil_to_db, get_coil_tag_from_db, search_coil_tag_job_order, get_coil_detail_per_tag, delete, issue

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def home():
    return render_template('main.html')

@views.route('/job-order/', methods=["GET", "POST"])
def job_order():
    all_tags = get_coil_tag_from_db()
    search = request.args.get(key='search', default="")

    if search:
        all_tags = search_coil_tag_job_order(search)
        
    tag = request.form.get(key='tag', default="")
    supplier = request.form.get(key='supplier', default="")
    color = request.form.get(key='color', default="")
    gauge = request.form.get(key='gauge', default="")
    weight = request.form.get(key='weight', default="")
    location = request.form.get(key='location', default="")

    if request.method == 'POST':
        coil_details_to_db = tag, supplier, color, gauge, weight, location
        insert_new_coil_to_db(coil_details_to_db)
        return redirect(url_for('views.job_order'))
    
    return render_template('job-order.html', tags=all_tags)

@views.route('/job-order-issue-coil/', methods=["GET", "POST"])
def job_order_coil_issue():
    coil_tag = request.args.get('showCoilDetails')
    if not coil_tag:
        flash("Invalid coil tag", "error")
        return redirect(url_for('views.job_order'))

    coil_details = get_coil_detail_per_tag(coil_tag)
    if not coil_details:
        flash("Coil not found!", "error")
        return redirect(url_for('views.job_order'))

    return render_template('job-order-issue-coil.html', coil_tag=coil_details)

@views.route('/delete-coil/<coil_tag>', methods=["POST"])
def delete_coil(coil_tag):
    deleted = delete(coil_tag)

    if deleted:
        flash(f"Coil with tag {coil_tag} has been successfully deleted.", "success")
        return redirect(url_for('views.job_order'))
    else:
        flash(f"Failed to delete coil with tag {coil_tag}.", "error")
        return redirect(url_for('views.job_order'))
    
@views.route('/issue-coil/<coil_tag>', methods=["POST"])
def issue_coil(coil_tag):
    issue(coil_tag)
    return redirect(url_for('views.job_order'))

@views.route('/operator/')
def operator():
    return render_template('operator.html')