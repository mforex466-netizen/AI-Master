import json
import os
import re
import hashlib
import secrets
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.core.clipboard import Clipboard

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "ai_master_data.json")

KV = r"""
#:import dp kivy.metrics.dp
<DarkButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: (0.35, 0.28, 0.95, 1) if self.state == 'normal' else (0.25, 0.20, 0.75, 1)
    color: 1,1,1,1
    bold: True
    font_size: '14sp'
    size_hint_y: None
    height: dp(48)

<SoftButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: (0.12, 0.16, 0.25, 1)
    color: (0.86,0.89,1,1)
    font_size: '13sp'
    size_hint_y: None
    height: dp(44)

<Heading@Label>:
    color: (0.95,0.96,1,1)
    bold: True
    font_size: '22sp'
    halign: 'left'
    valign: 'middle'
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1] + dp(8)

<SubText@Label>:
    color: (0.68,0.73,0.84,1)
    font_size: '13sp'
    halign: 'left'
    valign: 'top'
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1] + dp(10)

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(18)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.035,0.05,0.10,1)
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(42)
            Label:
                text: '[b]AI[/b] [color=8C7CFF]MASTER[/color]'
                markup: True
                font_size: '23sp'
                halign: 'left'
                color: 1,1,1,1
            Label:
                text: 'ACADEMY'
                color: (0.5,0.58,0.75,1)
                font_size: '10sp'
                size_hint_x: None
                width: dp(65)
        Label:
            text: root.profile_text
            color: (0.72,0.76,0.9,1)
            font_size: '12sp'
            size_hint_y: None
            height: dp(24)
            halign: 'left'
        Heading:
            text: 'Sun’iy intellektni boshqarishni o‘rgan!'
        SubText:
            text: 'O‘rgan • Sinab ko‘r • Yarat • Xavfsiz foydalan'
        BoxLayout:
            size_hint_y: None
            height: dp(82)
            padding: dp(12)
            canvas.before:
                Color:
                    rgba: (0.10,0.13,0.23,1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(14)]
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'SENING O‘QUV NATIJANG'
                    color: (0.62,0.69,0.83,1)
                    font_size: '10sp'
                    halign: 'left'
                Label:
                    text: root.progress_text
                    color: (0.65,0.58,1,1)
                    bold: True
                    font_size: '23sp'
                    halign: 'left'
        ScrollView:
            do_scroll_x: False
            GridLayout:
                cols: 1
                spacing: dp(9)
                size_hint_y: None
                height: self.minimum_height
                DarkButton:
                    text: '✦  PROMPT AKADEMIYASI'
                    on_release: root.manager.current = 'learn'
                DarkButton:
                    text: '⚡  PROMPT DOCTOR'
                    on_release: root.manager.current = 'doctor'
                DarkButton:
                    text: '▧  AI IMAGE & VIDEO LAB'
                    on_release: root.manager.current = 'lab'
                DarkButton:
                    text: '◈  5 TA MUHIM AI PLATFORMASI'
                    on_release: root.manager.current = 'tools'
                DarkButton:
                    text: '盾  AI XAVFSIZLIGI'
                    on_release: root.manager.current = 'safety'
                DarkButton:
                    text: '✓  TEST MARKAZI'
                    on_release: root.manager.current = 'quiz'
                DarkButton:
                    text: '▤  PROMPT KUTUBXONASI'
                    on_release: root.manager.current = 'library'
        SoftButton:
            text: 'CHIQISH / PROFILNI ALMASHTIRISH'
            on_release: root.app.logout()
        SoftButton:
            text: 'LOYIHA HAQIDA'
            on_release: root.manager.current = 'about'

<ContentScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.035,0.05,0.10,1)
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(42)
            SoftButton:
                text: '‹ ORQAGA'
                size_hint_x: None
                width: dp(105)
                on_release: root.manager.current = 'home'
            Label:
                text: root.title_text
                color: (0.93,0.94,1,1)
                bold: True
                font_size: '17sp'
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: body
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
"""


