# -*- coding: utf-8 -*-

import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = 'YOUR_API_KEY'
WEBHOOK_URL = 'YOUR_URL'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'banana',
        'world_peace',
        'world_destroy',
        'fall_down',
        'man',
        'netizen',
        'place',
        'live',
        'murder'
    ],
    transitions=[
        #start
        {
            'trigger': 'start',
            'source': 'banana',
            'dest': 'world_destroy',
            'conditions': 'pick_up_banana'
        },
        {
            'trigger': 'start',
            'source': 'banana',
            'dest': 'fall_down',
            'conditions': 'no_pick_up_banana',
        },
        {
            'trigger': 'start',
            'source': 'banana',
            'dest': 'place',
            'conditions': 'one_more_banana',
        },
        {
            'trigger': 'start',
            'source': 'banana',
            'dest': 'live',
            'conditions': 'prepare_live',
        },
        #poor_man
        {
            'trigger': 'poor_man',
            'source': 'fall_down',
            'dest': 'world_peace',
            'conditions': 'help_the_man'
        },
        {
            'trigger': 'poor_man',
            'source': 'fall_down',
            'dest': 'man',
            'unless': 'help_the_man'
        },
        #man_decision
        {
            'trigger': 'man_decision',
            'source': 'man',
            'dest': 'world_peace',
            'conditions': 'go_to_hospital'
        },
        {
            'trigger': 'man_decision',
            'source': 'man',
            'dest': 'netizen',
            'unless': 'go_to_hospital'
        },
        #effect
        {
            'trigger': 'effect',
            'source': 'netizen',
            'dest': 'world_peace',
            'conditions': 'good_word'
        },
        {
            'trigger': 'effect',
            'source': 'netizen',
            'dest': 'world_destroy',
            'unless': 'good_word'
        },
        #place_where
        {
            'trigger': 'place_where',
            'source': 'place',
            'dest': 'world_destroy',
            'conditions': 'near'
        },
        {
            'trigger': 'place_where',
            'source': 'place',
            'dest': 'fall_down',
            'unless': 'near'
        },
        #interview
        {
            'trigger': 'interview',
            'source': 'live',
            'dest': 'murder',
            'conditions': 'accept_interview'
        },
        {
            'trigger': 'interview',
            'source': 'live',
            'dest': 'world_destroy',
            'unless': 'accept_interview'
        },
        #go_back
        {
            'trigger': 'go_back',
            'source': [
                'world_peace',
                'world_destroy',
                'murder'
            ],
            'dest': 'banana'
        }
    ],
    initial='banana',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    
    machine.image = 0
    
    if(machine.state == 'banana'):
        machine.start(update)
    elif(machine.state == 'fall_down'):
        machine.poor_man(update)
    elif(machine.state == 'man'):
        machine.man_decision(update)
    elif(machine.state == 'netizen'):
        machine.effect(update)
    elif(machine.state == 'place'):
        machine.place_where(update)
    elif(machine.state == 'live'):
        machine.interview(update)
        
    
    if(machine.image == 1):
        bot.send_photo(chat_id=chat_id, photo=open('images/world_destroy.jpg', 'rb'))
        update.message.reply_text("你僥倖逃的活了下來，並得到回到過去的能力")
        bot.send_photo(chat_id=chat_id, photo=open('images/back.jpg', 'rb'))
        update.message.reply_text("你回到了最初的選擇......")
        update.message.reply_text("在一個風和日麗的午後，你在路上看到香蕉皮，你要把它撿起來嗎?")
        update.message.reply_text("要/不要/再放一個/準備直播")
        machine.second = 0
    elif(machine.image == 2):
        bot.send_photo(chat_id=chat_id, photo=open('images/fall_down.jpg', 'rb'))
        update.message.reply_text("這位先生看起來摔得很重，你要幫他叫救護車嗎?")
        update.message.reply_text("幫/不幫")
    elif(machine.image == 3):
        bot.send_photo(chat_id=chat_id, photo=open('images/ruthless.png', 'rb'))
        update.message.reply_text("這位先生倒在地上起不來，他接下來應該怎麼辦?")
        update.message.reply_text("叫救護車/發文")
    elif(machine.image == 4):
        bot.send_photo(chat_id=chat_id, photo=open('images/peace.jpg', 'rb'))
        update.message.reply_text("世界和平了，但是在一個風和日麗的午後，你又在路上看到香蕉皮，你要把它撿起來嗎?")
        update.message.reply_text("要/不要/再放一個/準備直播")
        machine.second = 0
    elif(machine.image == 5):
        bot.send_photo(chat_id=chat_id, photo=open('images/cry.jpg', 'rb'))
        update.message.reply_text("嘲笑他/關心他")
    elif(machine.image == 6):
        bot.send_photo(chat_id=chat_id, photo=open('images/murder.jpg', 'rb'))
        update.message.reply_text("也許你做了什麼令人怨恨的事......")
        update.message.reply_text("不過幸運的是，你竟然重生了!回到了最初的選擇......")
        bot.send_photo(chat_id=chat_id, photo=open('images/baby.jfif', 'rb'))
        update.message.reply_text("在一個風和日麗的午後，你在路上看到香蕉皮，你要把它撿起來嗎?")
        update.message.reply_text("要/不要/再放一個/準備直播")
        machine.second = 0
        
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()