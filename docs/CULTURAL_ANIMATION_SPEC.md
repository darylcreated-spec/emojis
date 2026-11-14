# CULTURAL ANIMATION DESIGN SPECIFICATION: PEELOFF TRINIDAD & TOBAGO (188 STICKERS)
## The Authoritative Cultural Reference Guide, Kinesic Profile & Procedural Animation Physics Engine

---

**Document Status:** Production Specification (Milestone 1 Deliverable)  
**Standard Version:** 1.0.0  
**Target Architecture:** PeelOff Client-Side PWA, Native Mobile Sharing, and Procedural Generator Pipeline  
**Asset Targets:** 188 3D Stickers (100 Themed Cultural Pack Stickers + 88 Literal Visual Slang Stickers)  
**Output Streams:** 376 Files (188 Animated 512×512 WebP RGBA + 188 Animated 512×512 Dark Card GIF89a)  
**Effective Cadence:** Strictly 24 Frames @ 90ms / frame = 2,160ms (2.16s) Infinite Looping Cycle  

---

## TABLE OF CONTENTS
1. [Section 1: Executive Summary & Cultural Animation Philosophy](#section-1-executive-summary--cultural-animation-philosophy)
   - 1.1 Executive Vision & Cultural Imperative
   - 1.2 Sociolinguistic Foundations of Trinidadian Creolese
   - 1.3 Polyrhythmic Dynamics: Calypso, Soca, and Caribbean Kinesics
   - 1.4 Group Chat Tactical Psychology in Trinidad & Tobago
2. [Section 2: Linguistic & Emotional Registers Taxonomy](#section-2-linguistic--emotional-registers-taxonomy)
   - 2.1 The Master 9-Register Framework
   - 2.2 Deep Sociolinguistic & Kinematic Register Profiles
   - 2.3 Master Register Comparison Matrix
3. [Section 3: Authentic Physical Gestures & Comedic Tropes](#section-3-authentic-physical-gestures--comedic-tropes)
   - 3.1 Biomechanical & Anatomical Framework
   - 3.2 Deep Kinematic Analysis of the 12 Core Gestures
   - 3.3 Visual Comedic Tropes & Caricature Exaggeration Rules
4. [Section 4: Procedural Motion Primitives & Mathematical Specifications](#section-4-procedural-motion-primitives--mathematical-specifications)
   - 4.1 The 24-Frame @ 90ms Standard Timeline
   - 4.2 Volume-Preserving Mesh Transformation Physics
   - 4.3 Mathematical Easing Models & Comic Timing Curves
   - 4.4 Exhaustive Mathematical Models for the 14 Motion Primitives
   - 4.5 Procedural Vector Graphic FX Engine
5. [Section 5: Master Cultural Mapping Matrix for All 188 Stickers](#section-5-master-cultural-mapping-matrix-for-all-188-stickers)
   - 5.1 Matrix Schema Architecture (9 Columns)
   - 5.2 Complete 188-Sticker Mapping Matrix Table (Rows 1–188)
6. [Section 6: Procedural Animation Engine Technical Architecture](#section-6-procedural-animation-engine-technical-architecture)
   - 6.1 PIL MESH Transform & Deformation Mechanics
   - 6.2 Breathing Room & Anti-Clipping Standards (`prep_breathing_room`)
   - 6.3 Frame Coalescing Elimination & The Micro-Motion Living Hold
   - 6.4 Procedural Vector Ink Engine & Layering Architecture
   - 6.5 Dual-Stream Production Export Pipeline
7. [Section 7: Quality Assurance, Verification Harness & Acceptance Criteria](#section-7-quality-assurance-verification-harness--acceptance-criteria)
   - 7.1 Quantitative Verification Assertions (Q1–Q11)
   - 7.2 Qualitative Cultural & Aesthetic Standards
   - 7.3 Automated Verification Harness Contract (`scripts/verify_animated_stickers.py`)
   - 7.4 Downstream Implementation Roadmap (Milestones 2–5)

---

## SECTION 1: EXECUTIVE SUMMARY & CULTURAL ANIMATION PHILOSOPHY

### 1.1 Executive Vision & Cultural Imperative
The PeelOff sticker suite is an open, cross-platform animated sticker engine designed to express the wit, physical theatre, and emotional richness of Trinidad & Tobago culture across global messaging ecosystems (WhatsApp, iMessage, Instagram Stories, TikTok, Discord, and Telegram). In modern digital communication, stickers do not merely decorate text—they act as surrogate vocal cords, physical postures, and cultural punctuation marks.

In early digital implementations of Caribbean emojis, technical pipelines frequently relied on generic mechanical deformers: uniform vertical sinusoidal squashes, rigid horizontal pans, or symmetrical rotation rocks. While computationally trivial, these mechanical loops actively strip Trinidadian communication of its soul. In Trinidad & Tobago, speech is an inherently bodily performance. An expression like *"ENT?!"* is never a disembodied word; it is an aggressive, sassy 20-degree neck cock, an arched eyebrow, and a hip shift. A *"STEUPS"* is not a sound effect; it is an explosive clench of the facial musculature followed by a contemptuous diagonal neck snap and an acoustic air jet.

This specification establishes the definitive design framework to eliminate all generic mechanical deformations. Every single sticker among the 188 catalog entities is grounded in authentic Caribbean kinesics, sociolinguistic intent, and calypso/soca polyrhythms.

### 1.2 Sociolinguistic Foundations of Trinidadian Creolese
Trinidadian Creolese (Trini Vernacular) is a dynamic linguistic creole shaped by centuries of historical syncretism:
- **West African Syntactic Structures**: Tonal pitch contours, high-context verbal economy, aspectual verbal markers, and call-and-response dynamics originating from Niger-Congo language families (Yoruba, Ibo, Akan).
- **French Patois (Antillean Creole)**: The linguistic backbone of Carnival, folklore, and rural banter (*bazodee*, *maljo*, *chupidee*, *pommerac*, *mauvais langue*, *jouvert*, *douen*).
- **Bhojpuri & Hindustani**: Deeply embedded agricultural, culinary, and social vocabulary brought by 19th-century indentured laborers (*channa*, *bara*, *roti*, *parsad*, *deya*, *kurma*, *pholourie*, *jharay*, *tassa*, *chowtal*).
- **Spanish Colonial Echoes**: Foundational holiday and musical customs (*parang*, *cuatro*, *pastelle*, *chac-chac*, *bocas*).
- **British English Subversion**: The sharp, satirical re-engineering of formal English syntax into biting irony, dramatic hyperbole, and competitive verbal sparring (*picong*).

Because Trini Creolese is highly oral and theatrical, meaning is heavily conveyed through bodily kinesics, timing, eye contact, and acoustic mouth movements. An animated sticker that fails to model the physical posture of the speaker fails to convey the linguistic message.

### 1.3 Polyrhythmic Dynamics: Calypso, Soca, and Caribbean Kinesics
Caribbean physical movement does not adhere to rigid European metronomic 4/4 beats. Instead, it is governed by:
- **The Calypso Syncopated Lilt**: An unhurried, swaying, confident weight shift (*contrapposto*) where the torso anticipates the beat, lingering in comedic suspension before dropping into the pocket.
- **The Power Soca Drive (140–160 BPM)**: An explosive, high-energy centrifugal cadence marked by airborne hops, rapid rotational rag windmills, and violent bass drops.
- **The Steelpan Triplet Rebound**: High-velocity elastic mallet strikes characterized by instantaneous physical contact followed by a spring-like micro-rebound and decaying structural acoustic shudder.

In procedural 2D animation, this polyrhythmic vitality is captured through **non-linear comic easing**: elongated suspenseful anticipation holds ($t_{antic}$), terminal-velocity acceleration strikes, damped resonant impact shakes, and living micro-motion holds during pauses.

### 1.4 Group Chat Tactical Psychology in Trinidad & Tobago
Stickers within Caribbean messaging groups fulfill five distinct tactical communicative functions:
1. **The Tactical Picong Drop**: When a friend overreaches, boasts, or suffers an embarrassing mishap, a roasting sticker must land with immediate comedic timing. The visual punchline must register within the first 6 frames (< 540ms) of playback.
2. **The "Maco" Surveillance Reflex**: Group chats thrive on drama, "tea", and community gossip (*mauvais langue*). Lurking members deploy voyeuristic eye-pops, binocular sweeps, and blind-parting animations to signal silent, rapt attention.
3. **The Co-Sign & Validation Loop**: Trinbagonians rarely offer passive agreement; agreement is an energetic validation stamp (*"ENT?!"*, *"REL BESS!"*, *"REAL TALK"*, *"NO CAP"*).
4. **The Friday 3:00 PM Hype Escalation**: The psychological escape from the working week into the weekend "lime" or fete. Visuals feature exploding coolers, clinking drinks, roaring sound systems, and fluttering flags.
5. **Shared Grievance & Comedic Resilience**: Everyday civil infrastructure absurdities (water outages from WASA, power blackouts from T&TEC, highway traffic gridlock, maternal disciplinary slippers) are neutralized through shared satirical endurance.

---

## SECTION 2: LINGUISTIC & EMOTIONAL REGISTERS TAXONOMY

### 2.1 The Master 9-Register Framework
Every expression, gesture, and character concept in the 188-sticker catalog maps into one of nine foundational linguistic and emotional registers. These registers define the emotional state, physical acceleration profile, color palette, and vector FX vocabulary of each animation.

```
+=========================================================================================================+
|                                  THE 9 TRINIDADIAN EMOTIONAL REGISTERS                                  |
+----+-----------------------------+-----------------------+---------------------+------------------------+
| #  | REGISTER                    | EMOTIONAL INTENT      | KINETIC PROFILE     | CHROMATIC FX PALETTE   |
+----+-----------------------------+-----------------------+---------------------+------------------------+
| 01 | Bacchanal & Hype            | Ecstatic Celebration  | 140–160 BPM pulse   | #DA121A, #00E5FF, Gold |
| 02 | Picong & Banter             | Satirical Roasting    | Recoil, jets & slap | #FFD43B, #FF6B6B, Ink  |
| 03 | Skepticism & Shade          | Exposing Falsehood    | Cut-eye flick & cock| #9B51E0, #4A90E2, Cyan |
| 04 | Dismissal & Contempt        | Boundary Termination  | Snappy neck recoil  | #14161D, #DA121A, White|
| 05 | Culinary Reverence          | Sacred Food Ritual    | Cantilever & drip   | #EBAF28, #D35400, Amber|
| 06 | Lovesickness & Heartbreak   | Melodramatic Tabanca  | Gravitational sag   | #3498DB, #2980B9, Soft |
| 07 | Surveillance & Gossip       | Voyeuristic Inquiry   | Creep & optical zoom| #16A085, #27AE60, Gold |
| 08 | Supernatural & Folkloric    | Mythic Moral Guard    | Sinuous undulation  | #8E44AD, #1446DC, Mist |
| 09 | Island Resilience & Satire  | Wry Endurance         | Sputter, snap & arc | #7F8C8D, #BDC3C7, Red  |
+----+-----------------------------+-----------------------+---------------------+------------------------+
```

### 2.2 Deep Sociolinguistic & Kinematic Register Profiles

#### Register 01: Bacchanal & Hype
- **Cultural Rationale & Social Role**: Represents the spirit of Dionysian Carnival freedom, boundless euphoria, and communal feting. "Bacchanal" is not mere disorder—it is the joyous, deliberate shedding of corporate and societal repressions.
- **Sociolinguistic Application**: Used to rally group members (*"Leh we go!"*, *"Yuh outside?!"*), celebrate weekend liberation, amplify musical drops, or toast national pride.
- **Kinematic & Deformation Profile**: Driven by high-frequency vertical bouncing (2.3–2.6 Hz, matching 140–160 BPM Power Soca rhythms), violent overhead centrifugal rotation (rag windmill), sudden vertical squash-stretch pops ($S_y = 1.0 \pm 0.15$), and radial explosive dispersion of secondary debris.
- **Chromatic & FX Language**: High-saturation Caribbean palette featuring National Scarlet (`#DA121A`), Electric Cyan (`#00E5FF`), and Sunshine Gold (`#FFD43B`). Particle FX include flying confetti, speed streaks, and multi-point starbursts.
- **Key Catalog Stickers**: `weyyyy` (#7), `rel-bess` (#12), `bacchanal` (#23), `wait-for-riddim` (#58), `wave-yuh-rag` (#59), `dutty-jouvert` (#57), `slang-vibes` (#169), `slang-yuh-outside` (#166).

#### Register 02: Picong & Banter
- **Cultural Rationale & Social Role**: Originating from the French patois *piquant* (sharp/pricking), *picong* is the celebrated Caribbean art of competitive verbal roasting. Governed by the strict cultural code *Doh Tote* ("Do not carry grudges"), picong bonds communities by checking egos and puncturing self-importance through shared laughter.
- **Sociolinguistic Application**: Deployed to react to hilarious fails, mock friends who boast excessively, or react to absurd conversational claims.
- **Kinematic & Deformation Profile**: Asymmetrical kinetic comedy characterized by backward torso collapses (incline $-24^\circ$), rhythmic double-takes, high-velocity horizontal tear sprays shooting from outer ocular corners, and violent thigh/knee-slap impacts.
- **Chromatic & FX Language**: Bright comic yellows (`#FFD43B`), tear cyan (`#00E5FF`), and rich comic ink (`#14161D`). Vector FX include dual horizontal liquid jets, bouncing jester bells, floating giggle notes, and vibrating sound waves.
- **Key Catalog Stickers**: `ah-eh-able` (#3), `doh-tote` (#10), `killing-me-dead` (#11), `just-picong` (#16), `kicksin` (#28), `slang-doh-kill-meh` (#133), `slang-is-a-jokes` (#135), `slang-im-weak` (#176).

#### Register 03: Skepticism & Shade
- **Cultural Rationale & Social Role**: The sharp, unvarnished defense mechanism against "cap" (lies), exaggerations, bragging, or suspicious behavior. In Trinidadian social spaces, claims are never accepted blindly; they are immediately cross-examined with piercing ocular scrutiny.
- **Sociolinguistic Application**: Used to demand receipts, question dubious statements, or puncture someone acting "grand" (*"Ent?!"*, *"Fuh real?!"*, *"Watch nah"*, *"Yuh too lie"*).
- **Kinematic & Deformation Profile**: Highly minimalist body movement contrasting with intense, snappy ocular choreography. Eyelids compress into a tight cut-eye squint ($S_y = 0.85$); pupils snap diagonally upward ($15^\circ$ elevation); one eyebrow executes a sharp overshoot lift (`ease_out_back`); head performs an asymmetric sardonic cock.
- **Chromatic & FX Language**: Skeptical violets (`#9B51E0`), ice blues (`#4A90E2`), and electric yellow accents. Overlays include vibrating question marks, searching flashlight beams, and Pinocchio-style extending wooden noses.
- **Key Catalog Stickers**: `ent` (#1), `fuh-real` (#9), `slang-ent` (#108), `slang-watch-nah` (#117), `slang-yuh-jokin` (#123), `slang-yuh-too-lie` (#132), `slang-cap` (#173), `slang-be-so-for-real` (#181).

#### Register 04: Dismissal & Contempt
- **Cultural Rationale & Social Role**: The ultimate cultural boundary-enforcing mechanism. When banter crosses the line, or when someone brings unadulterated foolishness into a conversation, dismissal is immediate, definitive, and physically punctuated by the iconic *Steups*.
- **Sociolinguistic Application**: Terminating foolish arguments, rejecting disrespect, or telling someone to cease speaking (*"Steups"*, *"Cyah take dat"*, *"Ah done"*, *"Doh start"*).
- **Kinematic & Deformation Profile**: High-acceleration acoustic snap. The animation begins with an anticipatory mouth purse and clench ($t \in [0.0, 0.14]$), explodes into a sudden diagonal neck retraction ($\Delta y = -16\text{px}, \theta = -12^\circ$), and discharges a pressurized conical air blast before settling into a cold, motionless turn away.
- **Chromatic & FX Language**: Deep ink charcoal (`#14161D`), abrupt crimson flashes (`#DA121A`), and stark white acoustic puffs. Vector overlays feature directional air shockwaves, padlock closures, and dusting-off hand clouds.
- **Key Catalog Stickers**: `steups` (#2), `cyah-take-dat` (#13), `doh-make-joke` (#26), `slang-steups` (#128), `slang-doh-start` (#116), `slang-ah-done` (#134), `slang-doh-watch-me` (#145), `slang-mind-yuh-business` (#146).

#### Register 05: Culinary Reverence
- **Cultural Rationale & Social Role**: The sacred, multi-ethnic culinary heritage of Trinidad & Tobago (Doubles, Pelau, Buss Up Shut, Bake & Shark, Crab & Dumpling). Food in T&T is not mere fuel; it is a spiritual lime ritual, a hangover cure, and an expression of love.
- **Sociolinguistic Application**: Announcing cravings, debating pepper sauce intensity, sharing weekend breakfast locations, or declaring culinary satisfaction (*"Ate and left no crumbs"*).
- **Kinematic & Deformation Profile**: Viscous, organic, rhythmic dynamics. Features the iconic forward 45° street-food cantilever lean, rhythmic mastication chewing cadences ($\omega = 4\pi\text{ rad/s}$), swirling aromatic steam curls, and viscous sauce droplets stretching with elastic surface tension before snapping downward.
- **Chromatic & FX Language**: Warm appetizing amber (`#EBAF28`), rich Scotch Bonnet crimson (`#DA121A`), golden split-pea yellow, and translucent aromatic white steam. Overlays include shimmering heat distortion lines, savory steam curls, and falling sauce droplets.
- **Key Catalog Stickers**: `doubles-3d` (#31), `slight-pepper` (#32), `doubles-lean` (#33), `bake-and-shark` (#34), `buss-up-shut` (#35), `pelau-pot` (#38), `corn-soup` (#39), `pholourie` (#40), `crab-and-dumpling` (#89), `slang-ate` (#178).

#### Register 06: Lovesickness & Heartbreak (Tabanca)
- **Cultural Rationale & Social Role**: *Tabanca* is the unique Trinidadian condition of acute, melancholy romantic heartbreak or the tragicomic post-Carnival withdrawal when normal reality resumes. It is treated with compassionate mockery, rum, and classic calypso commiseration.
- **Sociolinguistic Application**: Venting romantic rejection, mourning the end of Carnival Tuesday, or expressing theatrical misery in group chats.
- **Kinematic & Deformation Profile**: Dramatic downward gravitational sag ($S_y = 0.88, S_x = 1.06$). Torso droops in a heavy, languid pendulum sigh oscillation (0.5 Hz); shoulders slope downward; floating broken hearts pulse mournfully; tears stretch downward with exaggerated viscoelastic gravity.
- **Chromatic & FX Language**: Melancholy marine blues (`#3498DB`), desaturated indigo (`#2980B9`), and cracked crimson. Overlays feature elongating teardrops, pulsing cracked hearts, fluttering falling feathers, and raincloud mists.
- **Key Catalog Stickers**: `pure-bazodee` (#6), `chupidee` (#14), `real-tabanca` (#21), `carnival-tabanca` (#24), `sunday-coma` (#37), `slang-tabanca` (#163), `slang-left-on-read` (#187), `slang-delulu` (#182).

#### Register 07: Surveillance & Gossip (Maco & Mauvais Langue)
- **Cultural Rationale & Social Role**: The compulsive, voyeuristic appetite for community news, neighborhood drama, and spicy gossip (*mauvais langue*). The *Maco* is the legendary neighborhood investigator perched behind wooden jalousie louvers, armed with binoculars, noticing everything and missing nothing.
- **Sociolinguistic Application**: Signaling silent lurking in a heated group chat, requesting more details on emerging drama, or calling out an intruder.
- **Kinematic & Deformation Profile**: Asymmetric piecewise stealth mechanics. Begins with a slow, creeping emergence from behind wooden shutters ($t^3$ ease-in), followed by a sudden forward optical punch ($1.35\times$ lens zoom via `ease_out_back`), horizontal micro-saccadic eye panning ($\pm 18\text{px}$), and an instantaneous panic snap back into concealment.
- **Chromatic & FX Language**: Stealth jalousie green (`#16A085`), brass optics gold, and neon surveillance cyan. Overlays include targeting crosshairs, expanding binocular iris rings, sweeping searchlight cones, and twitching eyelids.
- **Key Catalog Stickers**: `look-trouble` (#4), `maco` (#19), `yuh-too-fas` (#25), `mauvais-langue` (#29), `slang-lemme-see` (#125), `slang-high-beam` (#138), `slang-fass` (#161), `slang-maco` (#162).

#### Register 08: Supernatural & Folkloric
- **Cultural Rationale & Social Role**: The mythic pantheon of Trinidad & Tobago folklore (Soucouyant, Papa Bois, Mama Dlo, Douen, La Diablesse, Lagahoo, Blue Devil) and spiritual defenses against envy (*maljo*). These entities serve as ancestral moral guardians and personifications of the mysterious tropical rainforest.
- **Sociolinguistic Application**: Evoking ancestral reverence, warning children against reckless behavior, warding off bad vibes, or celebrating traditional Carnival masquerade.
- **Kinematic & Deformation Profile**: Eerie, sinuous, non-human locomotion. Characterized by low-frequency undulating levitation, serpentine S-curve ripples along river coils, backward stepping motions (Douen reversed feet), explosive shapeshifting fireball comet arcs, and glowing protective talisman shield pulses.
- **Chromatic & FX Language**: Mystic Paramin Cobalt (`#1446DC`), ethereal purple (`#8E44AD`), blazing orange fireball cores, and shimmering cobalt-blue glass protection halos (`#00E5FF`). Overlays include flaming comet tails, swirling river currents, clanking chains, and expanding warding shields.
- **Key Catalog Stickers**: `soucouyant` (#67), `salt-in-mortar` (#68), `la-diablesse` (#69), `mama-dlo` (#70), `papa-bois` (#71), `douen` (#72), `lagahoo` (#73), `no-maljo` (#74), `silk-cotton-tree` (#76).

#### Register 09: Island Resilience & Grievance
- **Cultural Rationale & Social Role**: The sharp, comedic coping mechanisms developed by Trinbagonians to survive civil infrastructure hurdles (WASA water shortages, T&TEC power cuts, East-West corridor traffic gridlock) and the legendary matriarchal discipline of the Caribbean mother's flying slipper.
- **Sociolinguistic Application**: Commiserating over shared hardships, bonding over power outages, or warning someone that maternal wrath is imminent.
- **Kinematic & Deformation Profile**: Comic anticlimax and ballistic mechanics. Begins with high-tension mechanical bulging/quivering followed by pathetic deflation (a single dry droplet and a dust puff); sudden square-wave state transitions (100% light $\to$ 0% darkness $\to$ match spark $\to$ candle flicker); or high-velocity parabolic projectile trajectories rotating at $\omega = 8\pi\text{ rad/s}$.
- **Chromatic & FX Language**: Sputtering pipe gray, sudden blackout black (`#000000`), warm candle amber (`#FFD43B`), and danger crimson. Overlays include dry dust puffs, ticking panic clocks, spinning slippers, and comic starburst impact craters.
- **Key Catalog Stickers**: `highway-traffic` (#94), `trini-mom-spoon` (#95), `flying-slipper` (#96), `wasa-water-gone` (#97), `ttec-current-gone` (#98), `crapaud-pipe` (#17).

---

### 2.3 Master Register Comparison Matrix

| Register Name | Cultural Essence | Dominant BPM / Tempo | Primary Physics Routine | Dominant Visual Element | Secondary FX Primitives |
|---|---|---|---|---|---|
| **Bacchanal & Hype** | Wild fete celebration & liberation | 140–160 BPM (Fast) | 3D Conical rag windmill & vertical hop | Flying flags, feathers, confetti | `draw_comic_twinkle`, `speed_lines` |
| **Picong & Banter** | Sharp witty roasting without malice | 110–130 BPM (Bouncy) | Torso recline, knee-slap, tear jets | Wide laughing grin, slapped knees | `draw_comic_droplet`, `soundwaves` |
| **Skepticism & Shade** | Calling out lies & checking egos | 80–100 BPM (Deliberate) | Cut-eye squint, eyebrow pop, head cock | Narrowed pupils, arched brow | `draw_comic_starburst`, `lens_glint` |
| **Dismissal & Contempt** | Ending foolishness & drawing line | Explosive Snap (< 300ms) | Clenched purse $\to$ snappy neck recoil | Pursed lips, 180° turn away | `draw_comic_puff`, `air_shockwave` |
| **Culinary Reverence** | Sacred road-food appreciation | 60–80 BPM (Smooth) | 45° Cantilever lean, chewing bob | Steaming bara, dripping sauce | `draw_comic_droplet`, `steam_curls` |
| **Lovesickness (Tabanca)**| Heartbreak blues & post-mas daze | 40–60 BPM (Languid) | Gravitational sag, pendulum sigh | Drooping feathers, cracked heart | `draw_comic_droplet`, `broken_heart` |
| **Surveillance (Maco)** | Looking at neighborhood drama | Sneaky crawl $\to$ Fast pop | Peeping creep $\to$ $1.35\times$ optical zoom | Binoculars, louvers, twitching iris | `draw_comic_speed_lines`, `reticle` |
| **Supernatural & Folklore**| Ancestral spirits & mythic guards | Sinuous Wave (0.8 Hz) | Undulating levitation & comet spin | Horns, backward feet, chains, fire | `draw_comic_starburst`, `mist_aura` |
| **Island Resilience** | Satirical survival of daily chaos | Sputter & Sudden Strike | Ballistic arc, pipe cough, match strike | Slipper, dry tap, candle, match | `draw_comic_puff`, `starburst_flash` |

---

## SECTION 3: AUTHENTIC PHYSICAL GESTURES & COMEDIC TROPES

### 3.1 Biomechanical & Anatomical Framework
To translate physical human Caribbean kinesics into procedural 2D vertex mesh deformation without losing anatomical plausibility, the PeelOff engine establishes a hierarchical skeletal pivot model.

```
       [CRANIUM / BROW]       <--- Eyebrow Pop, Cut-Eye Squint, Horn Eruption
              |
         [CERVICAL]           <--- Neck Recoil, Head Cock (-18° to +22°)
              |
       [THORACIC / ARMS]      <--- Chest Inflation, Table Slam, Rag Windmill
              |
      [LUMBAR / PELVIS]       <--- Akumbo Hip Shift, 45° Cantilever Lean, Wine
              |
       [GROUND / STILTS]      <--- Table Impact Contact, Stilt Steps
```

Deformations are applied as weighted radial basis influences originating from designated anatomical anchors. When a character's neck recoils backward during a Steups, the deformation does not shear the entire canvas; it displaces vertices within a Gaussian envelope centered on the cervical spine anchor, preserving the stability of the lower torso while violently snapping the head and facial features.

All spatial deformations strictly enforce volume preservation:
$$S_x(t) = \frac{1}{\sqrt{S_y(t)}}$$
When a character squashes vertically upon landing ($S_y = 0.70$), the horizontal waistline expands by $1.195\times$ (+19.5%), preserving the visual mass of the character.

---

### 3.2 Deep Kinematic Analysis of the 12 Core Gestures

#### Gesture 01: The Steups (Acoustic Suck-Teeth / Chups)
- **Cultural Performance & Social Meaning**: Produced by drawing air inward across the incisors with pursed lips, producing an acoustic sound ranging from a short dismissive "chups" to a drawn-out, furious "stchewwwwps." It communicates annoyance, profound disdain, impatience, and instant dismissal of foolishness.
- **Anatomical Choreography & Mechanics**:
  - *Mouth & Jaw*: Lips purse tightly inward into a puckered puckering cone ($S_x = 0.88$); jaw tenses and drops $4\text{px}$.
  - *Cervical Spine*: Sudden high-acceleration backward diagonal neck retraction ($\Delta y = -16\text{px}, \theta = -12^\circ$). The acceleration reaches its peak at Frame 5 ($a = 5.4 \cdot \Delta t^2$).
  - *Eyes & Brow*: Eyelids drop into a heavy half-mast cut-eye squint ($S_y = 0.85$); pupils flick $20^\circ$ to the upper-right corner.
- **Comedic Caricature Rules**:
  - Exaggerate neck retraction by 35% beyond human anatomical range to emphasize dismissive disdain.
  - Hold the peak recoiled pose for a full 8 frames ($720\text{ms}$) with subtle living micro-motion before allowing a slow, reluctant ease-in settle.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Anticipation** | f0–f3 | 0–270ms | Lips purse inward ($S_x = 0.88$); jaw compresses; eyes narrow | Pre-strike tension line on jaw |
| **Kinetic Strike**| f4–f6 | 360–540ms | Violent neck recoil backward ($\Delta y = -16\text{px}, \theta = -12^\circ$) | Conical white air puff erupts at mouth |
| **Living Hold** | f7–f15 | 630–1350ms | Disdainful hold; head swivels $+15^\circ$; chest micro-heave | Expanding directional air shockwave |
| **Settle & Loop**| f16–f23| 1440–2070ms| Reluctant cubic return to neutral resting pose | Air shockwave dissipates ($\alpha \to 0$) |

---

#### Gesture 02: The 45° Doubles Lean
- **Cultural Performance & Social Meaning**: The universal roadside posture adopted by street-food patrons across Trinidad & Tobago. The patron hinges forward at the hips over the pavement so curried channa, pepper sauce, and tamarind chutney drip safely onto the ground rather than shirts, ties, or footwear.
- **Anatomical Choreography & Mechanics**:
  - *Base of Support*: Feet spread wide at shoulder width (simulated stability).
  - *Pelvis & Spine*: Hips hinge strictly at a $40^\circ\text{–}45^\circ$ forward angle. The spine stays rigid as a cantilever beam, shifting center of mass forward by $\Delta x = +22\text{px}$.
  - *Upper Limbs*: Elbows flare outward laterally like wings at $70^\circ$, hands cupping the wax paper wrapper $20\text{cm}$ below the mouth.
  - *Jaw*: Rhythmic mastication chewing cadence ($\omega = 4\pi\text{ rad/s}$, 2 cycles per loop).
- **Comedic Caricature Rules**:
  - The forward cantilever angle is maintained statically while the mouth bobs vertically in continuous satisfaction.
  - The amber curry droplet must stretch elastically to $3.5\times$ its initial diameter before detaching, mimicking viscous surface tension.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Cantilever Lean**| f0–f5 | 0–450ms | Upper body shears forward $42^\circ$ over hip anchor; jaw chews | Aromatic steam curls rise from bara |
| **Viscous Drip** | f6–f12 | 540–1080ms | Sustained lean; amber sauce stretches down ($L = 10 \to 45\text{px}$) | Droplet necks down via surface tension |
| **Pinch-Off Fall** | f13–f17 | 1170–1530ms| Droplet detaches and falls freely; bara snaps up $3\text{px}$ | Amber drop accelerates down off-canvas |
| **Chew & Loop** | f18–f23 | 1620–2070ms| Jaw completes chew cycle 2; steam curls fade and loop | Fresh steam curls emerge at top |

---

#### Gesture 03: The All Fours Table Slam ("Hang Jack!")
- **Cultural Performance & Social Meaning**: In Trinidad's national card game of All Fours, capturing the opponent's Jack of Trumps ("Hang Jack!") or executing a 12–0 "Bullseye" shutout requires slamming the card onto the wooden table with bone-rattling force to assert dominance.
- **Anatomical Choreography & Mechanics**:
  - *Apex Hold*: Player's arm and card are cocked high overhead ($\Delta y = -50\text{px}, \theta = +35^\circ$), quivering with suspense for 6 frames.
  - *Downward Strike*: Arm accelerates downward with quadratic terminal comic velocity ($a = 4.2 \cdot \Delta t^2$).
  - *Seismic Impact*: Instantaneous card contact at frame 10. Maximum squash deformation ($S_y = 0.68, S_x = 1.21$).
  - *Table Resonance*: Decaying sinusoidal vibration ($A e^{-18t} \sin(95t)$) shaking the table surface, scattering loose cards and chalk dust.
- **Comedic Caricature Rules**:
  - Prolong the anticipation hold to maximize comedic tension before the instantaneous 2-frame downstrike.
  - The impact must trigger an explosive 10-point golden starburst and horizontal chalk dust dispersion.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Suspense Hold** | f0–f6 | 0–540ms | Arm cocked high overhead; card trembling at $\Delta y = -50\text{px}$| High-tension anticipation quiver |
| **Downstrike** | f7–f9 | 630–810ms | Violent terminal-velocity downward acceleration | Speed streaks trail card edge |
| **Table Impact** | f10 | 900ms | Card contacts table; violent squash ($S_y = 0.68, S_x = 1.21$)| 10-point explosive golden starburst |
| **Decay & Settle** | f11–f23 | 990–2070ms| High-frequency table shake ($12\text{px}$); arm retracts to chest | White chalk dust puffs scatter outward |

---

#### Gesture 04: The Soca Rag Windmill
- **Cultural Performance & Social Meaning**: The definitive kinetic expression of Power Soca. Revelers take a microfiber cloth, bandana, or national flag and swing it overhead in wide, continuous circular arcs to generate communal euphoria.
- **Anatomical Choreography & Mechanics**:
  - *Orbital Cone*: The arm sweeps through an overhead 3D elliptical cone with semi-major axis $R_x = 110\text{px}$ and semi-minor axis $R_y = 38\text{px}$, inclined $20^\circ$ toward the viewer.
  - *Cloth Aerodynamic Lag*: The tip of the rag trails the hand position by a phase shift $\Delta \phi = 0.52\text{ rad}$ (2 frames of cloth aerodynamic wave lag).
  - *Snap-Whip Downbeats*: On musical downbeats (Frames 0, 8, 16), the wrist snaps sharply, creating a localized S-curve ripple across the fabric mesh.
- **Comedic Caricature Rules**:
  - The rag must elongate by +15% during the high-speed downward sweep and billow into a wider sail on the upward sweep.
  - Continuous circular speed ribbons and floating confetti particles amplify the momentum.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Downbeat Sweep 1**| f0–f7 | 0–630ms | Arm sweeps from right apex down across front; cloth trails | Flying iridescent confetti particles |
| **Upward Ascent** | f8–f15 | 720–1350ms| Arm ascends to left apex; fabric billows into wide sail | Double speed lines along trailing edge |
| **Back Arc Whip** | f16–f23 | 1440–2070ms| Arm sweeps overhead back loop; sharp wrist whip snap | Radial confetti burst at frame 16 |

---

#### Gesture 05: The Tanty Stance (Akumbo & Sassy Tilt)
- **Cultural Performance & Social Meaning**: The matriarchal stance of authority. Tanty places both hands on her hips ("akumbo"), puffs her chest, tilts her head with an arched eyebrow, and wags a stern finger to interrogate foolishness or dismiss nonsense.
- **Anatomical Choreography & Mechanics**:
  - *Pelvis & Spine*: Asymmetric lateral pelvic tilt of $14^\circ$, shifting body weight onto one hip.
  - *Cervical Spine*: Head counter-tilts $18^\circ\text{–}22^\circ$ opposite the hip roll, executing a rhythmic side-to-side wobble ($\omega = 2\pi\text{ rad/s}$).
  - *Facial Musculature*: One eyebrow arches high with overshoot (`ease_out_back`); eyelids narrow into a piercing cut-eye squint.
  - *Hand Wag*: Index finger wags rhythmically ($\omega = 6\pi\text{ rad/s}$, 3 wags per cycle).
- **Comedic Caricature Rules**:
  - Glasses perched low on the nose bridge must slide down $2\text{px}$ on the head snap.
  - A bright yellow comic punctuation starburst pops above the arched brow.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Hip Shift Right** | f0–f6 | 0–540ms | Hips sway right ($+14^\circ$); head tilts left ($-18^\circ$); cut-eye | Eyebrow pops up with starburst |
| **Neutral Transition**| f7–f12 | 630–1080ms| Weight shifts across center; finger completes wag cycle 1 | Glasses slide down nose ($2\text{px}$) |
| **Hip Shift Left** | f13–f18 | 1170–1620ms| Hips sway left ($-14^\circ$); head tilts right ($+18^\circ$); wag cycle 2| Specular glint on gold earrings |
| **Settle & Loop** | f19–f23 | 1710–2070ms| Smooth cubic return toward initial right-leaning stance | Stern nod and settle to f0 |

---

#### Gesture 06: The Bazodee Spiral & Infatuation Daze
- **Cultural Performance & Social Meaning**: Expressing head-spinning infatuation, romantic daze, drunkenness, or utter confusion (from French patois *abasourdi*).
- **Anatomical Choreography & Mechanics**:
  - *Torso & Cranium*: Torso translates along a Lemniscate of Gerono (figure-8 path):
    $$x(t) = 22 \sin(2\pi t), \quad y(t) = 12 \sin(4\pi t)$$
  - *Ocular Swirl*: Both pupils are replaced with counter-rotating logarithmic Archimedean spirals revolving at $\omega = 4\pi\text{ rad/s}$.
  - *Celestial Orbit*: 3 golden stars and 2 pastel hearts orbit the head in an inclined Keplerian ellipse ($R_x = 105\text{px}, R_y = 22\text{px}$).
- **Comedic Caricature Rules**:
  - The head droops languidly at the extremities of the figure-8 trajectory.
  - Stars must rotate continuously with angular velocity $\omega = \pi t$.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Figure-8 Loop Right**| f0–f6 | 0–540ms | Head loops through upper-right quadrant; eye spirals spin CW | Orbiting star 0 crosses foreground |
| **Center Cross Dip** | f7–f12 | 630–1080ms| Head dips through center cross; eye spirals reverse CCW | Orbiting star 1 crosses foreground |
| **Figure-8 Loop Left** | f13–f18 | 1170–1620ms| Head loops through upper-left quadrant; dazed smile slumps | Orbiting star 2 crosses foreground |
| **Lower Loop Settle** | f19–f23 | 1710–2070ms| Head returns through lower loop; seamless continuous cycle | Pulsing broken heart floats up |

---

#### Gesture 07: The Maco Peeping Zoom & Binocular Sweep
- **Cultural Performance & Social Meaning**: The intrusive neighborhood spy looking through wooden jalousie louvers or binoculars to capture gossip and inspect drama.
- **Anatomical Choreography & Mechanics**:
  - *Stealth Emergence*: Head and binoculars inch slowly upward from behind wooden louvers ($\Delta y = -30\text{px}$, eased by $u^3$).
  - *Optical Punch*: Binoculars snap forward; lenses expand by 35% ($S = 1.35$) using `ease_out_back`.
  - *Surveillance Scan*: Head pans horizontally left-to-right ($\pm 18\text{px}$) with rapid micro-saccadic eye twitches.
  - *Panic Snap*: Detected! Head snaps straight down behind shutters in 2 frames ($\Delta y = +32\text{px}$), blinds slamming shut.
- **Comedic Caricature Rules**:
  - Exaggerate the optical magnification of the lenses to create comedic fish-eye distortion.
  - Twin cyan lens glints (`#00E5FF`) flare at the apex of the zoom.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Stealth Creep** | f0–f5 | 0–450ms | Louvers part slightly; head inches upward $30\text{px}$ ($u^3$) | Shaded wood louvers slide open |
| **Optical Zoom** | f6–f9 | 540–810ms | Binoculars snap forward; lenses expand 35% (`ease_out_back`)| Twin cyan lens glints flare |
| **Surveillance Scan** | f10–f17 | 900–1530ms| Lateral eye scan ($\pm 18\text{px}$); iris rings pulse | Targeting crosshairs and speed lines |
| **Panic Retraction** | f18–f23 | 1620–2070ms| Panic snap! Head drops $32\text{px}$ behind louvers in 2 frames | Blinds rattle shut with impact shudder |

---

#### Gesture 08: The Horn Infidelity Guilt Shudder
- **Cultural Performance & Social Meaning**: Romantic betrayal ("getting a horn") or comedic panic when caught in an indiscretion or lie.
- **Anatomical Choreography & Mechanics**:
  - *Horn Eruption*: Two glossy crimson bull/stag horns sprout from the cranium ($S_{horn} = 0 \to 1.2 \to 1.0$).
  - *Spinal Tremor*: High-frequency 30 Hz micro-tremor along the spine ($\Delta x = \pm 4\text{px} \cdot \sin(30\pi t)$).
  - *Sweat Launch*: Large comic sweat droplets launch horizontally from temples.
- **Comedic Caricature Rules**:
  - Overhead red emergency siren light alternates with $180^\circ$ phase shift.
  - Horns shudder with elastic resonance after sprouting.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Guilt Inhalation** | f0–f4 | 0–360ms | Cranium tenses; eyes dart sideways; head pulls down $4\text{px}$ | Red warning glow starts on brow |
| **Horn Eruption** | f5–f10 | 450–900ms | Crimson horns sprout upward with overshoot ($S = 1.2 \to 1.0$) | Flashing red siren light beam sweeps |
| **Spinal Shudder** | f11–f17 | 990–1530ms| 30 Hz micro-tremor along spine ($\pm 4\text{px}$); sweat beads pop | Horizontal sweat droplets spray outward |
| **Nervous Settle** | f18–f23 | 1620–2070ms| Horns vibrate with decaying resonance; guilty swallow | Siren beam fades before loop reset |

---

#### Gesture 09: The J'Ouvert Mud & Paint Splatter Burst
- **Cultural Performance & Social Meaning**: 4:00 AM Carnival Monday liberation. Covered head-to-toe in wet mud, cobalt blue paint, cocoa, or motor oil, dancing to booming mobile sound trucks.
- **Anatomical Choreography & Mechanics**:
  - *Radial Fluid Ejection*: Viscous paint and mud droplets eject radially along ballistic vectors:
    $$\vec{v}_i = (v_0 \cos \alpha_i, v_0 \sin \alpha_i - g t)$$
  - *Bass Pulse Squash*: Character torso squashes and stretches violently on downbeats ($S_y = 1.0 \pm 0.12$ at 140 BPM).
  - *Mud Surface Tension*: Droplets stretch into elongated teardrops before detaching.
- **Comedic Caricature Rules**:
  - Neon paint streaks trail behind limb movements.
  - Mud splatters stick to the canvas perimeter with decaying opacity.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Bass Pre-Drop** | f0–f4 | 0–360ms | Torso crouches low in anticipation ($S_y = 0.88$); mud drips | Ground vibration lines throb |
| **Explosive Burst** | f5–f10 | 450–900ms | Violent vertical leap ($S_y = 1.15$); arms thrust upward | Radial mud/paint droplets burst outward |
| **Fluid Dispersion** | f11–f17 | 990–1530ms| Torso pulses to secondary bass bounce; paint streaks fan out | Paint droplets arch downward under gravity |
| **Settle & Loop** | f18–f23 | 1620–2070ms| Crouch recovery to initial posture; splatters settle | Mud puddles reform at base |

---

#### Gesture 10: The Moko Jumbie Stilt Sway
- **Cultural Performance & Social Meaning**: Towering West African-rooted stilt guardian towering 10 to 15 feet in the air, swaying rhythmically above Carnival crowds to ward off evil spirits.
- **Anatomical Choreography & Mechanics**:
  - *Inverted Pendulum*: Torso oscillates slowly with period $T = 2\pi \sqrt{L/g}$, pivoting around stilt foot contact.
  - *Alternating Stilt Lift*: Left and right stilts step with a $180^\circ$ phase offset, lifting vertically $\Delta y = -24\text{px}$.
  - *Satin Cloth Wave*: Voluminous satin pant legs billow with a 3-frame spatial wave lag ($0.015y$).
- **Comedic Caricature Rules**:
  - Exaggerate stilt height using vertical scale padding (`scale=0.88`).
  - Billowing satin fabric flares outward at the extremes of each sway.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Left Stilt Lift** | f0–f6 | 0–540ms | Left stilt lifts upward $24\text{px}$; torso sways right ($+15^\circ$) | Satin fabric billows to the left |
| **Center Plant** | f7–f12 | 630–1080ms| Left stilt plants firmly; weight transitions through center | Dust puff at stilt contact point |
| **Right Stilt Lift** | f13–f18 | 1170–1620ms| Right stilt lifts upward $24\text{px}$; torso sways left ($-15^\circ$) | Satin fabric billows to the right |
| **Sway Reset** | f19–f23 | 1710–2070ms| Right stilt plants; body smoothly settles toward neutral | Smooth periodic loop reset |

---

#### Gesture 11: The Lip Point ("Look Dey")
- **Cultural Performance & Social Meaning**: The traditional Afro-Caribbean directional gesture where pointing with an index finger is considered ill-mannered ("doh point yuh finger in people face!"); direction is indicated solely by pursing the lips and thrusting the chin toward the target.
- **Anatomical Choreography & Mechanics**:
  - *Upper Limbs*: Arms and hands remain completely stationary at sides.
  - *Tubular Pucker (Localized Oral Deformation)*: The orbicularis oris muscle contracts circumferentially, funneling the mouth into an elongated conical tube ($S_x = 0.70, S_y = 0.85, \Delta x_{\text{mouth}} = +22\text{px}$).
    > **Localized Volume Preservation Architecture**:
    > The parameters $S_x = 0.70$ and $S_y = 0.85$ govern a **strictly localized oral sub-domain**, not a global whole-body scale. Fleshy tissue mass is conserved through 3D elongation along the forward projection vector ($+z$ axis toward target):
    > $$S_z = \frac{1.0}{S_x \cdot S_y} = \frac{1.0}{0.70 \times 0.85} = \frac{1.0}{0.5950} \approx 1.6807$$
    > Transverse narrowing concentrates mass into a $+68.07\%$ forward snout protrusion, which is rendered on the 2D canvas as an apparent forward translation ($\Delta x = +22\text{px}, \Delta y = -8\text{px}$).
    > On the $18 \times 18$ MESH grid, deformation is isolated via a 2D Gaussian envelope centered at $(cx_{\text{mouth}}, cy_{\text{mouth}}) = (256, 310)$:
    > $$w_{\text{mouth}}(x, y) = \exp\left( -\left[ \left(\frac{x - 256}{42}\right)^2 + \left(\frac{y - 310}{28}\right)^2 \right] \right)$$
    > Outside the oral envelope ($r > 2.5\sigma$), $w_{\text{mouth}} \to 0$, guaranteeing that the cranium, cheeks, and torso retain 100% resting volume with zero global deflation.
  - *Chin & Brow*: Chin thrusts diagonally upward at $25^\circ$; eyebrows lift synchronously into high arches.
- **Comedic Caricature Rules**:
  - The mouth extension must overshoot by 25% before settling into a rigid directional pointer.
  - Target sightline beams or crosshairs pulse in the indicated direction.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Pre-Pucker Clench**| f0–f4 | 0–360ms | Facial muscles draw toward nose; eyes lock onto target | Sightline focus beam sparks on brow |
| **Tubular Thrust** | f5–f10 | 450–900ms | Lips thrust forward into elongated tube ($\Delta x = +22\text{px}$) | Directional pointer arrow pops at lips |
| **Directional Hold** | f11–f18 | 990–1620ms| Rigid chin hold at $+25^\circ$; eyebrows arched; micro-sway | Pulsing target crosshair in distance |
| **Relax & Loop** | f19–f23 | 1710–2070ms| Lips relax back to neutral mouth; chin lowers | Target crosshair dissolves |

---

#### Gesture 12: The Heat-Seeking Slipper (Maternal Missile)
- **Cultural Performance & Social Meaning**: The Caribbean mother's legendary disciplinary projectile that defies aerodynamics, curving around hallway corners with 100% laser accuracy.
- **Anatomical Choreography & Mechanics**:
  - *Ballistic Trajectory*: Parabolic curve traversing from screen right to center:
    $$x(t) = 490 - 234 \cdot u(t), \quad y(t) = 280 - 180 \sin(\pi u(t))$$
  - *Spin Angular Velocity*: Continuous planar rotation at $\omega = 8\pi\text{ rad/s}$ (4 full revolutions per cycle).
  - *Terminal Impact*: Starburst impact flash at frame 16 with comic impact clouds.
- **Comedic Caricature Rules**:
  - Slipper squashes along its longitudinal axis upon impact ($S_y = 0.70, S_x = 1.20$).
  - Speed lines curve dynamically behind the slipper flight path.
- **24-Frame Timing Schedule**:

| Phase | Frames | Time ($t$) | Anatomical State & Mesh Dynamics | Secondary FX & Overlays |
|---|---|---|---|---|
| **Launch Wind-Up** | f0–f4 | 0–360ms | Slipper exits upper-right screen, spinning rapidly ($\omega = 8\pi$)| Curving aerodynamic speed lines |
| **Parabolic Flight** | f5–f11 | 450–990ms | Slipper arches over center canvas; rotation continues | Dynamic flight trail ribbon |
| **Terminal Lock-On** | f12–f15 | 1080–1350ms| Slipper accelerates downward into target coordinate $(256, 280)$ | Target bullseye reticle locks on |
| **Impact & Tumbling**| f16–f23 | 1440–2070ms| Bullseye impact! Slipper squashes ($S_y = 0.70$); tumbles to rest| Multi-point starburst & comic dust puff |

---

### 3.3 Visual Comedic Tropes & Caricature Exaggeration Rules
To ensure the 188 sticker animations maintain the visual punch of golden-age Caribbean comic strips, the engine enforces four universal animation principles:

1. **Anticipation (Energy Coiling)**:
   - No violent action may occur without a preceding reverse motion. Before a table slam, the hand must cock backward for 6 frames; before a puncheon fire blast, the chest must inflate by +20%; before a steups, the lips must compress inward.
2. **Snappy Overshoot (`ease_out_back`)**:
   - Linear stops look robotic. When a head cocks, an eyebrow arches, or binoculars zoom, the property must overshoot its target by $15\text{–}20\%$ ($s = 1.70158$) before snapping back to rest.
3. **The Micro-Motion Living Hold**:
   - Static freezes are strictly prohibited. During a dramatic hold (e.g. after a card slam), characters maintain subtle breathing micro-motions ($0.5\text{px}$ sinusoidal oscillation) to preserve biological presence and prevent video codec coalescing.
4. **Secondary Emotional Debris**:
   - Emotional intensity must manifest as physical matter: spicy anger produces steam; picong laughter produces horizontal tear sprays; All Fours dominance scatters chalk dust; romantic tabanca drips heavy tears.

---

## SECTION 4: PROCEDURAL MOTION PRIMITIVES & MATHEMATICAL SPECIFICATIONS

### 4.1 The 24-Frame @ 90ms Standard Timeline
Every animated sticker in PeelOff operates on a strictly standardized 24-frame looping timeline:
$$\text{Total Frame Count } N = 24$$
$$\text{Frame Duration } \Delta t = 90\text{ milliseconds}$$
$$\text{Total Loop Duration } T = 24 \times 90\text{ ms} = 2,160\text{ ms} = 2.16\text{ seconds}$$
$$\text{Effective Framerate } FPS = \frac{1000}{90} \approx 11.11\text{ fps}$$

Normalized time $t$ for frame index $f \in \{0, 1, \dots, 23\}$ is defined as:
$$t = \frac{f}{24}, \quad t \in [0.000, 0.958]$$
All periodic trigonometric functions use cyclic angle $\theta = 2\pi t$, guaranteeing seamless, pop-free looping between frame 23 and frame 0.

### 4.2 Volume-Preserving Mesh Transformation Physics
All spatial deformations are calculated using Pillow's `Image.Transform.MESH` API operating over an $18 \times 18$ vertex grid (324 deformation quadrilaterals). Each quadrilateral maps destination screen coordinates $(x_0, y_0, x_1, y_1)$ to four sampled source coordinates $(x + dx, y + dy)$.

To prevent characters from looking rubbery or deflated, all vertical squash-and-stretch deformations strictly enforce volume preservation:
$$S_x(t) = \frac{1}{\sqrt{S_y(t)}}$$
Around a designated anchor point $(cx, cy)$, the source offset coordinates are calculated as:
$$\text{src}_x(x) = cx + \frac{x - cx}{S_x(t)}, \quad \text{src}_y(y) = cy + \frac{y - cy}{S_y(t)}$$
$$dx(x, y) = \text{src}_x(x) - x, \quad dy(x, y) = \text{src}_y(y) - y$$
Where vertical squash is clamped to $S_y \in [0.65, 1.45]$.

### 4.3 Mathematical Easing Models & Comic Timing Curves
Linear motion is prohibited. All kinetic trajectories are driven by the following parametric easing functions:

1. **Clamping Utility**:
   $$\text{clamp01}(u) = \max(0.0, \min(1.0, u))$$

2. **Cubic Ease-In-Out**:
   $$E_{\text{cubic}}(u) = \begin{cases} 4u^3 & u < 0.5 \\ 1 - \frac{(-2u + 2)^3}{2} & u \ge 0.5 \end{cases}$$

3. **Overshoot Ease-Out-Back**:
   $$E_{\text{back}}(u, s) = 1 + (s + 1)(u - 1)^3 + s(u - 1)^2 \quad (\text{standard } s = 1.70158)$$

4. **Anticipation Ease-In-Back**:
   $$E_{\text{in\_back}}(u, s) = (s + 1)u^3 - s u^2 \quad (\text{standard } s = 1.70158)$$

5. **Comic Pop Curve**:
   $$C(t) = \begin{cases}
   -0.35 \sin\left(\frac{t}{t_{\text{antic}}} \frac{\pi}{2}\right) & 0 \le t < t_{\text{antic}} \\
   -0.35 + 1.35 \cdot E_{\text{back}}\left(\frac{t - t_{\text{antic}}}{t_{\text{hit}} - t_{\text{antic}}}, 1.8\right) & t_{\text{antic}} \le t < t_{\text{hit}} \\
   1.0 + 0.06 \sin\left(\frac{t - t_{\text{hit}}}{t_{\text{hold}} - t_{\text{hit}}} 2\pi\right) & t_{\text{hit}} \le t < t_{\text{hold}} \\
   1.0 - E_{\text{cubic}}\left(\frac{t - t_{\text{hold}}}{1.0 - t_{\text{hold}}}\right) & t_{\text{hold}} \le t \le 1.0
   \end{cases}$$
   *(Standard keyframe thresholds: $t_{\text{antic}} = 0.16$, $t_{\text{hit}} = 0.32$, $t_{\text{hold}} = 0.68$).*

6. **Damped Exponential Impact Shake**:
   $$\Delta x_{\text{shake}}(t) = A \cdot e^{-\lambda(t - t_{\text{hit}})} \sin(95(t - t_{\text{hit}}))$$
   $$\Delta y_{\text{shake}}(t) = 0.6 A \cdot e^{-\lambda(t - t_{\text{hit}})} \cos(110(t - t_{\text{hit}}))$$
   *(Decay rate $\lambda = 18.0\text{ s}^{-1}$, impact amplitude $A = 8\text{–}12\text{px}$).*

---

### 4.4 Exhaustive Mathematical Models for the 14 Motion Primitives

```
+===========================================================================================================================+
|                                    14 PROCEDURAL MOTION PRIMITIVES SPECIFICATION TABLE                                    |
+----+----------------------------+-----------------------+------------+-----------------+----------------+-----------------+
| #  | PRIMITIVE NAME             | PRIMARY FREQ (ω)      | DAMPING (γ)| SQUASH (Sy)     | ROTATION (θ)   | TRANSLATION (Δ) |
+----+----------------------------+-----------------------+------------+-----------------+----------------+-----------------+
| 01 | soca_rag_windmill          | 2π rad/cycle (140BPM) | 0.00       | 0.95 – 1.05     | -25° to +25°   | Δx: ±35, Δy: ±15|
| 02 | steups_recoil_burst        | Piecewise Eased Pop   | 14.0 s⁻¹   | 0.82 – 1.29     | -14° to +6°    | Δx: ±8,  Δy: -16|
| 03 | allfours_table_slam        | Piecewise Grav + Osc  | 18.0 s⁻¹   | 0.68 – 1.25     | -8° to +35°    | Δx: ±12, Δy: +28|
| 04 | doubles_45_lean_drip       | 2.4π rad/cycle (Chew) | 0.00       | 0.92 – 1.08     | +38° to +45°   | Δx: +22, Δy: +18|
| 05 | tanty_akumbo_tilt          | 2π rad/cycle (Sway)   | 0.00       | 0.94 – 1.06     | -16° to +16°   | Δx: ±18, Δy: ±8 |
| 06 | bazodee_dazed_spiral       | Lissajous (ω₁=2π,ω₂=4π| 0.00       | 0.95 – 1.05     | -12° to +12°   | Δx: ±24, Δy: ±14|
| 07 | maco_peep_zoom             | Piecewise Asymmetric  | 12.0 s⁻¹   | 0.88 – 1.35     | -6° to +6°     | Δx: ±18, Δy: -30|
| 08 | heat_seeking_slipper_arc   | ω_spin = 8π rad/cycle | 0.00       | 0.85 – 1.20     | 0° to 1440°    | Ballistic Arc   |
| 09 | puncheon_fire_breath       | Piecewise Flame Pulse | 6.0 s⁻¹    | 0.78 – 1.22     | -8° to +8°     | Δx: ±6,  Δy: -12|
| 10 | steelpan_rebound           | 4π rad/cycle (Triplet)| 15.0 s⁻¹   | 0.86 – 1.14     | -5° to +5°     | Δx: ±4,  Δy: ±12|
| 11 | killing_dead_collapse      | 2π rad/cycle (Laugh)  | 4.0 s⁻¹    | 0.75 – 1.20     | -28° to +12°   | Δx: ±14, Δy: +22|
| 12 | ttec_blackout_candle       | Square Wave + 1/f     | 0.00       | 0.96 – 1.04     | -3° to +3°     | Δx: ±3,  Δy: ±4 |
| 13 | moko_jumbie_stilt_sway     | 2π rad/cycle (Invert) | 0.00       | 0.92 – 1.08     | -15° to +15°   | Δx: ±28, Δy: ±20|
| 14 | wasa_dry_shower_cough      | Piecewise Pressure    | 16.0 s⁻¹   | 0.80 – 1.18     | -5° to +5°     | Δx: ±6,  Δy: -14|
+----+----------------------------+-----------------------+------------+-----------------+----------------+-----------------+
```

---

#### 1. `soca_rag_windmill`
- **Physical Concept**: Conical 3D overhead rotation of fabric with aerodynamic wave lag and downbeat snap-whip reversals.
- **Parametric Equations**:
  $$\theta(t) = 2\pi t$$
  $$x_{\text{hand}}(t) = cx + R_x \cos(\theta(t)), \quad y_{\text{hand}}(t) = cy + R_y \sin(\theta(t))$$
  $$x_{\text{cloth}}(t) = cx + R_x \cos(\theta(t) - \Delta \phi), \quad y_{\text{cloth}}(t) = cy + R_y \sin(\theta(t) - \Delta \phi) + A_{\text{lag}} \sin(2\theta(t))$$
  Where anchor $c = (256, 180)$, $R_x = 110\text{px}$, $R_y = 38\text{px}$, $\Delta \phi = 0.52\text{ rad}$ (cloth aerodynamic lag).
- **Mesh Displacement Function**:
  $$disp(x, y) = \big(x + \Delta x_{\text{idle}} + w_{\text{top}}(y) \cdot (x_{\text{cloth}}(t) - cx), \ y + \Delta y_{\text{idle}} + w_{\text{top}}(y) \cdot (y_{\text{cloth}}(t) - cy)\big)$$
  Where $w_{\text{top}}(y) = e^{-((y - 140) / 95)^2}$.
- **24-Frame Keyframe Timing**:
  - *Frames 0–7 ($t = 0.000\text{–}0.292$)*: Hand sweeps from right apex down across front; cloth trails behind. Downbeat whip at Frame 0.
  - *Frames 8–15 ($t = 0.333\text{–}0.625$)*: Hand ascends to left apex; cloth billows upward into a wide sail. Second whip at Frame 8.
  - *Frames 16–23 ($t = 0.667\text{–}0.958$)*: Hand completes overhead loop; cloth unfolds into apex. Third whip at Frame 16.

---

#### 2. `steups_recoil_burst`
- **Physical Concept**: Anticipatory mouth purse suction (inward cheek clench with vertical jaw tension), explosive neck retraction recoil, and directional air burst expulsion.
- **Parametric Equations**:
  Comic pop progress curve $p(t) = C(t)$ with keyframe thresholds $t_{\text{antic}} = 0.14, t_{\text{hit}} = 0.28, t_{\text{hold}} = 0.65$.
  To resolve lateral expansion contradictions and rigorously preserve 3D cylindrical volume ($S_x^2 \cdot S_y = 1.0$), deformation is formulated piecewise across the clench and recoil phases:
  $$S_x(t) = \begin{cases}
  1.0 - 0.12 \cdot \sin\left(\frac{t}{t_{\text{antic}}} \frac{\pi}{2}\right) = 1.0 - 0.12 \cdot \left(\frac{\max(0.0, -p(t))}{0.35}\right) & 0 \le t < t_{\text{antic}} \\
  0.88 + 0.12 \cdot E_{\text{back}}\left(\frac{t - t_{\text{antic}}}{t_{\text{hit}} - t_{\text{antic}}}, 1.8\right) & t_{\text{antic}} \le t < t_{\text{hit}} \\
  1.0 + 0.02 \cdot \sin\left(\frac{t - t_{\text{hit}}}{t_{\text{hold}} - t_{\text{hit}}} 2\pi\right) & t_{\text{hit}} \le t < t_{\text{hold}} \\
  1.0 & t_{\text{hold}} \le t \le 1.0
  \end{cases}$$
  Matching vertical scale preserving 3D cylindrical mass ($V = S_x^2 \cdot S_y \equiv 1.000$):
  $$S_y(t) = \frac{1.0}{(S_x(t))^2}$$
  *(Note: At peak anticipation $t = t_{\text{antic}} = 0.14$, cheeks clench horizontally to $S_x = 0.8800$, while the jaw tenses vertically to $S_y = 1/(0.88)^2 = 1.2913$, perfectly conserving volume. Under 2D planar area preservation $S_x \cdot S_y = 1.0$, $S_y = 1/0.88 = 1.1364$).*
  $$\Delta y_{\text{neck}}(t) = -16.0 \cdot \max(0.0, p(t)), \quad \theta_{\text{head}}(t) = -12^\circ \cdot p(t)$$
  $$\text{Air Burst Radius: } R_{\text{puff}}(t) = \begin{cases} 0 & t < 0.28 \\ 8.0 + 42.0 \cdot \frac{t - 0.28}{0.40} & 0.28 \le t \le 0.68 \\ 0 & t > 0.68 \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–3 ($t = 0.000\text{–}0.125$)*: Anticipatory cheek compression ($S_x: 1.00 \to 0.88$, jaw tenses vertically $S_y: 1.00 \to 1.29$).
  - *Frames 4–7 ($t = 0.167\text{–}0.292$)*: Sudden neck snap recoil ($\Delta y = -16\text{px}, \theta = -12^\circ$). Cheeks spring back outward to $S_x = 1.00$. Directional air burst ignites at mouth $(256, 310)$.
  - *Frames 8–15 ($t = 0.333\text{–}0.625$)*: Disdainful living hold; air puff expands and dissipates ($\alpha: 255 \to 0$); head rolls slightly away ($+15^\circ$); subtle breathing oscillation ($\pm 2\%$).
  - *Frames 16–23 ($t = 0.667\text{–}0.958$)*: Cubic ease-in-out restoration to neutral resting pose ($S_x = 1.00, S_y = 1.00$).

---

#### 3. `allfours_table_slam`
- **Physical Concept**: Cocked card suspense hold, downward gravitational acceleration, damped seismic table vibration, and chalk dust dispersion.
- **Parametric Equations**:
  $$y_{\text{arm}}(t) = \begin{cases} 
  -50.0 \cdot \sin\left(\frac{t}{0.25} \frac{\pi}{2}\right) & t < 0.25 \\
  -50.0 + 85.0 \cdot \left(\frac{t - 0.25}{0.12}\right)^2 & 0.25 \le t < 0.37 \\
  35.0 \cdot e^{-12(t - 0.37)} \cos(8\pi(t - 0.37)) & t \ge 0.37
  \end{cases}$$
  $$(sh_x(t), sh_y(t)) = \begin{cases}
  (0, 0) & t < 0.37 \\
  (12 \cdot e^{-18(t - 0.37)} \sin(95(t - 0.37)), \ 8 \cdot e^{-18(t - 0.37)} \cos(110(t - 0.37))) & t \ge 0.37
  \end{cases}$$
  $$S_y(t) = \begin{cases} 1.0 & t < 0.37 \\ 0.68 & t = 0.37 \ (\text{Impact}) \\ 1.0 + 0.15 \cdot e^{-14(t - 0.37)} \cos(25(t - 0.37)) & t > 0.37 \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–6 ($t = 0.000\text{–}0.250$)*: Suspense apex hold. Arm hovers overhead; card quivers at $y = -50\text{px}$.
  - *Frames 7–9 ($t = 0.292\text{–}0.375$)*: Downward smash acceleration. Velocity increases quadric-wise.
  - *Frame 10 ($t = 0.417$)*: Impact! Card hits table. Maximum squash ($S_y = 0.68, S_x = 1.21$). 10-point starburst flash at $(256, 420)$.
  - *Frames 11–15 ($t = 0.458\text{–}0.625$)*: High-frequency seismic shake; chalk dust particles scatter horizontally ($\pm 45\text{px}$).
  - *Frames 16–23 ($t = 0.667\text{–}0.958$)*: Arm retracts into triumphant chest rest; dust settles.

---

#### 4. `doubles_45_lean_drip`
- **Physical Concept**: Cantilever forward 45° posture, cyclic mastication bob, viscous amber sauce stretching with surface tension droplet detachment and off-canvas gravitational acceleration.
- **Parametric Equations**:
  $$\Delta x_{\text{lean}}(y) = (y - 512.0) \cdot \tan(42^\circ) \cdot w_{\text{body}}(y)$$
  $$y_{\text{jaw}}(t) = 6.0 \cdot |\sin(4\pi t)|, \quad S_{\text{jaw}}(t) = 1.0 + 0.04 \cdot \sin(4\pi t)$$
  $$\text{Elastic Sauce Stub: } L_{\text{stub}}(t) = \begin{cases}
  10.0 + 35.0 \cdot \text{clamp01}\left(\frac{t - 0.20}{0.50}\right) & t < 0.70 \\
  10.0 + 35.0 \cdot e^{-18(t - 0.70)} \cos(12\pi(t - 0.70)) & t \ge 0.70
  \end{cases}$$
  $$\text{Detached Droplet Trajectory: } y_{\text{drop}}(t) = \begin{cases}
  y_{\text{bara}} + L_{\text{stub}}(t) & t < 0.70 \\
  y_{\text{bara}} + 45.0 + 2400.0 \cdot (t - 0.70)^2 & 0.70 \le t \le 0.92 \\
  y_{\text{bara}} + 10.0 \ (\text{Off-canvas Seam Reset}) & t > 0.92
  \end{cases}$$
  $$\alpha_{\text{drop}}(t) = \begin{cases} 255 & t \le 0.92 \\ 0 & t > 0.92 \ (\text{Invisible Reset for } y > 512\text{px}) \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–5 ($t = 0.000\text{–}0.208$)*: Sustained 45° cantilever lean; jaw chewing bob cycles 1 & 2; aromatic steam curls rise from bara; curry stub rests at $L = 10\text{px}$.
  - *Frames 6–16 ($t = 0.250\text{–}0.667$)*: Viscous amber curry droplet accumulates at wrapper base; elongates downward under gravity ($L = 10 \to 45\text{px}$).
  - *Frames 17–19 ($t = 0.708\text{–}0.792$)*: Pinch-off! Droplet detaches and accelerates freely under gravity ($a = 4800\text{px/s}^2$); bara wrapper stub snaps back elastically ($L_{\text{stub}} \to 10\text{px}$).
  - *Frames 20–22 ($t = 0.833\text{–}0.917$)*: Droplet accelerates past canvas bottom edge ($y > 512\text{px}$); alpha resets to 0 at $t = 0.92$.
  - *Frame 23 ($t = 0.958$)*: Droplet is off-canvas and completely invisible ($\alpha_{\text{drop}} = 0$); position resets to $y_{\text{bara}} + 10\text{px}$; jaw completes chewing cycle 4; seamless continuous loop back to Frame 0.

---

#### 5. `tanty_akumbo_tilt`
- **Physical Concept**: Asymmetric contrapposto hip sway, coupled counter-tilt neck wobble, piercing side-eye and rhythmic finger wag.
- **Parametric Equations**:
  $$\theta_{\text{hip}}(t) = 14^\circ \cdot \sin(2\pi t)$$
  $$\theta_{\text{neck}}(t) = -18^\circ \cdot \sin(2\pi t + 0.35) \quad (\text{Coupled phase shift})$$
  $$\Delta x_{\text{pelvis}}(t) = 16.0 \cdot \sin(2\pi t), \quad \Delta y_{\text{bob}}(t) = -6.0 \cdot |\cos(2\pi t)|$$
  $$\theta_{\text{finger}}(t) = 22^\circ \cdot \sin(6\pi t) \cdot w_{\text{hand}}(x, y)$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–6 ($t = 0.000\text{–}0.250$)*: Hips sway right ($+14^\circ$); head tilts sharply left ($-18^\circ$); left eye narrows into cut-eye.
  - *Frames 7–12 ($t = 0.292\text{–}0.500$)*: Transition through neutral; finger completes wag cycle 1; glasses slide down nose ($2\text{px}$).
  - *Frames 13–18 ($t = 0.542\text{–}0.750$)*: Hips sway left ($-14^\circ$); head tilts right ($+18^\circ$); finger completes wag cycle 2.
  - *Frames 19–23 ($t = 0.792\text{–}0.958$)*: Smooth settle back toward initial right-leaning stance.

---

#### 6. `bazodee_dazed_spiral`
- **Physical Concept**: Lemniscate of Gerono torso trajectory, logarithmic eye swirls, Keplerian orbiting stars.
- **Parametric Equations**:
  $$x_{\text{sway}}(t) = 22.0 \cdot \sin(2\pi t), \quad y_{\text{sway}}(t) = 12.0 \cdot \sin(4\pi t)$$
  $$\theta_{\text{vortex}}(r, t) = 0.75 \cdot \sin(4\pi t) \cdot e^{-(r / 40.0)^2}$$
  $$\text{Orbiting Star } i \in \{0, 1, 2\}: \begin{cases}
  x_i(t) = 256 + 105 \cdot \cos\left(2\pi t + \frac{2\pi i}{3}\right) \\
  y_i(t) = 90 + 22 \cdot \sin\left(2\pi t + \frac{2\pi i}{3}\right)
  \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–6 ($t = 0.000\text{–}0.250$)*: Head loops through top-right quadrant of figure-8; eye spirals rotate clockwise; star 0 crosses foreground.
  - *Frames 7–12 ($t = 0.292\text{–}0.500$)*: Head dips through center cross; eye spirals reverse direction; star 1 crosses foreground.
  - *Frames 13–18 ($t = 0.542\text{–}0.750$)*: Head loops through top-left quadrant; star 2 crosses foreground; heart particle pulses.
  - *Frames 19–23 ($t = 0.792\text{–}0.958$)*: Head returns through lower loop; seamless continuous periodic cycle.

---

#### 7. `maco_peep_zoom`
- **Physical Concept**: Creeping emergence from blinds, sudden optical lens zoom, horizontal scan, lightning panic retreat.
- **Parametric Equations**:
  $$y_{\text{creep}}(t) = \begin{cases}
  -30.0 \cdot \left(\frac{t}{0.25}\right)^3 & t < 0.25 \\
  -30.0 & 0.25 \le t < 0.75 \\
  -30.0 + 30.0 \cdot E_{\text{in\_back}}\left(\frac{t - 0.75}{0.25}, 1.7\right) & t \ge 0.75
  \end{cases}$$
  $$S_{\text{lens}}(t) = \begin{cases}
  1.0 & t < 0.25 \\
  1.0 + 0.35 \cdot E_{\text{back}}\left(\frac{t - 0.25}{0.15}, 1.8\right) & 0.25 \le t < 0.40 \\
  1.35 + 0.05 \cdot \sin(10\pi t) & 0.40 \le t < 0.75 \\
  1.0 & t \ge 0.75
  \end{cases}$$
  $$x_{\text{pan}}(t) = 18.0 \cdot \sin\left(\frac{t - 0.40}{0.35} \cdot 2\pi\right) \quad (0.40 \le t \le 0.75)$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–5 ($t = 0.000\text{–}0.208$)*: Stealth emergence. Blinds crack open; head inches up $30\text{px}$.
  - *Frames 6–9 ($t = 0.250\text{–}0.375$)*: Optical punch! Binoculars snap forward; lenses expand 35% with `ease_out_back`.
  - *Frames 10–17 ($t = 0.417\text{–}0.708$)*: Lateral surveillance scan. Eyes twitch left-to-right ($\pm 18\text{px}$); iris rings pulse.
  - *Frames 18–23 ($t = 0.750\text{–}0.958$)*: Panic snap! Head slams straight down in 2 frames; blinds rattle shut.

---

#### 8. `heat_seeking_slipper_arc`
- **Physical Concept**: Maternal flip-flop flying on a parabolic ballistic trajectory with planar rotation, comic impact starburst, damped floor bounce, and an invisible loop-seam reset.
- **Parametric Equations**:
  $$\text{Flight Interpolant: } u(t) = \min\left(1.0, \frac{t}{0.65}\right)$$
  $$x_{\text{pos}}(t) = \begin{cases}
  490.0 - 234.0 \cdot u(t) & t < 0.65 \ (\text{Ballistic Flight}) \\
  256.0 & 0.65 \le t < 0.70 \ (\text{Impact Squash}) \\
  256.0 + 4.0 \cdot e^{-12(t - 0.70)} \sin(12\pi(t - 0.70)) & 0.70 \le t < 0.85 \ (\text{Damped Settle}) \\
  256.0 & 0.85 \le t < 0.95 \ (\text{Fade-out}) \\
  256.0 + 234.0 \cdot \left(\frac{t - 0.95}{0.05}\right) & 0.95 \le t \le 1.0 \ (\text{Invisible Trajectory Reset})
  \end{cases}$$
  $$y_{\text{pos}}(t) = \begin{cases}
  280.0 - 180.0 \cdot \sin(\pi u(t)) & t < 0.65 \ (\text{Parabolic Flight Arc}) \\
  280.0 & 0.65 \le t < 0.70 \\
  280.0 - 8.0 \cdot e^{-14(t - 0.70)} |\sin(16\pi(t - 0.70))| & 0.70 \le t < 0.85 \ (\text{Damped Floor Bounce}) \\
  280.0 & t \ge 0.85 \ (\text{Resting Plane})
  \end{cases}$$
  $$\theta_{\text{spin}}(t) = \begin{cases}
  8\pi \cdot u(t) & t < 0.65 \ (\text{4 Full Revolutions during Flight}) \\
  8\pi & 0.65 \le t < 0.95 \\
  8\pi \cdot \left(1.0 - \frac{t - 0.95}{0.05}\right) & 0.95 \le t \le 1.0 \ (\text{Invisible Angular Reset})
  \end{cases}$$
  $$\alpha_{\text{slipper}}(t) = \begin{cases}
  255 & t \le 0.85 \\
  255 \cdot \left(1.0 - \frac{t - 0.85}{0.10}\right)^2 & 0.85 < t \le 0.95 \ (\text{Quadratic Dissolve}) \\
  0 & 0.95 < t \le 1.0 \ (\text{Zero Alpha Seam Reset})
  \end{cases}$$
  $$R_{\text{flash}}(t) = \begin{cases}
  0 & t < 0.65 \\
  55.0 \cdot \sin\left(\frac{t - 0.65}{0.20} \cdot \pi\right) & 0.65 \le t < 0.85 \\
  0 & t \ge 0.85 \ (\text{Strictly 0 at Frame 23})
  \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–4 ($t = 0.000\text{–}0.167$)*: Launch! Slipper enters upper-right canvas perimeter $(490, 280)$, spinning rapidly ($\theta: 0^\circ \to 360^\circ$).
  - *Frames 5–11 ($t = 0.208\text{–}0.458$)*: Parabolic apex. Slipper arches over center canvas; speed trail lines stretch behind.
  - *Frames 12–15 ($t = 0.500\text{–}0.625$)*: Target descent. Slipper accelerates into center target $(256, 280)$.
  - *Frames 16–17 ($t = 0.667\text{–}0.708$)*: Bullseye impact! Slipper squashes ($S_y = 0.70, S_x = 1.195$); multi-point comic starburst ignites ($R = 55\text{px}$).
  - *Frames 18–20 ($t = 0.750\text{–}0.833$)*: Damped impact rebound; slipper settles to floor; starburst flash contracts to $R = 0$ at $t = 0.85$.
  - *Frames 21–22 ($t = 0.875\text{–}0.917$)*: Slipper fades to zero alpha ($\alpha: 255 \to 0$ at $t = 0.95$); impact dust cloud dissipates.
  - *Frame 23 ($t = 0.958$)*: Slipper is completely invisible ($\alpha_{\text{slipper}} = 0$, $R_{\text{flash}} = 0$); coordinates reset smoothly to launch point $(490, 280)$ without popping; seamless loop wrap to Frame 0.

---

#### 9. `puncheon_fire_breath`
- **Physical Concept**: Massive chest inhalation expansion, pressurized flame eruption cone, smoky cough recoil.
- **Parametric Equations**:
  $$S_y(t) = \begin{cases}
  1.0 + 0.18 \cdot \sin\left(\frac{t}{0.22} \frac{\pi}{2}\right) & t < 0.22 \\
  1.18 - 0.38 \cdot \left(\frac{t - 0.22}{0.12}\right) & 0.22 \le t < 0.34 \\
  0.80 + 0.20 \cdot \left(1.0 - e^{-8(t - 0.34)}\right) & t \ge 0.34
  \end{cases}$$
  $$R_{\text{flame}}(t) = \begin{cases}
  0 & t < 0.24 \\
  85.0 \cdot \sin\left(\frac{t - 0.24}{0.45} \cdot \pi\right) & 0.24 \le t \le 0.69 \\
  0 & t > 0.69
  \end{cases}$$
  $$\Delta x_{\text{cough}}(t) = 7.0 \cdot \sin(16\pi t) \cdot e^{-5(t - 0.69)} \quad (t \ge 0.69)$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–5 ($t = 0.000\text{–}0.208$)*: Inhalation. Torso puffs up 18% ($S_y = 1.18, S_x = 0.92$); eyes bulge.
  - *Frames 6–9 ($t = 0.250\text{–}0.375$)*: Eruption! Torso snaps forward ($S_y = 0.80$); roaring yellow/blue flame cone blasts from mouth.
  - *Frames 10–16 ($t = 0.417\text{–}0.667$)*: Sustained flamethrower cone; heat distortion ripples canvas; ember sparks fly outward.
  - *Frames 17–23 ($t = 0.708\text{–}0.958$)*: Flame exhausts; character coughs violently ($\Delta x = \pm 7\text{px}$); black smoke rings drift up.

---

#### 10. `steelpan_rebound`
- **Physical Concept**: Calypso/soca polyrhythmic mallet strikes, rapid triplet elastic rebound, and synchronized integer-multiple acoustic wavefronts decaying to zero alpha at loop boundaries.
- **Parametric Equations**:
  $$\tau(t) = \text{mod}(t \cdot 3.0, 1.0)$$
  $$y_{\text{mallet}}(\tau) = \begin{cases} -28.0 \cdot (1.0 - \tau / 0.3) & \tau < 0.3 \ (\text{Strike Down}) \\ 0.0 & \tau = 0.3 \ (\text{Contact}) \\ -28.0 \cdot \sin\left(\frac{\tau - 0.3}{0.7} \pi\right) \cdot e^{-3.5\tau} & \tau > 0.3 \ (\text{Elastic Rebound}) \end{cases}$$
  $$\Delta y_{\text{pan}}(x, y, \tau) = -8.0 \cdot e^{-((r_{\text{strike}}) / 65)^2} \cdot \sin(8\pi \tau) \cdot e^{-12\tau}$$
  $$R_{\text{ring}}(t) = \text{mod}(t \cdot 360.0, 120.0)$$
  $$\alpha_{\text{ring}}(t) = 240.0 \cdot \left(\max\left(0.0, 1.0 - \frac{R_{\text{ring}}(t)}{105.0}\right)\right)^2$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–7 ($t = 0.000\text{–}0.292$)*: Triplet strike 1. Mallet hits pan note; acoustic wavefront 1 expands from $R = 0$ to $105\text{px}$ and decays to $\alpha = 0$ at Frame 7; pan surface vibrates with damped sinusoidal resonance.
  - *Frames 8–15 ($t = 0.333\text{–}0.625$)*: Triplet strike 2 (alternate hand mallet). Mallet hits note; acoustic wavefront 2 expands ($R = 0 \to 105\text{px}$) and dissolves cleanly to $\alpha = 0$ at Frame 15.
  - *Frames 16–23 ($t = 0.667\text{–}0.958$)*: Triplet strike 3. Mallet hits note; acoustic wavefront 3 expands ($R = 0 \to 105\text{px}$) and completely dissolves to $\alpha = 0$ at Frame 23 ($t = 23/24$); zero lingering overlay at loop seam; seamless loop wrap to downbeat strike at Frame 0.

---

#### 11. `killing_dead_collapse`
- **Physical Concept**: Hysterical laughing fit; torso hinges backward, high-velocity horizontal tear jets spray, rhythmic knee-slap bouncing.
- **Parametric Equations**:
  $$\theta_{\text{torso}}(t) = -24^\circ + 8^\circ \cdot \sin(6\pi t)$$
  $$\Delta y_{\text{laugh}}(t) = 18.0 + 10.0 \cdot |\cos(6\pi t)|$$
  $$S_y(t) = 1.0 + 0.12 \cdot \cos(6\pi t), \quad S_x(t) = \frac{1.0}{\sqrt{S_y(t)}}$$
  $$\text{Tear Jet } (\pm x): \begin{cases}
  x_{\text{tear}}(t) = cx \pm (25.0 + 110.0 \cdot \text{mod}(t \cdot 2, 1.0)) \\
  y_{\text{tear}}(t) = cy - 20.0 \cdot \sin(\pi \cdot \text{mod}(t \cdot 2, 1.0)) + 65.0 \cdot (\text{mod}(t \cdot 2, 1.0))^2
  \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–5 ($t = 0.000\text{–}0.208$)*: Torso reclines backward ($-24^\circ$); mouth widens into giant grin; first tear pair erupts.
  - *Frames 6–11 ($t = 0.250\text{–}0.458$)*: Laughing bounce pulse 1; torso bobs vertically ($18\text{px}$); hands slap knees; tears arc outward.
  - *Frames 12–17 ($t = 0.500\text{–}0.708$)*: Laughing bounce pulse 2; second pair of tear jets spray horizontally ($\pm 135\text{px}$).
  - *Frames 18–23 ($t = 0.750\text{–}0.958$)*: Laughing bounce pulse 3; breathless comic wheeze; tears splash at canvas edges.

---

#### 12. `ttec_blackout_candle`
- **Physical Concept**: Sudden power grid blackout, wooden match strike friction flash, diffusive candle flame glow bubble with 1/f flicker, followed by an authentic T&TEC power restoration transition with dissipating smoke curl.
- **Parametric Equations**:
  $$\text{Grid Illumination Factor: } L(t) = \begin{cases}
  1.0 & t < 0.16 \ (\text{Overhead Electric Bulb On}) \\
  0.0 & 0.16 \le t < 0.32 \ (\text{Total Blackout}) \\
  0.15 + 0.85 \cdot \text{clamp01}\left(\frac{t - 0.32}{0.20}\right) & 0.32 \le t < 0.85 \ (\text{Candle Lit}) \\
  0.0 & 0.85 \le t < 0.88 \ (\text{Power Restoration: Pre-surge Dip}) \\
  0.75 & 0.88 \le t < 0.92 \ (\text{Power Restoration: Voltage Surge}) \\
  0.30 & 0.92 \le t < 0.95 \ (\text{Power Restoration: Arc Dip}) \\
  1.0 & 0.95 \le t \le 1.0 \ (\text{Full Electric Grid Lock-in})
  \end{cases}$$
  $$R_{\text{flash}}(t) = \begin{cases}
  0 & t < 0.32 \\
  45.0 \cdot e^{-25(t - 0.32)} & 0.32 \le t < 0.50 \ (\text{Match Strike Friction Flash}) \\
  0 & t \ge 0.50
  \end{cases}$$
  $$\theta_{\text{flame}}(t) = 4^\circ \cdot \sin(14\pi t) + 2^\circ \cdot \sin(33\pi t) \quad (0.32 \le t < 0.85)$$
  $$R_{\text{glow}}(t) = \begin{cases}
  0 & t < 0.32 \\
  90.0 + 12.0 \cdot \sin(8\pi t) & 0.32 \le t < 0.85 \\
  (90.0 + 12.0 \cdot \sin(8\pi t)) \cdot \left(1.0 - \frac{t - 0.85}{0.10}\right)^2 & 0.85 \le t \le 0.95 \ (\text{Flame Blowout Glow Fade}) \\
  0 & t > 0.95 \ (\text{Strictly 0 at Frame 23})
  \end{cases}$$
  $$\alpha_{\text{candle}}(t) = \begin{cases}
  0 & t < 0.32 \\
  255 & 0.32 \le t < 0.85 \\
  255 \cdot \left(1.0 - \frac{t - 0.85}{0.10}\right)^2 & 0.85 \le t \le 0.95 \\
  0 & t > 0.95
  \end{cases}$$
  $$\text{Dissipating Smoke Curl } (0.85 \le t \le 0.95): \begin{cases}
  x_{\text{smoke}}(t) = 256.0 + 12.0 \cdot \sin(16\pi(t - 0.85)) \\
  y_{\text{smoke}}(t) = 320.0 - 180.0 \cdot (t - 0.85) \\
  \alpha_{\text{smoke}}(t) = 180.0 \cdot \left(1.0 - \frac{t - 0.85}{0.10}\right)^2 \quad (\alpha_{\text{smoke}} \equiv 0 \text{ for } t > 0.95)
  \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–3 ($t = 0.000\text{–}0.125$)*: Full bright illumination ($L = 1.0$); overhead electric bulb glows cleanly.
  - *Frames 4–7 ($t = 0.167\text{–}0.292$)*: Current cut! Sudden total blackout ($L = 0.0$); pure darkness with two nervous cartoon eyes blinking.
  - *Frame 8 ($t = 0.333$)*: Sssssk! Match strike friction flash ($R_{\text{flash}} = 45\text{px}$, bright yellow/white core).
  - *Frames 9–19 ($t = 0.375\text{–}0.833$)*: Candle burns; warm amber glow bubble expands ($R = 90\text{px}$); flame tip sways with $1/f$ flutter.
  - *Frames 20–22 ($t = 0.833\text{–}0.917$)*: Current come back! Grid voltage flickers; candle flame is blown out; thin curling smoke wisp drifts upward and dissolves ($\alpha_{\text{smoke}} \to 0$).
  - *Frame 23 ($t = 0.958$)*: Overhead electric bulb locks into full steady illumination ($L = 1.0$); smoke completely dissipated ($\alpha_{\text{smoke}} = 0$, $R_{\text{glow}} = 0$); seamless continuous loop back to Frame 0.

---

#### 13. `moko_jumbie_stilt_sway`
- **Physical Concept**: High-elevation inverted pendulum oscillation, alternating stilt elevation with $180^\circ$ phase shift, billowing satin trails.
- **Parametric Equations**:
  $$\theta_{\text{sway}}(t) = 15^\circ \cdot \sin(2\pi t)$$
  $$\Delta y_{\text{left}}(t) = -24.0 \cdot \max(0.0, \sin(2\pi t))$$
  $$\Delta y_{\text{right}}(t) = -24.0 \cdot \max(0.0, -\sin(2\pi t))$$
  $$\Delta x_{\text{torso}}(t) = -12.0 \cdot \sin(2\pi t)$$
  $$\Delta x_{\text{fabric}}(y, t) = 18.0 \cdot \sin(2\pi t - 0.015 y) \cdot \left(\frac{y - 200}{312}\right)$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–6 ($t = 0.000\text{–}0.250$)*: Left stilt lifts upward ($24\text{px}$); torso sways right ($+15^\circ$); satin fabric billows left.
  - *Frames 7–12 ($t = 0.292\text{–}0.500$)*: Left stilt plants firmly on ground; weight transitions across center of gravity.
  - *Frames 13–18 ($t = 0.542\text{–}0.750$)*: Right stilt lifts upward ($24\text{px}$); torso sways left ($-15^\circ$); satin fabric billows right.
  - *Frames 19–23 ($t = 0.792\text{–}0.958$)*: Right stilt plants; body smoothly settles toward neutral center line.

---

#### 14. `wasa_dry_shower_cough`
- **Physical Concept**: Galvanized water pipe bulging with pressure, followed by the release of a single pathetic water drop accelerating off-canvas, an authentic 3D mass-preserving volume rebound, and a dry puff of dust.
- **Parametric Equations**:
  $$S_x(t) = \begin{cases}
  1.0 + 0.16 \cdot \sin\left(\frac{t}{0.28} \frac{\pi}{2}\right) & t < 0.28 \ (\text{Groaning Pressure Bulge}) \\
  1.16 - 0.26 \cdot \left(\frac{t - 0.28}{0.08}\right) & 0.28 \le t < 0.36 \ (\text{Violent Shudder Recoil}) \\
  0.90 + 0.10 \cdot \left(1.0 - e^{-10(t - 0.36)}\right) & t \ge 0.36 \ (\text{Relaxation to Neutral})
  \end{cases}$$
  $$S_y(t) = \frac{1.0}{(S_x(t))^2} \quad (\text{Mass-Preserving Volume Invariance Law})$$
  $$y_{\text{drop}}(t) = \begin{cases}
  280.0 & t < 0.36 \ (\text{Contained in Nozzle}) \\
  280.0 + 2600.0 \cdot (t - 0.36)^2 & 0.36 \le t \le 0.68 \ (\text{Gravitational Acceleration}) \\
  280.0 \ (\text{Off-canvas Reset}) & t > 0.68 \ (y > 546\text{px, off-canvas})
  \end{cases}$$
  $$\alpha_{\text{drop}}(t) = \begin{cases}
  0 & t < 0.36 \ (\text{Unformed}) \\
  255 & 0.36 \le t \le 0.68 \ (\text{Falling Droplet}) \\
  0 & t > 0.68 \ (\text{Invisible Off-canvas Seam Reset})
  \end{cases}$$
  $$R_{\text{dust}}(t) = \begin{cases}
  0 & t < 0.40 \\
  38.0 \cdot \sin\left(\frac{t - 0.40}{0.45} \cdot \pi\right) & 0.40 \le t \le 0.85 \\
  0 & t > 0.85 \ (\text{Strictly 0 at Frame 23})
  \end{cases}$$
- **24-Frame Keyframe Timing**:
  - *Frames 0–6 ($t = 0.000\text{–}0.250$)*: False hope! The dry tap/pipe shudders and bulges with groaning effort ($S_x = 1.16, S_y = 0.74$).
  - *Frames 7–9 ($t = 0.292\text{–}0.375$)*: Pipe shudders violently; single tiny pathetic droplet squeezes out of nozzle at $(256, 280)$.
  - *Frames 10–16 ($t = 0.417\text{–}0.667$)*: Solitary droplet plummets downward, accelerating off-canvas bottom ($y > 546\text{px}$ at $t = 0.68$); dry brown dust puff expands from nozzle ($R = 38\text{px}$).
  - *Frames 17–20 ($t = 0.708\text{–}0.833$)*: Droplet is off-canvas ($\alpha_{\text{drop}} = 0$) and resets to nozzle position invisibly; dust cloud dissipates ($R_{\text{dust}} \to 0$ at $t = 0.85$).
  - *Frames 21–23 ($t = 0.875\text{–}0.958$)*: Tap settles into dead stillness ($S_x \to 1.0, S_y \to 1.0$); all overlays have zero alpha at Frame 23; ironic disappointment settles; seamless loop wrap to Frame 0.

---

### 4.5 Procedural Vector Graphic FX Engine
All secondary graphic overlays are rendered in a separate RGBA buffer using Pillow `ImageDraw` before compositing onto the deformed character frame.

#### 4.5.1 Ink Line Styling Standard
- **Color**: Pure deep charcoal ink `INK = (20, 22, 29, 255)` (`#14161D`).
- **Outer Silhouettes & Borders**: Width $4\text{–}6\text{px}$.
- **Interior Seams**: Width $2\text{–}3\text{px}$.
- **Specular Highlight Lines**: Width $2\text{px}$ pure white `(255, 255, 255, alpha)` with top-edge offset.

#### 4.5.2 Procedural Vector FX Primitives
1. **`draw_comic_starburst(draw, cx, cy, rout, n_pts=8, color=GOLD)`**:
   Multi-point star polygon alternating outer radius $R_{\text{out}}$ and inner radius $R_{\text{in}} = 0.55 R_{\text{out}}$. Outer stroke in 3px ink, inner core in creamy white `(255, 255, 240)` at 55% radius.
2. **`draw_comic_puff(draw, cx, cy, r_base, color=WHITE)`**:
   Multi-lobed cluster (center + 4 orbital lobes). Multi-pass: Pass 1 draws all lobe circles in dark ink with radius $R \cdot s_r + 2.5\text{px}$; Pass 2 fills lobes in body color, producing a clean, unified comic puff with crisp outer ink and zero internal seams.
3. **`draw_comic_droplet(draw, cx, cy, radius, color=CYAN)`**:
   Teardrop polygon with sharp top apex and bulbous rounded base, outlined in 2px ink. Upper-left quadrant includes an anti-aliased white elliptical specular reflection.
4. **`draw_comic_music_note(draw, cx, cy, scale=1.0)`**:
   Tilted elliptical note head with 2px ink outline, vertical stem (7px ink, 3px cyan core), and curved hook flag with a white crescent reflection.
5. **`draw_comic_speed_lines(draw, cx, cy, r1, r2, angles)`**:
   Radial line pairs originating from radius $R_1$ to $R_2$ along angle vectors. Under-stroke in dark ink (width $W+3$), over-stroke in bright color (width $W$).
6. **`draw_comic_twinkle(draw, cx, cy, radius)`**:
   8-point diamond star rotating with angular velocity $\omega = \pi t$, centered on a circular specular core.
7. **`draw_comic_anger_vein(draw, cx, cy, radius)`**:
   4-quadrant curved cross arc. Outlined with 6px ink width, 3px crimson red core (`#DA121A`).

---

## SECTION 5: MASTER CULTURAL MAPPING MATRIX FOR ALL 188 STICKERS

### 5.1 Matrix Schema Architecture (9 Columns)
Every sticker in the PeelOff catalog is rigorously defined across a 9-column architectural schema:
1. **`#`**: Global catalog index (1 to 188).
2. **`Sticker ID`**: Canonical asset identifier matching `data/packs.js` and `data/trini-slang.js`.
3. **`Pack/Category`**: Architectural grouping (Packs 1–8 or Slang Categories 1–6).
4. **`Cultural Meaning & Context`**: Sociolinguistic definition, emotional register, and conversational usage.
5. **`Visual Metaphor & 3D Elements`**: Specific 3D character, prop, expression, and material details.
6. **`Primary Authentic Motion Primitive`**: Designated motion routine from the 14 primitives (zero generic fallback remnants).
7. **`Secondary Graphic FX`**: Procedural vector overlay elements and comic styling.
8. **`Keyframe Timing (24f @ 90ms)`**: 4-phase micro-motion timing schedule across the 2.16s loop.
9. **`Framing Bounds / Breathing Room`**: Safe margin scaling (`scale=0.91`, `scale=0.88`, or `scale=0.93`).

---

### 5.2 Complete 188-Sticker Mapping Matrix Table (Part 1: Themed Pack Stickers 1–100)

| # | Sticker ID | Pack/Category | Cultural Meaning & Context | Visual Metaphor & 3D Elements | Primary Authentic Motion Primitive | Secondary Graphic FX | Keyframe Timing (24f @ 90ms) | Framing Bounds / Breathing Room |
|---|---|---|---|---|---|---|---|---|
| 1 | `ent` | Pack 1: Ent?! & Comment Section Vibes | ENT?! — Universal Trini confirmation ('Isn't it true?!', 'Right?!', 'Tell dem!'). Ultimate co-sign & agreement. | Sassy head tilt with raised eyebrow [Style: sticker] | tanty_akumbo_tilt | Comic punctuation starburst + snappy nod | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 2 | `steups` | Pack 1: Ent?! & Comment Section Vibes | STEUPS — Iconic Trini teeth-sucking sound expressing annoyance, dismissal, or 'stop talking nonsense'. Maximum dismissal. | Jaw clenches, head jerks back [Style: 3d] | steups_recoil_burst | Expanding acoustic shockwave + air puff | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.91 (466x466, 23px margin) |
| 3 | `ah-eh-able` | Pack 1: Ent?! & Comment Section Vibes | AH EH ABLE! — 'I cannot deal with this / Too funny or ridiculous.' Classic reaction to pure comedy or drama. | Hand fanning face, rolling eyes back [Style: sticker] | killing_dead_collapse | Sweating droplets + fluttering hand fan | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 4 | `look-trouble` | Pack 1: Ent?! & Comment Section Vibes | LOOK TROUBLE! — Drama, chaos, or a sticky situation unfolding in real time in the group chat. Grabbing popcorn. | Peering over sunglasses with wide eyes [Style: sticker] | maco_peep_zoom | Flashing yellow hazard warning lights | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 5 | `mamaguy` | Pack 1: Ent?! & Comment Section Vibes | MAMAGUY — Flattery, sweet-talking, or trying to butter someone up with smooth charm. Sweet-talking alert. | Sugary sweet smile with halo fluttering [Style: 3d] | tanty_akumbo_tilt | Melting syrup drips + floating hearts | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 6 | `pure-bazodee` | Pack 1: Ent?! & Comment Section Vibes | PURE BAZODEE! — Dizzy, infatuated, confused, or head-over-heels dazed (from French patois abasourdi). | Head swaying in figure-8 with dazed eyes [Style: sticker] | bazodee_dazed_spiral | Orbiting yellow stars and fluttering birds | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 7 | `weyyyy` | Pack 1: Ent?! & Comment Section Vibes | WEYYYY! — Exclamation of pure shock, hype, or disbelief when someone drops tea or a big tune. | Jaw dropping open, hands flying to cheeks [Style: sticker] | puncheon_fire_breath | Comic megaphone shockwave + exclamation marks | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 8 | `scene` | Pack 1: Ent?! & Comment Section Vibes | SCENE. — 'Understood', 'Bet', or passive-aggressive 'I see how it is.' Cool nod / noted. | Cool nod with sunglasses adjusting [Style: 3d] | tanty_akumbo_tilt | Specular glint on sunglasses lens | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.93 (476x476, 18px margin) |
| 9 | `fuh-real` | Pack 1: Ent?! & Comment Section Vibes | FUH REAL?! — 'Are you serious right now?!' Skeptical side-eye reaction. | Dramatic diagonal cut-eye with arched brow [Style: 3d] | tanty_akumbo_tilt | Question mark pop + skeptical head cock | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 10 | `doh-tote` | Pack 1: Ent?! & Comment Section Vibes | DOH TOTE! — 'Don't take a joke (picong) personally / Don't carry a grudge.' Banter code. | Unbothered shoulder brush and hand wave [Style: sticker] | tanty_akumbo_tilt | Dust brushed off shoulder + breezy puff | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 11 | `killing-me-dead` | Pack 1: Ent?! & Comment Section Vibes | KILLING ME DEAD — Dying of laughter; peak comedy in the comments or group chat. | Torso thrown back, clapping hands [Style: sticker] | killing_dead_collapse | Horizontal tear jets + laughing soundwaves | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 12 | `rel-bess` | Pack 1: Ent?! & Comment Section Vibes | REL BESS! — Top-tier, amazing, delicious, or 10/10 quality. Chef's kiss approval. | Golden chef's kiss or crown sparkling [Style: sticker] | soca_rag_windmill | Golden shimmering starbursts + crown bounce | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 13 | `cyah-take-dat` | Pack 1: Ent?! & Comment Section Vibes | CYAH TAKE DAT! — Firm refusal to tolerate disrespect, heat, or madness. Drawing the line. | Palm thrust forward in "stop" gesture [Style: sticker] | steups_recoil_burst | Brick wall barrier impact + dust puff | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.91 (466x466, 23px margin) |
| 14 | `chupidee` | Pack 1: Ent?! & Comment Section Vibes | CHUPIDEE — Acting silly, foolish, or making zero sense (Côté Ci Côté Là classic). Classic dotish moment. | Silly face with spinning goofy eyes [Style: 3d] | bazodee_dazed_spiral | Swirling spiral eyes + floppy ear wobble | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 15 | `freshwater-yankee` | Pack 1: Ent?! & Comment Section Vibes | FOREIGN — Travelling abroad, living in 'foreign' (NY, Miami, Toronto, London), or brand new accent. | Suitcase bouncing with exaggerated strut [Style: 3d] | soca_rag_windmill | Floating boarding pass + snowflake sparkles | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 16 | `just-picong` | Pack 1: Ent?! & Comment Section Vibes | JUST PICONG! — Good-natured teasing, roasting, and playful banter among friends. Playful banter. | Playful elbow jab and winking grin [Style: 3d] | killing_dead_collapse | Comic jester bell bounce + teasing tongue | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 17 | `crapaud-pipe` | Pack 1: Ent?! & Comment Section Vibes | CRAPAUD SMOKE YUH PIPE — Classic proverb meaning 'You are in serious trouble now / Your goose is cooked!' | Toad in swamp puffing a smoking pipe [Style: 3d] | puncheon_fire_breath | Smoke rings rising from pipe + blinking eyes | f0-f4 Throat sac inhalation puff -> f5-f9 Slow exhalation into smoking pipe -> f10-f17 Expanding concentric smoke rings floating up -> f18-f23 Blinking toad eyes & settle | scale=0.88 (450x450, 31px margin) |
| 18 | `trini-chow` | Pack 1: Ent?! & Comment Section Vibes | MANGO & POMERAC CHOW — Mouthwatering fruit chow with Scotch bonnet, garlic, chadon beni, salt, lime. | Pepper-dusted bowl shaking with spice heat [Style: 3d] | doubles_45_lean_drip | Rising spicy heat fumes + jumping pepper seeds | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 19 | `maco` | Pack 2: Maco, Horn & Tabanca | MACO! — Nosy person peeping through curtains or lurking in group chat to read drama. Nosy neighbor. | Parting jalousie louvers with binoculars [Style: sticker] | maco_peep_zoom | Optical magnifying lens distortion + iris twitch | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 20 | `horning` | Pack 2: Maco, Horn & Tabanca | HORNING — Cheating on a partner—OR betraying friends by eating doubles/liming without inviting them! | Sprouting sharp stag horns with guilty eyes [Style: 3d] | puncheon_fire_breath | Flashing red siren light + broken trust crack | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 21 | `real-tabanca` | Pack 2: Maco, Horn & Tabanca | REAL TABANCA — Deep lovesickness, heartbreak, or missing someone (or Carnival) terribly. | Slumped posture with weeping broken heart [Style: sticker] | bazodee_dazed_spiral | Dripping blue tear + pulsing cracked heart | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 22 | `wha-appen` | Pack 2: Maco, Horn & Tabanca | WHA'APPEN! — The classic warm Trinidad & Tobago greeting and fist bump. Everyday greeting. | Two hands meeting in an energetic fist bump [Style: sticker] | soca_rag_windmill | Comic impact flash + kinetic speed lines | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 23 | `bacchanal` | Pack 2: Maco, Horn & Tabanca | BACCHANAL — Total excitement, wild celebration, or chaotic drama breaking loose. Wild party or scandal. | Exploding carnival speaker with confetti [Style: 3d] | soca_rag_windmill | High-frequency bass rumble + flying glitter | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 24 | `carnival-tabanca` | Pack 2: Maco, Horn & Tabanca | CARNIVAL TABANCA — Post-Carnival depression when music stops and you return to work. Post-Mas withdrawal. | Mas costume feather drooping sadly [Style: 3d] | bazodee_dazed_spiral | Floating solitary feather + tear puddle | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 25 | `yuh-too-fas` | Pack 2: Maco, Horn & Tabanca | YUH TOO FAS'! — Telling someone they are overstepping, being too nosy, or rushing ahead. Mind your business!. | Finger wagging vigorously with scowl [Style: sticker] | tanty_akumbo_tilt | Sassy head snap + yellow warning tape | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 26 | `doh-make-joke` | Pack 2: Maco, Horn & Tabanca | DOH MAKE JOKE! — Expressing utter disbelief or warning someone not to play with you. Don't play with me!. | Piercing glare with clenched fist [Style: 3d] | steups_recoil_burst | Simmering anger sparks + ground tremble | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.91 (466x466, 23px margin) |
| 27 | `vex-pepper` | Pack 2: Maco, Horn & Tabanca | VEX LIKE PEPPER! — Steaming angry and ready to breathe fire like a Moruga Scorpion pepper. Steaming mad. | Red hot Scotch Bonnet shaking with fury [Style: 3d] | puncheon_fire_breath | Jet of steam from ears/top + flame base | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 28 | `kicksin` | Pack 2: Maco, Horn & Tabanca | KICKSIN'! — Having carefree fun, joking around, and not taking life too seriously. Carefree vibes. | Goofy bouncing sneaker or clowning grin [Style: sticker] | killing_dead_collapse | Bouncing spring coil + musical giggle notes | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 29 | `mauvais-langue` | Pack 2: Maco, Horn & Tabanca | MAUVAIS LANGUE — Spreading spicy gossip or talking about someone behind their back. Spicy gossip. | Forked tongue whispering behind hand [Style: sticker] | maco_peep_zoom | Hot pink gossip speech bubble + venom drop | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 30 | `owah` | Pack 2: Maco, Horn & Tabanca | OWAH?! — Slapped onto end of a question for bold Trini emphasis ('We liming tonight owah?!'). Or what?! | Exaggerated forward head thrust and squint [Style: sticker] | tanty_akumbo_tilt | Triple question mark vibration + eyebrow bounce | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 31 | `doubles-3d` | Pack 3: Bess Belly & Doubles Lean | DOUBLES — Trinidad's #1 street food icon: two golden bara with curried channa, chadon beni & pepper. | Golden bara wrapper opening to show channa [Style: 3d] | doubles_45_lean_drip | Aromatic steam curls + savory channa bounce | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 32 | `slight-pepper` | Pack 3: Bess Belly & Doubles Lean | SLIGHT PEPPER! — Ordering Doubles with a fiery kick of Scotch Bonnet pepper sauce. Spicy heat!. | Ladle splashing fiery red pepper sauce [Style: sticker] | puncheon_fire_breath | Sizzling chili sparks + fiery splash drop | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 33 | `doubles-lean` | Pack 3: Bess Belly & Doubles Lean | 45° DOUBLES LEAN — Mandatory 45-degree roadside forward lean so sauce doesn't drip on work clothes. | Character leaning forward at precise 45° [Style: sticker] | doubles_45_lean_drip | Viscous amber curry drip stretching down | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 34 | `bake-and-shark` | Pack 3: Bess Belly & Doubles Lean | BAKE & SHARK — Golden fried bake stuffed with shark, pineapple, tamarind, garlic, and chadon beni sauce. | Puffy golden bake stuffed with pineapple/slaw [Style: 3d] | doubles_45_lean_drip | Crispy bite crunch lines + garlic sauce drip | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 35 | `buss-up-shut` | Pack 3: Bess Belly & Doubles Lean | BUSS UP SHUT — Flaky, beaten paratha roti served with curried chicken, goat, duck, potato, and channa. | Wooden dabla clapping flaky paratha roti [Style: 3d] | allfours_table_slam | Flaky roti crumbs flying + fragrant curry steam | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 36 | `sunday-lunch` | Pack 3: Bess Belly & Doubles Lean | SUNDAY LUNCH TRINITY — Sacred Sunday plate: Macaroni Pie, Callaloo, Stew Chicken, red beans, plantain. | Sacred plate wobbling with steaming bounty [Style: 3d] | doubles_45_lean_drip | Melted cheese pull + glossy stew shimmer | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 37 | `sunday-coma` | Pack 3: Bess Belly & Doubles Lean | SUNDAY LUNCH COMA — Unavoidable 3:00 PM Sunday deep sleep after Callaloo and Macaroni Pie. | Snoring character under ceiling fan [Style: 3d] | bazodee_dazed_spiral | Floating 'Zzz' bubbles + fan blade spin | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 38 | `pelau-pot` | Pack 3: Bess Belly & Doubles Lean | PELAU & COLE SLAW — Caramelized sugar chicken and pigeon peas rice cooked in coconut milk with slaw. | Cast iron pot bubbling with wooden pot spoon [Style: 3d] | doubles_45_lean_drip | Slow aromatic steam puffs + pot lid rattle | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 39 | `corn-soup` | Pack 3: Bess Belly & Doubles Lean | 3AM CORN SOUP — Hot cup of split-pea and corn soup with dumplings right outside a fete at 3 AM. | Steaming styrofoam cup with corn cob bobbing [Style: 3d] | doubles_45_lean_drip | Floating corn cob bob + swirling split pea steam | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 40 | `pholourie` | Pack 3: Bess Belly & Doubles Lean | PHOLOURIE & TAMARIND — Fluffy spiced split-pea balls fried golden and drenched in sweet-sour tamarind sauce. | Golden dough ball dipping into tamarind chutney [Style: 3d] | doubles_45_lean_drip | Tangy brown chutney drizzle + dough bounce | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 41 | `crix-and-cheese` | Pack 3: Bess Belly & Doubles Lean | CRIX, CHEESE & SOLO — The undefeated Trini snack combo: Crix crackers, sharp cheddar cheese, and red Solo. | Round Crix biscuit snapping with sharp cheese [Style: sticker] | allfours_table_slam | Biscuit crumbs popping + soda fizz bubbles | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.93 (476x476, 18px margin) |
| 42 | `savannah-coconut` | Pack 3: Bess Belly & Doubles Lean | SAVANNAH COCONUT — Cold coconut water around Queen's Park Savannah, chopped open to scoop soft jelly. | Cutlass slicing coconut top with ice splash [Style: 3d] | allfours_table_slam | Cutlass gleam + refreshing splashing water | f0-f5 Overhead cutlass wind-up -> f6-f8 Diagonal cleave chop -> f9-f16 Water splash spray & blade specular glint -> f17-f23 Jelly revealed & blade reset | scale=0.91 (466x466, 23px margin) |
| 43 | `hang-jack` | Pack 4: Hang Jack & Stress-Free Lime | HANG JACK! — Slamming Ace or King down to capture opponent's Jack in All Fours. Total dominance. | Hand high overhead slamming card onto table [Style: 3d] | allfours_table_slam | Impact shockwave + cards flying in air | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 44 | `stress-free-liming` | Pack 4: Hang Jack & Stress-Free Lime | STRESS-FREE LIMING — Unbothered weekend relaxation with cold drinks, coconut water, and good company. | Character in beach chair sipping coconut water [Style: sticker] | tanty_akumbo_tilt | Gentle hammock swing + clinking ice cubes | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 45 | `sou-sou-drop` | Pack 4: Hang Jack & Stress-Free Lime | SOU-SOU DROP! — Glorious payday when rotating savings club ('Sou-Sou') lump sum hand finally drops! | Golden pouch dropping stacks of cash [Style: sticker] | allfours_table_slam | Flying green bills + golden coin sparkles | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 46 | `bullseye-allfours` | Pack 4: Hang Jack & Stress-Free Lime | BULLSEYE! (12-0) — Losing an All Fours match without scoring a single chalk and getting roasted. Pack up!. | Giant chalk bullseye stamping with red '0' [Style: sticker] | allfours_table_slam | Flying chalk dust puff + broken card shards | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 47 | `puncheon-fire` | Pack 4: Hang Jack & Stress-Free Lime | PUNCHEON FIRE — Taking a shot of legendary 75% ABV white rum that warms your whole soul. Dragon fire. | Rum shot glass bursting into blue flame [Style: 3d] | puncheon_fire_breath | Expanding blue ethanol flame + coughing puff | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 48 | `rum-punch` | Pack 4: Hang Jack & Stress-Free Lime | ANGOSTURA RUM PUNCH — Cold Caribbean rum punch topped with dashes of famous aromatic bitters. | Punch glass with dashed bitters swirling [Style: 3d] | doubles_45_lean_drip | Swirling red bitters + sweating condensation | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 49 | `ddi-boat` | Pack 4: Hang Jack & Stress-Free Lime | DDI (DOWN DI ISLANDS) — Taking a boat out through the Bocas del Dragón for a bay lime. Boat lime ready. | Speedboat carving through turquoise sea [Style: sticker] | soca_rag_windmill | Ocean spray foam + sun glint on water | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 50 | `river-lime` | Pack 4: Hang Jack & Stress-Free Lime | CAURA RIVER LIME — Cooking curry duck or pelau on a three-stone wood fireside beside a cool mountain river. | Pot bubbling over wood fire stones [Style: 3d] | doubles_45_lean_drip | Crackling wood fire embers + water ripples | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 51 | `bess-cutters` | Pack 4: Hang Jack & Stress-Free Lime | BESS CUTTERS — Spicy bar snacks ('cutters') seasoned with roasted geera (cumin) and pepper. Pass the toothpicks!. | Skewer of spicy geera meat sizzling [Style: 3d] | doubles_45_lean_drip | Sizzling oil splatter + aromatic geera steam | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 52 | `potcake-dog` | Pack 4: Hang Jack & Stress-Free Lime | TRINI POTHOUND — Street-smart, loyal local brown dog who knows every shortcut and shows up at every lime. | Pothound wagging tail, perking ears up [Style: 3d] | tanty_akumbo_tilt | Energetic tail wag + panting tongue bob | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 53 | `one-for-de-road` | Pack 4: Hang Jack & Stress-Free Lime | ONE FOR DE ROAD! — Saying 'I'm leaving now, just one for the road' and staying for 3 more hours. | Toasting glass tipping back with enthusiasm [Style: sticker] | soca_rag_windmill | Liquid slosh + celebratory cheers stars | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 54 | `cricket-six` | Pack 4: Hang Jack & Stress-Free Lime | OVAL BOUNDARY SIX! — Celebrating a massive cricket six into the Trini Posse Stand! West Indies pride. | Cricket bat swinging and smashing leather ball [Style: sticker] | allfours_table_slam | Blazing ball comet trail + stadium cheers | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 55 | `steelpan-3d` | Pack 5: Mas, Soca & Steelpan | STEELPAN — National musical instrument of T&T—invented in Laventille and celebrated worldwide. | Rubber-tipped mallets rolling on pan notes [Style: 3d] | steelpan_rebound | Expanding concentric acoustic rings + glint | f0-f3 Mallet arm backswing -> f4-f8 Rapid strike with triplet elastic rebound -> f9-f16 Expanding concentric acoustic ripple rings -> f17-f23 Resonant chrome vibration settle | scale=0.91 (466x466, 23px margin) |
| 56 | `carnival-mas-3d` | Pack 5: Mas, Soca & Steelpan | CARNIVAL MAS — Crossing Queen's Park Savannah stage in dazzling feathers and jewels. Savannah stage ready!. | Spectacular feather backpack swaying [Style: 3d] | soca_rag_windmill | Swaying iridescent plumage + body glitter | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.88 (450x450, 31px margin) |
| 57 | `dutty-jouvert` | Pack 5: Mas, Soca & Steelpan | DUTTY J'OUVERT! — Pre-dawn Carnival Monday celebration drenched in neon paint, mud, cocoa, and powder. | Horned reveler drenched in paint splashing [Style: sticker] | soca_rag_windmill | Wet mud/paint splatters + paint streak trails | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 58 | `wait-for-riddim` | Pack 5: Mas, Soca & Steelpan | WAIT FOR DE RIDDIM! — Holding the crew back until the Soca bassline drops and everyone loses control. | Reveler coiling low, waiting for drop [Style: sticker] | soca_rag_windmill | Vibrating ground lines + sudden bass jump | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 59 | `wave-yuh-rag` | Pack 5: Mas, Soca & Steelpan | WAVE YUH RAG! — Waving a rag, bandana, or T&T flag high in the air to a Power Soca anthem. | Microfiber rag spinning in circular vortex [Style: sticker] | soca_rag_windmill | Aerodynamic ribbon trails + confetti shower | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 60 | `moko-jumbie` | Pack 5: Mas, Soca & Steelpan | MOKO JUMBIE — Towering West African-rooted Carnival guardian spirit dancing high on wooden stilts. | Moko Jumbie stepping rhythmically on stilts [Style: 3d] | moko_jumbie_stilt_sway | Dramatic vertical sway + billowing satin cloth | f0-f6 Left stilt lift ($24\text{px}$) & sway right ($+15^\circ$) -> f7-f12 Left stilt plants firmly -> f13-f18 Right stilt lift & sway left ($-15^\circ$) -> f19-f23 Settle to center | scale=0.88 (450x450, 31px margin) |
| 61 | `midnight-robber` | Pack 5: Mas, Soca & Steelpan | MIDNIGHT ROBBER — Traditional Mas icon in fringed sombrero and cape delivering booming 'Robber Talk'. | Robber flourishing cape, pointing skull gun [Style: sticker] | steups_recoil_burst | Swirling brimstone smoke + skull gun flash | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.88 (450x450, 31px margin) |
| 62 | `dame-lorraine` | Pack 5: Mas, Soca & Steelpan | DAME LORRAINE — Satirical French plantation parody character with exaggerated padded hips, fan, and dress. | Dame Lorraine shaking voluminous hips [Style: 3d] | tanty_akumbo_tilt | Rhythmic hip bounce + fluttering hand fan | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 63 | `blue-devil` | Pack 5: Mas, Soca & Steelpan | PARAMIN BLUE DEVIL — Cobalt-blue Jab Mas from the hills of Paramin breathing fire to biscuit tins. | Blue devil lunging with pitchfork, spitting fire [Style: 3d] | puncheon_fire_breath | Erupting yellow fireball + clattering tin can | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 64 | `jab-molassie` | Pack 5: Mas, Soca & Steelpan | JAB MOLASSIE — Traditional Carnival devil painted in black molasses/grease with chains and white eyes. | Chained devil writhing in greasy black dance [Style: 3d] | soca_rag_windmill | Dripping black molasses + rattling chains | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 65 | `pierrot-grenade` | Pack 5: Mas, Soca & Steelpan | PIERROT GRENADE — Traditional Mas jester in colorful cloth strips who spells big words using Creole wordplay. | Pierrot bowing theatrically with book/whip [Style: sticker] | killing_dead_collapse | Fluttering fabric rags + alphabet letter pops | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 66 | `tassa-chutney` | Pack 5: Mas, Soca & Steelpan | TASSA & CHUTNEY — Fiery Tassa drums heated by flames and beaten with cane sticks ('chop') for celebrations. | Hosay sticks beating dholak & cutter drum [Style: 3d] | steelpan_rebound | High-speed stick blur + sonic shockwaves | f0-f3 Mallet arm backswing -> f4-f8 Rapid strike with triplet elastic rebound -> f9-f16 Expanding concentric acoustic ripple rings -> f17-f23 Resonant chrome vibration settle | scale=0.91 (466x466, 23px margin) |
| 67 | `soucouyant` | Pack 6: Soucouyant & Papa Bois | SOUCOUYANT — Witch who sheds her skin into a mortar and flies across the night sky as a ball of fire. | Blazing fireball streaking across night sky [Style: 3d] | heat_seeking_slipper_arc | Flaming comet tail + sparks crackling | f0-f3 Wrist snap launch anticipation -> f4-f11 Parabolic curving arc with 360 deg spin -> f12-f16 Bullseye impact flash & comic starburst -> f17-f23 Ballistic rebound wobble | scale=0.88 (450x450, 31px margin) |
| 68 | `salt-in-mortar` | Pack 6: Soucouyant & Papa Bois | SALT IN DE MORTAR! — Stopping a Soucouyant from putting her skin back on—catching someone's sneaky plan! | Salt shaker raining grains into mortar bowl [Style: sticker] | allfours_table_slam | Burning white sizzling sparks + screaming puff | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 69 | `la-diablesse` | Pack 6: Soucouyant & Papa Bois | LA DIABLESSE — Glamorous lady in wide-brimmed hat and petticoat hiding one cloven cow hoof on country roads. | Beautiful woman stepping, lifting gown corner [Style: 3d] | tanty_akumbo_tilt | Flashing cloven hoof + ghostly blue mist | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 70 | `mama-dlo` | Pack 6: Soucouyant & Papa Bois | MAMA DLO — Half-woman, half-giant anaconda guardian of Trinidad's rivers who combs her hair on river rocks. | Serpentine coils gliding through water ripples [Style: 3d] | soca_rag_windmill | Swirling water vortex + glistening scales | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 71 | `papa-bois` | Pack 6: Soucouyant & Papa Bois | PAPA BOIS — Half-man, half-stag protector of the forest and wildlife who blows a bull's horn to warn animals. | Ancient bearded forest father blowing cow horn [Style: 3d] | puncheon_fire_breath | Rustling forest leaves + animal call waves | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 72 | `douen` | Pack 6: Soucouyant & Papa Bois | DOUEN — Folklore child spirit in large straw hat with feet turned backward—never answer your name in bush! | Small figure walking, feet pointing backwards [Style: 3d] | tanty_akumbo_tilt | Footprints appearing reversed in mud | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 73 | `lagahoo` | Pack 6: Soucouyant & Papa Bois | LAGAHOO — Shape-shifting nocturnal creature who drags heavy iron chains down lonely country streets. | Monster lumbering with rattling iron chains [Style: 3d] | allfours_table_slam | Heavy chain dragging sparks + glowing red eyes | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 74 | `no-maljo` | Pack 6: Soucouyant & Papa Bois | NO MALJO! 🧿 — Warding off bad eye ('maljo') and jealousy with a cobalt-blue bottle or jharay blessing. | Deep blue glass bead glowing with protection [Style: sticker] | tanty_akumbo_tilt | Expanding blue protective shield pulse | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 75 | `bush-tea` | Pack 6: Soucouyant & Papa Bois | DRINK BUSH TEA! — Granny's universal herbal remedy (lemongrass, wonder-of-the-world, cerasee) for anything. | Steaming enamel mug of dark herbal brew [Style: sticker] | doubles_45_lean_drip | Spiraling healing herbal steam + floating leaf | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 76 | `silk-cotton-tree` | Pack 6: Soucouyant & Papa Bois | SILK COTTON TREE — Sacred towering tree where folklore spirits dwell—even road crews pave around it! | Ancient massive tree with buttress roots swaying [Style: 3d] | tanty_akumbo_tilt | Whispering autumn leaves + mystical aura pulse | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 77 | `parang-vibes` | Pack 7: Parang, Divali, Eid & Phagwa | PARANG VIBES — House-to-house Christmas serenading with 4-string Cuatro, maracas (chac-chac), and box bass. | Cuatro strumming rapidly with maracas shaking [Style: 3d] | steelpan_rebound | Strumming hand blur + rhythmic music notes | f0-f3 Mallet arm backswing -> f4-f8 Rapid strike with triplet elastic rebound -> f9-f16 Expanding concentric acoustic ripple rings -> f17-f23 Resonant chrome vibration settle | scale=0.91 (466x466, 23px margin) |
| 78 | `parang-season` | Pack 7: Parang, Divali, Eid & Phagwa | PARANG SEASON! — Hot pastelles paired with ice-cold spiced ruby-red sorrel. Trini Christmas pride. | Singer holding maracas, singing with joy [Style: sticker] | soca_rag_windmill | Shaking maraca blur + festive green/red stars | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 79 | `deya-parsad` | Pack 7: Parang, Divali, Eid & Phagwa | DEYA & PARSAD — Lighting glowing clay oil deyas on bamboo arches and sharing warm ghee parsad for Divali. | Clay deya lamp flickering with ghee flame [Style: 3d] | ttec_blackout_candle | Warm golden light glow expanding + ghee flicker | f0-f4 Lightbulb buzzing -> Sudden 0% blackout -> f5-f8 Matchstick strike spark & flare -> f9-f17 Warm candle aura expansion & flame sway -> f18-f23 Settle before loop cycle | scale=0.93 (476x476, 18px margin) |
| 80 | `ponche-de-creme` | Pack 7: Parang, Divali, Eid & Phagwa | PONCHE DE CRÈME — Rich, creamy Christmas punch with condensed milk, eggs, Angostura bitters, and dark rum. | Bottle pouring thick creamy golden drink [Style: 3d] | doubles_45_lean_drip | Grated nutmeg dusting + rich liquid swirl | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 81 | `trini-black-cake` | Pack 7: Parang, Divali, Eid & Phagwa | TRINI BLACK CAKE — Dense fruitcake soaked in rum and cherry brandy for months—one slice puts you to sleep. | Dense dark cake slice with rum glaze [Style: 3d] | doubles_45_lean_drip | Glistening dark rum drizzle + sugar holly | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 82 | `divali-sweet-bag` | Pack 7: Parang, Divali, Eid & Phagwa | WHERE MEH SWEET BAG? — Beloved tradition of receiving a bag of Divali sweets and parsad from friends. | Brown paper bag bursting with kurma & barfi [Style: sticker] | allfours_table_slam | Sweet powdered sugar puff + popping kurma | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 83 | `eid-sawine` | Pack 7: Parang, Divali, Eid & Phagwa | SEND MEH SAWINE! — Spiced sweet milk and toasted vermicelli dessert with almonds and raisins for Eid. | Spoon lifting silky sweet sawine with almonds [Style: 3d] | doubles_45_lean_drip | Cardamom steam curls + floating almond slice | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 84 | `phagwa-holi` | Pack 7: Parang, Divali, Eid & Phagwa | HOLI HAI! (PHAGWA) — Spring festival of colors spraying pink abeer liquid from pichkaree and throwing powder. | Water gun (pichkari) spraying vibrant dye [Style: sticker] | soca_rag_windmill | Exploding magenta and cyan powder clouds | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 85 | `chowtal-jhaal` | Pack 7: Parang, Divali, Eid & Phagwa | CHOWTAL & JHAAL — Fast-paced traditional folk singing with dholak drums and ringing brass jhaal cymbals. | Brass cymbals (jhaal) clashing together [Style: 3d] | allfours_table_slam | Golden cymbal clash spark + sonic chime wave | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 86 | `christmas-curtains` | Pack 7: Parang, Divali, Eid & Phagwa | CHRISTMAS CURTAINS! — Mandatory Dec 24th marathon of scrubbing walls and hanging brand new curtains. | Frilly lace curtains hanging and fluttering [Style: sticker] | tanty_akumbo_tilt | Fluttering lace hem + sparkling clean sparkles | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 87 | `emancipation-pride` | Pack 7: Parang, Divali, Eid & Phagwa | EMANCIPATION PRIDE — Celebrating African Emancipation Day in royal Dashiki attire with African drumming. | African djembe drum beating with royal kente [Style: 3d] | steelpan_rebound | Deep bass pulse rings + vibrant kente flutter | f0-f3 Mallet arm backswing -> f4-f8 Rapid strike with triplet elastic rebound -> f9-f16 Expanding concentric acoustic ripple rings -> f17-f23 Resonant chrome vibration settle | scale=0.91 (466x466, 23px margin) |
| 88 | `every-creed-and-race` | Pack 7: Parang, Divali, Eid & Phagwa | EVERY CREED & RACE — 'Here every creed and race find an equal place.' National anthem unity. | Interlocking hands forming national red heart [Style: sticker] | soca_rag_windmill | Glowing rainbow/national flag halo pulse | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 89 | `crab-and-dumpling` | Pack 8: Bago Vibes & Everyday T&T | CRAB & DUMPLING — Tobago's signature dish: curried blue crab over dense flour dumplings at Store Bay. | Whole curried blue crab holding flat dumpling [Style: 3d] | doubles_45_lean_drip | Thick curry gravy bubbling + claw snap | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 90 | `maxi-taxi` | Pack 8: Bago Vibes & Everyday T&T | MAXI TAXI — Color-banded commuter Maxi Taxi booming bass along the Priority Bus Route. | Red-band maxi taxi bouncing over a pothole [Style: sticker] | soca_rag_windmill | Exhaust pipe puff + bumper bounce squash | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.88 (450x450, 31px margin) |
| 91 | `buccoo-goat-race` | Pack 8: Bago Vibes & Everyday T&T | BUCCOO GOAT RACE! — Tobago's Easter tradition where barefoot jockeys sprint behind racing goats. | Determined goat galloping with jockey running [Style: sticker] | heat_seeking_slipper_arc | Kicking up dirt clouds + goat bell jingling | f0-f3 Wrist snap launch anticipation -> f4-f11 Parabolic curving arc with 360 deg spin -> f12-f16 Bullseye impact flash & comic starburst -> f17-f23 Ballistic rebound wobble | scale=0.88 (450x450, 31px margin) |
| 92 | `nylon-pool` | Pack 8: Bago Vibes & Everyday T&T | NYLON POOL VIBES — Crystal-clear waist-deep coral sandbar in middle of the ocean off Tobago. Pure paradise. | Crystal clear water rippling over white sand [Style: 3d] | soca_rag_windmill | Shimmering caustic water lines + seafoam | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 93 | `pure-bago-vibes` | Pack 8: Bago Vibes & Everyday T&T | PURE BAGO VIBES — Tobago's unhurried, peaceful island rhythm where stress disappears crossing the water. | Palm tree leaning over turquoise beach [Style: sticker] | tanty_akumbo_tilt | Coconut swaying + gentle tropical breeze wave | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 94 | `highway-traffic` | Pack 8: Bago Vibes & Everyday T&T | HIGHWAY GRIDLOCK! — Stuck bumper-to-bumper on Uriah Butler Highway or Port of Spain flash flooding. | Line of cars bumper-to-bumper inching forward [Style: sticker] | doubles_45_lean_drip | Blinking brake lights + frustrated car horn puff | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.88 (450x450, 31px margin) |
| 95 | `trini-mom-spoon` | Pack 8: Bago Vibes & Everyday T&T | TAKE OUT DE CHICKEN?! — Pure panic when mother's car pulls into yard and chicken is still rock-solid in freezer. | Thawing block of rock-hard frozen chicken [Style: sticker] | allfours_table_slam | Ticking panic clock + cold ice vapor smoke | f0-f4 Ticking panic clock hand spin -> f5-f9 Rock-hard chicken counter slam -> f10-f17 Cold vapor smoke & trembling sweat drops -> f18-f23 Head-clutch panic loop | scale=0.91 (466x466, 23px margin) |
| 96 | `flying-slipper` | Pack 8: Bago Vibes & Everyday T&T | HEAT-SEEKING SLIPPER — Trini mother's rubber slipper that curves around corners with 100% accuracy. | Rubber flip-flop spinning through air [Style: 3d] | heat_seeking_slipper_arc | Curving motion trail + comic bullseye impact | f0-f3 Wrist snap launch anticipation -> f4-f11 Parabolic curving arc with 360 deg spin -> f12-f16 Bullseye impact flash & comic starburst -> f17-f23 Slipper rebound wobble | scale=0.88 (450x450, 31px margin) |
| 97 | `wasa-water-gone` | Pack 8: Bago Vibes & Everyday T&T | WASA WATER GONE! — When you have shampoo in your hair and the shower coughs twice and goes bone dry. | Dry water tap spitting a single pitiful drop [Style: sticker] | wasa_dry_shower_cough | Solitary water droplet drip + dust cloud puff | f0-f4 Dry tap pipe cough tremor -> f5-f8 Pitiful solitary water drop falls -> f9-f16 Hollow dust puff & dry pipe shudder -> f17-f23 Sputter reset to silence | scale=0.91 (466x466, 23px margin) |
| 98 | `ttec-current-gone` | Pack 8: Bago Vibes & Everyday T&T | CURRENT GONE! (BLACKS) — Waking up sweating at 2 AM because power went and fan stopped spinning. | Lightbulb turning off, single match striking [Style: sticker] | ttec_blackout_candle | Sudden pitch black screen + warm candle flame | f0-f4 Lightbulb buzzing -> Sudden 0% blackout -> f5-f8 Matchstick strike spark & flare -> f9-f17 Warm candle aura expansion & flame sway -> f18-f23 Settle before loop cycle | scale=0.91 (466x466, 23px margin) |
| 99 | `scarlet-ibis-cocrico` | Pack 8: Bago Vibes & Everyday T&T | IBIS & COCRICO — Brilliant red Scarlet Ibis of Trinidad and Cocrico of Tobago—national birds on Coat of Arms. | Scarlet Ibis and Cocrico flapping wings [Style: 3d] | soca_rag_windmill | Crimson and brown feather flutter + sunbeam | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 100 | `sweet-tt-heart` | Pack 8: Bago Vibes & Everyday T&T | SWEET ISLAND HEART — Pure love and pride for Trinidad & Tobago in iconic Red, White, and Black colors. | Glowing red/black/white national flag heart [Style: 3d] | soca_rag_windmill | Rhythmic heartbeat thumping + radiant sparkle | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |

### 5.3 Complete 188-Sticker Mapping Matrix Table (Part 2: Wordless 3D Slang Stickers 101–188)

| # | Sticker ID | Pack/Category | Cultural Meaning & Context | Visual Metaphor & 3D Elements | Primary Authentic Motion Primitive | Secondary Graphic FX | Keyframe Timing (24f @ 90ms) | Framing Bounds / Breathing Room |
|---|---|---|---|---|---|---|---|---|
| 101 | `slang-wha-yuh-say` | Slang: Greetings & Links | Wha yuh say? — someone speaking but listener hears nothing. Muted audio reaction. | Hand cupped to ear with muted soundwaves [Style: 3d] | tanty_akumbo_tilt | Expanding blue acoustic wave ripples | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 102 | `slang-wha-go-on` | Slang: Greetings & Links | Wha go on? — how are you doing. Energetic Caribbean check-in. | Two fists bumping together [Style: 3d] | soca_rag_windmill | Comic spark burst at contact point | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.93 (476x476, 18px margin) |
| 103 | `slang-doh-study-dat` | Slang: Co-Signs & Facts | Doh study dat — something bad happening but I have a solution. Unbothered calm. | Character under golden umbrella in rain [Style: 3d] | tanty_akumbo_tilt | Raindrops bouncing off umbrella dome | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 104 | `slang-leh-we-go` | Slang: Greetings & Links | Leh we go . — follow me / let's head to the lime. Moving out. | Running sneaker with angel wings fluttering [Style: 3d] | soca_rag_windmill | Speed dust cloud + fluttering wings | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 105 | `slang-ah-coming` | Slang: Greetings & Links | Ah coming — I will be there but running slightly late. Classic Trini time. | Running person with clock and coffee [Style: 3d] | heat_seeking_slipper_arc | Spinning clock hands + coffee sloshing | f0-f3 Wrist snap launch anticipation -> f4-f11 Parabolic curving arc with 360 deg spin -> f12-f16 Bullseye impact flash & comic starburst -> f17-f23 Ballistic rebound wobble | scale=0.88 (450x450, 31px margin) |
| 106 | `slang-ah-reach` | Slang: Greetings & Links | Ah reach — I have arrived at the destination. Touchdown. | Location pin landing with a bounce [Style: 3d] | allfours_table_slam | Circular ground ripple + triumphant star | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 107 | `slang-ah-gone` | Slang: Greetings & Links | Ah gone — I am leaving / dipping out of the fete. Vanishing act. | Peace sign hand with puff of smoke [Style: 3d] | puncheon_fire_breath | Poof smoke cloud expanding + fading sparkle | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 108 | `slang-ent` | Slang: Co-Signs & Facts | Ent? — look for affirmation from a friend ('Right?!'). Sacred validation. | Hand over golden heart in affirmation [Style: 3d] | tanty_akumbo_tilt | Pulsing golden heart glow + snappy nod | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 109 | `slang-right-dey` | Slang: Greetings & Links | Right dey — someone is very close / right around corner. Pinpoint accuracy. | Target crosshair locking onto position [Style: 3d] | tanty_akumbo_tilt | Crosshair pulse + lock-on beep lines | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 110 | `slang-just-now` | Slang: Greetings & Links | Just now — wait a couple of seconds (or minutes/hours!). Elastic time. | Hourglass with sand trickling slowly [Style: 3d] | doubles_45_lean_drip | Trickling golden sand + floating question marks | f0-f5 Top bulb full of golden sand -> f6-f14 Rapid sand stream pours through neck -> f15-f19 Bottom bulb rising pile & glass sparkle -> f20-f23 Glass tilt & loop reset | scale=0.91 (466x466, 23px margin) |
| 111 | `slang-small-ting` | Slang: Co-Signs & Facts | Small ting — no problem at all / don't sweat it. Carefree reassurance. | Tiny pebble held lightly in fingers [Style: 3d] | tanty_akumbo_tilt | Gentle finger flick + nonchalant sparkle | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.93 (476x476, 18px margin) |
| 112 | `slang-no-scene` | Slang: Co-Signs & Facts | No scene. — yes / absolutely fine / zero worries. Certified approval. | Emerald-green 3D checkmark badge [Style: 3d] | soca_rag_windmill | Green badge sparkle + gentle bounce | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.93 (476x476, 18px margin) |
| 113 | `slang-all-ah-dat` | Slang: Co-Signs & Facts | All ah dat. — plenty stuff to do / everything included. Overwhelming haul. | Towering stack of colourful parcels [Style: 3d] | allfours_table_slam | Wobbling parcels balance + star sparkles | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.88 (450x450, 31px margin) |
| 114 | `slang-yuh-good` | Slang: Greetings & Links | Yuh good? — is everything ok with you? Checking on friends. | Warm thumbs-up beside a golden heart [Style: 3d] | tanty_akumbo_tilt | Pulsing golden heart glow + thumbs-up pop | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 115 | `slang-how-yuh-mean` | Slang: Disbelief & Comedy | How yuh mean? — explain yourself / obviously!. Incredulous confirmation. | Tilted 3D question mark with raised eyebrow [Style: 3d] | tanty_akumbo_tilt | Rhythmic double nod + confirmation checkmark | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 116 | `slang-doh-start` | Slang: Attitude & Shade | Doh start — keep quiet / don't even begin that topic. Preemptive shutdown. | 3D lips zipped shut with golden zipper [Style: 3d] | steups_recoil_burst | Metal zipper sliding + key sparkling away | f0-f4 Pursed lips pre-silence tremble -> f5-f9 Golden zipper pulls across mouth -> f10-f16 Padlock snaps shut with corner gleam -> f17-f23 Defiant locked-mouth hold | scale=0.93 (476x476, 18px margin) |
| 117 | `slang-watch-nah` | Slang: Disbelief & Comedy | Watch nah — take notice / look at this madness. Demanding visual attention. | Wide 3D cartoon side-eyes with sparkle [Style: 3d] | maco_peep_zoom | Eyebrow raise + downward sightline glint | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 118 | `slang-hear-nah` | Slang: Disbelief & Comedy | Hear nah — stop talking and listen to me closely. Urgent gossip preamble. | Hand cupping attentive ear with soundwaves [Style: 3d] | tanty_akumbo_tilt | Whispering wave trail + attention sparkle | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 119 | `slang-for-true` | Slang: Co-Signs & Facts | For true? — I am not lying / speak the absolute truth. Swearing on it. | Open palm raised over glowing golden heart [Style: 3d] | allfours_table_slam | Golden heart aura pulse + sincere nod | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 120 | `slang-real-talk` | Slang: Co-Signs & Facts | Real talk — absolute facts / no debate needed. Mic drop authority. | Golden studio microphone drop [Style: 3d] | allfours_table_slam | Mic drop shockwave + reverb sound rings | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 121 | `slang-bet` | Slang: Co-Signs & Facts | Bet. — agreed / deal sealed / say less. Shaking on it. | Two hands locked in a firm handshake [Style: 3d] | allfours_table_slam | Handshake grip spark + coin flip spin | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.93 (476x476, 18px margin) |
| 122 | `slang-yuh-mad` | Slang: Attitude & Shade | Yuh mad? — are you completely out of your mind?! Shocked reaction. | Red 3D thermometer bursting with fire [Style: 3d] | bazodee_dazed_spiral | Mercury shooting out top + fiery sparks | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 123 | `slang-yuh-jokin` | Slang: Disbelief & Comedy | Yuh jokin' — what you are saying is unreal / absurd comedy. | Colourful 3D jester hat with golden bells [Style: 3d] | killing_dead_collapse | Jingling bells bounce + flying question mark | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 124 | `slang-doh-play` | Slang: Disbelief & Comedy | Doh play — stop acting childish / make sense. Serious warning. | Yellow 3D caution warning triangle [Style: 3d] | allfours_table_slam | Flashing warning blink + firm slam | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 125 | `slang-lemme-see` | Slang: Disbelief & Comedy | Lemme see — examine the receipts closely. Deep forensic scrutiny. | Golden magnifying glass with turquoise lens [Style: 3d] | maco_peep_zoom | Optical text enlargement + inquisitive twitch | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 126 | `slang-nah-man` | Slang: Disbelief & Comedy | Nah man! — you are definitely not speaking the truth. Firm denial. | Arms crossed in a bold X over a red X [Style: 3d] | steups_recoil_burst | Rapid horizontal blur + waving dismissive hands | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.91 (466x466, 23px margin) |
| 127 | `slang-boy-please` | Slang: Disbelief & Comedy | Boy, please! — immediately stop your action / dismissive palm. | Raised talk-to-the-hand stop palm [Style: 3d] | tanty_akumbo_tilt | Sassy cut-eye flick + palm pushing away | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 128 | `slang-steups` | Slang: Attitude & Shade | Steups — acoustic teeth-sucking disapproval and dismissive disgust. | Unimpressed disapproval expression [Style: 3d] | steups_recoil_burst | Puffed cheek release + dismissive air puff | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.93 (476x476, 18px margin) |
| 129 | `slang-tanty` | Slang: People & Drama | Tanty! — matriarchal elder aunt / village moral arbiter. Authority. | Tanty with hands on waist, glasses perched [Style: 3d] | tanty_akumbo_tilt | Glasses sliding down nose + firm head nod | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 130 | `slang-gyal` | Slang: People & Drama | Gyal! — spirited Caribbean woman / friend / queen. Empowered energy. | Crowned Caribbean woman with star earrings [Style: 3d] | soca_rag_windmill | Shimmering diamond facets + sassy bounce | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 131 | `slang-boi` | Slang: People & Drama | Boi! — young Caribbean man expressing sudden astonished disbelief. | Expressive young Caribbean man with fade [Style: 3d] | tanty_akumbo_tilt | Eyebrow lift overshoot + astonished gaze | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 132 | `slang-yuh-too-lie` | Slang: Disbelief & Comedy | Yuh too lie! — caught completely red-handed in an overt fib. Cap! | 3D face with long wooden Pinocchio nose [Style: 3d] | steups_recoil_burst | Rapid nose extension shoot + leafy twig pop | f0-f4 Shifty guilty side-eye darting -> f5-f9 Wooden nose 45px extension -> f10-f16 Leafy twigs sprout with comic pop bubbles -> f17-f23 Sheepish blink & retraction | scale=0.91 (466x466, 23px margin) |
| 133 | `slang-doh-kill-meh` | Slang: Disbelief & Comedy | Doh kill meh — unrealistic, hilarious story causing laughing tears. | Laughing 3D face crying rivers of tears [Style: 3d] | killing_dead_collapse | Rhythmic laughter torso bounce + tears | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 134 | `slang-ah-done` | Slang: Attitude & Shade | Ah done — completely finished talking / dusting hands off. Exit. | Two hands dusting each other off [Style: 3d] | steups_recoil_burst | Hand clapping dust cloud + turning away | f0-f3 Pursed lips & jaw pull-back -> f4-f7 Snappy 18 deg backward neck recoil -> f8-f16 Directional acoustic shockwave & air puff -> f17-f23 Settle to neutral | scale=0.91 (466x466, 23px margin) |
| 135 | `slang-is-a-jokes` | Slang: Disbelief & Comedy | Is a jokes — totally unfactual, comedic claim. Pure banter. | Colourful Carnival jester comedy mask [Style: 3d] | killing_dead_collapse | Sputtering laugh wobble + comic squeak | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 136 | `slang-mad-ting` | Slang: Disbelief & Comedy | Mad ting — unreal, mind-blowing news exploding in chat. Wild chaos. | Mind-blown head erupting with fireworks [Style: 3d] | puncheon_fire_breath | Exploding multicolored fireworks + smoke | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 137 | `slang-wicked` | Slang: People & Drama | Wicked! — mischievously evil person stirring up spicy trouble. | Purple 3D smiling devil face with horns [Style: 3d] | puncheon_fire_breath | Flaming golden horn tips + mischievous wink | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 138 | `slang-high-beam` | Slang: People & Drama | high beam — peak excitement / blinding radiance in the room. | Two blazing car high-beam headlights [Style: 3d] | maco_peep_zoom | Intense white beam cone glare + lens flares | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 139 | `slang-a-week` | Slang: Disbelief & Comedy | a week — a situation so funny it takes a whole week to process. | Yellow laughing face melting into a puddle [Style: 3d] | soca_rag_windmill | Melting liquid ripple + laughter notes | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 140 | `slang-too-much` | Slang: Attitude & Shade | Too much — extreme oversharing / TMI / clamp ears shut. | Two hands clamping firmly over both ears [Style: 3d] | doubles_45_lean_drip | Soundwave rejection barrier + head shake | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 141 | `slang-dohh-bother` | Slang: Attitude & Shade | Dohh bother — nevermind / not worth my breath or energy. | Hand doing a dismissive wave-off [Style: 3d] | tanty_akumbo_tilt | Casual shrug drop + dismissive sigh puff | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 142 | `slang-mash-up` | Slang: Vibes, Belly & Money | Mash up — totally destroy something / shatter expectations. | Wooden mallet smashing a rock into shards [Style: 3d] | allfours_table_slam | Flying rock shards + ground impact crater | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.88 (450x450, 31px margin) |
| 143 | `slang-real-bad` | Slang: Vibes, Belly & Money | Real bad — serious, critical problems brewing. Code red. | Flashing red 3D emergency siren light [Style: 3d] | puncheon_fire_breath | Rotating dual-color siren beams + alarm rings | f0-f4 Red/blue lamp dual-beam rotation start -> f5-f12 360 deg Flashing warning sweep -> f13-f18 Concentric alarm sound rings -> f19-f23 Emergency rotation settle | scale=0.91 (466x466, 23px margin) |
| 144 | `slang-ah-screaming` | Slang: Disbelief & Comedy | Ah screaming! — screaming with pure laughter and joy. Peak fete. | Colourful megaphone blasting party confetti [Style: 3d] | killing_dead_collapse | Vibrating megaphone cone + outward blast rings | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.88 (450x450, 31px margin) |
| 145 | `slang-doh-watch-me` | Slang: Attitude & Shade | Doh watch me — pay no attention to what I am doing / look away. | Dark sunglasses with hand blocking view [Style: 3d] | tanty_akumbo_tilt | Reflective glare flash + turning away | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.93 (476x476, 18px margin) |
| 146 | `slang-mind-yuh-business` | Slang: Attitude & Shade | Mind yuh business — focus on yourself and stay out of mine. | Sipping coconut water inside golden bubble [Style: 3d] | allfours_table_slam | Golden bubble shield shimmer + straw sip | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 147 | `slang-stay-in-yuh-lane` | Slang: Attitude & Shade | Stay in yuh lane — don't speak about matters you don't understand. | Driving strictly inside painted road lanes [Style: 3d] | allfours_table_slam | Solid neon lane lines + car wheel bounce | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 148 | `slang-yuh-too-bold` | Slang: Attitude & Shade | Yuh too bold — making brazen statements without the facts. Penalty. | Hand holding up crimson penalty Red Card [Style: 3d] | tanty_akumbo_tilt | Dramatic red card thrust + whistle sound rings | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 149 | `slang-yuh-real-brave` | Slang: People & Drama | Yuh real brave — fearless confidence / stepping into the fray. | Majestic golden-maned lion wearing medal [Style: 3d] | puncheon_fire_breath | Expanding roar soundwaves + golden mane shake | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 150 | `slang-badmind` | Slang: Attitude & Shade | Badmind — bitter envy and resentment toward someone who won. | Jealous green side-eye next to trophy [Style: 3d] | maco_peep_zoom | Slit pupil constriction + poisonous green fume | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.88 (450x450, 31px margin) |
| 151 | `slang-vex` | Slang: Attitude & Shade | Vex — genuinely boiling mad / ready to erupt like hot pepper. | Fiery red Scotch Bonnet blowing steam [Style: 3d] | puncheon_fire_breath | Throbbing red pulse + pressurized steam jets | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 152 | `slang-dont-hot-up-yuh-head` | Slang: Co-Signs & Facts | dont Hot up yuh head — chill out / don't let stress overheat you. | Glowing turquoise melting 3D ice cube [Style: 3d] | doubles_45_lean_drip | Cooling water vapor + soothing blue wave | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.93 (476x476, 18px margin) |
| 153 | `slang-take-a-set` | Slang: Attitude & Shade | Take a set — sit down, pay attention, and prepare to listen. | Striped folding veranda beach chair [Style: 3d] | allfours_table_slam | Spring-loaded chair unfolding + sand puff | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 154 | `slang-doh-get-on-so` | Slang: Attitude & Shade | Doh get on so — behave yourself / stop acting wildly inappropriate. | Hand wagging index finger sternly [Style: 3d] | doubles_45_lean_drip | Stern finger wag blur + scolding brow | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 155 | `slang-yuh-feeling-yuhself` | Slang: People & Drama | Yuh feeling yuhself — acting haughty, proud, or narcissistic. Vanity. | Hand holding ornate golden mirror with sparkles [Style: 3d] | soca_rag_windmill | Mirror specular shine + vanity sparkles | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 156 | `slang-big-up-yuhself` | Slang: Co-Signs & Facts | Big up yuhself — take a well-deserved bow / salute your achievement. | Jewel-encrusted golden royal crown [Style: 3d] | soca_rag_windmill | Bursting confetti fountain + trophy gleam | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 157 | `slang-respect` | Slang: Co-Signs & Facts | Respect — honorable salute to a friend or milestone. Pure integrity. | Two-finger forehead salute with golden star [Style: 3d] | allfours_table_slam | Heartfelt salute snap + golden halo | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 158 | `slang-liming` | Slang: Greetings & Links | Liming — gathering with friends to drink, talk, and relax. Essential culture. | Group of coconut drinks with straws [Style: 3d] | tanty_akumbo_tilt | Clinking straws + floating lime wedge | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 159 | `slang-doh-be-a-dotish` | Slang: Attitude & Shade | Doh be a dotish — don't act like a silly, foolish person. Rebuking folly. | Dizzy cartoon face with spiral eyes & stars [Style: 3d] | allfours_table_slam | Orbiting yellow stars + spinning spiral eyes | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 160 | `slang-dotishness` | Slang: Attitude & Shade | Dotishness — pure stupidity or absurd antics triggering a facepalm. | Expressive character doing a facepalm [Style: 3d] | allfours_table_slam | Slap impact starburst + wobbling cranium | f0-f4 Hand raises in sheer disbelief -> f5-f8 Solid forehead slap impact -> f9-f16 Comic starburst flash & cranium wobble -> f17-f23 Drag down face & sigh settle | scale=0.91 (466x466, 23px margin) |
| 161 | `slang-fass` | Slang: People & Drama | Fass — meddling in other people's affairs and peeking into secrets. | Brass-and-gold extending spyglass telescope [Style: 3d] | maco_peep_zoom | Telescopic brass extension click + lens glint | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 162 | `slang-maco` | Slang: People & Drama | Maco — watching neighborhood affairs in full 4K definition. | Peeking through curtains with binoculars [Style: 3d] | maco_peep_zoom | Binocular sweep + targeting reticle focus | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 163 | `slang-tabanca` | Slang: People & Drama | Tabanca — agonizing heartbreak and melancholy over a lost love. | Glossy 3D broken heart with blue tear drop [Style: 3d] | bazodee_dazed_spiral | Dripping blue tear + pulsing cracked heart | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 164 | `slang-horn` | Slang: People & Drama | Horn — infidelity and betrayal triggering guilt and comedic panic. | Pair of glossy golden-red bull horns [Style: 3d] | puncheon_fire_breath | Red warning alarm flash + shivering horns | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.91 (466x466, 23px margin) |
| 165 | `slang-wha-yuh-on` | Slang: Attitude & Shade | Wha yuh on? — what nonsense are you on right now?! Skeptical query. | Squinting face with raised brow & flashlight [Style: 3d] | tanty_akumbo_tilt | Flashlight search beam + skeptical squint | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 166 | `slang-yuh-outside` | Slang: Greetings & Links | Yuh outside? — asking if the crew is already at the party venue. | Open nightclub door with neon strobe [Style: 3d] | soca_rag_windmill | Flashing neon strobes + pumping bass waves | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 167 | `slang-link-me` | Slang: Greetings & Links | Link me — call me / message me / get in touch directly. Urgent link. | Ringing smartphone vibrating violently [Style: 3d] | steelpan_rebound | High-frequency phone vibration lines | f0-f4 Incoming call notification pop -> f5-f12 40Hz Lateral phone vibration -> f13-f18 Expanding golden ring chime waves -> f19-f23 Vibrate settle & re-trigger | scale=0.91 (466x466, 23px margin) |
| 168 | `slang-link-up` | Slang: Greetings & Links | Link up — meeting up with friends to initiate the lime. Snap together. | Interlocking chain links snapping together [Style: 3d] | allfours_table_slam | Metallic snap spark + locking click lines | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 169 | `slang-vibes` | Slang: Vibes, Belly & Money | Vibes — experiencing peak musical and emotional harmony together. | Vibrant 3D boombox with neon music notes [Style: 3d] | steelpan_rebound | Pumping speaker cones + pulsing music notes | f0-f3 Mallet arm backswing -> f4-f8 Rapid strike with triplet elastic rebound -> f9-f16 Expanding concentric acoustic ripple rings -> f17-f23 Resonant chrome vibration settle | scale=0.91 (466x466, 23px margin) |
| 170 | `slang-good-vibes-only` | Slang: Vibes, Belly & Money | Good vibes only — no hate, shade, or negative energy permitted here. | Smiling golden sun wearing cool sunglasses [Style: 3d] | tanty_akumbo_tilt | Rotating warm sun rays + radiant sparkle | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 171 | `slang-the-vibe-different` | Slang: Vibes, Belly & Money | The vibe different — sensing a strange or frosty shift in energy. | Thermometer gauge needle in icy blue zone [Style: 3d] | doubles_45_lean_drip | Shivering frost particles + needle wobble | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 172 | `slang-no-cap` | Slang: Co-Signs & Facts | No cap — 100% genuine truth / no exaggeration whatsoever. Verified. | Blue baseball cap with red prohibition slash [Style: 3d] | allfours_table_slam | Clean slash spark + green verified badge | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 173 | `slang-cap` | Slang: Disbelief & Comedy | Cap — pure fiction, boasting, or exaggerated untruth. Rejected. | Single vibrant electric-blue baseball cap [Style: 3d] | allfours_table_slam | Cap dropping over eyes + buzzer 'X' | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 174 | `slang-lowkey` | Slang: Vibes, Belly & Money | Lowkey — making a quiet move without drawing public attention. Stealth. | Sneaky hoodie character tip-toeing past spotlight [Style: 3d] | maco_peep_zoom | Sneaky tip-toe bob + dimming ambient light | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 175 | `slang-highkey` | Slang: Vibes, Belly & Money | Highkey — deliberately loud, proud, and broadcasting to the world. | Two golden stage spotlights crossing beams [Style: 3d] | puncheon_fire_breath | Crossing sweeping searchlights + beam glare | f0-f4 Chest expansion (120% scale) -> f5-f10 Explosive flamethrower cone blast -> f11-f17 Smoky coughing recoil & ember dissipation -> f18-f23 Smoke rings & chest deflate | scale=0.88 (450x450, 31px margin) |
| 176 | `slang-im-weak` | Slang: Disbelief & Comedy | I'm weak — laughing so hysterically that physical strength dissolves. | Laughing face melting into rainbow puddle [Style: 3d] | killing_dead_collapse | Wobbly jelly collapse + soft comic plop | f0-f4 Chest heave & laughter intake -> f5-f10 Violent torso recoil & explosive knee slap -> f11-f17 Horizontal tear spray arcs & laugh waves -> f18-f23 Wobbly chuckle bounce | scale=0.91 (466x466, 23px margin) |
| 177 | `slang-im-dead` | Slang: Vibes, Belly & Money | I'm dead — soon to suffer catastrophic trouble or comedic demise. | Expressive 3D cartoon skull with lightning [Style: 3d] | bazodee_dazed_spiral | Wobbling skull chatter + electric spark arc | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 178 | `slang-ate` | Slang: Vibes, Belly & Money | Ate — belly full and thoroughly satisfied after a feast. Contentment. | Happy 3D character rubbing a full round belly [Style: 3d] | allfours_table_slam | Circular belly rub motion + content smile | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 179 | `slang-ate-and-left-no-crumbs` | Slang: Vibes, Belly & Money | Ate and left no crumbs — flawless performance; plate cleared completely. | Sparkling-clean plate with golden fork & knife [Style: 3d] | allfours_table_slam | Sparkling halo shimmer + twirling golden fork | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.91 (466x466, 23px margin) |
| 180 | `slang-its-not-giving` | Slang: Vibes, Belly & Money | It's not giving — failing to deliver the expected energy or quality. | Bold 3D hand giving a giant thumbs-down [Style: 3d] | doubles_45_lean_drip | Drooping thumb + wilted flower petal drop | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.93 (476x476, 18px margin) |
| 181 | `slang-be-so-for-real` | Slang: Vibes, Belly & Money | Be so for real — stop fronting and come back to reality. Deadpan. | Flat deadpan unimpressed 3D face [Style: 3d] | allfours_table_slam | Deadpan stare + dry blinking eyelids | f0-f5 High overhead suspense hold -> f6-f8 Terminal velocity downward slam -> f9-f16 Impact shake (12px) & chalk dust burst -> f17-f23 Resonant table shudder settle | scale=0.93 (476x476, 18px margin) |
| 182 | `slang-delulu` | Slang: Vibes, Belly & Money | Delulu — living in a romantic or fantastical delusion. Floating. | Floating on pink clouds with heart glasses [Style: 3d] | bazodee_dazed_spiral | Floating cloud bob + sparkling rainbow arch | f0-f6 Torso slump into orbital sway -> f7-f13 Spiral counter-clockwise eye spin -> f14-f18 Orbiting yellow stars & floating hearts -> f19-f23 Elastic bob recovery | scale=0.91 (466x466, 23px margin) |
| 183 | `slang-rizz` | Slang: Vibes, Belly & Money | Rizz — effortless romantic charm and charismatic banter. Magnetic wink. | Smooth winking 3D face lowering sunglasses [Style: 3d] | tanty_akumbo_tilt | Magnetic charm spark lines + cool wink glint | f0-f4 Hip shift to akumbo stance -> f5-f10 Snappy 20 deg head tilt & cut-eye flick -> f11-f18 Stern finger wag & starburst pop -> f19-f23 Counter-sway settle to center | scale=0.91 (466x466, 23px margin) |
| 184 | `slang-red-flag` | Slang: Vibes, Belly & Money | Red flag — warning of toxic, suspicious, or dangerous behavior. Alert. | Single vibrant crimson flag on golden pole [Style: 3d] | soca_rag_windmill | Sharp fabric ripple snaps + alarm flashes | f0-f4 Anticipation crouch -> f5-f12 360 deg Circular windmill sweep (2f cloth lag) -> f13-f18 Snap-whip reversal & confetti pop -> f19-f23 Settle to f0 | scale=0.91 (466x466, 23px margin) |
| 185 | `slang-soft-launch` | Slang: Greetings & Links | Soft launch — discreetly teasing a new relationship or lime. Peek. | Curtain parting slightly with a peek [Style: 3d] | maco_peep_zoom | Subtle curtain flutter + discreet wink glint | f0-f5 Stealthy shutter slide-in -> f6-f11 Forward pop & 1.35x optical binocular zoom -> f12-f17 Double-take pupil scan & speed lines -> f18-f23 Fast snap-back concealment | scale=0.91 (466x466, 23px margin) |
| 186 | `slang-hard-lucks-dey` | Slang: Vibes, Belly & Money | Hard lucks Dey — everything finished right before your turn. Empty pot. | Single open, completely empty black iron pot [Style: 3d] | doubles_45_lean_drip | Sad empty pot resonance + floating fly | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 187 | `slang-left-on-read` | Slang: Vibes, Belly & Money | Left on read — ignored message or completely empty pockets. Solitary moth. | Pockets inside-out with moth & cobweb [Style: 3d] | doubles_45_lean_drip | Fluttering moth loop + floating dust cobweb | f0-f5 Forward 45 deg cantilever lean -> f6-f12 Micro-chew bob & viscous drip stretch -> f13-f17 Drip splash & aromatic steam curl -> f18-f23 Elastic upward settle & loop | scale=0.91 (466x466, 23px margin) |
| 188 | `slang-the-eagle-has-landed` | Slang: Vibes, Belly & Money | the eagle has landed — payday arrived / cash transferred successfully. | Eagle swooping down clutching stack of cash [Style: 3d] | heat_seeking_slipper_arc | Flapping wing thrust + falling cash bills | f0-f3 Wrist snap launch anticipation -> f4-f11 Parabolic curving arc with 360 deg spin -> f12-f16 Bullseye impact flash & comic starburst -> f17-f23 Ballistic rebound wobble | scale=0.88 (450x450, 31px margin) |

---

## SECTION 6: PROCEDURAL ANIMATION ENGINE TECHNICAL ARCHITECTURE

### 6.1 PIL MESH Transform & Deformation Mechanics
The PeelOff animation engine uses Pillow's C-accelerated `Image.Transform.MESH` API to perform real-time non-linear spatial warping of 512×512 RGBA sticker assets.

#### 6.1.1 Inverse Quad Coordinate Mapping
In PIL MESH transformations, the mapping function operates in reverse (destination pull to source sample). For a destination bounding rectangle $(x_0, y_0, x_1, y_1)$, the engine supplies the four source vertices that map into those corners:
$$\text{Quad} = \big( (x_0, y_0, x_1, y_1), (x_{nw}, y_{nw}, x_{sw}, y_{sw}, x_{se}, y_{se}, x_{ne}, y_{ne}) \big)$$
Where:
- Destination corners: North-West $(x_0, y_0)$, South-West $(x_0, y_1)$, South-East $(x_1, y_1)$, North-East $(x_1, y_0)$.
- Source sample points: $(x + dx, y + dy)$ calculated via the rig displacement function `disp(x, y)`.
- *Polarity Rule*: Positive displacement $dx > 0$ samples from the right, shifting the apparent visual feature on screen to the left.

#### 6.1.2 Vertex Grid Resolution Standards
- **Standard Character & Organic Grid**: $18 \times 18$ vertices (324 deformation quads). Step size $\Delta x = \Delta y = 28.44\text{ px}$. This resolution is mandatory for all characters, facial gestures, swaying fabric, and food items to eliminate polygonal creasing along curved contours.
- **Rigid & Mechanical Grid**: $16 \times 16$ vertices (256 deformation quads). Step size $\Delta x = \Delta y = 32.0\text{ px}$. Permitted for rigid items (microphones, dominoes, phones, road signs).
- **Interpolation Filter**: `Image.Resampling.BICUBIC` must be used across all transforms to guarantee smooth sub-pixel gradient resampling without stair-stepping artifacts.

---

### 6.2 Safety Margin & Anti-Clipping Standards (`prep_breathing_room`)
To preserve the 3D die-cut white sticker border and prevent visual clipping against canvas edges during comic motion jumps, all static source images must be pre-processed before deformation:

```python
def prep_breathing_room(im: Image.Image, scale: float = 0.91) -> Image.Image:
    w, h = im.size
    nw, nh = int(round(w * scale)), int(round(h * scale))
    small = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(small, ((w - nw) // 2, (h - nh) // 2))
    return canvas
```

- **Scaling Factor Standards**:
  - `scale = 0.91`: Standard characters and emojis ($466 \times 466\text{px}$, leaving a $23\text{px}$ transparent margin on all sides).
  - `scale = 0.88`: Wide, tall, or ballistic projectiles ($450 \times 450\text{px}$, leaving a $31\text{px}$ margin for slippers, stilts, and maxis).
  - `scale = 0.93`: Compact centered icons ($476 \times 476\text{px}$, leaving an $18\text{px}$ margin).
- **Clipping Invariance Rule**: Under maximum volumetric horizontal stretch ($S_x = 1.195$) or maximum vertical translation ($\Delta y = \pm 22\text{px}$), the transformed boundary must remain strictly within $x \in [0, 511]$ and $y \in [0, 511]$.

---

### 6.3 Canvas Coordinate Systems, Anchor Points & Mass Conservation
The PeelOff canvas operates in standard 2D screen coordinate space: origin $(0, 0)$ at top-left, $(512, 512)$ at bottom-right, center at $(256, 256)$.

#### 6.3.1 Canonical Anchor Point Schema
| Anchor Name | Coordinate $(cx, cy)$ | Anatomical / Physical Role | Used in Rigs |
|---|---|---|---|
| `ANCHOR_CENTER` | $(256, 256)$ | Center of mass / card pivot | Clinks, spins, floating items |
| `ANCHOR_GROUND` | $(256, 380)$ to $(256, 410)$ | Base of support / feet / table contact | All Fours slam, jumping mas, potholes |
| `ANCHOR_HEAD` | $(256, 180)$ to $(256, 220)$ | Cranium / eye level / brow | Cut-eye, steups, dazed spirals, horn sprouts |
| `ANCHOR_HAND_L` | $(140, 260)$ | Character left hand / gesture pivot | Claps, shrugs, fanning |
| `ANCHOR_HAND_R` | $(370, 260)$ | Character right hand / weapon pivot | Cutlass chops, slippers, card slams |

#### 6.3.2 Mass-Preserving Volume Elasticity Formula
Volumetric squash-and-stretch must preserve visual mass. When an object compresses vertically by $S_y$, its horizontal scale $S_x$ must dilate inversely:
$$S_x = \frac{1}{\sqrt{S_y}}$$
The inverse source offset function around anchor $(cx, cy)$ is:
$$\text{src}_x(x) = cx + \frac{x - cx}{S_x}, \quad \text{src}_y(y) = cy + \frac{y - cy}{S_y}$$
$$\Delta x = \text{src}_x - x, \quad \Delta y = \text{src}_y - y$$
Clamping limit: $S_y \in [0.65, 1.45]$.

---

### 6.4 Frame Timing, Coalescing Elimination & The Micro-Motion Living Hold
#### 6.4.1 Root Cause of Frame Coalescing
During Pillow export (`save_all=True`), internal encoders for WebP (`libwebp`) and GIF execute frame deduplication:
1. When consecutive frames $F_i$ and $F_{i+1}$ have bitwise identical pixel arrays (in WebP) or identical quantized color palette index matrices (in GIF), Pillow discards $F_{i+1}$.
2. Pillow increments the `duration` of $F_i$ by the duration of $F_{i+1}$.
3. In legacy builds of PeelOff, 15 rigs implemented "hold" or "rest" periods where displacement functions evaluated to exact zero ($dx = 0, dy = 0$) and vector overlays were empty.
4. Consequently:
   - `slang-link-me` had 6 identical frames coalesced $\to$ exported as **18 frames**.
   - 14 stickers (`bullseye-allfours`, `hang-jack`, `savannah-coconut`, etc.) had 4 identical frames coalesced $\to$ exported as **20 frames**.
5. This anomaly causes verification failures and non-uniform playback across messaging platforms.

#### 6.4.2 The Micro-Motion Living Hold Specification
To guarantee that Pillow preserves all 24 frames without coalescing, every rig must implement a **Micro-Motion Living Hold**:
1. At no point in the 24-frame timeline may a rig's deformation function evaluate to an idle state of $(0.0, 0.0)$ across consecutive frames.
2. Even during dramatic holds, pauses, or post-impact rests, the deformation function must inject a continuous sub-pixel sinusoidal micro-motion:
   $$dx_{\text{idle}}(t) = A_x \cdot \sin(2\pi t), \quad dy_{\text{idle}}(t) = A_y \cdot \cos(2\pi t)$$
   $$\text{Where: } A_x = 0.8\text{ pixels}, \quad A_y = 0.5\text{ pixels}$$
3. Because the bicubic interpolation kernel recalculates sub-pixel weights on every frame, every raster buffer differs slightly at the pixel level.
4. This completely eliminates Pillow frame coalescing, guaranteeing **strictly 24 frames @ 90ms on both WebP and GIF streams for all 188 stickers**.

---

### 6.5 Procedural Vector Ink Engine & Layering Architecture
All graphic overlays are rendered in a separate RGBA buffer using Pillow `ImageDraw` before compositing onto the deformed character frame.

#### 6.5.1 Master Color Palette & Inking Standards
| Style Element | Hex Code | RGBA Tuple | Usage |
|---|---|---|---|
| **Comic Dark Ink** | `#14161D` | `(20, 22, 29, 255)` | All outer silhouettes, speed lines, comic borders |
| **National Scarlet** | `#DA121A` | `(218, 18, 26, 255)` | T&T flag elements, anger veins, danger sirens |
| **Sunshine Gold** | `#FFD43B` | `(255, 212, 59, 255)` | Starbursts, halos, coin sparkles, curry highlights |
| **Electric Cyan** | `#00E5FF` | `(0, 229, 255, 255)` | Music notes, speed arcs, tears, water droplets |
| **Paramin Cobalt** | `#1446DC` | `(20, 70, 220, 255)` | Blue devil body, protective maljo shields |
| **Curry Ochre** | `#EBAF28` | `(235, 175, 40, 255)` | Doubles channa gravy, bake & shark sauce drips |
| **Pure White** | `#FFFFFF` | `(255, 255, 255, 255)` | Specular gleams, eye glints, teeth highlights |

#### 6.5.2 Multi-Pass Clean Vector Compositing
To prevent ugly intersecting ink seams when drawing multi-lobed structures like steam clouds or smoke puffs (`draw_comic_puff`), the engine employs a two-pass compositing technique:
- **Pass 1 (Silhouette)**: Draw all lobe circles in ink color with radius $R_{\text{lobe}} + 2.5\text{px}$, fusing into a single solid outer boundary.
- **Pass 2 (Fill)**: Draw all lobe circles in body fill color with radius $R_{\text{lobe}}$, completely eliminating internal ink seams.

#### 6.5.3 Alpha Decay Rule for Clean Looping
To prevent visual popping at loop boundaries, all transient vector FX must apply quadratic alpha decay:
$$\alpha(u) = \alpha_{\max} \cdot (1 - u)^2 \quad \text{where } u = \frac{t - t_{\text{start}}}{t_{\text{duration}}}$$
No overlay may have alpha $> 0$ at frame index $f = 23$.

---

### 6.6 Dual-Stream Production Export Pipeline
Every sticker must be compiled into two distinct, high-quality animated file streams in `assets/animated/`:

#### 6.6.1 Stream 1: Animated WebP (`assets/animated/{id}.webp`)
- **Format**: Animated WebP (Extended File Format VP8X with `ANIM` and `ANMF` chunks).
- **Canvas Dimensions**: Strictly $512 \times 512$ pixels.
- **Color Mode**: 32-bit RGBA with full 8-bit alpha transparency.
- **Compression Mode**: Lossy WebP, `quality = 76`.
- **Method Parameter**: `method = 4` (optimal balance between encoding speed and compression quality).
- **Frame Timing**: 24 frames @ 90ms duration per frame ($2160\text{ms}$ total duration).
- **Loop Configuration**: `loop = 0` (infinite looping).
- **Target Size**: 350 KB – 1.8 MB.

#### 6.6.2 Stream 2: Animated GIF (`assets/animated/{id}.gif`)
- **Format**: Compuserve GIF89a.
- **Canvas Dimensions**: Strictly $512 \times 512$ pixels.
- **Studio Card Background**: Solid dark card background `#10141E` (`rgb(16, 20, 30)`), matching PeelOff dark UI card theme.
- **Color Quantization**: 128 colors via `Image.Quantize.FASTOCTREE`.
- **Dither Mode**: Strictly `dither = Image.Dither.NONE` (eliminates noisy background crawl and grain artifacts).
- **Optimization Flag**: `optimize = False` (prevents frame coalescing).
- **Frame Timing**: 24 frames @ 90ms duration per frame ($2160\text{ms}$ total duration).
- **Loop Configuration**: `loop = 0` (infinite looping).

---

## SECTION 7: QUALITY ASSURANCE, VERIFICATION HARNESS & ACCEPTANCE CRITERIA

### 7.1 Quantitative Verification Assertions (Q1–Q11)
The production asset build must satisfy 100% of the following quantitative checks across all generated files:

| # | Metric | Specification | Verification Method | Pass Threshold |
|---|---|---|---|---|
| **Q1** | Total Sticker Coverage | Exactly 188 stickers | Filename match against `data/packs.js` (100) & `data/trini-slang.js` (88) | 188 / 188 (100%) |
| **Q2** | Dual-Stream Production | 376 total animated files | Count `.webp` and `.gif` files in `assets/animated/` | Exactly 376 files |
| **Q3** | Non-Zero Byte Audit | Zero 0-byte files | File size check `os.path.getsize(p) > 0` | 0 files with 0 bytes |
| **Q4** | Frame Count Invariance | Strictly 24 frames per file | `Image.open(p).n_frames == 24` | 376 / 376 (100%) |
| **Q5** | Frame Timing Standard | Strictly 90ms per frame | `im.info['duration'] == 90` across all frames | 376 / 376 (100%) |
| **Q6** | Total Loop Duration | Strictly 2.16 seconds ($2160\text{ms}$) | $\sum_{i=1}^{24} \text{duration}_i == 2160$ | 376 / 376 (100%) |
| **Q7** | Canvas Dimensions | Strictly $512 \times 512$ pixels | `im.size == (512, 512)` | 376 / 376 (100%) |
| **Q8** | Header Format Integrity | Valid magic bytes | WebP: `RIFF....WEBPVP8X`; GIF: `GIF89a` | 376 / 376 (100%) |
| **Q9** | Infinite Loop Configuration | Loop count = 0 | `im.info.get('loop', 0) == 0` | 376 / 376 (100%) |
| **Q10**| WebP Alpha Integrity | 8-bit Alpha Channel present | `im.mode == 'RGBA'` with transparent exterior | 188 / 188 WebPs |
| **Q11**| GIF Card Integrity | Solid `#10141E` background | Card corners sample `rgb(16, 20, 30)` | 188 / 188 GIFs |

---

### 7.2 Qualitative Cultural & Aesthetic Acceptance Criteria
In addition to automated numeric metrics, every sticker animation must pass visual inspection against the following qualitative criteria:
1. **Elimination of Generic Fallbacks**:
   - Zero instances of the generic `articulated_gesture` bounce in `scripts/build_animated_stickers.py`.
   - Every sticker must execute an individualized cultural motion routine or an authentic shared thematic rig.
2. **Die-Cut Border Preservation**:
   - The white contour border of the 3D sticker must never touch, flatten against, or clip across the $512 \times 512$ canvas boundary at any frame during the loop.
3. **Loop Smoothness & Continuity**:
   - The animation must cycle seamlessly from frame 23 back to frame 0 with zero visible popping, snapping, or jump cuts.
4. **Immediate Mobile Chat Punch**:
   - The primary comedic gesture (e.g., eye roll, card slam, steam burst, cut-eye) must trigger and register within the first 6 frames ($< 540\text{ms}$) so the reaction is immediately apparent in messaging app preview bubbles.
5. **Graphic Inking Consistency**:
   - All secondary vector lines must utilize the `#14161D` ink standard and clean layered specular highlights without pixelated dither artifacts.

---

### 7.3 Automated Verification Harness Contract (`scripts/verify_animated_stickers.py`)
Milestone 3 requires the implementation of an automated test script `scripts/verify_animated_stickers.py`.

#### 7.3.1 Script Interface Contract
- **Command Line**: `python scripts/verify_animated_stickers.py`
- **Execution Environment**: Workspace Python virtual environment (`.venv\Scripts\python.exe`).
- **Dependencies**: `Pillow >= 10.0.0`.
- **Exit Codes**:
  - `0`: All 376 animated files strictly pass all Q1–Q11 assertions.
  - `1`: Any assertion failure, corrupted header, incorrect frame count, or missing file.

#### 7.3.2 Verification Test Routine Structure
```python
"""
scripts/verify_animated_stickers.py
===================================
Automated Verification Suite for PeelOff Animated Stickers (Milestone 3).

Enforces 100% compliance across Quantitative Verification Assertions Q1–Q11
in docs/CULTURAL_ANIMATION_SPEC.md:
  - Q1: Exactly 188 sticker IDs enumerated from data/packs.js (100) & data/trini-slang.js (88)
  - Q2: Exactly 376 production assets present (188 .webp + 188 .gif)
  - Q3: Non-zero file sizes (> 1024 bytes)
  - Q4: Frame count invariance (strictly 24 frames)
  - Q5: Frame timing standard (strictly 90ms per frame)
  - Q6: Total loop duration (strictly 2160ms = 2.16s)
  - Q7: Canvas dimensions (strictly 512x512 pixels)
  - Q8: Header format integrity (WebP: RIFF....WEBPVP8X; GIF: GIF89a magic bytes)
  - Q9: Infinite loop configuration (loop == 0)
  - Q10: WebP alpha integrity (RGBA mode + transparent exterior corners alpha == 0)
  - Q11: GIF studio card integrity (solid #10141E dark card background)

Exit Codes:
  0: All 376 assets pass all Q1–Q11 assertions.
  1: Any assertion failure, corrupted header, timing defect, or missing file.
"""

import os
import sys
import re
import struct
from PIL import Image


def parse_webp_anmf_durations(path: str) -> list[int]:
    """Extract frame durations (ms) directly from WebP ANMF container chunks.

    Pillow's WebP decoder does not populate im.info['duration'] when seeking frames
    (evaluating to None). This parser inspects the raw RIFF bitstream directly.
    In WebP Extended Format (VP8X), animated frames are stored in 'ANMF' chunks:
      - Bytes 0..3: FourCC b'ANMF'
      - Bytes 4..7: Chunk payload size (uint32, little-endian)
      - Payload Bytes 12..14: Frame duration in ms (uint24, little-endian)
    """
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 16 or data[0:4] != b"RIFF" or data[8:12] != b"WEBP":
        return []

    durations = []
    offset = 12
    data_len = len(data)
    while offset + 8 <= data_len:
        fourcc = data[offset:offset + 4]
        chunk_size = struct.unpack("<I", data[offset + 4:offset + 8])[0]
        chunk_start = offset + 8
        if fourcc == b"ANMF":
            if chunk_start + 15 <= data_len:
                payload = data[chunk_start:chunk_start + chunk_size]
                if len(payload) >= 15:
                    dur = payload[12] | (payload[13] << 8) | (payload[14] << 16)
                    durations.append(dur)
        padded_size = chunk_size + (chunk_size % 2)
        offset = chunk_start + padded_size
    return durations


def enumerate_sticker_ids(root_dir: str = ".") -> list[str]:
    """Enumerate all 188 sticker IDs from data/packs.js and data/trini-slang.js."""
    packs_path = os.path.join(root_dir, "data", "packs.js")
    slang_path = os.path.join(root_dir, "data", "trini-slang.js")

    assert os.path.exists(packs_path), f"Missing catalog file: {packs_path}"
    assert os.path.exists(slang_path), f"Missing catalog file: {slang_path}"

    with open(packs_path, "r", encoding="utf-8") as f:
        packs_text = f.read()
    with open(slang_path, "r", encoding="utf-8") as f:
        slang_text = f.read()

    # 100 Pack stickers: match id fields, excluding app launcher icons ('icon-') and pack containers ('pack-')
    pack_ids = [
        sid for sid in re.findall(r'id:\s*["\']([a-zA-Z0-9_-]+)["\']', packs_text)
        if not sid.startswith("icon-") and not sid.startswith("pack-")
    ]

    # 88 Slang stickers: match id fields in trini-slang.js
    slang_ids = re.findall(r'["\']id["\']\s*:\s*["\']([a-zA-Z0-9_-]+)["\']', slang_text)

    # Combine and preserve order while ensuring uniqueness
    all_ids = []
    seen = set()
    for sid in pack_ids + slang_ids:
        if sid not in seen:
            seen.add(sid)
            all_ids.append(sid)

    assert len(pack_ids) == 100, f"Expected 100 pack stickers, found {len(pack_ids)}"
    assert len(slang_ids) == 88, f"Expected 88 slang stickers, found {len(slang_ids)}"
    assert len(all_ids) == 188, f"Expected exactly 188 total stickers (Q1), found {len(all_ids)}"
    return all_ids


def verify_animated_file(path: str, expected_format: str) -> None:
    """Verify an individual animated WebP or GIF asset against Q3–Q11 assertions."""
    # Q3: Non-Zero Byte Audit
    assert os.path.exists(path), f"Missing asset: {path}"
    size = os.path.getsize(path)
    assert size > 1024, f"File too small or 0 bytes ({size} bytes): {path}"

    # Q8: Raw Binary Magic Byte Inspection
    with open(path, "rb") as f:
        header = f.read(16)

    if expected_format == "WEBP":
        assert header[0:4] == b"RIFF" and header[8:16] == b"WEBPVP8X", (
            f"Invalid WebP magic bytes {header[:16]!r} in {path} (expected RIFF....WEBPVP8X)"
        )
    elif expected_format == "GIF":
        assert header[0:6] == b"GIF89a", (
            f"Invalid GIF magic bytes {header[:6]!r} in {path} (expected GIF89a)"
        )

    # Container and raster inspection via Pillow
    with Image.open(path) as im:
        assert im.format == expected_format, f"Invalid format {im.format} for {path}"
        # Q7: Canvas Dimensions
        assert im.size == (512, 512), f"Invalid dimensions {im.size} for {path}"
        # Q4: Frame Count Invariance
        assert im.n_frames == 24, f"Frame count {im.n_frames} != 24 for {path}"
        # Q9: Infinite Loop Configuration
        assert im.info.get("loop", 0) == 0, f"Loop configuration != 0 in {path}"

        if expected_format == "WEBP":
            # Q10: WebP Alpha Integrity & Transparent Exterior Corners
            assert im.mode == "RGBA", f"WebP mode {im.mode} != RGBA in {path}"
            corners = [(0, 0), (511, 0), (0, 511), (511, 511)]
            for c in corners:
                px = im.getpixel(c)
                assert px[3] == 0, f"WebP corner {c} non-transparent (alpha={px[3]}) in {path}"

            # Q5 & Q6: Timing inspection via direct WebP ANMF chunk parsing
            # (Pillow im.info['duration'] returns None on WebP seek)
            anmf_durs = parse_webp_anmf_durations(path)
            assert len(anmf_durs) == 24, (
                f"WebP ANMF frame count {len(anmf_durs)} != 24 in {path}"
            )
            for f_idx, d in enumerate(anmf_durs):
                assert d == 90, f"WebP ANMF frame {f_idx} duration {d}ms != 90ms in {path}"
            assert sum(anmf_durs) == 2160, (
                f"WebP total duration {sum(anmf_durs)}ms != 2160ms in {path}"
            )

        elif expected_format == "GIF":
            # Q5 & Q6: Frame Timing on GIF via Pillow seek
            total_dur = 0
            for f_idx in range(im.n_frames):
                im.seek(f_idx)
                d = im.info.get("duration")
                assert d == 90, f"GIF frame {f_idx} duration {d}ms != 90ms in {path}"
                total_dur += d
            assert total_dur == 2160, f"GIF total duration {total_dur}ms != 2160ms in {path}"

            # Q11: GIF Studio Card Background (#10141E)
            # Sample exterior corners; allow maximum channel delta <= 1 for FASTOCTREE quantization
            rgb_im = im.convert("RGB")
            corners = [(0, 0), (2, 2), (511, 0), (0, 511), (511, 511)]
            for c in corners:
                px = rgb_im.getpixel(c)
                max_delta = max(abs(a - b) for a, b in zip(px, (16, 20, 30)))
                assert max_delta <= 1, (
                    f"GIF corner {c} {px} deviates from studio card (16, 20, 30) in {path}"
                )


def main():
    # Detect project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    if os.path.exists(os.path.join(script_dir, "data", "packs.js")):
        root_dir = script_dir
    elif os.path.exists(os.path.join(os.path.dirname(script_dir), "data", "packs.js")):
        root_dir = os.path.dirname(script_dir)
    else:
        root_dir = os.getcwd()

    animated_dir = os.path.join(root_dir, "assets", "animated")
    assert os.path.exists(animated_dir), f"Animated assets directory missing: {animated_dir}"

    print(f"PeelOff Animated Sticker Verifier (Milestone 3)")
    print(f"Root: {root_dir}")
    print(f"Asset directory: {animated_dir}")

    # Q1: Enumerate all 188 sticker IDs
    sticker_ids = enumerate_sticker_ids(root_dir)
    print(f"Enumerated {len(sticker_ids)} stickers from packs.js and trini-slang.js (Q1 PASS)")

    errors = []
    verified_files = 0

    for sid in sticker_ids:
        webp_path = os.path.join(animated_dir, f"{sid}.webp")
        gif_path = os.path.join(animated_dir, f"{sid}.gif")

        # Verify Stream 1: WebP
        try:
            verify_animated_file(webp_path, "WEBP")
            verified_files += 1
        except Exception as e:
            errors.append((webp_path, str(e)))

        # Verify Stream 2: GIF
        try:
            verify_animated_file(gif_path, "GIF")
            verified_files += 1
        except Exception as e:
            errors.append((gif_path, str(e)))

    # Q2: Dual-Stream Production count (376 total assets)
    expected_files = len(sticker_ids) * 2
    print(f"\nVerification Results:")
    print(f"  Total target files: {expected_files} (188 WebP + 188 GIF)")
    print(f"  Successfully passed: {verified_files}")
    print(f"  Defects / Errors: {len(errors)}")

    if errors:
        print(f"\nFAILED: {len(errors)} defect(s) detected across {len(sticker_ids)} stickers:")
        for path, err in errors[:25]:
            print(f"  [FAIL] {path}: {err}")
        if len(errors) > 25:
            print(f"  ... and {len(errors) - 25} more failures.")
        sys.exit(1)

    assert verified_files == 376, f"Expected 376 verified files (Q2), got {verified_files}"
    print(f"\nALL 376 ANIMATED ASSETS (188 WebP + 188 GIF) STRICTLY VERIFIED (Q1–Q11 PASS)")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

### 7.4 Downstream Implementation Roadmap (Milestones 2–5)
1. **Milestone 2 (Animation Generator Overhaul & Rig Redesign)**:
   - Refactor `scripts/build_animated_stickers.py` to implement the 14 procedural motion primitives and individualized rig mappings.
   - Eliminate all references to the generic `articulated_gesture` fallback.
   - Implement the Micro-Motion Living Hold across all rigs to eliminate the Pillow frame coalescing defect.
   - Regenerate the 6 corrupted 0-byte WebP files.
2. **Milestone 3 (Batch Production & Automated Verification)**:
   - Execute multiprocessing batch generator across all 188 stickers.
   - Run `scripts/verify_animated_stickers.py` to assert 100% compliance across Q1–Q11.
   - Confirm all 376 animated files are present and verified on disk.
3. **Milestone 4 (Web App Integration & Manifest Alignment)**:
   - Verify `app.js` and `index.html` render animated WebPs and GIFs seamlessly without performance lag.
   - Update `assets/contents.json` with animated sticker pack support flags.
4. **Milestone 5 (E2E Verification & Adversarial Hardening)**:
   - Execute the 5-Tier comprehensive E2E test suite.
   - Validate 100% pass rate under stress conditions and cross-platform sharing simulations.