class LoginScreen(Screen):
    """Local prototype authentication. Google OAuth requires a configured backend."""
    app = None
    mode = StringProperty("login")

    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(22), spacing=dp(12))
        with root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.035, 0.05, 0.10, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *_: setattr(self._bg, "pos", root.pos),
                  size=lambda *_: setattr(self._bg, "size", root.size))

        brand = Label(text='[b]AI[/b] [color=8C7CFF]MASTER[/color]', markup=True,
                      font_size="30sp", size_hint_y=None, height=dp(58))
        root.add_widget(brand)
        subtitle = Label(text="Sun’iy intellekt akademiyasiga xush kelibsiz",
                         color=(.7,.75,.86,1), font_size="14sp",
                         size_hint_y=None, height=dp(42))
        root.add_widget(subtitle)

        self.name_input = TextInput(hint_text="Ismingiz (ro‘yxatdan o‘tishda)",
            multiline=False, size_hint_y=None, height=dp(48), opacity=1 if self.mode=="register" else 0,
            disabled=self.mode!="register", background_color=(.10,.13,.21,1),
            foreground_color=(1,1,1,1), hint_text_color=(.6,.65,.75,1), padding=dp(12))
        root.add_widget(self.name_input)
        self.email_input = TextInput(hint_text="Email manzil", multiline=False,
            size_hint_y=None, height=dp(48), background_color=(.10,.13,.21,1),
            foreground_color=(1,1,1,1), hint_text_color=(.6,.65,.75,1), padding=dp(12))
        root.add_widget(self.email_input)
        self.password_input = TextInput(hint_text="Parol (kamida 8 belgi)", password=True,
            multiline=False, size_hint_y=None, height=dp(48), background_color=(.10,.13,.21,1),
            foreground_color=(1,1,1,1), hint_text_color=(.6,.65,.75,1), padding=dp(12))
        root.add_widget(self.password_input)

        self.message = Label(text="Mahalliy sinov hisobi. Parolingiz qurilmada xeshlangan holda saqlanadi.",
            color=(.65,.7,.82,1), font_size="12sp", size_hint_y=None, height=dp(54),
            halign="left", valign="middle")
        self.message.bind(width=lambda i,v: setattr(i,"text_size",(v,None)))
        root.add_widget(self.message)

        action = Button(text="HISOBGA KIRISH" if self.mode=="login" else "HISOB YARATISH",
            size_hint_y=None, height=dp(50), background_normal="",
            background_color=(.35,.28,.95,1), color=(1,1,1,1), bold=True)
        action.bind(on_release=lambda *_: self.submit())
        root.add_widget(action)

        switch = Button(text="Yangi hisob yaratish" if self.mode=="login" else "Hisobim bor — kirish",
            size_hint_y=None, height=dp(42), background_normal="",
            background_color=(.12,.16,.25,1), color=(.9,.91,1,1))
        switch.bind(on_release=lambda *_: self.switch_mode())
        root.add_widget(switch)

        google = Button(text="G  GOOGLE ORQALI KIRISH",
            size_hint_y=None, height=dp(46), background_normal="",
            background_color=(.18,.20,.28,1), color=(1,1,1,1))
        google.bind(on_release=lambda *_: self.google_info())
        root.add_widget(google)

        guest = Button(text="MEHMON SIFATIDA DAVOM ETISH",
            size_hint_y=None, height=dp(46), background_normal="",
            background_color=(.10,.13,.21,1), color=(.8,.84,.95,1))
        guest.bind(on_release=lambda *_: self.guest())
        root.add_widget(guest)

        note = Label(text="Eslatma: Google tugmasi hozircha namoyish rejimida. Haqiqiy Google OAuth uchun server va OAuth sozlamalari kerak.",
            color=(.53,.59,.72,1), font_size="11sp", halign="left", valign="top")
        note.bind(width=lambda i,v: setattr(i,"text_size",(v,None)))
        root.add_widget(note)
        self.add_widget(root)

    def clear_widgets(self):
        super().clear_widgets()

    def switch_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.render()

    def submit(self):
        email = self.email_input.text.strip().lower()
        password = self.password_input.text
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.message.text = "Email manzilni to‘g‘ri kiriting."
            return
        if len(password) < 8:
            self.message.text = "Parol kamida 8 belgidan iborat bo‘lsin."
            return
        users = self.app.data.setdefault("users", {})
        if self.mode == "register":
            name = self.name_input.text.strip()
            if len(name) < 2:
                self.message.text = "Ismingizni kiriting."
                return
            if email in users:
                self.message.text = "Bu email bilan hisob mavjud. Kirish bo‘limidan foydalaning."
                return
            salt = secrets.token_hex(16)
            digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                         bytes.fromhex(salt), 180000).hex()
            users[email] = {"name": name, "salt": salt, "password_hash": digest}
            self.app.data["current_user"] = {"email": email, "name": name, "mode": "local"}
            self.app.save()
            self.app.manager.current = "home"
            return
        user = users.get(email)
        if not user:
            self.message.text = "Hisob topilmadi. Avval ro‘yxatdan o‘ting."
            return
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                     bytes.fromhex(user["salt"]), 180000).hex()
        if not secrets.compare_digest(digest, user["password_hash"]):
            self.message.text = "Parol noto‘g‘ri. Qayta urinib ko‘ring."
            return
        self.app.data["current_user"] = {"email": email, "name": user["name"], "mode": "local"}
        self.app.save()
        self.app.manager.current = "home"

    def guest(self):
        self.app.data["current_user"] = {"email": "", "name": "Mehmon", "mode": "guest"}
        self.app.save()
        self.app.manager.current = "home"

    def google_info(self):
        self.app.popup("GOOGLE KIRISH",
            "Google orqali haqiqiy kirish hali ulanmagan. Buning uchun Google OAuth Client ID, server tomondagi token tekshiruvi va maxfiy sozlamalar kerak. Hozircha email/parol yoki mehmon rejimidan foydalaning.")


