import pygame as pg
import csv
import matplotlib.pyplot as plt
import io

class StatsView:
    def __init__(self, screen, csv_path="results.csv"):
        self.screen = screen
        self.csv_path = csv_path
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 28)
        self.scroll_offset = 0
        self.scroll_speed = 30
        self.back_button_rect = pg.Rect(20, 20, 120, 40)

        self.stats_data = self.load_csv_data()
        self.graph_surfaces = self.generate_graphs() 

    def load_csv_data(self):
        try:
            with open(self.csv_path, newline='') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []

    def generate_graphs(self):
        if not self.stats_data:
            return []

        last_sessions = self.stats_data[-20:]
        all_sessions = list(range(len(self.stats_data)))
        recent_sessions = list(range(len(last_sessions)))
        metrics = ["WPM", "Accuracy (%)", "Score"]
        comparisons = [
            ("WPM vs Accuracy", "WPM", "Accuracy (%)"),
            ("Score vs Accuracy", "Score", "Accuracy (%)")
        ]

        surfaces = []

        for metric in metrics:
            y = [float(row.get(metric, 0)) for row in last_sessions]
            surfaces.append(self.plot_to_surface(recent_sessions, y, title=f"{metric} (Recent)"))

        for metric in metrics:
            y = [float(row.get(metric, 0)) for row in self.stats_data]
            surfaces.append(self.plot_to_surface(all_sessions, y, title=f"{metric} (All Time)"))

        for title, m1, m2 in comparisons:
            y1 = [float(row.get(m1, 0)) for row in last_sessions]
            y2 = [float(row.get(m2, 0)) for row in last_sessions]
            fig, ax = plt.subplots()
            ax.plot(recent_sessions, y1, marker='o', label=m1)
            ax.plot(recent_sessions, y2, marker='x', label=m2)
            ax.set_title(title)
            ax.legend()
            fig.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='PNG')
            plt.close(fig)
            buf.seek(0)
            surfaces.append(pg.image.load(buf))

        return surfaces

    def plot_to_surface(self, x, y, title="Stat"):
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o')
        ax.set_title(title)
        ax.set_xlabel("Sessions")
        ax.set_ylabel(title)
        fig.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close(fig)
        buf.seek(0)
        return pg.image.load(buf)

    def draw(self):
        self.screen.image.fill((10, 10, 30))

        # Draw graphs
        y_offset = 80 - self.scroll_offset
        for graph in self.graph_surfaces:
            self.screen.image.blit(graph, (50, y_offset))
            y_offset += graph.get_height() + 30

        # Draw Back Button (always on top)
        pg.draw.rect(self.screen.image, (50, 50, 150), self.back_button_rect, border_radius=8)
        back_text = self.small_font.render("< Back", True, (255, 255, 255))
        self.screen.image.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 8))

        pg.display.flip()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.button == 5:
                self.scroll_offset += self.scroll_speed
            elif self.back_button_rect.collidepoint(event.pos):
                return "menu"
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return "menu"
        return "stats"
