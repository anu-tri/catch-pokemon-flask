from flask import render_template, redirect, request, flash, url_for
import requests
from flask_login import login_required,current_user
from .import bp as main
from app.models import Pokemon, User
from .forms import PokemonForm

#Routes
@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    
    if request.method == 'POST':
        if form.submit.id == "search":
            name = request.form.get('name').lower()
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            pokemon_details = []

            if response.ok:
                    #request worked
                    if not response.json():
                        return "Error loading pokemon details."
                    pokemon = response.json()
                    
                    pokemon_data={
                        'id': pokemon['id'],
                        'name': pokemon['name'],
                        'order': pokemon['order'],
                        'hp': pokemon['stats'][0]['base_stat'],
                        'defense': pokemon['stats'][2]['base_stat'],
                        'attack': pokemon['stats'][1]['base_stat'],
                        'url': pokemon['sprites']['front_shiny']
                    }
                    print(current_user.count_of_pokemon())
                    if (current_user.count_of_pokemon()) < 5:
                        new_pokemon = Pokemon()
                        new_pokemon.user_id = current_user.id
                        new_pokemon.from_dict(pokemon_data)
                        new_pokemon.save()
                        current_user.remove_duplicates()
                    pokemon_details.append(pokemon_data)
            else:
                # The request fail
                # error_string = "<br><h6>We have a problem. Please search for another pokemon.<h6>"
                # return render_template('pokemon.html.j2', error = error_string, form=form)
                flash('We could not find that entry in our database.', 'danger')
                return redirect(url_for('main.pokemon'))
                    
            return render_template('pokemon.html.j2', pokemon=pokemon_details, form=form)  
    return render_template('pokemon.html.j2', form=form)  


@main.route('/show_pokemon', methods=['GET','POST'])
@login_required
def show_pokemon():
    pokemon = current_user.pokemon.all()
    return render_template('show_pokemon.html.j2', pokemon = pokemon)

@main.route('/remove_pokemon/<int:id>', methods=['GET','POST'])
@login_required
def remove_pokemon(id):
    poke = Pokemon.query.get(id)
    # if request.method=='POST': 
    current_user.release(poke)
    flash(f'{poke.name} has been released', 'warning')
    return redirect(url_for('main.show_pokemon'))

@main.route('/add_pokemon/<int:id>', methods=['GET','POST'])
@login_required
def add_pokemon(id):
    poke = Pokemon.query.get(id)
    if request.method=='POST': 
        current_user.catch(poke)
        flash(f'{poke.name} has been caught', 'success')
        return redirect(url_for('main.pokemon'))


@main.route('/view_pokemon/<int:id>')
@login_required
def view_pokemon(id):
    poke = Pokemon.query.get(id)
    return render_template('view_pokemon.html.j2', poke = poke)
    

@main.route('/show_users_pokemon')
@login_required
def show_users_pokemon():
    users = User.query.all()
    pokemon = Pokemon.query.join(User, (Pokemon.user_id == User.id))
    return render_template('show_users_pokemon.html.j2', pokemon = pokemon, users = users)
    