from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  #  ここに秘密鍵を設定してください

#  シンプルなユーザーデータの辞書(適宜DB接続等実施してください)
users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'}
}

#  一覧表示する情報の辞書
communities = {
    'community1': {
        'name': 'Community  1',
        'secretary': 'Secretary  1',
        'overview': 'This is community  1.',
        'contact': 'contact1@example.com'
    },
    'community2': {
        'name': 'Community  2',
        'secretary': 'Secretary  2',
        'overview': 'This is community  2.',
        'contact': 'contact2@example.com'
    }
}

@app.route("/")
def main_page():
    return render_template('login.html')

#  ログイン処理
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #  画面で入力された情報を取得
        username = request.form['username']
        password = request.form['password']

        #  ログイン可否を判定
        if username in users and users[username]['password'] == password:
            session['username'] = username

            #  ログイン成功でdashboard.htmlを返す
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    # GETの場合はログイン画面へ戻す
    return render_template('login.html')

# URL直接参照の場合
@app.route('/home')
def home():
    #  ログインしている場合はdashboard.htmlへ
    if 'username' in session:
        return render_template('home.html')  #  ファイル名を修正
    else:
        return redirect(url_for('login'))

#  ログアウト機能
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#  ダッシュボードページで一覧表示
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', communities=communities)
    else:
        return redirect(url_for('login'))

@app.route('/selected_communities', methods=['POST'])
def selected_communities():
    selected_communities_ids = request.form.getlist('selected_communities')
    #  ここで選択されたコミュニティーに対する処理を実行
    #  例:  選択されたコミュニティーの詳細を表示するなど
    return redirect(url_for('dashboard'))  #  ダッシュボードにリダイレクト

#  ダッシュボードページで項目を登録
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if 'username' in session:
            name = request.form['name']
            secretary = request.form['secretary']
            overview = request.form['overview']
            contact = request.form['contact']
            new_community_id = f'community{len(communities) +  1}'
            communities[new_community_id] = {
                'name': name,
                'secretary': secretary,
                'overview': overview,
                'contact': contact
            }
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('add_item.html')
    
# 項目の編集
@app.route('/edit_item/<community_id>', methods=['GET', 'POST'])
def edit_item(community_id):
    if request.method == 'POST':
        if 'username' in session:
            name = request.form['name']
            secretary = request.form['secretary']
            overview = request.form['overview']
            contact = request.form['contact']
            communities[community_id] = {
                'name': name,
                'secretary': secretary,
                'overview': overview,
                'contact': contact
            }
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    else:
        if community_id in communities:
            return render_template('edit_item.html', community_id=community_id, community=communities[community_id])
        else:
            return redirect(url_for('dashboard'))

# 項目の削除
@app.route('/delete_item/<community_id>', methods=['GET', 'POST'])
def delete_item(community_id):
    if request.method == 'POST':
        if 'username' in session:
            if community_id in communities:
                del communities[community_id]
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    else:
        if community_id in communities:
            return render_template('delete_item.html', community_id=community_id, community=communities[community_id])
        else:
            return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run()
