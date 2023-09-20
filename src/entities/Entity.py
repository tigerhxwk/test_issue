from __future__ import annotations
import random

ENTITY_MIN_HP = 0
ENTITY_MAX_HP = 100
ENTITY_MIN_ATTACK = 1
ENTITY_MAX_ATTACK = 30
ENTITY_MIN_DMG = 1
ENTITY_MAX_DMG = 15

ENTITY_DICE_MIN = 1
ENTITY_DICE_MAX = 6
class CmnEntity:
    def __init__(self):
        self.maxHp = random.randint(ENTITY_MIN_HP + 1, ENTITY_MAX_HP)
        self.currHp = self.maxHp
        self.attack = random.randint(ENTITY_MIN_ATTACK, ENTITY_MAX_ATTACK)
        self.armor = random.randint(ENTITY_MIN_ATTACK, ENTITY_MAX_ATTACK)
        self.maxDamage = ENTITY_MAX_DMG


    def setMaxHp (self, maxHp = ENTITY_MAX_HP):
        if maxHp < ENTITY_MIN_HP or maxHp > ENTITY_MAX_HP:
            # this is going to make entity disappear
            self.setCurrHp(ENTITY_MIN_HP)
            return

        self.maxHp = maxHp
        self.setCurrHp (self.maxHp)


    def setCurrHp (self, currHp):
        if currHp < ENTITY_MIN_HP:
            self.setCurrHp(ENTITY_MIN_HP)
            return
        if currHp > ENTITY_MAX_HP:
            self.setCurrHp(ENTITY_MAX_HP)
            return
        self.currHp = currHp


    def getMaxHp (self):
        return self.maxHp


    def getCurrHp (self):
        return self.currHp


    def getAttack (self):
        return self.attack


    def getArmor (self):
        return self.armor


    def getDamage (self):
        return self.maxDamage


    def handleIncomingDamage (self, damage):
        if damage < ENTITY_MIN_DMG or damage > ENTITY_MAX_DMG:
            # ignore that something
            return
        print(f"damage taken {damage}")
        self.setCurrHp(self.getCurrHp() - damage)

    def DamageAttempt (self, opponent: CmnEntity):
        atkModifier = opponent.getAttack() - self.getArmor() + 1
        for diceCounter in range (0, atkModifier if atkModifier > 0 else 1):
            diceVal = random.randint(ENTITY_DICE_MIN, ENTITY_DICE_MAX)
            if diceVal == 5 or diceVal == 6:
                damage = random.randrange (1, opponent.getDamage( ))
                self.handleIncomingDamage(damage)
                return True, damage
        print("lucky boy, no damage taken")
        return False, 0


    def isEntityDown (self):
        if self.getCurrHp() <= 0:
            return True

        return False
