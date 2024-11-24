import tkinter as tk
import random

class BouncingBalls:
    def __init__(self, root):
        self.root = root
        self.root.title("Zıplayan Toplar")

        # Canvas ve kontrol paneli
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white") #Panelin boyutu ve rengi
        self.canvas.pack()
        self.control_frame = tk.Frame(root, bg="white")
        self.control_frame.pack(pady=10)

        # Boyut ve renk değişkenleri
        self.size_var = tk.IntVar(value=20)
        self.color_var = tk.StringVar(value="red")

        # Boyut düğmeleri
        size_frame = tk.Frame(self.control_frame, bg="white")
        size_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(size_frame, text="Boyut:", bg="white").pack(anchor=tk.W)

        for size in [20, 30, 40]:  # Boyut seçenekleri
            self.create_round_button(size_frame, size, "gray", size, self.add_random_ball)

        # Renk düğmeleri
        color_frame = tk.Frame(self.control_frame, bg="white")
        color_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(color_frame, text="Renk:", bg="white").pack(anchor=tk.W) #Yazı etiketi oluşturur ve konumunu belirler

        for color in ["red", "blue", "green"]:  #Renk seçenekleri
            self.create_round_button(color_frame, 30, color, color, self.set_color)

        #Kontrol düğmeleri
        control_frame = tk.Frame(self.control_frame, bg="white")
        control_frame.pack(side=tk.LEFT, padx=20)

        self.start_button = tk.Button(control_frame, text="START", command=self.start_animation, bg="white", fg="black", width=8, height=2)
        self.start_button.pack(side=tk.TOP, pady=5)

        self.stop_button = tk.Button(control_frame, text="STOP", command=self.stop_animation, bg="white", fg="black", width=8, height=2)
        self.stop_button.pack(side=tk.TOP, pady=5)

        self.reset_button = tk.Button(control_frame, text="RESET", command=self.reset_canvas, bg="white", fg="black", width=8, height=2)
        self.reset_button.pack(side=tk.TOP, pady=5)

        self.speedup_button = tk.Button(control_frame, text="Speed Up", command=self.speed_up, bg="white", fg="black", width=8, height=2)
        self.speedup_button.pack(side=tk.TOP, pady=5)

        #Top bilgileri
        self.balls = [] #Boş liste
        self.running = False
        self.speed_factor = 1 #Hız başlangıçta 1

        #Fare ile top ekleme
        self.canvas.bind("<Button-1>", self.add_ball)

    def create_round_button(self, parent, size, color, value, command):
        #Yuvarlak bir düğme oluşturur.
        canvas = tk.Canvas(parent, width=size, height=size, bg="white", highlightthickness=0)
        canvas.create_oval(0, 0, size, size, fill=color, outline="")
        canvas.pack(side=tk.LEFT, padx=5)
        canvas.bind("<Button-1>", lambda e: command(value))

    def add_ball(self, event):
        #Seçilen boyut ve renkte bir top ekler.
        size = self.size_var.get()
        color = self.color_var.get()
        x, y = event.x, event.y
        dx, dy = random.choice([-2, 2]), random.choice([-2, 2]) #Topları tuvale rastgele atar ve rastgele bir yön verir.
        ball = {
            "id": self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color),
            "dx": dx,
            "dy": dy,
            "size": size,
        }
        self.balls.append(ball)

    def add_random_ball(self, size):
        self.size_var.set(size)    #Seçilen boyutu ayarlar.
        x = random.randint(size, 600 - size)
        y = random.randint(size, 400 - size)
        self.add_ball_to_canvas(x, y)

    def add_ball_to_canvas(self, x, y):
        #Canvas üzerine bir top ekler.
        size = self.size_var.get()
        color = self.color_var.get()
        dx, dy = random.choice([-2, 2]), random.choice([-2, 2])
        ball = {
            "id": self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color),
            "dx": dx,
            "dy": dy,
            "size": size,
        }
        self.balls.append(ball)

    def set_color(self, color):
        #Top rengini ayarlar.
        self.color_var.set(color)

    def move_blls(self):
        #Topları hareket ettirir ve kenarlardan sekmesini sağlar.
        for ball in self.balls:
            self.canvas.move(ball["id"], ball["dx"] * self.speed_factor, ball["dy"] * self.speed_factor) #Her topu "id" X ve Y ekseninde, dx,dy ve hız faktörü ile hareket ettirir.
            x1, y1, x2, y2 = self.canvas.coords(ball["id"])
            if x1 <= 0 or x2 >= 600:
                ball["dx"] = -ball["dx"]
            if y1 <= 0 or y2 >= 400:
                ball["dy"] = -ball["dy"]

    def start_animation(self):
        #Animasyonu başlatır.
        if not self.running:
            self.running = True
            self.animate()

    def stop_animation(self):
        #Animasyonu durdurur.
        self.running = False

    def reset_canvas(self):
        #Tuvali sıfırlar.
        self.stop_animation()
        self.canvas.delete("all")
        self.balls = []
        self.speed_factor = 1

    def speed_up(self):
        #Topların hızını 0.5 artırır.
        self.speed_factor += 0.5

    def animate(self):
        #Animasyonu devam ettirir.
        if self.running:
            self.move_blls()
            self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBalls(root)
    root.mainloop()