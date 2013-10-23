from flask.ext.flails import FlailsView
from flask import render_template, redirect, url_for, request
#from config import db
import models
import forms

class AppView(FlailsView):
    def app_index(self):
        object_list = models.Post.query.all()
        return render_template('post/index.slim', object_list=object_list)

    def app_show(self, ident):
        post = models.Post.query.get(ident)
        form = forms.CommentForm()
        return render_template('post/show.slim', post=post, form=form)

    def app_new(self):
        form = forms.PostForm()
        if form.validate_on_submit():
            post = models.Post(form.name.data, form.title.data, form.content.data)
            #db.session.add(post)
            #db.session.commit()
            return redirect(url_for('post.index'))
        return render_template('post/new.slim', form=form)

    def app_edit(self, ident):
        post = models.Post.query.get(ident)
        form = forms.PostForm(request.form, post)
        if form.validate_on_submit():
            post.name = form.name.data
            post.title = form.title.data
            post.content = form.content.data
            #db.session.add(post)
            #db.session.commit()
            return redirect(url_for('post.show', ident=ident))
        return render_template('post/edit.slim', form=form, post=post)

    def app_delete(self, ident):
        post = models.Post.query.get(ident)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.index'))

    def app_comment_new(self, post_id):
        post = models.Post.query.get(post_id)
        form = forms.CommentForm()
        if form.validate_on_submit():
            comment = models.Comment(form.commenter.data, form.body.data, post_id)
            #db.session.add(comment)
            #db.session.commit()
            return redirect(url_for('.show', ident=post_id))
        return render_template('post/show.slim', post=post, form=form)

    def app_comment_delete(self, post_id, ident):
        comment = models.Comment.query.get(ident)
        #db.session.delete(comment)
        #db.session.commit()
        return redirect(url_for('.show', ident=post_id))
