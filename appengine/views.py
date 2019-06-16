from datetime import datetime
from django.shortcuts import render


action_dict_stable = {
    0:'Working day',
    1:'Working night',
    2:'Free day'
}

def create_gen(action):
    start = False
    for i in range(8):
        if start:
            yield action_dict_stable.get(i%3)
        if action==action_dict_stable.get(i%3):
            start = True

def get_action_by_date(period, action, date_check):
    gen_iter = create_gen(action)

    action_dict = {}
    for i in range(-2, 3):
        action_dict.update({i: next(gen_iter)})

    a = datetime.strptime(period, "%d-%m-%Y")
    b = datetime.strptime(date_check, "%d-%m-%Y")

    return action_dict.get((b - a).days%3, 'Unknown')


def intro(request):
    action=[]
    period=[]
    date_check=[]
    if request.POST:
        period = request.POST.get("datetimes")
        action = request.POST.get("controlselect")
        date_check = request.POST.get("date_check")

    if date_check:
        action_check = get_action_by_date(period, action, date_check)
    else:
        action_check =[]


    return render(request, 'index.html', context={'period': period,
                                                  'action': action,
                                                  'date_check': date_check,
                                                  'action_check': action_check})