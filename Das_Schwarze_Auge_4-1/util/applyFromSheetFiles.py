#!/usr/bin/env python3

# Write Changes Back From Generated Files
# With the dev split 2024 new people contributed for the first time.
# Unfortunately, some of them were unaware of the consequences of applying
# their changes to the sheet files directly. In order to fix their commits, the
# concatenation must be executed in reverse ("decatenation"?). Since every file
# contains a unique header and a matching unique footer this should work without
# major issues.
#
# Running the Script
# Always run in the top directory of the sheet. The script will look for the
# respective signatures for the single files, save the line numbers and then cut
# the full files. THIS OVERWRITES THE EXISTING SOURCE FILES!
#
# Disclaimer
# This script is far from being "hardened" and should only be used when really
# sure to understand what the script is supposed to do.

import re

# Setup
## List of the files normally generated through running "make"
generated = [
	'dsa4_1_character_sheet_roll20.html',
	'dsa4_1_character_sheet_roll20.css'
]

## List of the files that make up the sheet's HTML file (order important)
filesHTML = [
	'dev/html/sheet/intro.html',
	'dev/html/sheet/header.html',
	'dev/html/sheet/sections/general.html',
	'dev/html/sheet/sections/stats.html',
	'dev/html/sheet/sections/advantages_disadvantages_special_skills.html',
	'dev/html/sheet/sections/inventory/intro.html',
	'dev/html/sheet/sections/inventory/header.html',
	'dev/html/sheet/sections/inventory/main.html',
	'dev/html/sheet/sections/inventory/purse.html',
	'dev/html/sheet/sections/inventory/outro.html',
	'dev/html/sheet/sections/talents/intro.html',
	'dev/html/sheet/sections/talents/header.html',
	'dev/html/sheet/sections/talents/combat_techniques.html',
	'dev/html/sheet/sections/talents/physical.html',
	'dev/html/sheet/sections/talents/social.html',
	'dev/html/sheet/sections/talents/nature.html',
	'dev/html/sheet/sections/talents/knowledge.html',
	'dev/html/sheet/sections/talents/languages.html',
	'dev/html/sheet/sections/talents/crafts.html',
	'dev/html/sheet/sections/talents/gifts.html',
	'dev/html/sheet/sections/talents/meta.html',
	'dev/html/sheet/sections/talents/outro.html',
	'dev/html/sheet/sections/magic/intro.html',
	'dev/html/sheet/sections/magic/header.html',
	'dev/html/sheet/sections/magic/aventuria/spells.html',
	'dev/html/sheet/sections/magic/myranor/conjuration.html',
	'dev/html/sheet/sections/magic/aventuria/rituals.html',
	'dev/html/sheet/sections/magic/advantages_disadvantages_special_skills.html',
	'dev/html/sheet/sections/magic/outro.html',
	'dev/html/sheet/sections/liturgies.html',
	'dev/html/sheet/sections/combat/intro.html',
	'dev/html/sheet/sections/combat/header.html',
	'dev/html/sheet/sections/combat/equipment.html',
	'dev/html/sheet/sections/combat/hand_to_hand.html',
	'dev/html/sheet/sections/combat/ranged.html',
	'dev/html/sheet/sections/combat/special_skills.html',
	'dev/html/sheet/sections/combat/outro.html',
	'dev/html/sheet/sections/regeneration/intro.html',
	'dev/html/sheet/sections/regeneration/header.html',
	'dev/html/sheet/sections/regeneration/relax.html',
	'dev/html/sheet/sections/regeneration/rest.html',
	'dev/html/sheet/sections/regeneration/sleep.html',
	'dev/html/sheet/sections/regeneration/astral_meditation.html',
	'dev/html/sheet/sections/regeneration/karmic_meditation.html',
	'dev/html/sheet/sections/regeneration/outro.html',
	'dev/html/sheet/sections/notes/intro.html',
	'dev/html/sheet/sections/notes/header.html',
	'dev/html/sheet/sections/notes/main.html',
	'dev/html/sheet/sections/notes/entities.html',
	'dev/html/sheet/sections/notes/locations.html',
	'dev/html/sheet/sections/notes/outro.html',
	'dev/html/sheet/sections/config.html',
	'dev/html/sheet/sections/info.html',
	'dev/html/sheet/footer.html',
	'dev/html/sheet/outro.html',
	'dev/html/roll_templates/intro.html',
	'dev/html/roll_templates/crp/intro.html',
	'dev/html/roll_templates/crp/talents.html',
	'dev/html/roll_templates/crp/spells.html',
	'dev/html/roll_templates/crp/liturgies.html',
	'dev/html/roll_templates/crp/hand_to_hand_combat.html',
	'dev/html/roll_templates/crp/outro.html',
	'dev/html/roll_templates/regeneration/intro.html',
	'dev/html/roll_templates/regeneration/deepbreath.html',
	'dev/html/roll_templates/regeneration/relax.html',
	'dev/html/roll_templates/regeneration/rest.html',
	'dev/html/roll_templates/regeneration/sleep.html',
	'dev/html/roll_templates/regeneration/astralmeditation.html',
	'dev/html/roll_templates/regeneration/karmicmeditation.html',
	'dev/html/roll_templates/regeneration/outro.html',
	'dev/html/roll_templates/legacy/intro.html',
	'dev/html/roll_templates/legacy/talents.html',
	'dev/html/roll_templates/legacy/spells.html',
	'dev/html/roll_templates/legacy/liturgies.html',
	'dev/html/roll_templates/legacy/stats.html',
	'dev/html/roll_templates/legacy/hand_to_hand_combat.html',
	'dev/html/roll_templates/legacy/ranged_combat.html',
	'dev/html/roll_templates/legacy/combat_shared.html',
	'dev/html/roll_templates/legacy/outro.html',
	'dev/html/roll_templates/tests.html',
	'dev/html/roll_templates/outro.html',
	'dev/js/intro.js',
	'dev/js/constants.js',
	'dev/js/utilities_general.js',
	'dev/js/utilities_dsa.js',
	'dev/js/initialization_migration_common.js',
	'dev/js/initialization.js',
	'dev/js/migration.js',
	'dev/js/base_values.js',
	'dev/js/advantages_disadvantages.js',
	'dev/js/talents.js',
	'dev/js/magic.js',
	'dev/js/magic_myranor.js',
	'dev/js/liturgies.js',
	'dev/js/melee.js',
	'dev/js/ranged_combat_calculator.js',
	'dev/js/ranged_combat_other.js',
	'dev/js/armour_encumbrance_initiative.js',
	'dev/js/wounds.js',
	'dev/js/regeneration.js',
	'dev/js/debug_mode.js',
	'dev/js/roll_macro_generator.js',
	'dev/js/other.js',
	'dev/js/outro.js'
]

