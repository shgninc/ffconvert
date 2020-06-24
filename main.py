#!/usr/bin/env python3

# https://github.com/kkroening/ffmpeg-python
# https://kkroening.github.io/ffmpeg-python/

# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import ffmpeg
# import json
# from sqlalchemy import create_engine, MetaData, Table
# import subprocess
import sys
# from pprint import pprint
from importlib import reload

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = './uploads/'
# 16 megabytes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # * 1024

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mkv', 'wav', 'ogg', 'wmv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=u'مدیریت سرویسها')


@app.route('/videoInfo', methods=['GET', 'POST'])
def videoInfo():
    if request.method == 'POST':
        try:
            file = request.files['file']
            print('hee')
        except RequestEntityTooLarge as e:
            # we catch RequestEntityTooLarge exception
            app.logger.info(e)
            return render_template('videoInfo.html', error=e, title=u'اطلاعات ویدیو')

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            info = None
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                info = ffmpeg.probe(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except ffmpeg.Error as e:
                print(e.stderr)
                sys.exit(1)

            video_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                print('No video stream found')
                sys.exit(1)
            key1 = 'disposition'
            key2 = 'tags'
            if key1 in video_stream:
                del video_stream[key1]
            if key2 in video_stream:
                del video_stream[key2]
            return render_template('videoInfo.html', info=video_stream, title=u'اطلاعات ویدیو')
    return render_template('videoInfo.html', title=u'اطلاعات ویدیو')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print(f)
        return 'file uploaded successfully'


# @app.route('/new_service', methods=["GET", "POST"])
# def new_service():
#     res_service = core_service.select(core_service.c.id).where(core_service.c.enable == 1). \
#         order_by(core_service.c.id.desc()).limit(1).execute().first()
#     form = ServiceForm()
#     if form.validate_on_submit():
#         # flash('Login requested for user {}, remember_me={}'.format(form.name.data, form.description.data))
#         data = {'id': form.id.data, 'name': form.name.data, 'description': form.description.data,
#                 'city_id': form.city_id.data,
#                 'dnid': form.dnid.data, 'service_number': form.service_number.data, 'startdate': form.start_date.data,
#                 'company_name': form.company_name.data, 'enable': form.enable.data}
#         print(data)
#         try:
#             conn = engine_service.connect()
#             result = conn.execute(core_service.insert(), [data])
#             # flash('Number of row affected{}'.format(str(result.rowcount)))
#             if (result):
#                 conn.close()
#                 return redirect('/all_service')
#
#         except Exception as e:
#             flash('Error in inserting new service - {}'.format(e))
#
#     return render_template('new_service.html', title=u'مدیریت سرویسها', form=form, id=(res_service['id'] + 1))


# @app.route('/update_service', methods=["GET", "POST"])
# def update_service():
#     if request.method == 'GET':
#         id = request.form['servie_id']
#     # res_service = core_service.select(core_service.c.id).where(core_service.c.enable == 1).\
#     #                 order_by(core_service.c.id.desc()).limit(1).execute().first()
#     # form = ServiceForm()
#     # if form.validate_on_submit():
#     #     #flash('Login requested for user {}, remember_me={}'.format(form.name.data, form.description.data))
#     #     data = {'id':form.id.data, 'name': form.name.data, 'description': form.description.data, 'city_id': form.city_id.data,
#     #             'dnid': form.dnid.data, 'service_number': form.service_number.data, 'startdate': form.start_date.data,
#     #             'company_name': form.company_name.data, 'enable': form.enable.data}
#     #     print(data)
#     #     try:
#     #         conn = engine_service.connect()
#     #         result = conn.execute(core_service.insert(), [data])
#     #         #flash('Number of row affected{}'.format(str(result.rowcount)))
#     #         if (result):
#     #             conn.close()
#     #             return redirect('/all_service')
#     #
#     #     except Exception as e:
#     #         flash('Error in inserting new service - {}'.format(e))
#
#     return render_template('update_service.html', title=u'مدیریت سرویسها')


if __name__ == '__main__':
    app.run(debug=True)
