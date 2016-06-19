class Brew(object):
    """Help you to brew coffee."""

    ratio = 30 / 1000 # grams per mililitre

    def _water(self, grounds):
        """Determine how much water (in mililitre) to use for a given
        number of grounds (in grams) in a direct drip style brew.
        """
        return grounds / self.ratio

    def _grounds(self, water):
        """Determine how much coffee grounds (in grams) needs to be
        added to a given amount of water (in militres).
        """
        return  water * self.ratio

class ColdBrew(Brew):
    """Help you to make cold brew coffee, i.e. to keep ratios and dilutions
    straight.

    Examples:
        # 1)
        # if you have made some cold brew concentrate using some random
        # combination of grounds and coffee, create an object using the
        # fromResults class method
        coffee = ColdBrew.fromResults(grounds=75, water=600)

        # call getDrink on the object to know how you need to dilute it
        coffee.getDrink(size=250)
        > Mix 60 ml concentrate with 190 ml water!

        # 2)
        # before creating the concentrate, call water() or grounds() on a
        # ColdBrew object to determine how to create a concentrate that will
        # need to be diluted to a given ratio
        concentrate = ColdBrew(dilution=3) # will need to be diluted 1 to 3
        concentrate.water(grounds=50) # how much water to add to 50 grams
                                      # of coffee grounds
        > 416.6666666666667
    """

    _dilution = 4 # default dilution

    def __init__(self, dilution=_dilution):
        """The dilution refers to how concentrated we want to the cold
        brew to be, i.e. to what ratio we will have to dilute it before
        drinking. Ratio is given as n in 1/n, where a dilution of 1/n
        means add 1 unit of concentrate to n units of solvent.
        """
        self.dilution = dilution

    def __repr__(self):
        return "Represents a concentrate with a dilution ratio of 1 over %.1f" % self.dilution

    @classmethod
    def fromResults(cls, grounds, water):
        """Given the result of a brew with a number of grounds [gram]
        per water [mililitre], set the dilution ratio.
        """
        extraction = grounds / water
        required = grounds / Brew.ratio
        difference = required - water
        if difference < 0:
            raise Exception("Brew is already too dilute!")
        else:
            ratio = (required - water) / water
        return cls(ratio)

    def _water(self, grounds):
        """Determine how much water (in mililitres) needs to be added to a
        given amount of coffee grounds (in grams).
        """
        water = super()._water(grounds) / (self.dilution + 1)
        return water

    def water(self, grounds):
        print("Add %.0f ml of water" % self._water(grounds))

    def _grounds(self, water):
        """Determine how much coffee grounds (in grams) needs to be
        added to a given amount of water (in mililitres).
        """
        grounds = super()._grounds(water) * (self.dilution + 1)
        return grounds

    def grounds(self, water):
        print("Add %.0f g of coffee" % self.grounds(water))

    def getDrink(self, size):
        """Tell how much water needs to be added to what amount of concentrate
        to create a given volume of drink (in mililitres).
        """
        concentrate = size / (1 + self.dilution)
        mixer = size - concentrate
        print("Mix %.0f ml concentrate with %.0f ml water!" % (concentrate,
            mixer))

    def useConcentrate(self, concentrate):
        """Tell how much water needs to be added to a given amount of
        concentrate.  Useful when there's some concentrate left over or if the
        user poured too much concentrate.
        """
        mixer = concentrate * self.dilution
        print("Add %.0f ml water for a drink of %.0f ml!" % (mixer, mixer +
            concentrate))