## List of the files that make up the sheet's CSS file (order important)
filesCSS = [
	'dev/css/style.css'
]

fileSignaturesHTMLRest = {
	'dev/js/intro.js': [ '<!-- js intro start -->', '/* js intro end */' ],
	'dev/js/constants.js': [ '/* constants begin */', '/* constants end */' ],
	'dev/js/utilities_general.js': [ '/* utilities general begin */', '/* utilities general end */' ],
	'dev/js/utilities_dsa.js': [ '/* utilities dsa begin */', '/* utilities dsa end */' ],
	'dev/js/initialization_migration_common.js': [ '/* initialization migration common begin */', '/* initialization migration common end */' ],
	'dev/js/initialization.js': [ '/* initialization begin */', '/* initialization end */' ],
	'dev/js/migration.js': [ '/* migration begin */', '/* migration end */' ],
	'dev/js/base_values.js': [ '/* base values begin */', '/* base values end */' ],
	'dev/js/advantages_disadvantages.js': [ '/* advantages disadvantages begin */', '/* advantages disadvantages end */' ],
	'dev/js/talents.js': [ '/* talents begin */', '/* talents end */' ],
	'dev/js/magic.js': [ '/* magic begin */', '/* magic end */' ],
	'dev/js/magic_myranor.js': [ '/* magic_myranor begin */', '/* magic_myranor end */' ],
	'dev/js/liturgies.js': [ '/* liturgies begin */', '/* liturgies end */' ],
	'dev/js/melee.js': [ '/* melee begin */', '/* melee end */' ],
	'dev/js/ranged_combat_calculator.js': [ '/* ranged combat calculator begin */', '/* ranged combat calculator end */' ],
	'dev/js/ranged_combat_other.js': [ '/* ranged combat other begin */', '/* ranged combat other end */' ],
	'dev/js/armour_encumbrance_initiative.js': [ '/* armour encumbrance initiative begin */', '/* armour encumbrance initiative end */' ],
	'dev/js/wounds.js': [ '/* wounds begin */', '/* wounds end */' ],
	'dev/js/regeneration.js': [ '/* regeneration begin */', '/* regeneration end */' ],
	'dev/js/debug_mode.js': [ '/* debug mode begin */', '/* debug mode end */' ],
	'dev/js/roll_macro_generator.js': [ '/* roll macro generator begin */', '/* roll macro generator end */' ],
	'dev/js/other.js': [ '/* other begin */', '/* other end */' ],
	'dev/js/outro.js': [ '/* js outro start */', '<!-- js outro end -->' ]
}
fileSignaturesCSS = {
	'dev/css/style.css': [ '/* start CSS */', '/* end CSS */' ]
}

