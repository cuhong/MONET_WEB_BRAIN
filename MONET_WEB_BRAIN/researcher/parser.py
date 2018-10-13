import sys
from copy import deepcopy

class Stimulus():
    def __init__(self, identifier, stimulusObject):
        self.identifier = identifier
        self.stimulusObject = stimulusObject

    def get_html(self): return self.stimulusObject.get_html()

    def get_plugin(self):
        return self.stimulusObject.get_plugin()

    def get_choice_html(self):
        return self.stimulusObject.get_choice_html()

class Text():
    def __init__(self, content, font_size, font_color):
        self.content = content
        self.font_size = font_size
        self.font_color = font_color

    def get_plugin(self):
        return "html-button-response"

    def get_html(self):
        if self.font_color == "n" and self.font_size == "n":
            return self.content
        elif self.font_color != "n" and self.font_size == "n":
            return "<div style=\"color:" + self.font_color +";\">" + self.content + "</div>"
        elif self.font_color == "n" and self.font_size != "n":
            return "<div style=\"font_size:" + self.font_size + "px;\">" + self.content + "</div>"
        else:
            return "<div style=\"color:" + self.font_color +"; font_size:" + self.font_size + "px;\">" + self.content + "</div>"

    def get_choice_html(self):
        return self.get_html()

class TextFile():
    def __init__(self, path, font_size, font_color):
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            lines = [line.replace("\n", "<br>") for line in lines]
            content = ''.join(lines)
        self.content = content
        self.font_size = font_size
        self.font_color = font_color

    def get_plugin(self):
        return "html-button-response"

    def get_html(self):
        if self.font_color == "n" and self.font_size == "n":
            return self.content
        elif self.font_color != "n" and self.font_size == "n":
            return "<div style=\"color:" + self.font_color +";\">" + self.content + "</div>"
        elif self.font_color == "n" and self.font_size != "n":
            return "<div style=\"font_size:" + self.font_size + "px;\">" + self.content + "</div>"
        else:
            return "<div style=\"color:" + self.font_color +"; font_size:" + self.font_size + "px;\">" + self.content + "</div>"

    def get_choice_html(self):
        return self.get_html()

class Image():
    def __init__(self, path):
        self.path = path

    def get_plugin(self):
        return "image-button-response"

    def get_html(self):
        return self.path

    def get_choice_html(self):
        return "<img src=\""+self.path+"\"><br><br>"


class Audio():
    def __init__(self, path):
        self.path = path

    def get_plugin(self):
        return "audio-button-response"

    def get_html(self):
        return self.path

    def get_choice_html(self):
        print("ERROR: audio cannot be a choice")
        sys.exit()


class Video():
    def __init__(self, path):
        self.path = path

    def get_plugin(self):
        return "video-button-response"

    def get_html(self):
        return self.path

    def get_choice_html(self):
        print("ERROR: video cannot be a choice")
        sys.exit()


stimulus_dict = {}
speed_limit = None
def parse_stimulus(line):
    global stimulus_dict
    line = line.split(' ')
    identifier = line[1]
    if line[0] == "text":
        font_color = line.pop()
        font_size = line.pop()
        text = ' '.join(line[2:])
        stimulus_obj = Text(text[1:-1].replace('\'', '\\\'').replace('\"', '\\\"'), font_size, font_color)
    elif line[0] == "text_file":
        stimulus_obj = TextFile(line[2], line[3], line[4])
    elif line[0] == "image":
        stimulus_obj = Image(line[2])
    elif line[0] == "audio":
        stimulus_obj = Audio(line[2])
    elif line[0] == "video":
        stimulus_obj = Video(line[2])
    elif line[0] == "speed_limit":
        speed_limit = int(line[1]) 
    else:
        print("wrong stimulus type")
    stimulus = Stimulus(identifier, stimulus_obj)
    stimulus_dict[identifier] = stimulus


