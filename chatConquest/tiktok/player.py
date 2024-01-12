from chatConquest.game.character import create_character


class _Players:
    class _Player:
        def __init__(self, username):
            self.username = username

            self.character = None
            self.team = None

        def character_killed(self):
            self.character = None

        def new_character(self, unit_type='a'):
            match unit_type:
                case 'a':
                    self.character = create_character(self.team.castle.id_, self.team, "knight", self.character_killed)

    def __init__(self):
        self.players = []

    def __call__(self, username):
        for player in self.players:
            if player.username == username:
                return player
        else:
            self.players.append(self._Player(username))

    def __str__(self):
        string = ""
        for player in self.players:
            string += player.username
            string += ", "
        return string


players = _Players()
