# Looking after the HR-V — daily, weekly, monthly

A 2019 car with 190,000 km is past the stage where a service book covers
everything. Most of what goes wrong now announces itself early, and the
whole point of a routine is to be there when it does.

Time cost: about 10 seconds a day and 5 minutes a week.

## Daily — the ten-second habit

**As you walk up to it**

- Does any tyre look low or different to the others? The eye is surprisingly
  good at this once it's a habit.
- Any puddle or drip where it was parked? Clear water from the air
  conditioner is normal in summer. Anything coloured or oily is not.

**As you start it**

- Watch the warning lights go out. The ones that matter: **oil pressure**
  (red can/genie lamp), **battery/charging**, **temperature**. If the oil
  pressure light stays on or comes on while driving, stop the engine
  immediately — that is the one fault that destroys an engine in minutes,
  not days.
- The airbag, ABS and check-engine lights should also extinguish. If one
  stays on, it isn't an emergency, but note it and get it read.

**In the first minute**

- Any new noise? Squeal, knock, grinding at the first brake application.
- Don't work the engine hard until the temperature gauge has lifted off
  cold. Most engine wear happens in the first few minutes.

## Weekly — five minutes

**Engine oil.** The single highest-value check on a high-kilometre car. Park
level, engine cold (or 10 minutes after switching off), pull the dipstick,
wipe, reinsert, read. Keep it between the marks. A car at this mileage using
some oil between services is not unusual — running it low is what kills it.
If you're topping up more than a litre between services, tell a mechanic.

**Tyres.** Pressures to **33 psi cold**, front and rear, plus a look for
cuts, bulges and uneven wear. Wear on one edge means alignment; wear in the
middle means over-inflation; wear on both edges means it's been driven soft.
Log it: `./car.py tyres --fl 33 --fr 33 --rl 33 --rr 33`

**Coolant.** Check the level in the plastic overflow bottle against its
min/max marks. **Never open the radiator cap on a warm engine** — it is
pressurised and will scald you. If the bottle keeps dropping, that's a leak
worth chasing early.

**Washer fluid and wipers.** Queensland sun destroys wiper rubber; smearing
blades at night in rain are a real hazard and blades are cheap.

**Lights.** Headlights, indicators, reverse, and both brake lights — back up
to a wall or window at dusk and watch the reflection. A dead brake light is
invisible from the driver's seat and is exactly what gets you rear-ended.

**Glass.** Clean the inside of the windscreen, not just the outside. Interior
film is what turns low sun into a wall of glare.

## Monthly

- Wash it, and do the underside if you've been near the coast. Bird droppings
  and tree sap etch clear coat within days in this sun — get those off now,
  not at the weekend.
- Brake fluid level in its reservoir. A slowly falling level means either worn
  pads or a leak; neither should be ignored.
- Battery terminals for white/blue crust. Queensland heat is harder on
  batteries than cold is — three to four years is a realistic life here, not
  the five or six you'd get further south.
- Spare tyre pressure. It is always flat when you need it.
- Run the air conditioning for ten minutes even in winter. It keeps the
  compressor seals lubricated; letting it sit unused is how they start
  leaking.

## What matters specifically at 190,000 km

- **Oil leaks.** Check where you park. A small weep now is a cheap gasket;
  ignored, it becomes an oil-starved engine.
- **CVT fluid.** Honda specifies HCF-2 and it is an interval item, not
  fill-for-life. At this mileage it's the most likely thing to be overdue,
  and CVTs are expensive to be wrong about. Any shudder at low speed or
  whine that rises with road speed — get it looked at promptly.
- **CV boots.** Clicking on full lock means a torn boot has thrown its
  grease. Cheap to fix early, a whole driveshaft if left.
- **Brake fluid** absorbs moisture from the air and should be changed roughly
  every two years regardless of kilometres.
- **Suspension.** Clunks over bumps usually mean bushes or links — not urgent,
  but it fails a roadworthy inspection.
- The 1.8 uses a timing **chain**, not a belt, so there's no replacement
  interval to budget for. Worth confirming against your service book, since
  getting that wrong is an expensive assumption either way.

## Habits that outlast any checklist

- **Warm it gently.** Not idling on the driveway — just drive softly for the
  first few kilometres.
- **Short trips are hard on an engine.** If most of your driving is under ten
  minutes, the engine never fully warms, moisture and fuel accumulate in the
  oil, and the exhaust rots from the inside. One longer run a week clears it.
- **Coast to red lights** instead of braking late. Cheaper brakes, better fuel.
- **Park in shade** where you can, and use a windscreen shade. It protects the
  dashboard from cracking and takes a real load off the air conditioning.

## Keep in the car

Tyre gauge, jumper leads or a jump pack, torch, gloves, water, and the wheel
brace and jack where you can actually reach them. Check the jack is there —
they get borrowed and not returned.

## When something changes

Log it, don't just notice it. A note now is what tells a mechanic in six
months that the noise started at 191,000 km:

```bash
./car.py service --odo 191200 --type "Noted" --cost 0 \
    --description "Light knock from front right over speed humps"
```