class SequenceVariable():
    def __init__(self, onSetTime, identifier, stimDur, choices, choiceDur, answer, choiceOnsetRelativeToSim, reactionTime, feed_back_type, feed_back_duration, feed_back_1, feed_back_2, test):
        global stimulus_dict
        self.onSetTime = onSetTime
        self.identifier = identifier
        self.stimDur = stimDur
        self.choiceDur = choiceDur
        self.choices_str = choices
        self.answer = answer
        self.choiceOnsetRelativeToSim = choiceOnsetRelativeToSim
        self.reactionTime = reactionTime
        self.feed_back_type = feed_back_type
        self.feed_back_duration = feed_back_duration
        self.feed_back_1 = feed_back_1
        self.feed_back_2 = feed_back_2
        self.test = test
        # add stimulus objects
        self.stimulus = stimulus_dict[self.identifier]
        if self.choices_str != 'n':
            self.choices = [stimulus_dict[_id] for _id in self.choices_str.split(",")]
        if self.feed_back_1 != 'n':
            self.feed_back_1 = stimulus_dict[self.feed_back_1]
        if self.feed_back_2 != 'n':
            self.feed_back_2 = stimulus_dict[self.feed_back_2]

    def add_sequence_block(self):
        block_string = "timeline.push({\n"
        if self.choices_str != "n":
            block_string += "type: \"%s\",\n"%(self.stimulus.get_plugin())
        else:
            block_string += "type: \"%s\",\n"%(self.stimulus.get_plugin().replace("button", "keyboard"))
        block_string += "stimulus: \'%s\',\n"%(self.stimulus.get_html())
        if self.stimDur != "inf":
            if 'image' in self.stimulus.get_plugin() or 'html' in self.stimulus.get_plugin():
                block_string += "stimulus_duration: %s,\n"%(self.stimDur)
        if self.reactionTime != "inf":
            if 'video' not in self.stimulus.get_plugin():
                block_string += "trial_duration: %s,\n"%(self.reactionTime)
        elif self.choices_str == "n":
            block_string += "trial_duration: %s,\n"%(self.stimDur)
        if self.choices_str == "n":
            block_string += "choices: jsPsych.NO_KEYS,\n"
        else:
            block_string += "choices: ["
            for choice_obj in self.choices:
                block_string += "\'%s\',"%(choice_obj.get_choice_html())
            block_string = block_string[:-1]
            block_string += "],\n"
        if self.answer != "n":
            block_string += "data: { correct_response: %s,"%(self.answer)
            if self.test == "y":
                block_string += " test_part: \"test\"},\n"
                block_string += "on_finish: function(data){\n\
                                    data.correct = data.button_pressed == data.correct_response;\n\
                                    var current_time = new Date();\n\
                                    end_time_list.push(current_time);\n\
                                    user_choices.push(data.button_pressed);\n\
                                    data.choices = [%s]\n\
                                    },\n"%(','.join(['\''+choice_obj.get_choice_html()+'\'' for choice_obj in self.choices]))
                block_string += "on_load: function(data){\n\
                                    var current_time = new Date();\n\
                                    start_time_list.push(current_time);\n\
                                    },\n"
            else:
                block_string += "},\n"
        elif self.test == "y":
            block_string += "data: {test_part: \"test\"},\n"
            block_string += "on_finish: function(data){\n\
                                var current_time = new Date();\n\
                                end_time_list.push(current_time);\n\
                                user_choices.push(data.button_pressed);\n\
                                data.choices = [%s]\n\
                                },\n"%(','.join(['\''+choice_obj.get_choice_html()+'\'' for choice_obj in self.choices]))
            block_string += "on_load: function(data){\n\
                                var current_time = new Date();\n\
                                start_time_list.push(current_time);\n\
                                },\n"
        block_string += "});\n"
        return block_string

    def add_feedback_block(self):
        if self.feed_back_type == "n":
            return ''
        if self.feed_back_duration == "n":
            print("ERROR: feed back durtaion must be specified")
            sys.exit()
        elif self.feed_back_type == "c":
            feedback_str =  "timeline.push({\n"+\
                                "type:\'%s\',\n"%(self.choices[0].get_plugin().replace("button", "keyboard"))+\
                                "stimulus:jsPsych.data.get().last(1).values()[0].choices[jsPsych.data.get().last(1).values()[0].button_pressed],\n"
            if self.feed_back_duration != "n":
                feedback_str += "trial_duration: %s\n});\n"%(self.feed_back_duration)
            else:
                feedback_str += "});\n"
        elif self.feed_back_type == "a":
            feedback_str =  "timeline.push({\n"+\
                                "type:\'%s\',\n"%(self.feed_back_1.get_plugin().replace("button","keyboard"))+\
                                "stimulus:\'%s\',\n"%(self.feed_back_1.get_html())
            if self.feed_back_duration != "n":
                feedback_str += "trial_duration: %s\n});"%(self.feed_back_duration)
            else:
                feedback_str += "});\n"
        elif self.feed_back_type == "tf":
            corr_block =  "timeline.push({\n\
                        timeline: [%s],\n\
                        conditional_function: function (data) {\n\
                            var data = jsPsych.data.get().last(1).values()[0];\n\
                            if (data.correct_response == data.button_pressed) {\n\
                                return true;\n\
                            } else {\n\
                                return false;\n\
                            }\n\
                        }\n\
                    });\n"%("{type: \'%s\',\nstimulus:\'%s\',\ntrial_duration:%s\n}\n"%(self.feed_back_1.get_plugin().replace("button","keyboard"), self.feed_back_1.get_html(), self.feed_back_duration))
            wrong_block =  "timeline.push({\n\
                        timeline: [%s],\n\
                        conditional_function: function (data) {\n\
                            var data = jsPsych.data.get().last(1).values()[0];\n\
                            if (data.correct_response == data.button_pressed) {\n\
                                return false;\n\
                            } else {\n\
                                return true;\n\
                            }\n\
                        }\n\
                    });\n"%("{type: \'%s\',\nstimulus:\'%s\',\ntrial_duration:%s\n}\n"%(self.feed_back_2.get_plugin().replace("button","keyboard"), self.feed_back_2.get_html(), self.feed_back_duration))
            feedback_str = corr_block + wrong_block
        return feedback_str

