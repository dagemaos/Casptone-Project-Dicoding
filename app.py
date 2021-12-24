from flask import Flask, render_template, request
import csv
import pickle
import numpy as np
import pandas as pd

dataset = pd.read_csv('./dataset/Hotels_Jakarta.csv')
cosine_simA = pickle.load(open('cosine_simA.pkl', 'rb'))
dataset = dataset.reset_index()
indices = pd.Series(dataset.index, index=dataset['hotel_name'])

app = Flask(__name__)

def recommend(hotel_name):
    idx = indices[hotel_name]
    sim_scores = list(enumerate(cosine_simA[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[2:12]
    hotel_indices = [i[0] for i in sim_scores]
    recommended_hotel_names = dataset['hotel_name'].iloc[hotel_indices]
    recommended_hotel_scores = dataset['review_score'].iloc[hotel_indices]
    recommended_hotel_titles = dataset['review_score_title'].iloc[hotel_indices]
    recommended_hotel_prices =dataset['hotel_price'].iloc[hotel_indices]

    return_dataset = pd.DataFrame(columns=['hotel_name','review_score', 'review_score_title', 'hotel_price'])
    return_dataset['hotel_name'] = recommended_hotel_names
    return_dataset['review_score'] = recommended_hotel_scores
    return_dataset['review_score_title'] = recommended_hotel_titles
    return_dataset['hotel_price'] = recommended_hotel_prices

    return return_dataset

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return(render_template('index.html'))

    if request.method == 'POST':
        hotel_name = request.form['hotel_name']
        result_final = recommend(hotel_name)
        recommended_hotel_name = []
        recommended_hotel_score = []
        recommended_hotel_title = []
        recommended_hotel_price = []
        for i in range(len(result_final)):
            recommended_hotel_name.append(result_final.iloc[i][0])
            recommended_hotel_score.append(result_final.iloc[i][1])
            recommended_hotel_title.append(result_final.iloc[i][2])
            recommended_hotel_price.append(result_final.iloc[i][3])

    return render_template ('hasil.html', hotel_names=recommended_hotel_name, hotel_scores=recommended_hotel_score, hotel_titles=recommended_hotel_title, hotel_prices=recommended_hotel_price, search_hotel=hotel_name)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
