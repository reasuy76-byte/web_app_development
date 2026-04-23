from flask import render_template, request, redirect, url_for
from app import app, db
from app.models.recipe import Recipe

@app.route('/')
@app.route('/recipes')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    if request.method == 'POST':
        new_item = Recipe(
            title=request.form['title'],
            ingredients=request.form['ingredients'],
            instructions=request.form['instructions']
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html')
