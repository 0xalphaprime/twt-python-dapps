import hashlib
import time

class Move: 
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __init__(self, commitment, move=0):
        self.commitment = commitment
        self.move = move
    
    @classmethod
    def move_to_str(cls, move):
        return {
            cls.NONE: "None",
            cls.ROCK: "Rock",
            cls.PAPER: "Paper",
            cls.SCISSORS: "Scissors" 
        }[move]
    

class Challenge:
    def __init__(self, creator_address, _id, commitment):
        self.creator_address = creator_address
        self.opponent_address = None
        self.commitments = {
            self.creator_address: Move(commitment)
        }
        self.id = _id

        self.winner_address = None
        self.created_at = time.time() 

    def add_oponent(self, address, commitment):
        self.opponent_address = address
        self.commitments[address] = Move(commitment)

    def reveal(self, address, move, nonce):
        if not self.has_opponent_committed():
            raise Exception("Opponent not set")
        
        reveal_hash = Challenge.generate_hash(nonce + move)
        committed_move = self.commitments.get(address)
        if committed_move.commitment != reveal_hash:
            raise Exception("Invalid reveal hash")
        
        self.commitments[address].move = int(move)


        
    @staticmethod
    def generate_hash(input):
        return hashlib.sha256(input.encode()).hexdigest()
    
    def both_revealed(self):
        opponent_move = self.commitments[self.opponent_address].move
        creator_move = self.commitments[self.creator_address].move
        return opponent_move != Move.NONE and creator_move != Move.NONE
    
    def has_opponent_committed(self):
        return self.commitments.get(self.opponent_address) != None

    def evalaute_winner(self):
        opponent_move = self.commitments[self.opponent_address].move
        creator_move = self.commitments[self.creator_address].move

        if creator_move == Move.ROCK and opponent_move == Move.SCISSORS:
            self.winner_address = self.creator_address
        elif creator_move == Move.PAPER and opponent_move == Move.ROCK:
            self.winner_address = self.creator_address
        elif creator_move == Move.SCISSORS and opponent_move == Move.PAPER:
            self.winner_address = self.creator_address
        elif opponent_move == Move.ROCK and creator_move == Move.SCISSORS:
            self.winner_address = self.opponent_address
        elif opponent_move == Move.PAPER and creator_move == Move.ROCK:
            self.winner_address = self.opponent_address
        elif opponent_move == Move.SCISSORS and creator_move == Move.PAPER:
            self.winner_address = self.opponent_address
        
        return self.winner_address
    