class MainScreen(Screen):
    app = None
    progress_text = StringProperty("0 BALL  •  0 DARS")
    profile_text = StringProperty("Foydalanuvchi")
    def on_pre_enter(self, *args):
        if self.app:
            self.progress_text = self.app.progress_text
            profile = self.app.data.get("current_user") or {"name": "Foydalanuvchi", "mode": "guest"}
            self.profile_text = f"Profil: {profile.get('name', 'Mehmon')}  •  {profile.get('mode', 'guest').upper()}"

class ContentScreen(Screen):
    title_text = StringProperty("AI MASTER")
    def clear(self):
        self.ids.body.clear_widgets()
    def add_label(self, text, size=14, color=(0.78,0.82,0.91,1), bold=False):
        w = Label(text=text, markup=True, size_hint_y=None, halign="left", valign="top",
                  color=color, font_size=f"{size}sp", bold=bold)
        w.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))
        w.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]+dp(8)))
        self.ids.body.add_widget(w)
        return w
    def add_input(self, hint, text="", height=130):
        w = TextInput(hint_text=hint, text=text, multiline=True, size_hint_y=None,
                     height=dp(height), background_normal="", background_active="",
                     background_color=(0.09,0.12,0.20,1), foreground_color=(1,1,1,1),
                     hint_text_color=(0.55,0.61,0.73,1), padding=dp(12), font_size="14sp")
        self.ids.body.add_widget(w)
        return w
    def add_button(self, text, callback):
        b = Button(text=text, size_hint_y=None, height=dp(47), bold=True,
                   background_normal="", background_color=(0.35,0.28,0.95,1),
                   color=(1,1,1,1))
        b.bind(on_release=lambda *_: callback())
        self.ids.body.add_widget(b)
        return b

