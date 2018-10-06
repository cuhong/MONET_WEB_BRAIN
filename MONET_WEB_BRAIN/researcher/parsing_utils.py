import shutil
import json
import csv
import dateutil.parser as dt
import os
import codecs

from django.conf import settings
from . import parser


def txt_preprocessing(exp_file, exp_dir): 
    """
    Change the path of text_file from relative path to absolute path
    """
    fsrc = codecs.open(exp_file, 'r', encoding='utf-8')
    lines = fsrc.readlines()
    fdest = open(exp_file, 'w', encoding='utf-8')
    for line in lines:
        #line = line.replace(replace, path+'/'+replace)
        if "text_file" in line:
            line_list = line.split(' ')
            line_list[2] = exp_dir + '/' + line_list[2]
            line = ' '.join(line_list)
        fdest.write(line)

def html_postprocessing(html_file, researcher_name, prj_name, exp_name):
    """
    Change the path from relative to absolute so that can be found by apache2 server.
    """
    def img_parse(line, researcher_name, prj_name, exp_name):
        line = line.replace("img/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/img/')
        return line

    def audio_parse(line, researcher_name, prj_name, exp_name):
        line = line.replace("audio/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/audio/')
        return line

    def video_parse(line, researcher_name, prj_name, exp_name):
        line = line.replace("video/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/video/')
        return line

    def jspsych_parse(line):
        line = line.replace("jspsych.js", "{% static 'game/scripts/jspsych.js")  # {% static 'game/scripts/jspsych.js' %} => /static/game/scripts/jspsych.js
        line = line.replace("jspsych-6", "{% static 'game/jspsych-6")
        line = line.replace(".js\">", ".js' %}\">")
        line = line.replace("jspsych.css", "{% static 'game/styles/jspsych.css' %}")
        return line

    def send_result(line, researcher_name, prj_name, exp_name):
        line = line.replace("/* yumin accuracy */", "\
            accuracy = accuracy.toString();\n\
            start_time_list = start_time_list.toString();\n\
            end_time_list = end_time_list.toString();\n\
            response_time_list = rt.toString();\n\
            response_list = user_choices.toString();\n\
            /* \n\
            var gyro_x_avg = 0;\n\
            var gyro_y_avg = 0;\n\
            var gyro_z_avg = 0;\n\
            for(var i=0; i<gyro_x.length; i++) {\n\
                gyro_x_avg += gyro_x[i];\n\
                gyro_y_avg += gyro_y[i];\n\
                gyro_z_avg += gyro_z[i];\n\
            }\n\
            gyro_x_avg /= gyro_x.length;\n\
            gyro_y_avg /= gyro_x.length;\n\
            gyro_z_avg /= gyro_x.length;\n\
            var gyro_mag = Math.sqrt(Math.pow(gyro_x_avg, 2) + Math.pow(gyro_y_avg, 2) + Math.pow(gyro_z_avg, 2)).toString();\n\
            */ \n\
            gyro_mag = gyro_x.toString();\n\
            var xhr = new XMLHttpRequest();\n\
            xhr.open('POST', '/researcher/" + researcher_name +  "/" + prj_name + "/" + exp_name + "/', true);\n\
            xhr.setRequestHeader('Content-type', 'application/json');\n\
            xhr.onreadystatechange = function () {\n\
                if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
                    window.location.replace('/researcher/" + researcher_name + "/" + prj_name + "/" + exp_name + "/result');\n\
                }\n\
            };\n\
            xhr.send(accuracy + '!' + response_time_list + '!' + start_time_list + '!' + end_time_list + '!' + response_list + '!' + gyro_mag);\n\
            ")

        line = line.replace("/* yumin no accuracy */", "\
            start_time_list = start_time_list.toString();\n\
            end_time_list = end_time_list.toString();\n\
            response_time_list = rt.toString();\n\
            /* \n\
            var gyro_x_avg = 0;\n\
            var gyro_y_avg = 0;\n\
            var gyro_z_avg = 0;\n\
            for(var i=0; i<gyro_x.length; i++) {\n\
                gyro_x_avg += gyro_x[i];\n\
                gyro_y_avg += gyro_y[i];\n\
                gyro_z_avg += gyro_z[i];\n\
            }\n\
            gyro_x_avg /= gyro_x.length;\n\
            gyro_y_avg /= gyro_x.length;\n\
            gyro_z_avg /= gyro_x.length;\n\
            gyro_mag = Math.sqrt(Math.pow(gyro_x_avg, 2) + Math.pow(gyro_y_avg, 2) + Math.pow(gyro_z_avg, 2)).toString();\n\
            */ \n\
            gyro_mag = gyro_x.toString();\n\
            var xhr = new XMLHttpRequest();\n\
            xhr.open('POST', '/researcher/" + researcher_name +  "/" + prj_name + "/" + exp_name + "/', true);\n\
            xhr.setRequestHeader('Content-type', 'application/json');\n\
            xhr.onreadystatechange = function () {\n\
                if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
                    window.location.replace('/researcher/" + researcher_name + "/" + prj_name + "/" + exp_name + "/result');\n\
                }\n\
            };\n\
            xhr.send(response_time_list + '!' + start_time_list + '!' + end_time_list + '!' + response_list + '!' + gyro_mag);\n\
            ")
        return line

    f = codecs.open(html_file, 'r', encoding='utf-8')
    lines = f.readlines()
    fout = open(html_file, 'w', encoding='utf-8')

    i = 0
    for line in lines:
        if i == 0:
            line = line.replace(line, line+'{% load static %}\n')
            i += 1
        line = jspsych_parse(line)
        line = img_parse(line, researcher_name, prj_name, exp_name)
        line = audio_parse(line, researcher_name, prj_name, exp_name)
        line = video_parse(line, researcher_name, prj_name, exp_name)
        line = send_result(line, researcher_name, prj_name, exp_name)
        fout.write(line)

def parse_descriptor(researcher_name, prj_name, prj_dir):
    exp_names = []
    exp_descriptions = []
    exp_playtimes = []
    exp_kor_names = [] 

    with open(os.path.join(prj_dir, 'descriptor.txt'), 'r', encoding='utf-8') as f:  # /uploads/{{researcher_name}}/{{prj_name}}/descriptor.txt
        print("Read descriptor.txt!")
        rows = f.readlines()
        rows = [row.replace('\n', '') for row in rows]
        for row in rows:
            # Read exp_name from descriptor.txt
            if row == '\n' or row == '':
                continue
            exp_name, exp_kor_name, exp_description, exp_playtime = row.split(':')
            exp_names.append(exp_name)
            exp_descriptions.append(exp_description)
            exp_playtimes.append(int(exp_playtime))
            exp_kor_names.append(exp_kor_name)

            exp_dir = os.path.join(prj_dir, exp_name)  # exp_dir = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}
            exp_file = os.path.join(exp_dir, 'exp.txt')  # exp_file = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}/exp.txt
            html_file = os.path.join(exp_dir, exp_name+'.html')  # html_file = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}/{{exp_name}}.html

            # If the exp_name starts with 'balloon', then this is balloon project.
            if exp_name.startswith('balloon'):
                balloon_src = os.path.join(settings.BASE_DIR, 'game/templates/game/balloon.html')
                balloon_dest = os.path.join(settings.MEDIA_ROOT, '{}/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name, exp_name))
                html_dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))
                text_file = os.path.join(settings.MEDIA_ROOT, '{}/{}/{}/{}.txt'.format(researcher_name, prj_name, exp_name, exp_name))

                questions = []
                with open(text_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.replace('\n', '')
                        questions.append(line)
                try:
                    questions.remove('')
                except:
                    pass
                questions = '|'.join(questions)  # don't use ',' as seperator. A question can have it in itself
                print(questions)

                shutil.copy2(balloon_src, balloon_dest)
                with open(balloon_dest, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    with open(balloon_dest, 'w', encoding='utf-8') as fw:
                        for line in lines:
                            line = line.replace('/game/balloon/', '/researcher/{}/{}/{}/'.format(researcher_name, prj_name, exp_name))
                            line = line.replace("{{ balloon_txts }}\".split(',')", questions+"\".split('|')")
                            line = line.replace('/game/balloon/game-result/', '/researcher/{}/{}/'.format(researcher_name, prj_name))
                            fw.write(line)

                shutil.copy2(balloon_dest, html_dest)
                continue
            elif exp_name.startswith('face'):
                html_dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))
                text_file = os.path.join(settings.MEDIA_ROOT, '{}/{}/{}/exp.txt'.format(researcher_name, prj_name, exp_name))
                original_html = os.path.join(settings.BASE_DIR, 'ML/templates/ML/video.html')
                
                with open(text_file, 'r', encoding='utf-8') as f:
                    strings = f.readlines()
                    strings = [string.replace('\n', '<br>') for string in strings]
                    string = ''.join(strings)

                with open(original_html, 'r', encoding='utf-8') as f:
                    with open(html_dest, 'w+', encoding='utf-8') as fw:
                        rows = f.readlines()
                        for row in rows:
                            row = row.replace('REPLACE_THIS', string)
                            fw.write(row)
                continue


            # Process the exp_file into html_file
            txt_preprocessing(exp_file, exp_dir)
            parser.generate_html(exp_file, html_file)
            html_postprocessing(html_file, researcher_name, prj_name, exp_name)

            # Copy result html_file into templates directory
            dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))
            shutil.copy2(html_file, dest)

    return exp_names, exp_kor_names, exp_descriptions, exp_playtimes

