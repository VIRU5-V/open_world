from flask import Blueprint, jsonify, render_template, redirect, url_for, request, current_app, abort, request, flash
from ..app import db, os
from ..models import Post, User, KeyWord
from flask_login import current_user, login_required
from .forms import UploadForm, SearchForm
from werkzeug.utils import secure_filename

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def posts():
    form = SearchForm()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts.html', posts=posts, form=form)

@main_blueprint.route('/search/<keyword>', methods=['GET', 'POST'])
@main_blueprint.route('/search', methods=['GET', 'POST'])
def search(keyword=''):
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.search.data
    res = Post.query.filter(Post.search_keywords.any(keyword=keyword)).all()
    return render_template('posts.html', posts=res, form=form, keyword=keyword)

@main_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = UploadForm()
    if form.validate_on_submit() and request.method == 'POST':
        all_keywords = []
        base_path = current_app.config['UPLOAD_FOLDER']
        keywords = form.keywords.data.split(', ')
        title = form.title.data

        # Create keywrods
        for keyword in keywords:
            kw = KeyWord(keyword=keyword.lower())
            db.session.add(kw)
            all_keywords.append(kw)

        # save image
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(base_path, filename))
        
        post = Post(
            title = title,
            photo = filename,
            user = current_user
        )
        post.search_keywords.extend(all_keywords)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.user', username=current_user.name))
    
    return render_template('create_post.html', form=form)

@main_blueprint.route('/like/<post_id>')
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    user = User.query.get(current_user.id)
    post.like(user)
    return redirect(url_for('.posts'))

@main_blueprint.route('/unlike/<post_id>')
@login_required
def unlike(post_id):
    post = Post.query.get(post_id)
    user = User.query.get(current_user.id)
    post.unlike(user)
    return redirect(url_for('.posts'))

@main_blueprint.route('/user/<username>')
def user(username):
    form = SearchForm()
    user = User.query.filter_by(name=username).first_or_404()
    posts = user.all_posts()

    return render_template('user.html', user=user, posts=posts, form=form)

@main_blueprint.route('/post_dete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if not post.is_own(current_user): return abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted :)')
    return redirect(url_for('.user', username=current_user.name))


@main_blueprint.route('/keyword', methods=['POST'])
def keyword():
    keyword = f"{request.json['keyword'].lower()}%"
    # get all realatable keywords from
    res = KeyWord.query.filter(KeyWord.keyword.like(keyword)).with_entities(KeyWord.keyword).all()
    # remove dublicate keyword
    res = list({ k.keyword for k in res})
    print(res)
    return jsonify({'data': {'keywords': res}})

# Ensure responses aren't cached
@main_blueprint.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response