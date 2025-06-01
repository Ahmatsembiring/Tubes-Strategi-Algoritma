# Import library standar Python
import time  # Digunakan untuk menghitung waktu eksekusi
import random  # Digunakan jika bot harus bergerak secara acak

# Import tipe data untuk penjelasan tipe variabel (type hinting)
from typing import Optional, List, Tuple

# Import dari game engine
from game.logic.base import BaseLogic  # Kelas dasar semua bot
from game.models import GameObject, Board, Position  # Model utama dalam game
from ..util import get_direction  # Fungsi bantu untuk menentukan arah gerakan

# GACORLOGIC adalah bot dengan strategi greedy berbasis jarak dan poin
class GacorLogic(BaseLogic):
    def __init__(self):
        # Inisialisasi variabel internal bot
        self.goal_position: Optional[Position] = None  # Posisi target utama (bisa None jika tidak ada)
        self.is_returning_to_base: bool = False  # Menandakan apakah bot sedang dalam perjalanan pulang
        self.list_objective = []  # Daftar target (diamond, tombol) dengan format: [posisi, poin, rasio prioritas]
        self.target_position: Optional[Position] = None  # Posisi target aktif saat ini
        self.teleporter = []  # Daftar teleporter (format: [(posisi, dummy_val)])
        self.base_position: Optional[Position] = None  # Posisi base (tempat kembali)
        self.current_position: Optional[Position] = None  # Posisi bot saat ini
        self.is_teleporter_move = False  # Menandakan apakah barusan menggunakan teleporter
        self.start_time = None  # Waktu mulai (opsional, untuk logging)

    def initialize(self, board_bot: GameObject, board: Board):
        # Update posisi penting saat ini dari board dan bot
        self.current_position = board_bot.position
        self.base_position = board_bot.properties.base
        # Ambil semua teleporter di board
        self.teleporter = [(tp.position, 0) for tp in board.game_objects if tp.type == "TeleportGameObject"]
        # Update daftar target
        self.set_list_objective(board)

    def get_distance(self, a: Position, b: Position) -> int:
        # Menghitung jarak Manhattan antara dua titik (tanpa diagonal)
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_distance_teleporter(self, a: Position, b: Position) -> int:
        # Menghitung jarak a → teleporter1 → teleporter2 → b
        if len(self.teleporter) < 2:
            return 999  # Teleporter tidak tersedia atau tidak cukup, beri nilai besar
        return self.get_distance(a, self.teleporter[0][0]) + self.get_distance(self.teleporter[1][0], b)

    def set_priority(self, obj) -> List:
        # Hitung prioritas berdasarkan rasio (jarak / poin)
        distance = min(
            self.get_distance(self.current_position, obj[0]),  # Jarak langsung
            self.get_distance_teleporter(self.current_position, obj[0])  # Jarak lewat teleporter
        )
        obj[2] = distance / obj[1] if obj[1] != 0 else float('inf')  # Rasio: makin kecil makin prioritas
        return obj

    def time_to_go_home(self, board_bot: GameObject) -> bool:
        # Mengecek apakah sudah saatnya pulang (berdasarkan waktu sisa)
        time_left = board_bot.properties.milliseconds_left // 1000  # Waktu tersisa dalam detik
        dist_normal = self.get_distance(self.current_position, self.base_position)
        dist_teleporter = self.get_distance_teleporter(self.current_position, self.base_position)

        # Jika jarak + buffer waktu (2 detik) lebih besar dari waktu sisa, maka pulang
        if dist_teleporter < dist_normal:
            return dist_teleporter + 2 >= time_left
        else:
            return dist_normal + 2 >= time_left

    def set_list_objective(self, board: Board):
        # Mengambil semua diamond dan tombol reset yang bisa dijadikan target
        temp_objective = [[x.position, x.properties.points, 0] for x in board.diamonds]
        reset_buttons = [x for x in board.game_objects if x.type == "DiamondButtonGameObject"]
        if reset_buttons:
            # Tambahkan tombol reset ke dalam daftar target dengan nilai poin 0.75
            temp_objective.append([reset_buttons[0].position, 0.75, 0])
        # Hitung prioritas semua target
        self.list_objective = list(map(self.set_priority, temp_objective))
        # Urutkan berdasarkan prioritas terkecil (rasio jarak/poin)
        self.list_objective.sort(key=lambda e: e[2])

    def should_use_teleporter(self, target: Position) -> bool:
        # Menentukan apakah harus menggunakan teleporter untuk menuju target
        if len(self.teleporter) < 2:
            return False  # Tidak ada cukup teleporter

        dist_direct = self.get_distance(self.current_position, target)
        dist_tp = self.get_distance_teleporter(self.current_position, target)

        return dist_tp + 1 < dist_direct  # Gunakan teleporter jika secara signifikan lebih cepat

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        # Fungsi utama yang menentukan langkah bot di setiap giliran

        time_start = time.time()  # Logging waktu mulai
        self.initialize(board_bot, board)  # Update posisi dan target

        if self.is_teleporter_move:
            self.start_time = time.time()  # Catat waktu teleportasi
            self.is_teleporter_move = False

        # Cetak informasi penting (debug)
        print("bot time remaining:", board_bot.properties.milliseconds_left)
        print("current position = ", self.current_position)
        print("inventory: ", board_bot.properties.diamonds)

        # Keputusan strategis: pulang jika waktu hampir habis atau inventory penuh
        if self.time_to_go_home(board_bot):
            print("=== TIME TO GO HOME")
            self.target_position = self.base_position
        elif board_bot.properties.diamonds == 5:
            print("=== INVENTORY PENUH")
            self.target_position = self.base_position
        else:
            if board_bot.properties.diamonds == 4:
                # Hindari diamond merah (poin 2) jika sudah punya 4 diamond
                print("== DIAMOND MERAH DIHAPUS")
                self.list_objective = list(filter(lambda x: x[1] != 2, self.list_objective))

            # Ambil target terbaik (prioritas tertinggi = rasio terkecil)
            if self.list_objective:
                self.target_position = self.list_objective[0][0]
            else:
                self.target_position = None  # Tidak ada target

        # Debugging
        print("Teleporter position:", self.teleporter)
        print("Target position:", self.target_position)

        # Menentukan arah gerakan
        if self.target_position:
            if self.should_use_teleporter(self.target_position):
                # Arahkan ke teleporter pertama jika lebih cepat
                tp_entry = self.teleporter[0][0]
                print("USING TELEPORTER to reach target")
                delta_x, delta_y = get_direction(
                    self.current_position.x,
                    self.current_position.y,
                    tp_entry.x,
                    tp_entry.y
                )
                if self.current_position == tp_entry:
                    self.is_teleporter_move = True  # Tandai bahwa teleportasi sedang terjadi
            else:
                # Gerak langsung ke target
                delta_x, delta_y = get_direction(
                    self.current_position.x,
                    self.current_position.y,
                    self.target_position.x,
                    self.target_position.y
                )
        else:
            # Jika tidak ada target, gerak acak
            delta_x, delta_y = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

        print("Elapsed Time:", time.time() - time_start)  # Waktu proses 1 langkah bot
        return delta_x, delta_y  # Kembalikan gerakan yang akan dijalankan
