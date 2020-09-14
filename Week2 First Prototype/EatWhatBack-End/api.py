from flask import Flask,request,render_template
import EatWhatDB
import algorithm
app = Flask(__name__,static_url_path='')

sdb = EatWhatDB.ServerDBUtils()
if sdb.dbconnect() == False:
    print("DB Connect Error! Please check EatWhatDB.ini ")

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
sdb = EatWhatDB.ServerDBUtils()

@app.route('/testtmp')
def testtmp():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("testtmp.html",
        title = 'Home',
        user = user)


@app.route('/')
def index():
    return app.send_static_file('input.html')

@app.route('/input')
def index2():
    return app.send_static_file('input.html')

@app.route('/calc_recomd',methods=['POST', "GET"], strict_slashes=False)
def calc_recomd2():
    username=request.form.get('username')
    sex = int(request.form.get('sex'))
    age = int(request.form.get('age'))
    height = int(request.form.get('height'))
    weight = int(request.form.get('weight'))
    goal = int(request.form.get('goal'))
    target_weight = int(request.form.get('target_weight'))
    activity_type = float(request.form.get('activity_type'))
    # return {"username": username ,"sex": sex,"age": age , "height": height, "weight": weight, "goal": goal,"target_weight": target_weight,"activity_type": activity_type}
    user = algorithm.User(sex, age, height, weight, goal, target_weight, activity_type)
    # male, 21 years old, 170cm , 80kg , goal: lose weight ,goalWeight:70kg, activityIndex:1.2
    rs = algorithm.RecommendationSystem()
    recipe, caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed = rs.recommend(user)
    return render_template("index.html",
                           caloeryNeed=int(caloeryNeed),
                           proteinNeed=int(proteinNeed),
                           carbohydrateNeed=int(carbohydrateNeed),
                           fatNeed=int(fatNeed),
                           weeksNeed=int(weeksNeed),
                           breakfast_1=recipe[0].getFoodName(),
                           breakfast_2=recipe[1].getFoodName(),
                           breakfast_3=recipe[2].getFoodName(),
                           lunch_1=recipe[3].getFoodName(),
                           lunch_2=recipe[4].getFoodName(),
                           lunch_3=recipe[5].getFoodName(),
                           dinner_1=recipe[6].getFoodName(),
                           dinner_2=recipe[7].getFoodName(),
                           dinner_3=recipe[8].getFoodName())


if __name__ == '__main__':
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)





