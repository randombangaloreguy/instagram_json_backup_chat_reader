import json
import datetime
import sys

start_template = \
"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="utf-8">
<style>
img {
  border: 1px solid #ddd;
  width: 150px;
}
</style>
</head>
<body>
"""
end_html = "</body>\n</html>"

media_dir = "/Users/jay/Downloads/sanjay22112_20210711/"

message_json_filename = 'messages.json'
participants = []
show_on_screen = False
#Loads the messages.json file
n = len(sys.argv)
#print("Total arguments passed:", n)
#print("\nArguments passed:", end = " ")
#for i in range(1, n):
#    print(sys.argv[i], end = " ")
if n==2:
    if sys.argv[1] == "show":
        show_on_screen = True
    else:
        message_json_filename = sys.argv[1]

print("Using file ", message_json_filename)

with open(message_json_filename, encoding="utf8") as f:
    print("loading json message file messages.json")
    jfile = json.load(f)


#Saves the messages of the conversation
def save_messages(name,texts_list):   
    with open(f"{name}.txt", "w",encoding="utf8") as f:
        for line in texts_list:
            f.write(line+"\n")
    print("Done")
    print("\033[1m" + "Done" + "\033[0m")

def make_html(name, texts_list):
    with open(f"{name}.html", "w",encoding="utf8") as f:
        f.write(start_template)
        for line in texts_list:
            f.write(line)
        f.write(end_html)

def main():
    p = jfile["participants"]
    print(len(p), "particepents")
    for ps in range(len(p)):
        name = p[ps]["name"]
        name = name.strip()
        name = name.replace(" ", "")
        participants.append(name)

    print("participent = ", participants)

    texts_list = []
    first_date = ""
    last_date = ""
    pre_date = ""
    pre_time = datetime.datetime.now()
    messages = jfile["messages"]
    print(len(messages))
    idx = len(messages)-1 #0 based index
    while idx>=0:
    #for idx in range(len(messages)):
        t = ""
        message = messages[idx]
        if 'content' not in message:
            if 'audio_files' in message:
                af = message["audio_files"]
                t = af[0]["uri"]
                if not show_on_screen:
                    t = "<a href=" + media_dir + t + ">Audio File </a>"

            elif 'photos' in message:
                pm = message["photos"]
                t = pm[0]["uri"]
                if not show_on_screen:
                    t = "<a href=" + media_dir + t + ">Photo </a>"
            else:
                idx-=1
                continue
        ms = message['timestamp_ms']
        sender = message["sender_name"]
        #sender = "\033[1m" + sender + "\033[0m"
        dt = datetime.datetime.fromtimestamp(ms/1000.0)
        dt = dt.replace(microsecond=0)
        cur_date = dt.date()
        cur_time = dt
        if t == "":
            t = message['content']

        #adding a visual indicator for each new date
        if cur_date != pre_date:
            time_change_msg = dt.strftime('%d/%m/%y')
            time_change_msg = "<h3>" + time_change_msg + "</h3>"
            texts_list.append(time_change_msg)
            pre_date=dt.date()
        else:
            ## same dat. check for time difference. If its more than 2 hours, put some gap 
            if cur_time - pre_time > datetime.timedelta(0, 7200):
                #print("2 hours gap", cur_time, cur_date, pre_time)
                texts_list.append("<p>.</p>")

        pre_time = cur_time

        if show_on_screen:
            text = str(dt.time()) + " - " + sender + "\t: "+ t
            print(text)

        text = "<p>" + str(dt.time()) + " - <b>" + sender + "</b> : " + t + "</p>"
        texts_list.append(text)
        if first_date == "":
            first_date = cur_date
        last_date = cur_date

        idx-=1

    #Save the last conversation   
    if texts_list:
        filename = str(participants[0]) + "_" + str(participants[1] + "_" + str(first_date) +"-"+str(last_date))
        #print(filename)
        save_messages(filename, texts_list)
        make_html(filename, texts_list)

if __name__ == '__main__':
    main()