sequence_list = []
def parse_sequence(line):
    global sequence_list
    line = line.split(' ')
    if len(line) != 13:
        print("ERROR: wrong length of a line")
        sys.exit()
    onSetTime = line[0]
    identifier = line[1]
    stimDur = line[2]
    choices = line[3]
    choiceDur = line[4]
    answer = line[5]
    choiceOnsetRelativeToSim = line[6]
    reactionTime = line[7]
    feed_back_type = line[8]
    feed_back_duration = line[9]
    feed_back_1 = line[10]
    feed_back_2 = line[11]
    test = line[12]
    sequence = SequenceVariable(onSetTime, identifier, stimDur, choices, choiceDur, answer, choiceOnsetRelativeToSim, reactionTime, feed_back_type, feed_back_duration, feed_back_1, feed_back_2, test)
    sequence_list.append(sequence)

def get_result_page():
    return "timeline.push({\n\
                type: \'html-keyboard-response\',\n\
                stimulus: function () {\n\
                                var trials = jsPsych.data.get().filter({ test_part: \"test\" });\n\
                                if(trials.count() > 0){\n\
                                    var correct_trials = trials.filter({ correct: true });\n\
                                    var accuracy = Math.round(correct_trials.count() / trials.count() * 100);\n\
                                    var rt = trials.select('rt').values;\n\
                                    console.log(accuracy);\n\
                                    console.log(start_time_list);\n\
                                    console.log(end_time_list);\n\
                                    console.log(rt);\n\
                                    /* yumin accuracy */\n\
                                    return \"<p>You responded correctly on \" + accuracy + \"% of the trials.</p>\" +\n\
                                        \"<p>Your average response time was \" + average(rt) / 1000 + \"s.</p>\";\n}\n\
                                else {\n\
                                    var rt = trials.select('rt').values;\n\
                                    console.log(start_time_list);\n\
                                    console.log(end_time_list);\n\
                                    console.log(rt);\n\
                                    /* yumin no accuracy */\n\
                                    return \"<p>Your average response time was \" + average(rt) / 1000 + \"s.</p>\";\n}\n\
                            },\n\
                trial_duration: 10000,\n\
                });\n"


