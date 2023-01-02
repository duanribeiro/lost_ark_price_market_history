from joblib import Parallel, delayed
from best_combinations.task_best_combinations import match_engravings
from settings import mongo_collection_builds


def start_build_combinations():
    builds = [
        {
            'name': 'Mayhem Berserker',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'Mayhem': 15,
                'Grudge': 15,
                'Mass Increase': 15,
                "Masters's Tenacity": 15,
                'Cursed Doll': 15
            }
        },
        {
            'name': 'Technique Berserker',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Ambush Master': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Berserker's Technique": 15,
                'Awakening': 15
            }
        },
        {
            'name': 'Combat Blue Gunlancer',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Combat Readiness': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Barricade": 15,
                'Awakening': 15
            }
        },
        {
            'name': 'Lone Red Gunlancer',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'Lone Knight': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Super Charge": 15,
                'Spirit Absorption': 15
            }
        },
        {
            'name': 'Blessed Support Pali',
            'stats': ['Specialization', 'Swiftness'],
            'engravings_to_max': {
                'Blessed Aura': 15,
                'Awakening': 15,
                'Expert': 15,
                "Spirit Absorption": 15,
                'Heavy Armor': 15
            }
        },
        {
            'name': 'Judgement DPS Pali',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'Judgement': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Adrenaline": 15,
                'Raid Captain': 15
            }
        },
        {
            'name': 'Deathblow Striker',
            'stats': ['Crit', 'Specialization'],
            'engravings_to_max': {
                'Deathblow': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Ambush Master": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Esoteric Fury Striker',
            'stats': ['Swiftness', 'Specialization', 'Crit'],
            'engravings_to_max': {
                'Esoteric Flurry': 15,
                'Grudge': 15,
                'Mass Increase': 15,
                "Ambush Master": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Robust Soulfist',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Robust Spirit': 15,
                'Mass Increase': 15,
                'Cursed Doll': 15,
                "Awakening": 15,
                'Adrenaline': 15
            }
        },
        {
            'name': 'Energy Soulfist',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'Energy Overflow': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Raid Captain": 15,
                'Precise Dagger': 15
            }
        },
        {
            'name': 'Taijutsu Scrapper',
            'stats': ['Crit', 'Swiftness'],
            'engravings_to_max': {
                'Taijutsu': 15,
                'Cursed Doll': 15,
                'Keen Blunt Weapon': 15,
                "Adrenaline": 15,
                'Ambush Master': 15
            }
        },
        {
            'name': 'Shock Scrapper',
            'stats': ['Crit', 'Specialization'],
            'engravings_to_max': {
                'Shock Training': 15,
                'Cursed Doll': 15,
                'Keen Blunt Weapon': 15,
                "Adrenaline": 15,
                'Ambush Master': 15
            }
        },
        {
            'name': 'Esoteric Wardancer',
            'stats': ['Specialization', 'Swiftness'],
            'engravings_to_max': {
                'Esoteric Skill Enhancement': 15,
                'Cursed Doll': 15,
                'Mass Increase': 15,
                "Ambush Master": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Intention Wardancer',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'First Intention': 15,
                'Cursed Doll': 15,
                'Mass Increase': 15,
                "Ambush Master": 15,
                'Raid Captain': 15
            }
        },
        {
            'name': 'Enhanced Deadeye',
            'stats': ['Specialization', 'Swiftness'],
            'engravings_to_max': {
                'Enhanced Weapon': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Ambush Master": 15,
                'Adrenaline': 15
            }
        },
        {
            'name': 'Pistoleer Deadeye',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Pistoleer': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Ambush Master": 15,
                'Adrenaline': 15
            }
        },
        {
            'name': 'Sharpshooter',
            'stats': ['Crit', 'Swiftness'],
            'engravings_to_max': {
                'Death Strike': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Loyal Companion": 15,
                'Hit Master': 15
            }
        },
        {
            'name': 'Firepower Artillerist',
            'stats': ['Crit', 'Swiftness'],
            'engravings_to_max': {
                'Firepower Enhancement': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Adrenaline": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Peacemaker Gunslinger',
            'stats': ['Crit', 'Swiftness'],
            'engravings_to_max': {
                'Peacemaker': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Hit Master": 15,
                'Adrenaline': 15
            }
        },
        {
            'name': 'Hunt Gunslinger',
            'stats': ['Crit', 'Specialization'],
            'engravings_to_max': {
                'Time to Hunt': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Peacemaker": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Surge Deathblade',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Surge': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Ambush Master": 15,
                'Adrenaline': 15
            }
        },
        {
            'name': 'Energy Deathblade',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Remaining Energy': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Super Charge": 15,
                'Ambush Master': 15
            }
        },
        {
            'name': 'Demonic Shadowhunter',
            'stats': ['Specialization', 'Crit'],
            'engravings_to_max': {
                'Demonic Impulse': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Adrenaline": 15,
                'Hit Master': 15
            }
        },
        {
            'name': 'Supression Shadowhunter',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'Perfect Suppression': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Ambush Master": 15,
                'Keen Blunt Weapon': 15
            }
        },
        {
            'name': 'Salvation Support Bard',
            'stats': ['Swiftness', 'Specialization'],
            'engravings_to_max': {
                'Desperate Salvation': 15,
                'Expert': 15,
                'Awakening': 15,
                "Heavy Armor": 15,
                'Increased Max MP': 15
            }
        },
        {
            'name': 'Valor DPS Bard',
            'stats': ['Swiftness', 'Crit'],
            'engravings_to_max': {
                'True Courage': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Keen Blunt Weapon": 15,
                'Spirit Absorption': 15
            }
        },
        {
            'name': 'Reflux Sorc',
            'stats': ['Crit', 'Swiftness'],
            'engravings_to_max': {
                'Reflux': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "Precise Dagger": 15,
                'Hit Master': 15
            }
        },
        {
            'name': 'Ignit Sorc',
            'stats': ['Crit', 'Specialization', 'Swiftness'],
            'engravings_to_max': {
                'Igniter': 15,
                'Grudge': 15,
                'Cursed Doll': 15,
                "All-Out Attack": 15,
                'Hit Master': 15
            }
        }
    ]
    mongo_collection_builds.drop()

    for region in ['North America West', 'Central Europe', 'South America']:
        Parallel(n_jobs=-1)(delayed(match_engravings)(build, region) for build in builds)


if __name__ == "__main__":
    start_build_combinations()