def CreatePrj(fzip, researcher_name, prj_name, prj_dir):
    # prj_dir = /uploads/{{researcher_name}}/{{prj_name}}
    fzip_file = prj_dir + '/' + prj_name + '.zip'

    # Create zipfile into /uploads/{{researcher_name}}/{{prj_name}}/{{prj_name}}.zip
    with open(fzip_file, 'wb+') as destination:
        for chunk in fzip.chunks():
            destination.write(chunk)

    # Unzip zipfile into prj_dir
    import zipfile
    zip_ref = zipfile.ZipFile(fzip_file, 'r')
    zip_ref.extractall(prj_dir)
    zip_ref.close()
    print("Successfully unzipped!")

    # Parse
    return parse_descriptor(researcher_name, prj_name, prj_dir)

    """
    # Preprocess
    txt_preprocessing(path, "exp.txt")

    # Generate HTML file from parser
    parser.generate_html(path+'/exp.txt', path+'/'+gname+'.html')  # /uploads/ymkim_test3/djgame3/test_exp.txt

    # Move the created file from here to template directory
    source = path+'/'+gname+'.html'
    html_postprocessing(source, rname, gname)
    dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}.html'.format(rname, gname))
    shutil.copy2(source + '.tmp', dest)
    """

def remove_prj_dir(researcher_name, prj_name):
    # Remove the prject directory /uploads/{{researcher_name}}/{{prj_name}}/
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, '{}/{}/'.format(researcher_name, prj_name)))
    # Remove the game's html file at /researcher/templates/researcher/researchers/{{researcher_name}}/{{prj_name}}
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/'.format(researcher_name, prj_name)))
    except:
        print("html not created")
