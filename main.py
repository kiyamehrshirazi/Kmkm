import random
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

WORDS = {
    "آسان": ["BOOK", "STAR", "FISH", "MOON", "TREE", "WIND"],
    "متوسط": ["PLANT", "BRAIN", "CLOUD", "NIGHT", "STONE", "DREAM"],
    "سخت": ["PYTHON", "PUZZLE", "PLANET", "MYSTIC", "SHADOW", "SPIRIT"],
}
LIMITS = {"آسان": 8, "متوسط": 7, "سخت": 6}

class WordLockApp(App):
    def build(self):
        self.title = "قفل کلمات"
        Window.clearcolor = (0.06, 0.08, 0.14, 1)
        self.total_score = 0
        self.root_box = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        self.root_box.add_widget(Label(text="قفل کلمات", font_size="30sp", bold=True,
                                       color=(0.45, 0.85, 1, 1), size_hint_y=None, height=dp(55)))
        self.root_box.add_widget(Label(text="کلمه مخفی را پیدا کن؛ راهنما می‌گوید چند حرف درست‌اند.",
                                       font_size="15sp", color=(1,1,1,1),
                                       size_hint_y=None, height=dp(44)))
        self.level = Spinner(text="متوسط", values=("آسان", "متوسط", "سخت"),
                             size_hint_y=None, height=dp(48))
        self.root_box.add_widget(self.level)
        self.status = Label(text="", font_size="16sp", color=(1,1,1,1),
                            size_hint_y=None, height=dp(70))
        self.root_box.add_widget(self.status)
        self.entry = TextInput(hint_text="حدس خود را با حروف انگلیسی بنویس",
                               multiline=False, font_size="22sp", size_hint_y=None, height=dp(52),
                               halign="center")
        self.entry.bind(on_text_validate=lambda *_: self.submit_guess())
        self.root_box.add_widget(self.entry)
        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.guess_btn = Button(text="ثبت حدس", background_color=(0.12, 0.55, 0.75, 1))
        self.guess_btn.bind(on_press=lambda *_: self.submit_guess())
        self.new_btn = Button(text="بازی جدید", background_color=(0.25, 0.35, 0.5, 1))
        self.new_btn.bind(on_press=lambda *_: self.new_game())
        buttons.add_widget(self.guess_btn)
        buttons.add_widget(self.new_btn)
        self.root_box.add_widget(buttons)
        self.log = Label(text="", font_size="16sp", color=(0.9,0.93,1,1),
                         size_hint_y=None, valign="top", halign="right")
        self.log.bind(texture_size=self._update_log_height)
        scroll = ScrollView()
        scroll.add_widget(self.log)
        self.root_box.add_widget(scroll)
        self.score_label = Label(text="امتیاز کل: 0", font_size="16sp",
                                 color=(0.55, 1, 0.65, 1),
                                 size_hint_y=None, height=dp(35))
        self.root_box.add_widget(self.score_label)
        self.new_game()
        return self.root_box

    def _update_log_height(self, instance, size):
        instance.height = max(size[1] + dp(12), dp(80))

    def new_game(self, *_):
        level = self.level.text
        self.secret = random.choice(WORDS[level])
        self.limit = LIMITS[level]
        self.used = 0
        self.over = False
        self.log.text = "شروع شد! حروف انگلیسی وارد کن.\n"
        self.status.text = f"کلمه {len(self.secret)} حرف دارد. فرصت‌ها: {self.limit}"
        self.entry.text = ""
        self.entry.hint_text = f"کلمه {len(self.secret)} حرفی"
        self.entry.disabled = False
        self.guess_btn.disabled = False

    def submit_guess(self, *_):
        if self.over:
            return
        guess = self.entry.text.strip().upper()
        if not guess.isalpha() or not guess.isascii():
            self.status.text = "لطفاً فقط حروف انگلیسی وارد کن."
            return
        if len(guess) != len(self.secret):
            self.status.text = f"حدس باید دقیقاً {len(self.secret)} حرف داشته باشد."
            return
        self.used += 1
        exact = sum(self.secret[i] == guess[i] for i in range(len(self.secret)))
        common = sum(min(self.secret.count(ch), guess.count(ch)) for ch in set(guess))
        misplaced = common - exact
        if guess == self.secret:
            points = (self.limit - self.used + 1) * 100
            self.total_score += points
            self.log.text += f"\n✓ {guess} — آفرین! قفل باز شد. +{points} امتیاز\n"
            self.status.text = f"بردی! تلاش‌ها: {self.used}"
            self.score_label.text = f"امتیاز کل: {self.total_score}"
            self.finish()
            return
        self.log.text += f"\n{self.used}. {guess}  | جای درست: {exact}  | جای اشتباه: {misplaced}\n"
        remaining = self.limit - self.used
        self.status.text = f"جای درست: {exact} | جای اشتباه: {misplaced} | فرصت: {remaining}"
        self.entry.text = ""
        if remaining <= 0:
            self.log.text += f"\nباختی! کلمه مخفی: {self.secret}\n"
            self.finish()

    def finish(self):
        self.over = True
        self.entry.disabled = True
        self.guess_btn.disabled = True

if __name__ == "__main__":
    WordLockApp().run()
