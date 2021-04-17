from views import *

@views.route('/experiments')
@login_required
def experiments():
    return render_template("experiments.html")

@views.route('/experiments/experimentdata')
@login_required
def experimentdata():
    return render_template("experimentdata.html")