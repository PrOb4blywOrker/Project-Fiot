from flask import Blueprint, render_template, url_for, request
from flask_login import login_required, current_user
import func

main = Blueprint('main', __name__)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/search_housing', methods=['post', 'get'])
def housing():
    variants_hotels={}
    dictionary = {'auto': {'distance': [], 'time': []}, 'foot': {'distance': [], 'time': []}}
    list_description=[]
    if request.method == 'POST':
        city = request.form.get('city')
        checkin_date = request.form.get('checkin_date')
        checkout_date = request.form.get('checkout_date')
        adults_number = request.form.get('adults_number')
        children_number = request.form.get('children_number')
        if int(children_number) > 0:
            dest_if_of_city = func.search_dest_id(city)
            variants_hotels = func.search_hotels(dest_if_of_city, checkin_date, checkout_date, adults_number, children_number)
            for j in range(10):
                desc=variants_hotels[j]['unit_configuration_label']
                try:
                    desc=desc.replace("<br/>", " ")
                except:
                    pass
                try:
                    desc=desc.replace("<b>", " ")
                except:
                    pass
                try:
                    desc=desc.replace("</b>", " ")
                except:
                    pass
                list_description.append(desc)

            for i in range(10):
                latitude_hotel = variants_hotels[i]['latitude']
                longitude_hotel = variants_hotels[i]['longitude']
                result_auto = func.matrix([func.my_location().latlng, [latitude_hotel, longitude_hotel]], 0)
                result_foot = func.matrix([func.my_location().latlng, [latitude_hotel, longitude_hotel]], 1)
                dictionary['auto']['distance'].append(int(result_auto["distances"] / 1000))
                dictionary['auto']['time'].append(int(result_auto["durations"] // 3600))
                dictionary['foot']['distance'].append(int(result_foot["distances"] / 1000))
                dictionary['foot']['time'].append(int(result_foot["durations"] // 3600))
        else:
            dest_if_of_city = func.search_dest_id(city)
            variants_hotels = func.search_hotels_without_children(dest_if_of_city, checkin_date, checkout_date, adults_number)
            for j in range(10):
                desc=variants_hotels[j]['unit_configuration_label']
                try:
                    desc=desc.replace("<br/>", " ")
                except:
                    pass
                try:
                    desc=desc.replace("<b>", " ")
                except:
                    pass
                try:
                    desc=desc.replace("</b>", " ")
                except:
                    pass
                list_description.append(desc)


            for i in range(10):
                latitude_hotel = variants_hotels[i]['latitude']
                longitude_hotel = variants_hotels[i]['longitude']
                result_auto = func.matrix([func.my_location().latlng, [latitude_hotel, longitude_hotel]], 0)
                result_foot = func.matrix([func.my_location().latlng, [latitude_hotel, longitude_hotel]], 1)
                dictionary['auto']['distance'].append(int(result_auto["distances"] / 1000))
                dictionary['auto']['time'].append(int(result_auto["durations"] // 3600))
                dictionary['foot']['distance'].append(int(result_foot["distances"] / 1000))
                dictionary['foot']['time'].append(int(result_foot["durations"] // 3600))



    return render_template('housing.html', variants_hotels=variants_hotels, dictionary=dictionary, list_description=list_description)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('login.html', name=current_user.name, email=current_user.email, phone=current_user.phone, gender=current_user.gender)
