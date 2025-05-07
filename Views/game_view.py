class GameView:
    def __init__(self, renderer, dashboard, wave_view):
        self.renderer = renderer
        self.dashboard = dashboard
        self.wave_view = wave_view

    def draw(self, game_stats):
        self.renderer.update()
        self.dashboard.draw(game_stats.export())
        self.wave_view.draw(self.renderer.screen.image, game_stats.get_wave())