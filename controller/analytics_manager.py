class AnalyticsManager:

    def __init__(self):

        self.current_game = "None"
        self.current_score = 0
        self.high_score = 0
        self.status = "Waiting"
        self.time_played = "00:00"
        self.gesture = "NO HAND"

        self.high_scores = {

            "Fruit Ninja": 0,
            "Snake": 0,
            "Racing": "00:00",
            "Flappy Bird": 0,
            "Space Shooter": 0

        }

    # ---------------------------------------
    # Update Live Game
    # ---------------------------------------

    def update(

        self,

        game,

        score,

        high_score,

        status,

        time_played,

        gesture

    ):

        self.current_game = game
        self.current_score = score
        self.high_score = high_score
        self.status = status
        self.time_played = time_played
        self.gesture = gesture

        if game in self.high_scores:

            self.high_scores[game] = high_score


analytics = AnalyticsManager()