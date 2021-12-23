from flask import Flask, render_template, request
import csv
import pickle
import numpy as np
import pandas as pd

dataset = pd.read_csv('./dataset/Hotels_Jakarta.csv')
cosine_simA = pickle.load(open('cosine_simA.pkl', 'rb'))
dataset = dataset.reset_index()
indices = pd.Series(dataset.index, index=dataset['hotel_name'])
all_hotels = [dataset['hotel_name'][i] for i in range(len(dataset['hotel_name']))]

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def recommend():
    hotel_name = request.form['hotel_name']
    
    idx = indices[hotel_name]
    sim_scores = list(enumerate(cosine_simA[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:12]
    hotel_indices = [i[0] for i in sim_scores]
    recommended_hotel_name = dataset['hotel_name'].iloc[hotel_indices]
    recommended_hotel_score = dataset['review_score'].iloc[hotel_indices]
    recommended_hotel_title = dataset['review_score_title'].iloc[hotel_indices]
    recommended_hotel_price =dataset['hotel_price'].iloc[hotel_indices]

    return_dataset = pd.DataFrame(columns=['hotel_name','review_score', 'review_score_title', 'hotel_price'])
    return_dataset['hotel_name'] = recommended_hotel_name
    return_dataset['review_score'] = recommended_hotel_score
    return_dataset['review_score_title'] = recommended_hotel_title
    return_dataset['hotel_price'] = recommended_hotel_price

    recommended_hotel_name = []
    recommended_hotel_score = []
    recommended_hotel_title = []
    recommended_hotel_price = []
    for i in hotel_indices[1:12]:
        recommended_hotel_name.append(dataset.iloc[i].hotel_name)
        recommended_hotel_score.append(dataset.iloc[i].review_score)
        recommended_hotel_title.append(dataset.iloc[i].review_score_title)
        recommended_hotel_price.append(dataset.iloc[i].hotel_price)

    return render_template ('index.html', search_hotel=recommended_hotel_name)

if __name__ == "__main__":
    app.run(port=3000, debug=True)