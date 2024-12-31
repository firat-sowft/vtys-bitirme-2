from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB bağlantısı
client = MongoClient('mongodb+srv://goymenmhmd:nZcPoO4NudGLxApx@cluster0.xue2b.mongodb.net/test?retryWrites=true&w=majority')
db = client['universities']
firat_collection = db['firatuniversity']
izmir_collection = db['izmireconomyuniversity']
comments_collection = db['yazilimMComment']
likes_collection = db['yazilimMLikes']
users_collection = db['users']
user_likes_collection = db['user_likes']
guest_interactions_collection = db['guest_interactions']  # New collection for guest interactions

@app.route('/yazilimM.html')
def firat_university_m():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Mühendislik Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    guest_interactions = list(guest_interactions_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked')] + [interaction['makale'] for interaction in guest_interactions if interaction.get('liked')]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like.get('liked'):
            like_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if interaction.get('liked'):
            like_counts[makale] += 1

    # Calculate comment counts
    comment_counts = {}
    for comment in comments:
        makale = comment['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        comment_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        if 'comments' in interaction:
            comment_counts[makale] += len(interaction['comments'])

    if university:
        print("University data found:", university)  # Hata ayıklama için veri yazdırma
        university.pop('_id', None)  # "_id" alanını şablonda göstermemek için kaldırıyoruz
        return render_template('yazilimM.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts, guest_interactions=guest_interactions)
    else:
        return "University data not found", 404

@app.route('/yazilimT.html')
def firat_university_t():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Teknoloji Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    guest_interactions = list(guest_interactions_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked')] + [interaction['makale'] for interaction in guest_interactions if interaction.get('liked')]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like.get('liked'):
            like_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if interaction.get('liked'):
            like_counts[makale] += 1

    # Calculate comment counts
    comment_counts = {}
    for comment in comments:
        makale = comment['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        comment_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        if 'comments' in interaction:
            comment_counts[makale] += len(interaction['comments'])

    if university:
        print("University data found:", university)  # Hata ayıklama için veri yazdırma
        university.pop('_id', None)  # "_id" alanını şablonda göstermemek için kaldırıyoruz
        return render_template('yazilimT.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts, guest_interactions=guest_interactions)
    else:
        return "University data not found", 404

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.json
    akademisyen = data['akademisyen']
    makale = data['makale']
    liked = data['liked']
    user_name = data['user_name']

    if user_name == 'Misafir Kullanıcı':
        guest_interactions_collection.update_one(
            {'akademisyen': akademisyen, 'makale': makale},
            {'$set': {'liked': liked}},
            upsert=True
        )
    else:
        likes_collection.update_one(
            {'akademisyen': akademisyen, 'makale': makale},
            {'$set': {'liked': liked}},
            upsert=True
        )

    return jsonify({'success': True})

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.json
    akademisyen = data['akademisyen']
    makale = data['makale']
    comment = data['comment']
    user_name = data['user_name']

    if user_name == 'Misafir Kullanıcı':
        guest_interactions_collection.update_one(
            {'akademisyen': akademisyen, 'makale': makale},
            {'$push': {'comments': {'user_name': user_name, 'comment': comment}}},
            upsert=True
        )
    else:
        comments_collection.insert_one({
            'akademisyen': akademisyen,
            'makale': makale,
            'comment': comment,
            'user_name': user_name
        })

    return jsonify({'success': True})

@app.route('/izmirE.html')
def izmir_economy_university():
    university = izmir_collection.find_one({'Bölüm': 'Yazılım Mühendisliği'})
    if not university:
        return "University data not found", 404

    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    guest_interactions = list(guest_interactions_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked')] + [interaction['makale'] for interaction in guest_interactions if interaction.get('liked')]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like.get('liked'):
            like_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if interaction.get('liked'):
            like_counts[makale] += 1

    # Calculate comment counts
    comment_counts = {}
    for comment in comments:
        makale = comment['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        comment_counts[makale] += 1
    for interaction in guest_interactions:
        makale = interaction['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        if 'comments' in interaction:
            comment_counts[makale] += len(interaction['comments'])

    university.pop('_id', None)  # "_id" alanını şablonda göstermemek için kaldırıyoruz
    return render_template('izmirE.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts, guest_interactions=guest_interactions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)