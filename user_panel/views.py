from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from mould.models import Mould 
import matplotlib.pyplot as plt 
import random 
import os 

@login_required 
def homePage(request): 
    context = {}
    print(request.user)
    context['user'] = request.user 
    print("-----------------------")
    print(context['user'])
    mould_data = Mould.objects.all()
    print(type(mould_data))
    mould_data = list(mould_data)
    print(mould_data)
    main_point = -1 
    for i in range(len(mould_data)): 
        if mould_data[i].general_alert() is True: 
            main_point += 1 
            temp = mould_data[i]
            mould_data[i] = mould_data[main_point]
            mould_data[main_point] = temp 

   
    graph_for_mould_number_vs_no_of_shots()
    context['mould_data'] = mould_data 
    print("----------------------")
    return render(request, 'user_panel/user_dashboard.html', context)
    

# ------------------------------------------------------------- 
# Graph Drawer. 

def graph_for_mould_number_vs_no_of_shots(): 
    mould_data = Mould.objects.all()
    mould_id = []
    mould_shots_count = []
    bar_color = []
    color_list = ['black', 'red', 'green']
    for i in range(len(mould_data)): 
        mould_id.append(mould_data[i].mould_id)
        mould_shots_count.append(mould_data[i].present_count)
        color_index = random.randint(0, 2)
        bar_color.append(color_list[color_index])
    mould_id.sort()
    plt.bar([str(i) for i in mould_id], mould_shots_count, color = bar_color)
    plt.title('Shots vs Mould ID')
    plt.xlabel('Mould ID')
    plt.ylabel('Number of Shots')
    print(mould_id)
    print(mould_shots_count)    
    plt.savefig('user_panel/static/images/number_of_mould_vs_shots.png')
    plt.close()