class AIMasterApp(App):
    points = NumericProperty(0)
    completed = NumericProperty(0)
    def build(self):
        self.title = "AI MASTER"
        self.data = self.load_data()
        self.data.setdefault("users", {})
        self.data.setdefault("current_user", None)
        self.points = self.data.get("points", 0)
        self.completed = self.data.get("completed", 0)
        Builder.load_string(KV)
        sm = ScreenManager()
        self.manager = sm
        login = LoginScreen(name="login"); login.app = self; sm.add_widget(login)
        home = MainScreen(name="home"); home.app = self; sm.add_widget(home)
        for cls, name in [(LearnScreen,"learn"),(DoctorScreen,"doctor"),(LabScreen,"lab"),
                          (ToolsScreen,"tools"),(SafetyScreen,"safety"),(QuizScreen,"quiz"),
                          (LibraryScreen,"library"),(AboutScreen,"about")]:
            sm.add_widget(cls(name=name, app=self))
        sm.current = "home" if self.data.get("current_user") else "login"
        return sm
    @property
    def progress_text(self):
        return f"{self.points} BALL  •  {self.completed} DARS"
    def load_data(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except Exception:
            return {"points":0, "completed":0, "quiz_done":False, "users": {}, "current_user": None}
    def save(self):
        self.data["points"] = int(self.points)
        self.data["completed"] = int(self.completed)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    def reward(self, points=10):
        self.points += points
        self.completed += 1
        self.save()
    def logout(self):
        self.data["current_user"] = None
        self.save()
        self.manager.current = "login"
    def popup(self, title, message):
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        lab = Label(text=message, color=(0.1,0.1,0.15,1), halign="left", valign="middle")
        lab.bind(width=lambda i,v:setattr(i,"text_size",(v,None)))
        box.add_widget(lab)
        btn = Button(text="YOPISH", size_hint_y=None, height=dp(42))
        box.add_widget(btn)
        pop = Popup(title=title, content=box, size_hint=(.88,.48))
        btn.bind(on_release=pop.dismiss); pop.open()

class LearnScreen(ContentScreen):
    app = None
    def on_enter(self):
        self.title_text="PROMPT AKADEMIYASI"; self.clear()
        self.add_label("[b]Professional prompt formulasi[/b]",20,(0.65,0.58,1,1))
        self.add_label("Yaxshi prompt AI ga aniq vazifa, kontekst, talab va natija formatini beradi.")
        parts = [
            ("1. ROL","AI kim sifatida ishlasin? Masalan: tajribali o‘qituvchi."),
            ("2. VAZIFA","Nima qilishi kerak? Masalan: mavzuni sodda tushuntir."),
            ("3. KONTEKST","Kim uchun va nima maqsadda? Masalan: 1-kurs o‘quvchisi."),
            ("4. CHEKLOVLAR","Til, hajm, uslub va xavfsizlik talablarini yoz."),
            ("5. FORMAT","Javob jadval, ro‘yxat yoki bosqichlar ko‘rinishida bo‘lsin.")
        ]
        for h,t in parts:
            self.add_label(f"[b]{h}[/b]\n{t}")
        self.add_label("[b]Namuna prompt[/b]",18)
        self.add_label("Sen tajribali informatika o‘qituvchisisan. 1-kurs o‘quvchisiga sun’iy intellekt nima ekanini o‘zbek tilida sodda tushuntir. 3 ta hayotiy misol keltir, oxirida 5 ta nazorat savoli ber.")
        self.add_button("DARSNI TUGATDIM  +10 BALL", lambda: self.app.reward(10))

class DoctorScreen(ContentScreen):
    app=None
    def on_enter(self):
        self.title_text="PROMPT DOCTOR"; self.clear()
        self.add_label("[b]Prompt tekshiruvchisi[/b]",20,(0.65,0.58,1,1))
        self.add_label("Promptingni kiriting. Tizim uning aniqligi va to‘liqligini mahalliy qoidalar asosida baholaydi. Bu haqiqiy AI modeli emas, o‘quv analizatori.")
        self.input=self.add_input("Masalan: Menga tarix haqida ma’lumot ber...")
        self.add_button("PROMPTNI TAHLIL QILISH", self.analyze)
        self.result=self.add_label("Tahlil natijasi shu yerda chiqadi.")
    def analyze(self):
        text=self.input.text.strip()
        if len(text)<8:
            self.result.text="Prompt juda qisqa. Kamida aniq vazifa yozing."; return
        checks = {
            "Rol": bool(re.search(r"\b(sen|rol|mutaxassis|o‘qituvchi|ekspert)\b",text,re.I)),
            "Aniq vazifa": bool(re.search(r"\b(yoz|tushuntir|yarat|tahlil|tayyorla|hisobla|taqqosla)\b",text,re.I)),
            "Kontekst": bool(re.search(r"\b(uchun|maqsad|o‘quvchi|talaba|loyiha|mavzu)\b",text,re.I)),
            "Format": bool(re.search(r"\b(jadval|ro‘yxat|bosqich|band|misol|hajm)\b",text,re.I)),
            "Til/uslub": bool(re.search(r"\b(o‘zbek|ingliz|sodda|rasmiy|qisqa|batafsil)\b",text,re.I))
        }
        score=sum(checks.values())*20
        missing=[k for k,v in checks.items() if not v]
        advice="\n".join("• "+x for x in missing) if missing else "Barcha asosiy elementlar bor. Endi natijani tekshirib, zarur bo‘lsa aniqlashtiring."
        self.result.text=f"[b]BAHO: {score}/100[/b]\n"+ "\n".join(("✓ " if v else "○ ")+k for k,v in checks.items())+"\n\n[b]TAVSIYA[/b]\n"+advice
        self.app.reward(5)

class LabScreen(ContentScreen):
    app=None
    def on_enter(self):
        self.title_text="IMAGE & VIDEO LAB"; self.clear()
        self.add_label("[b]AI uchun vizual prompt tuzuvchi[/b]",20,(0.65,0.58,1,1))
        self.add_label("Bu bo‘lim tasvir yoki video yaratish xizmatiga yuborish uchun batafsil prompt tayyorlaydi. Rasmni o‘zi generatsiya qilmaydi.")
        self.subject=self.add_input("Obyekt yoki sahna: masalan, texnikumdagi o‘quvchilar",70)
        self.style=self.add_input("Uslub: masalan, cinematic, realistic, professional",70)
        self.details=self.add_input("Qo‘shimcha talablar: rang, yorug‘lik, format, saqlanishi kerak bo‘lgan detallar",90)
        self.add_button("IMAGE PROMPT YARATISH", lambda:self.make_prompt("image"))
        self.add_button("VIDEO PROMPT YARATISH", lambda:self.make_prompt("video"))
        self.out=self.add_label("Tayyor prompt shu yerda paydo bo‘ladi.")
    def make_prompt(self,kind):
        subject=self.subject.text.strip(); style=self.style.text.strip(); details=self.details.text.strip()
        if not subject:
            self.out.text="Avval sahna yoki obyektni kiriting."; return
        typ="high-quality image" if kind=="image" else "short cinematic video"
        self.generated=f"Create a {typ} of: {subject}. Visual style: {style or 'realistic, professional'}. Details: {details or 'balanced lighting, clear composition'}. Preserve the subject's identity and important original features when editing a reference image. Avoid unwanted distortions, text artifacts and misleading representations. Output: vertical 9:16 composition unless another format is specified."
        self.out.text="[b]TAYYOR PROMPT[/b]\n"+self.generated
        self.add_button("PROMPTNI NUSXALASH", lambda:Clipboard.copy(self.generated))

class ToolsScreen(ContentScreen):
    app=None
    def on_enter(self):
        self.title_text="5 TA MUHIM AI"; self.clear()
        tools=[
            ("ChatGPT","Matn, g‘oya, tahlil, o‘qish va dasturlash yordamchisi.","https://chatgpt.com"),
            ("Claude","Uzun matnlar, hujjatlar, tahlil va kod bilan ishlash.","https://claude.ai"),
            ("Google Gemini","Matn va multimodal vazifalar, Google ekotizimi.","https://gemini.google.com"),
            ("Midjourney","Tasvir yaratish va vizual konseptlar.","https://www.midjourney.com"),
            ("Canva","Taqdimot, poster, dizayn va vizual materiallar.","https://www.canva.com")
        ]
        for name,desc,url in tools:
            self.add_label(f"[b]{name}[/b]\n{desc}\n{url}",16)
        self.add_label("Eslatma: xizmatlarning bepul imkoniyatlari, narxlari va yosh cheklovlari farq qiladi. Ro‘yxatdan o‘tishdan oldin rasmiy shartlarni tekshiring.")

class SafetyScreen(ContentScreen):
    app=None
    def on_enter(self):
        self.title_text="AI XAVFSIZLIGI"; self.clear()
        self.add_label("[b]7 ta oltin qoida[/b]",20,(0.65,0.58,1,1))
        rules=[
            "Parol, bank karta ma’lumoti va maxfiy hujjatlarni AI chatiga kiritmang.",
            "Boshqa insonning rasmi yoki ovozidan ruxsatsiz foydalanmang.",
            "AI javobini haqiqat deb qabul qilmang — muhim ma’lumotni ishonchli manbadan tekshiring.",
            "Noma’lum havolalar va soxta AI ilovalaridan ehtiyot bo‘ling.",
            "AI yaratgan rasm yoki matnni o‘zingiz yaratgandek ko‘rsatmang; kerak bo‘lsa AI ishlatilganini belgilang.",
            "Mualliflik huquqi va platforma qoidalariga rioya qiling.",
            "Shubhali yoki zararli so‘rovlarni bajarmang; xavfsiz alternativani tanlang."
        ]
        for i,r in enumerate(rules,1): self.add_label(f"[b]{i}.[/b] {r}")
        self.add_label("[b]Deepfake haqida[/b]",18)
        self.add_label("Rasm yoki videoning haqiqiyligini bitta belgi bilan aniqlab bo‘lmaydi. Manba, sana, kontekst va mustaqil tasdiqlarni tekshiring. Avtomatik detektorlar xato qilishi mumkin.")
        self.add_button("XAVFSIZLIK DARSI TUGADI +10",lambda:self.app.reward(10))

class QuizScreen(ContentScreen):
    app=None
    QUESTIONS=[
        ("Kuchli promptda eng muhim narsa nima?",["Aniq vazifa va kontekst","Faqat uzun matn","Ko‘p emoji"],0),
        ("Maxfiy parolni AI chatiga yuborish mumkinmi?",["Ha","Yo‘q","Faqat kechasi"],1),
        ("AI javobini qanday ishlatish kerak?",["Har doim tekshirish","Darhol haqiqat deb olish","Manbasiz tarqatish"],0),
        ("Prompt Doctor bu versiyada nima qiladi?",["Mahalliy qoidalar bilan tahlil","Rasm chizadi","Internetni boshqaradi"],0),
        ("Boshqa odam suratidan foydalanishda nima muhim?",["Ruxsat va maxfiylik","Hech narsa","Faqat filtr"],0)
    ]
    def on_enter(self):
        self.title_text="TEST MARKAZI"; self.clear(); self.index=0; self.score=0; self.answered=False
        self.qlabel=self.add_label("",18,(0.95,0.96,1,1),True)
        self.buttons=[]
        for i in range(3):
            b=Button(text="",size_hint_y=None,height=dp(48),background_normal="",background_color=(.12,.16,.25,1),color=(1,1,1,1))
            b.bind(on_release=lambda btn,idx=i:self.answer(idx))
            self.ids.body.add_widget(b); self.buttons.append(b)
        self.feedback=self.add_label("")
        self.add_button("KEYINGI SAVOL",self.next_question)
        self.show_question()
    def show_question(self):
        q=self.QUESTIONS[self.index]
        self.qlabel.text=f"SAVOL {self.index+1}/{len(self.QUESTIONS)}\n{q[0]}"
        for i,b in enumerate(self.buttons): b.text=q[1][i]; b.disabled=False
        self.feedback.text=""
    def answer(self,idx):
        if self.answered:return
        self.answered=True
        correct=self.QUESTIONS[self.index][2]
        if idx==correct:
            self.score+=1; self.feedback.text="✓ To‘g‘ri javob!"; self.feedback.color=(.4,.9,.65,1)
        else:
            self.feedback.text="To‘g‘ri javob: "+self.QUESTIONS[self.index][1][correct]; self.feedback.color=(1,.65,.55,1)
        for b in self.buttons:b.disabled=True
    def next_question(self):
        if not self.answered:
            self.feedback.text="Avval javobni tanlang."; return
        self.index+=1; self.answered=False
        if self.index>=len(self.QUESTIONS):
            self.app.points+=self.score*2; self.app.completed+=1; self.app.save()
            self.app.popup("TEST YAKUNLANDI",f"Natija: {self.score}/{len(self.QUESTIONS)}\nBonus: {self.score*2} ball")
            self.manager.current="home"
        else:self.show_question()

class LibraryScreen(ContentScreen):
    app=None
    PROMPTS=[
        ("Dars tushuntirish","Sen tajribali o‘qituvchisan. [MAVZU]ni [SINF/KURS] o‘quvchisiga sodda o‘zbek tilida tushuntir. 3 misol va 5 savol ber."),
        ("Taqdimot","[MAVZU] bo‘yicha 8 slaydlik taqdimot rejasi tuz. Har slaydga sarlavha, 3 asosiy fikr va rasm g‘oyasi yoz."),
        ("Rasm tahriri","Ushbu suratni [USLUB] ko‘rinishiga o‘zgartir. Asosiy shaxsning yuzi va o‘ziga xos belgilarini o‘zgartirma. Fon: [FON]. Format: 9:16."),
        ("Kod yordamchisi","Sen Python murabbiyisan. Quyidagi kodni tahlil qil, xatolarni tushuntir va xavfsiz, izohlangan tuzatilgan variantni ko‘rsat: [KOD]."),
        ("Intervyu","[TADBIR/MAVZU] haqida o‘quvchilarga berish uchun 10 ta qisqa, odobli va qiziqarli intervyu savoli tuz.")
    ]
    def on_enter(self):
        self.title_text="PROMPT KUTUBXONASI"; self.clear()
        self.add_label("Tayyor promptni tanlang va nusxalang.",15)
        for title,prompt in self.PROMPTS:
            self.add_label(f"[b]{title}[/b]\n{prompt}",14)
            self.add_button("NUSXALASH: "+title,lambda p=prompt:Clipboard.copy(p))

class AboutScreen(ContentScreen):
    app=None
    def on_enter(self):
        self.title_text="LOYIHA HAQIDA"; self.clear()
        self.add_label("[b]AI MASTER — Sun’iy intellekt akademiyasi[/b]",20,(0.65,0.58,1,1))
        self.add_label("Mualliflik o‘quv loyihasi: Sergeli tumani 1-son texnikum o‘quvchilari uchun AI savodxonligi, prompt engineering va raqamli xavfsizlikni o‘rgatish.")
        self.add_label("[b]Texnologiya[/b]\nPython + Kivy. O‘quv natijalari qurilmada JSON faylida saqlanadi.")
        self.add_label("[b]Muhim texnik izoh[/b]\nBu birinchi ishlaydigan MVP. Haqiqiy ChatGPT/Claude/Gemini API integratsiyasi, server orqali autentifikatsiya, bulutli sinxronlash va sertifikatni tekshirish tizimi keyingi bosqichda backend hamda maxfiy API kalitlari bilan qo‘shiladi. API kalitini mobil ilova ichiga ochiq yozish xavfsiz emas.")
        self.add_label("[b]Tanlov uchun keyingi rivojlantirish[/b]\n1. Backend va ma’lumotlar bazasi\n2. O‘qituvchi/admin paneli\n3. Haqiqiy AI API integratsiyasi\n4. O‘zbekcha video darslar\n5. QR-kodli sertifikat tekshiruvi\n6. Offline darslar va ko‘p tillilik")

if __name__ == "__main__":
    AIMasterApp().run()