def parse(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        phase = 0
        for line in f:
            line = line.replace("\n","")
            line = line.replace('\ufeff', '')
            #rint(line)
            #if not line: break
            if "Task WM" in line:
               # exp_name = line.replace("Task WM ","")
                exp_name = 'Experiment'
                continue
            elif "[Descriptions]" in line:
                phase = 1
                continue
            elif "[PreSeq]" in line:
                phase = 2
                continue
            elif "[MainSeq]" in line:
                phase = 3
                continue
            elif "[PostSeq]" in line:
                phase = 4
                continue
            elif "[End" in line:
                phase = 0
                if "[EndPostSeq]" in line:
                    return exp_name
                continue
            # print(phase)
            if phase == 1:
                parse_stimulus(line)
            elif phase > 1:
                parse_sequence(line)
    return exp_name

def get_header(exp_name):
    return "<head>\n\
        <title>%s</title>\n\
        <meta charset=\"utf-8\">\n\
        <script src=\"jspsych.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-html-keyboard-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-html-button-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-image-button-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-image-keyboard-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-audio-button-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-audio-keyboard-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-video.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-fullscreen.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-categorize-html.js\"></script>\n\
        <link rel=\"stylesheet\" href=\"jspsych.css\"></link>\n\
        <script src=\"https://code.jquery.com/jquery-3.3.1.min.js\" integrity=\"sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=\"\n\
        crossorigin=\"anonymous\"></script>\n\
        </head>\n\n"%(exp_name)

def get_body():
    global sequence_list
    global speed_limit
    body_string = "<body>\n<script>\n"
    if speed_limit:
        body_string += "var gyro_x = [];\n"
        body_string += "var gyro_y = [];\n"
        body_string += "var gyro_z = [];\n"
        body_string += "const sensorGyro = new Gyroscope();\n"
        body_string += "sensorGyro.start();\n"
        body_string += "$(document).ready(function(){\n\
                        setInterval(check_gyro, 100);\n\
                        });\n"
        body_string += "function check_gyro(){\n\
                        var avg_x = 0;\n\
                        var avg_y = 0;\n\
                        var avg_z = 0;\n\
                        for(var i=0;i<gyro_x.length;i++){\n\
                        avg_x += gyro_x[i];\n\
                        }\n\
                        for(var i=0;i<gyro_y.length;i++){\n\
                        avg_y += gyro_y[i];\n\
                        }\n\
                        for(var i=0;i<gyro_z.length;i++){\n\
                        avg_z += gyro_z[i];\n\
                        }\n\
                        avg_x /= gyro_x.length;\n\
                        avg_y /= gyro_y.length;\n\
                        avg_z /= gyro_z.length;\n\
                        speed = Math.sqrt((avg_x * avg_x + avg_y * avg_y + avg_z * avg_z)/3);\n\
                        if(speed>speed_limit){\n\
                            /* yumin redirection */\n\
                        }\n\
                        };\n"
    body_string += "var timeline = [];\n"
    body_string += "var start_time_list = [];\n"
    body_string += "var end_time_list = [];\n"
    body_string += "var user_choices = [];\n"
    body_string += "const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;"
    full_screen_block = "timeline.push({\n\
                        type: \'fullscreen\',\n\
                        fullscreen_mode: true\n\
                        });\n"
    body_string += full_screen_block
    for seq in sequence_list:
        body_string += seq.add_sequence_block() + seq.add_feedback_block()

    body_string += get_result_page()

    body_string += 	"jsPsych.init({\n\
			timeline: timeline,\n\
			show_preload_progress_bar: true,\n\
            on_finish: function() {\n\
                //jsPsych.data.get().localSave('csv','data.csv');\n\
            }\n\
		});\n"
    body_string += "</script>\n</body>\n"
    return body_string

def generate_html(fname, gname):
    exp_name = parse(fname)  # test_exp.txt  ==> /uploads/ResearcherName/gamename/test_exp.txt
    # exp_name = Experiment
    print()
    print('exp_name', exp_name)
    print("###fname in generate_html()###")
    print(fname)
    print("###gname in generate_html()###")
    print(gname)
    print("###")
    html = '<!DOCTYPE html>\n<html>\n'
    html += get_header(exp_name)
    html += get_body()
    html += '</html>'
    with open(gname, "w+", encoding="utf-8") as f:
        f.write(html)
    global sequence_list
    sequence_list = []

"""
if __name__ == "__main__":
    fname = sys.argv[1]
    generate_html(fname)
"""

