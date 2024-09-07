'''Este archivo devuelve las funciones correspondientes para la API'''

import pandas as pd

'''sklearn no se ejecuta en este branch del proyecto, pues Render no posee memoria suficiente. Deberá ejecutarse en local'''
# from sklearn.neighbors import NearestNeighbors
# from sklearn.preprocessing import OneHotEncoder

movies = pd.read_parquet('Machine Learning Model/movies_dataset_cleaned.parquet', engine='pyarrow')
actors = pd.read_parquet('Machine Learning Model/actors.parquet', engine='pyarrow')
crew = pd.read_parquet('Machine Learning Model/crew.parquet', engine='pyarrow')
ml_dataset = pd.read_parquet('Machine Learning Model/final_movie_set.parquet', engine='pyarrow')

def cantidad_filmaciones_mes(mes):
  meses = {
        'enero':1,
        'febrero':2,
        'marzo':3,
        'abril':4,
        'mayo':5,
        'junio':6,
        'julio':7,
        'agosto':8,
        'septiembre':9,
        'octubre':10,
        'noviembre':11,
        'diciembre':12
    }
  valor = meses[mes]
  movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
  return movies[movies['release_date'].dt.month == valor]['release_date'].count()


def cantidad_filmaciones_dia(dia):
  dias = {
    'lunes':'Monday',
    'martes':'Tuesday',
    'miercoles':'Wednesday',
    'jueves':'Thursday',
    'viernes':'Friday',
    'sabado':'Saturday',
    'domingo':'Sunday'
  }
  valor = dias[dia]
  movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
  return movies[movies['release_date'].dt.strftime('%A') == valor]['release_date'].count()

def total_votos(titulo=''):
  titulo = titulo.title()
  movies['title'] = movies['title'].str.title()
  movie_to_return = movies.iloc[movies.index[movies['title'] == titulo]]
  if movie_to_return['vote_count'].iloc[0] >= 2000:
    return {'message': f"La pelicula {movie_to_return['title'].iloc[0]} fue estrenada el año {movie_to_return['release_year'].iloc[0]}. La misma cuenta con un total de {movie_to_return['vote_count'].iloc[0].astype(int)} valoraciones, con un promedio de {movie_to_return['vote_average'].iloc[0].round(2)}"}
  else:
    return {'message':'La pelicula no cuenta con la cantidad de votaciones requerida para mostrar la informacion'}


def score_titulo(titulo=''):
  titulo = titulo.title()
  movies['title'] = movies['title'].str.title()
  movie_to_return = movies.iloc[movies.index[movies['title']==titulo]]
  return {'message': f"La pelicula {movie_to_return['title'].iloc[0]} fue estrenada el año {movie_to_return['release_year'].iloc[0]} con un score/popularidad de {movie_to_return['popularity'].iloc[0].round(2)}"}


def get_actor(actor=''):
  actor = actor.title()
  revenue = movies[['id','revenue']]
  revenue_actor = actors[['id','actor_name']].join(revenue.set_index('id'),on='id',how='left')
  return_movies = revenue_actor[revenue_actor['actor_name']==actor]['revenue'].sum()
  total_movies = revenue_actor[revenue_actor['actor_name']==actor]['revenue'].count()
  return_avg = revenue_actor[revenue_actor['actor_name']==actor]['revenue'].mean()
  return {'message':f"{actor} ha participado de {total_movies} cantidad de filmaciones. Ha conseguido un retorno de {'${:,.2f}'.format(return_movies)} con un promedio de {'${:,.2f}'.format(return_avg)} por filmación"}

def get_director(director=''):
  movie_costs = movies[['id','title','budget','revenue','release_date']].set_index('id')
  directors = crew[(crew['crew_job']=='Director')&(crew['crew_name']==director)]
  directors_movies = directors.join(movie_costs,on='id',how='left')
  return directors_movies[['id','title','crew_name','crew_job','revenue','budget','release_date']].rename(columns={'crew_name':'director_name','crew_job':'job'}).to_dict(orient='records')


'''Esta es la función de recomendación, se deja inactiva para la ejecución en Render'''

# def recommend_movie(title=""):
#   movie_title = ml_dataset["title"]
#   encoder = OneHotEncoder()
#   title_encoded = encoder.fit_transform(movie_title.values.reshape(-1,1))
#   recommender = NearestNeighbors(metric='cosine')
#   recommender.fit(title_encoded)

#   title_index = ml_dataset.index[ml_dataset['title']==title]
#   num_recommendations = 8

#   _, recommendations2 = recommender.kneighbors(title_encoded[title_index].toarray(), n_neighbors=num_recommendations)
#   recommended_movie_titles = ml_dataset.iloc[recommendations2[0]]['title']
#   return {'recommended_movies':list(recommended_movie_titles.values[-5:])}