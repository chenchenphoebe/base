import collections

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)]+list('JQKA')
    suits = 'red white yellow blue'.split()

    def __init__(self):
        self._ab = [Card(rank,suit)for rank in self.ranks for suit in self.suits ]
    def __len__(self):
        return len(self._ab)
    def __getitem__(self, position):
        return self._ab[position]


deck = FrenchDeck()
print(deck[::])