# Generate HTML File Signatures
## WIP: Currently only for sheet and roll_templates HTML, no JS
fileSignaturesHTML = {}
for file in filesHTML:
	topLevelPattern = re.compile(r"^(?P<prefix>dev/html)/(?P<type>sheet|roll_templates)/(?P<rest>.*)$")
	topLevelMatches = re.search(topLevelPattern, file)
	if topLevelMatches:
		snippetType = topLevelMatches.group('type')
		rest = topLevelMatches.group('rest')
		restPattern = re.compile(r"((?P<level1>[^/]+)/)?((?P<level2>[^/]+)/)?((?P<level3>[^/]+)/)?(?P<file>(?P<name>[^/]+)\.html)")
		restMatches = re.search(restPattern, rest)
		if restMatches:
			signatures = []
			maxLevel = 0
			name = restMatches.group('name')
			if restMatches.groupdict()['level1']:
				maxLevel += 1
				level1 = restMatches.group('level1')
				# Singular sections only exist in singular form
				if level1 == 'sections':
					level1 = 'section'
			if restMatches.groupdict()['level2']:
				maxLevel += 1
				level2 = restMatches.group('level2')
			if restMatches.groupdict()['level3']:
				maxLevel += 1
				level3 = restMatches.group('level3')
			match maxLevel:
				case 0:
					signature = '<!-- {type} {name} {{}} -->'.format(type = snippetType, name = name)
				case 1:
					signature = '<!-- {type} {l1} {name} {{}} -->'.format(type = snippetType, name = name, l1 = level1)
				case 2:
					signature = '<!-- {type} {l1} {l2} {name} {{}} -->'.format(type = snippetType, name = name, l1 = level1, l2 = level2)
				case 3:
					signature = '<!-- {type} {l1} {l2} {l3} {name} {{}} -->'.format(type = snippetType, name = name, l1 = level1, l2 = level2, l3 = level3)
				case _:
					print('maxLevel has suspicious value: {}'.format(maxLevel))
			signatures.append(signature.format('start'))
			signatures.append(signature.format('end'))
			print(signatures)
			fileSignaturesHTML[file] = signatures

fileSignaturesHTML |= fileSignaturesHTMLRest


# Finding Lines
with open("dsa4_1_character_sheet_roll20.html", mode = "r", encoding = "utf8") as html:
	htmlLines = html.readlines()

linesHTML = {}
for file in filesHTML:
	linesHTML[file] = []

for file in filesHTML:
	for entry in fileSignaturesHTML[file]:
		try:
			linesHTML[file].append(htmlLines.index(entry + '\n'))
		except:
			print(entry, 'could not be found')

with open("dsa4_1_character_sheet_roll20.css", mode = "r", encoding = "utf8") as css:
	cssLines = css.readlines()

linesCSS= {}
for file in filesCSS:
	linesCSS[file] = []

for file in filesCSS:
	for entry in fileSignaturesCSS[file]:
		try:
			linesCSS[file].append(cssLines.index(entry + '\n'))
		except:
			print(entry, 'could not be found')
exit()
# Writing files
for file in filesHTML:
	with open(file, mode = "w") as outfile:
		rangeStart = linesHTML[file][0]
		rangeEnd = linesHTML[file][1]+1
		print("file:", file, "rangeStart:", rangeStart, "rangeEnd:", rangeEnd)
		outfile.writelines(htmlLines[rangeStart:rangeEnd])
		outfile.close()

for file in filesCSS:
	with open(file, mode = "w") as outfile:
		rangeStart = linesCSS[file][0]
		rangeEnd = linesCSS[file][1]+1
		print("file:", file, "rangeStart:", rangeStart, "rangeEnd:", rangeEnd)
		outfile.writelines(cssLines[rangeStart:rangeEnd])
		outfile.close()
