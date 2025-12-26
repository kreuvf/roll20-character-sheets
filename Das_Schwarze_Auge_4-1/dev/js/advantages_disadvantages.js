/* advantages_disadvantages start */
/* Nightblind */
const attrsNightblind = [
	'nachteil_nachtblind',
];
Object.freeze(attrsNightblind);

on(attrsNightblind.map(attr => "change:" + attr).join(" ").toLowerCase(),
	function() {
		safeGetAttrs(
			attrsNightblind, function(v) {
				if(v.nachteil_nachtblind != "0")
				{
					safeSetAttrs({
							vorteil_daemmerungssicht: "0",
							vorteil_nachtsicht: "0"
						});
				}
		});
});

/* Enhanced vision */
const attrsEnhancedVision = [
	'vorteil_daemmerungssicht',
	'vorteil_nachtsicht',
];
Object.freeze(attrsEnhancedVision);

on(attrsEnhancedVision.map(attr => "change:" + attr).join(" ").toLowerCase(),
	function() {
		safeGetAttrs(
			attrsEnhancedVision, function(v) {
				if(v.vorteil_daemmerungssicht != "0" || v.vorteil_nachtsicht != "0")
				{
					safeSetAttrs({nachteil_nachtblind: "0"});
				}
		});
});

/* Crit-level affecting advantages/disadvantages */
const attrsCritLevel = [
	'n_tollpatsch',
	'n_wildemagie',
];
Object.freeze(attrsCritLevel);

on( [ 'safe-sheet-open', ...attrsCritLevel ].map(attr => "change:" + attr).join(" ").toLowerCase(),
	function(eventInfo) {
		const caller = "Action Listener (Crit Level Updater, Advantages/Disadvantages)";
		const trigger = eventInfo["triggerName"];
		const newValue = eventInfo["newValue"];

		safeGetAttrs(
			attrsCritLevel, function(v) {
				const results = calcCritLevels({'Tollpatsch': v['n_tollpatsch'], 'wilde Magie': v['n_wildemagie']});
				let attrsToChange = {
					'cs_talent': results['talent']['success'],
					'cf_talent': results['talent']['failure'],
					'cs_kampf_at': results['kampf_at']['success'],
					'cf_kampf_at': results['kampf_at']['failure'],
					'cs_kampf_pa': results['kampf_pa']['success'],
					'cf_kampf_pa': results['kampf_pa']['failure'],
					'cs_kampf_fk': results['kampf_fk']['success'],
					'cf_kampf_fk': results['kampf_fk']['failure'],
					'cs_zauber': results['zauber']['success'],
					'cf_zauber': results['zauber']['failure'],
					'cs_ritual': results['ritual']['success'],
					'cf_ritual': results['ritual']['failure']
				}
				safeSetAttrs(attrsToChange);
		});
});

on(
"change:safe-sheet-open " +
"change:v_festematrix " +
"change:n_spruchhemmung " +
"change:n_wildemagie", function(eventInfo) {
	var caller = "Action Listener (Firm Matrix/Spell Inhibition/Clumsy Fellow/Wild Magic)";
	const attrsToGet = [
		"v_festematrix",
		"n_spruchhemmung",
		"n_wildemagie"
	];

	safeGetAttrs(attrsToGet, function(v) {
		var trigger = eventInfo["sourceAttribute"];
		var newValue = eventInfo["newValue"];
		var festeMatrix = v["v_festematrix"];
		var spruchhemmung = v["n_spruchhemmung"];
		var wildeMagie = v["n_wildemagie"];

		var attrsToChange = {};
		// Firm Matrix cannot be taken with either Spell Inhibition or Wild Magic
		if (trigger === "v_festematrix" && newValue === "1")
		{
			attrsToChange["n_spruchhemmung"] = "0";
			attrsToChange["n_wildemagie"] = "0";
		}
		if (
			(trigger === "n_spruchhemmung" || trigger === "n_wildemagie")
			&&
			newValue === "1"
		)
		{
			attrsToChange["v_festematrix"] = "0";
		}

		// If this is triggered by sheet opening and we find an impossible situation, rectify it.
		if (trigger === "safe-sheet-open" && festeMatrix === "1")
		{
			if (
				(spruchhemmung === "1" && wildeMagie === "0") ||
				(spruchhemmung === "0" && wildeMagie === "1")
			)
			{
				attrsToChange["n_spruchhemmung"] = "0";
				attrsToChange["n_wildemagie"] = "0";
			} else if (spruchhemmung === "1" && wildeMagie === "1")
			{
				attrsToChange["v_festematrix"] = "0";
			}
		}

		if (
			!(
				Object.keys(attrsToChange).length === 0 &&
				Object.getPrototypeOf(attrsToChange) === Object.prototype
			)
		)
		{
			safeSetAttrs(attrsToChange);
		}
	});
});
/* advantages_disadvantages end */
