# -*- coding: utf-8 -*-

from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
        self.image = 0
        self.peace_con = 0 
        self.destroy_con = 0
        self.second = 0
        
    def pick_up_banana(self, update):
        text = update.message.text
        if(text == "要"):
            self.destroy_con = 1
        return text == "要"
        
    def no_pick_up_banana(self, update):
        text = update.message.text
        return text == "不要"
        
    def accept_interview(self, update):
        text = update.message.text
        if(text == "不要"):
            self.destroy_con = 4
        return text == "要"
        
    def one_more_banana(self, update):
        text = update.message.text
        return text == "再放一個"
        
    def prepare_live(self, update):
        text = update.message.text
        return text == "準備直播"
        
    def help_the_man(self, update):
        text = update.message.text
        if(text == "幫"):
            self.peace_con = 1
        return text == "幫"
    
    def go_to_hospital(self, update):
        text = update.message.text
        if(text == "叫救護車"):
            self.peace_con = 1
        return text == "叫救護車"
        
    def good_word(self, update):
        text = update.message.text
        if(text == "關心他"):
            self.peace_con = 2
        else:
            self.destroy_con = 2
        return text == "關心他"
        
    def near(self, update):
        text = update.message.text
        if(text == "旁邊"):
            self.destroy_con = 3
        elif(text == "3公尺外"):
            self.second = 1
        return text == "旁邊"
        
    def on_enter_world_peace(self, update):
        if(self.peace_con == 1):
            if(self.second == 1):
                update.message.reply_text("救護車來了以後把第二張香蕉皮壓爛了，沒有人再滑倒了。")
            update.message.reply_text("這位先生去醫院檢查後發現身體有奇怪的病毒......")
        elif(self.peace_con == 2):
            update.message.reply_text("你的關心讓他覺得溫暖，他決定去醫院......")
        update.message.reply_text("你的選擇拯救了世界!!!")
        self.image = 4
        self.go_back(update)
        
    def on_exit_world_peace(self, update):
        print('Leaving world_peace')
        
    def on_enter_world_destroy(self, update):
        if(self.destroy_con == 1):
            update.message.reply_text("香蕉皮被撿起來了......")
        elif(self.destroy_con == 2):
            update.message.reply_text("因為沒人關心他，這位男子落寞的回家了......")
        elif(self.destroy_con == 3):
            update.message.reply_text("兩張香蕉皮太明顯了，大家都繞過去......")
        elif(self.destroy_con == 4):
            update.message.reply_text("你不接受訪問，這件事不了了之......")
        update.message.reply_text("3個月後，爆發了殭屍病毒......")
        update.message.reply_text("世界毀滅了!!!")
        self.image = 1
        self.go_back(update)
        
    def on_exit_world_destroy(self, update):
        print('Leaving world_destroy')
        
    def on_enter_fall_down(self, update):
        update.message.reply_text("一位路過的先生踩到香蕉皮後跌倒了!")
        self.image = 2
        
    def on_exit_fall_down(self, update):
        print('Leaving fall_down')
        
    def on_enter_man(self, update):
        update.message.reply_text("你無情地離開了......")
        if(self.second == 1):
                update.message.reply_text("大家看到有人滑倒後，就發現第二張香蕉皮，沒有人再滑倒了。")
        self.image = 3
        
    def on_exit_man(self, update):
        print('Leaving man')
        
    def on_enter_netizen(self, update):
        update.message.reply_text("他把自己跌倒的事發到網路上求安慰，如果你看到了會怎麼做?")
        self.image = 5
        
    def on_exit_netizen(self, update):
        print('Leaving netizen')
    
    def on_enter_place(self, update):
        update.message.reply_text("你要放在什麼地方?")
        update.message.reply_text("旁邊/3公尺外")
        
    def on_exit_place(self, update):
        print('Leaving place')
        
    def on_enter_live(self, update):
        update.message.reply_text("這次直播爆紅了，有人想要訪問你，你要接受嗎?")
        update.message.reply_text("要/不要")
        
    def on_exit_live(self, update):
        print('Leaving live')
        
    def on_enter_murder(self, update):
        update.message.reply_text("接受訪問完3天......")
        update.message.reply_text("你被人謀殺了!")
        self.image = 6
        self.go_back(update)
        
    def on_exit_murder(self, update):
        print('Leaving murder')
        
